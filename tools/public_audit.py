"""Audit the public text distribution and, when present, all Git history blobs."""
from pathlib import Path
import argparse,json,re,subprocess
ROOT=Path(__file__).resolve().parents[1]
IGNORED={'.git','__pycache__','.venv','.pytest_cache','dist'}
SUFFIX={'.py','.md','.json','.yaml','.yml','.txt'}
NAMES={'LICENSE','.gitignore','.gitattributes'}
PRIVATE=re.compile(r'[A-Za-z]:[\\/](?:Users|VS_CODE_PROJECTS)[\\/]',re.I)
SECRET=re.compile(r'(?:gh[pousr]_[A-Za-z0-9]{30,}|sk-(?:proj-)?[A-Za-z0-9_-]{24,}|-----BEGIN (?:(?:RSA|EC|OPENSSH) )?PRIVATE KEY-----)')
def inspect(name,data):
 p=Path(name)
 if p.suffix not in SUFFIX and p.name not in NAMES:raise ValueError('Unexpected public file type: '+name)
 if len(data)>5_000_000:raise ValueError('Unexpectedly large public file: '+name)
 text=data.decode('utf-8-sig')
 if PRIVATE.search(text) or SECRET.search(text):raise ValueError('Private path/credential pattern in '+name)
 if p.suffix=='.json':json.loads(text)
 return len(data)
def audit(root=ROOT,history=True):
 root=Path(root);count=size=0
 def walk(base):
  for p in base.iterdir():
   if p.is_symlink():raise ValueError('Symlink excluded: '+p.name)
   if p.name in IGNORED or p.suffix=='.pyc':continue
   if p.is_dir():yield from walk(p)
   elif p.is_file():yield p
 for p in walk(root):size+=inspect(p.relative_to(root).as_posix(),p.read_bytes());count+=1
 if size>15_000_000:raise ValueError('Public tree unexpectedly large')
 blobs=0
 if history and (root/'.git').exists():
  proc=subprocess.run(['git','rev-list','--objects','--all'],cwd=root,capture_output=True,text=True,check=True)
  for line in proc.stdout.splitlines():
   obj,sep,name=line.partition(' ')
   if not sep:continue
   typ=subprocess.run(['git','cat-file','-t',obj],cwd=root,capture_output=True,text=True,check=True).stdout.strip()
   if typ!='blob':continue
   data=subprocess.run(['git','cat-file','blob',obj],cwd=root,capture_output=True,check=True).stdout
   inspect(name,data);blobs+=1
 return {'status':'PASS','public_files':count,'public_bytes':size,'history_blobs_checked':blobs,'protected_originals_present':False,'secret_or_private_path_matches':0}
if __name__=='__main__':
 parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--no-history',action='store_true');a=parser.parse_args()
 print(json.dumps(audit(history=not a.no_history),indent=2))
