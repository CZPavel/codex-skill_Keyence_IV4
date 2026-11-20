"""Read-only, bounded lookup for bundled IV4 references and an optional corpus."""
import argparse
from itertools import chain
import json
import os
from pathlib import Path
import re
import sys

SKILL = Path(__file__).resolve().parents[1]
PAGE = re.compile(r'^## (iv4_[0-9a-f]+) · PDF p\. (\d+)', re.I)


def load(path, default):
    return json.loads(path.read_text(encoding='utf-8-sig')) if path.is_file() else default


def corpus_dir(corpus):
    if not corpus:
        return None
    path = Path(corpus)
    path = path / 'knowledge' if (path / 'knowledge').is_dir() else path
    if not (path / '00_KNOWLEDGE_INDEX.json').is_file():
        raise ValueError('Optional corpus missing knowledge/00_KNOWLEDGE_INDEX.json')
    return path


def pages(folder):
    if folder is None:
        return
    for path in sorted(folder.glob('[A-G]_*.md')):
        with path.open(encoding='utf-8') as stream:
            current, lines = None, []
            for line in stream:
                match = PAGE.match(line)
                if match:
                    if current:
                        yield current, ''.join(lines)
                    current = f'{match[1]}:p{int(match[2]):04d}'
                    lines = [line]
                elif current:
                    lines.append(line)
            if current:
                yield current, ''.join(lines)


def references(skill):
    for path in sorted((skill / 'references').glob('*.md')):
        # Stable file-derived ID; sections remain within the same unit.
        yield 'REF-' + re.sub(r'[^a-z0-9]+', '-', path.stem.lower()).strip('-'), path.read_text(encoding='utf-8')


