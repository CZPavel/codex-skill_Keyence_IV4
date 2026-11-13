"""Validate and safely manage the local keyence-iv4 skill (stdlib only)."""
import argparse
import hashlib
import json
from pathlib import Path
import re
import shutil
import stat
import sys
import tempfile

ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / 'skills' / 'keyence-iv4'
MARKER = '.keyence-iv4-install.json'
NAME = 'keyence-iv4'


def is_link(path):
    try:
        info = path.lstat()
    except FileNotFoundError:
        return False
    return stat.S_ISLNK(info.st_mode) or bool(getattr(info, 'st_file_attributes', 0) & getattr(stat, 'FILE_ATTRIBUTE_REPARSE_POINT', 0x400))


def inventory(folder, reject_artifacts=False):
    folder = Path(folder)
    if not folder.is_dir() or is_link(folder):
        raise ValueError('Skill directory missing or is a link')
    files = {}
    def walk(base):
        for path in sorted(base.iterdir()):
            if is_link(path):
                raise ValueError(f'Link or junction is not allowed: {path.name}')
            if reject_artifacts and (path.name == '__pycache__' or path.suffix == '.pyc'):
                raise ValueError('Untracked artifact in installation')
            if path.is_dir():
                if path.name != '__pycache__':
                    walk(path)
            elif path.is_file() and path.name != MARKER and path.suffix != '.pyc':
                files[path.relative_to(folder).as_posix()] = hashlib.sha256(path.read_bytes()).hexdigest()
    walk(folder)
    return files


def validate(skill=SKILL):
    skill = Path(skill)
    files = inventory(skill)
    size = sum((skill / name).stat().st_size for name in files)
    if not files or len(files) > 100 or size > 10_000_000:
        raise ValueError('Unexpected distribution size')
    entry = (skill / 'SKILL.md').read_text(encoding='utf-8-sig')
    front = re.match(r'\A---[ \t]*\r?\n(.*?)\r?\n---[ \t]*(?:\r?\n|$)(.*)\Z', entry, re.S)
    if not front or not front.group(2).strip():
        raise ValueError('Missing closing frontmatter or skill body')
    fields = dict(re.findall(r'^([a-zA-Z_][\w-]*):[ \t]*(.+)$', front.group(1), re.M))
    if fields.get('name', '').strip(' \"\'') != NAME or not fields.get('description', '').strip(' \"\''):
        raise ValueError('Missing skill name or description')
    for name in files:
        path = skill / name
        if path.suffix not in ('.md', '.json', '.py') and name != 'agents/openai.yaml':
            raise ValueError(f'Unexpected file: {name}')
        content = path.read_text(encoding='utf-8-sig')
        if re.search(r'[A-Za-z]:[\\/](?:Users|VS_CODE_PROJECTS)[\\/]|sk-proj-[A-Za-z0-9]', content, re.I):
            raise ValueError(f'Private path or credential in {name}')
        if path.suffix == '.json':
            json.loads(content)
        if name == 'agents/openai.yaml':
            lines = [line for line in content.splitlines() if line.strip() and not line.lstrip().startswith('#')]
            if not lines or any('\t' in line or not re.match(r'^(?:  )*[\w-]+:\s*.*$', line) for line in lines):
                raise ValueError('Invalid simple agents/openai.yaml')
        if path.suffix == '.md':
            for link in re.findall(r'\]\(([^)]+)\)', content):
                link = link.split('#')[0].strip().split(' ')[0]
                if not link or re.match(r'^(https?://|mailto:)', link):
                    continue
                target = (path.parent / link).resolve()
                if not target.is_relative_to(skill.resolve()) or not target.exists():
                    raise ValueError(f'Broken or escaping link in {name}: {link}')
    for required in ('references/sources.json', 'references/commands.json', 'references/capabilities.json'):
        if required not in files:
            raise ValueError(f'Missing required file: {required}')
    return {'files': len(files), 'bytes': size}


def target_for(skills_dir=None):
    parent = Path(skills_dir) if skills_dir is not None else Path.home() / '.agents' / 'skills'
    # Reject any existing link in destination chain, including Windows junctions.
    for component in (parent, *parent.parents):
        if is_link(component):
            raise ValueError('Destination contains link or junction')
    return parent / NAME


def verify_managed(target):
    if is_link(target) or not (target / MARKER).is_file() or is_link(target / MARKER):
        raise ValueError('Refusing unmanaged or linked target')
    marker = json.loads((target / MARKER).read_text(encoding='utf-8'))
    if marker.get('owner') != NAME or inventory(target, reject_artifacts=True) != marker.get('files'):
        raise ValueError('Local modifications or invalid ownership manifest')


def status(skills_dir=None):
    target = target_for(skills_dir)
    candidates = [target]
    if skills_dir is None:
        candidates += [Path.home() / '.codex' / 'skills' / NAME]
        candidates += list((Path.home() / '.codex' / 'plugins' / 'cache').glob('*/*/*/skills/' + NAME))
    out = []
    for path in candidates:
        if path.exists() or is_link(path):
            try:
                verify_managed(path)
                state = 'managed'
            except (ValueError, OSError, json.JSONDecodeError):
                state = 'foreign_or_modified'
            out.append({'path': str(path), 'state': state})
    return {'target': str(target), 'existing': out}


def install(skills_dir=None, source=SKILL):
    validate(source)
    target = target_for(skills_dir)
    if skills_dir is None:
        conflicts = [x for x in status()['existing'] if Path(x['path']) != target]
        if conflicts:
            raise ValueError('Conflicting existing distribution: ' + ', '.join(x['path'] for x in conflicts))
    if target.exists() or is_link(target):
        verify_managed(target)
    target.parent.mkdir(parents=True, exist_ok=True)
    files = inventory(source)
    with tempfile.TemporaryDirectory(prefix='.iv4-stage-', dir=target.parent) as temp:
        stage, previous = Path(temp) / 'new', Path(temp) / 'previous'
        stage.mkdir()
        for name in files:
            dest = stage / name
            dest.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(Path(source) / name, dest)
        (stage / MARKER).write_text(json.dumps({'owner': NAME, 'files': files}, indent=2) + '\n', encoding='utf-8')
        if inventory(stage) != files:
            raise ValueError('Copy integrity failure')
        had_previous = target.exists()
        if had_previous:
            verify_managed(target)
            target.rename(previous)
        try:
            stage.rename(target)
        except OSError:
            if had_previous:
                previous.rename(target)
            raise
    return target


def uninstall(skills_dir=None):
    target = target_for(skills_dir)
    verify_managed(target)
    for name in inventory(target):
        (target / name).unlink()
    (target / MARKER).unlink()
    for path in sorted(target.rglob('*'), key=lambda p: len(p.parts), reverse=True):
        if path.is_dir() and not any(path.iterdir()):
            path.rmdir()
    target.rmdir()
    return target


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('action', choices=['validate', 'status', 'install', 'update', 'uninstall'])
    parser.add_argument('--skills-dir', type=Path, help='Isolated target parent for tests or explicit installation')
    args = parser.parse_args()
    try:
        if args.action == 'validate':
            result = validate()
        elif args.action == 'status':
            result = status(args.skills_dir)
        elif args.action in ('install', 'update'):
            result = str(install(args.skills_dir))
        else:
            result = str(uninstall(args.skills_dir))
        print(json.dumps(result, ensure_ascii=False, indent=2))
    except (ValueError, OSError, json.JSONDecodeError) as exc:
        print(f'Management error: {exc}', file=sys.stderr)
        return 2
    return 0


if __name__ == '__main__':
    sys.exit(main())