def excerpt(text, maximum, query=''):
    pos = text.casefold().find(query.casefold()) if query else -1
    start = max(0, pos - maximum // 3) if pos >= 0 else 0
    return {'text': text[start:start + maximum], 'truncated': start > 0 or start + maximum < len(text)}


def family_matches(item, family):
    if not family:
        return True
    value = item.get('family', '')
    if isinstance(value, list):
        return family.casefold() in [str(v).casefold() for v in value]
    return str(value).casefold() == family.casefold()


def descriptor_records(data):
    # Search records, not the giant registry or its raw JSON as one result.
    def walk(obj, path=()):
        if isinstance(obj, list):
            for i, item in enumerate(obj):
                yield from walk(item, path + (str(i),))
        elif isinstance(obj, dict):
            scalars = {k: v for k, v in obj.items() if isinstance(v, (str, int, float, bool)) or v is None}
            if scalars:
                yield {'path': '/'.join(path), 'record': scalars}
            for k, v in obj.items():
                if isinstance(v, (dict, list)):
                    yield from walk(v, path + (k,))
    yield from walk(data.get('adapter_descriptors', data))


def evidence(folder, source, page, limit, maximum):
    if not folder:
        return []
    index = load(folder / '00_KNOWLEDGE_INDEX.json', {})
    record = next((x for x in index.get('sources', []) if x.get('source_id') == source), None)
    if not record:
        return []
    digest = record.get('sha256') or record.get('source_sha256')
    if not isinstance(digest, str) or not re.fullmatch(r'[0-9a-fA-F]{64}', digest):
        return []
    root = folder.parent / 'evidence'
    output = []
    if not root.is_dir():
        return output
    for sr in root.glob('*/documents/*/source_record.json'):
        data = load(sr, {})
        if str(data.get('source_sha256', '')).casefold() != digest.casefold():
            continue
        for name in ('page_index.jsonl', 'table_index.jsonl', 'figure_index.jsonl'):
            path = sr.parent / name
            if not path.is_file():
                continue
            with path.open(encoding='utf-8') as stream:
                for line in stream:
                    item = json.loads(line)
                    if page is not None and item.get('pdf_page', item.get('page')) != page:
                        continue
                    # Avoid exposing local source or asset paths.
                    clean = {k: item[k] for k in ('page_id', 'pdf_page', 'printed_page', 'table_id', 'figure_id', 'title', 'caption', 'text', 'table_refs', 'figure_refs', 'rows', 'row_count', 'column_count', 'table_type', 'review_status', 'visual_text', 'legend', 'figure_type', 'description') if k in item}
                    raw = json.dumps(clean, ensure_ascii=False)
                    output.append({'kind': name.removesuffix('_index.jsonl'), **excerpt(raw, maximum)})
                    if len(output) >= limit:
                        return output
    return output


def registry_records(refs):
    for filename, key in (('commands.json', 'commands'), ('capabilities.json', 'capabilities'), ('descriptors.json', 'descriptors')):
        for item in load(refs / filename, {}).get(key, []):
            yield item


def runtime_records(refs, folder=None):
    """Independent observations; never merge documentation classifications or private source roots."""
    seen = set()
    for data, key in ((load(refs / 'runtime-observations.json', {}), 'observations'),
                      (load(folder / 'IV4_RESEARCH_FACTS.json', {}) if folder else {}, 'facts')):
        for item in data.get(key, []):
            ident = item.get('id')
            if ident and ident not in seen:
                seen.add(ident)
                # Optional private registry contains a separate sources[] catalog with local_root.
                # Return only logical locators and fact fields, never that catalog.
                yield {k: v for k, v in item.items() if k in (
                    'id', 'family', 'model', 'firmware', 'navigator_version', 'observed_on',
                    'evidence_category', 'title', 'observed', 'documented_context', 'limitations',
                    'statement', 'source_locators')}


def firmware_matches(item, firmware):
    value = item.get('firmware', '')
    versions = value if isinstance(value, list) else [value]
    return not firmware or firmware.casefold() in [str(v).casefold() for v in versions]


def bounded_record(item, maximum):
    raw = json.dumps(item, ensure_ascii=False)
    return item if len(raw) <= maximum else {'id': item.get('id'), **excerpt(raw, maximum)}


def public_page(refs, source, page, limit, maximum):
    matches = []
    for item in registry_records(refs):
        if str(item.get('source_id', '')).casefold() != source:
            continue
        cited = [item.get('pdf_page'), item.get('detail_pdf_page')] + item.get('pdf_pages', [])
        if page in cited:
            matches.append(bounded_record(item, maximum))
            if len(matches) >= limit:
                break
    ref_ids = []
    for ident, content in references(refs.parent):
        if source in content.casefold() and (str(page) in content or any(str(x.get('id', '')) in content for x in matches if x.get('id'))):
            ref_ids.append(ident)
    return {'mode': 'standalone-limited', 'id': f'{source}:p{page:04d}', 'full_page_available': False,
            'records': matches, 'references': ref_ids[:limit]}


def lookup(*, skill=SKILL, corpus=None, query=None, address=None, command=None, descriptor=None,
           status=False, literal=False, limit=10, family=None, firmware=None, neighbors=0, maximum=2500, include_evidence=False):
    if not 1 <= limit <= 100 or not 1 <= maximum <= 10000 or not 0 <= neighbors <= 20:
        raise ValueError('limit 1..100, max-chars 1..10000, neighbors 0..20')
    skill = Path(skill)
    folder = corpus_dir(corpus)
    refs = skill / 'references'
    commands = load(refs / 'commands.json', {}).get('commands', [])
    if status:
        return {'mode': 'standalone+corpus' if folder else 'standalone', 'corpus_available': bool(folder),
                'references': len(list(refs.glob('*.md'))), 'commands': len(commands),
                'capabilities_available': (refs / 'capabilities.json').is_file(),
                'runtime_observations': len(list(runtime_records(refs))),
                'corpus_research_available': bool(folder and (folder / 'IV4_RESEARCH_FACTS.json').is_file())}
    if firmware and (command is not None or descriptor is not None):
        raise ValueError('--firmware applies to runtime --query/--id; command/descriptor are documentation records')
    if command is not None:
        token = command.strip().casefold()
        results = [x for x in commands if str(x.get('code', '')).strip().casefold() == token and family_matches(x, family)]
        return {'results': [bounded_record(item, maximum) for item in results[:limit]], 'total_matches': len(results)}
    if descriptor is not None:
        local = {'capabilities': load(refs / 'capabilities.json', {}), 'descriptors': load(refs / 'descriptors.json', {})}
        external = load(folder / 'COMMUNICATION_REFERENCE.json', {}) if folder else {}
        needle = descriptor.casefold()
        found = []
        for source, data in [('bundled', local), ('corpus', external)]:
            for item in descriptor_records(data):
                raw = json.dumps(item, ensure_ascii=False)
                if needle in raw.casefold():
                    found.append({'source': source, **excerpt(raw, maximum, descriptor)})
                    if len(found) >= limit:
                        break
            if len(found) >= limit:
                break
        return {'results': found, 'corpus_available': bool(folder)}
    if address:
        for item in runtime_records(refs, folder):
            if str(item.get('id', '')).casefold() == address.casefold():
                if not firmware_matches(item, firmware) or not family_matches(item, family):
                    raise ValueError('Runtime ID does not match requested family/firmware')
                return {'id': item['id'], 'model': item.get('model'), 'firmware': item.get('firmware'),
                        'evidence_category': item.get('evidence_category'), 'record': bounded_record(item, maximum),
                        'historical': True, 'production_accepted': False}
        if firmware:
            raise ValueError('--firmware requires a runtime observation ID')
        allrefs = list(references(skill))
        for ident, content in allrefs:
            if ident.casefold() == address.casefold():
                return {'id': ident, **excerpt(content, maximum)}
        for filename, key in (('commands.json', 'commands'), ('capabilities.json', 'capabilities'), ('descriptors.json', 'descriptors'), ('sources.json', 'sources')):
            for item in load(refs / filename, {}).get(key, []):
                if str(item.get('id', '')).casefold() == address.casefold():
                    raw = json.dumps(item, ensure_ascii=False)
                    return {'id': item['id'], **excerpt(raw, maximum)}
        match = re.fullmatch(r'(iv4_[0-9a-f]+)(?::p(\d+))?', address, re.I)
        if not match:
            raise ValueError('Unknown ID; expected runtime ID, REF-... or iv4_<hash>[:pNNNN]')
        source, page = match[1].lower(), int(match[2]) if match[2] else None
        index = load(folder / '00_KNOWLEDGE_INDEX.json', {}) if folder else load(refs / 'sources.json', {})
        meta = next((x for x in index.get('sources', []) if x.get('source_id', '').lower() == source), None)
        if not meta:
            raise ValueError('Source ID not found')
        if page is None:
            safe = {k: v for k, v in meta.items() if k in ('id', 'source_id', 'filename', 'scope', 'version', 'actual_format', 'language', 'models', 'pages', 'review_status')}
            safe['pages_available'] = [p.get('pdf_page') for p in meta.get('pages_index', [])[:limit]]
            result = {'source': safe, 'pages_truncated': len(meta.get('pages_index', [])) > limit}
            if include_evidence:
                result['evidence'] = evidence(folder, source, None, limit, maximum)
            return result
        if not folder:
            return public_page(refs, source, page, limit, maximum)
        results = []
        for ident, content in pages(folder):
            sm = re.fullmatch(r'(iv4_[0-9a-f]+):p(\d+)', ident, re.I)
            if sm.group(1).lower() == source and abs(int(sm.group(2)) - page) <= neighbors:
                results.append({'id': ident, **excerpt(content, maximum)})
        if not any(x['id'].lower() == f'{source}:p{page:04d}' for x in results):
            raise ValueError('Source page not found')
        results.sort(key=lambda row: int(row['id'].rsplit('p', 1)[1]))
        result = {'results': results}
        if include_evidence:
            result['evidence'] = evidence(folder, source, page, limit, maximum)
        return result
    if query is None or not query.strip():
        raise ValueError('Provide a nonempty query')
    needle = query.casefold().strip()
    terms = [needle] if literal else re.findall(r'\w+', needle)
    if not terms:
        raise ValueError('Query contains no searchable terms; use --literal')
    results = []
    for item in runtime_records(refs, folder):
        content = json.dumps(item, ensure_ascii=False)
        if (all(term in content.casefold() for term in terms)
                and family_matches(item, family) and firmware_matches(item, firmware)):
            results.append({'id': item['id'], 'evidence_category': item.get('evidence_category'),
                            'model': item.get('model'), 'firmware': item.get('firmware'),
                            'historical': True, **excerpt(content, maximum, terms[0])})
            if len(results) == limit:
                return {'results': results, 'corpus_available': bool(folder)}
    if firmware:
        return {'results': results, 'corpus_available': bool(folder)}
    for item in registry_records(refs):
        content = json.dumps(item, ensure_ascii=False)
        if all(term in content.casefold() for term in terms) and (not family or family_matches(item, family)):
            results.append({'id': item.get('id'), **excerpt(content, maximum, terms[0])})
            if len(results) == limit:
                return {'results': results, 'corpus_available': bool(folder)}
    for ident, content in chain(references(skill), pages(folder)):
        folded = content.casefold()
        if all(term in folded for term in terms):
            # Family filter uses actual source text, never assumes inheritance.
            if family and not re.search(r'(?<![a-z0-9])' + re.escape(family.casefold()) + (r'(?![a-z0-9-])' if family == 'IV4' else r'(?![a-z0-9])'), folded):
                continue
            results.append({'id': ident, **excerpt(content, maximum, terms[0])})
            if len(results) == limit:
                break
    return {'results': results, 'corpus_available': bool(folder)}


def main():
    if hasattr(sys.stdout, 'reconfigure'):
        sys.stdout.reconfigure(encoding='utf-8')
    parser = argparse.ArgumentParser(description=__doc__)
    g = parser.add_mutually_exclusive_group(required=True)
    for option in ('query', 'id', 'command', 'descriptor'):
        g.add_argument('--' + option)
    g.add_argument('--status', action='store_true')
    parser.add_argument('--corpus', default=os.getenv('KEYENCE_IV4_KB'))
    parser.add_argument('--literal', action='store_true')
    parser.add_argument('--family', choices=['IV4', 'IV4-H'])
    parser.add_argument('--firmware', help='Exact firmware filter for historical runtime query/ID only')
    parser.add_argument('--limit', type=int, default=10)
    parser.add_argument('--neighbors', type=int, default=0)
    parser.add_argument('--max-chars', type=int, default=2500)
    parser.add_argument('--evidence', action='store_true')
    a = parser.parse_args()
    try:
        result = lookup(corpus=a.corpus, query=a.query, address=a.id, command=a.command, descriptor=a.descriptor,
                        status=a.status, literal=a.literal, limit=a.limit, family=a.family, firmware=a.firmware,
                        neighbors=a.neighbors, maximum=a.max_chars, include_evidence=a.evidence)
        print(json.dumps(result, ensure_ascii=False, indent=2))
    except (ValueError, OSError, json.JSONDecodeError) as exc:
        print(f'Lookup error: {exc}', file=sys.stderr)
        return 2
    return 0


if __name__ == '__main__':
    sys.exit(main())
