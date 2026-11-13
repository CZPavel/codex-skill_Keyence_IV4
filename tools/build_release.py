"""Package only Git-tracked public files; validate an isolated installed ZIP copy."""
import argparse,hashlib,importlib.util,json,subprocess,tempfile,zipfile,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def build(output):
 output=Path(output);output.mkdir(parents=True,exist_ok=True)
 if subprocess.run(['git','status','--porcelain','--untracked-files=no'],cwd=ROOT,capture_output=True,text=True,check=True).stdout.strip():raise ValueError('Release requires a clean committed tree')
 files=subprocess.run(['git','ls-files','-z'],cwd=ROOT,capture_output=True,check=True).stdout.decode('utf-8').split('\0');files=sorted(n for n in files if n)
 if not files:raise ValueError('No tracked public files')
 spec=importlib.util.spec_from_file_location('audit',ROOT/'tools/public_audit.py');audit=importlib.util.module_from_spec(spec);spec.loader.exec_module(audit);audit.audit()
 version=json.loads((ROOT/'skills/keyence-iv4/version.json').read_text(encoding='utf-8'))['version'];dest=output/('keyence-iv4-'+version+'.zip')
 if dest.exists():raise ValueError('Refuse to overwrite existing release archive')
 with zipfile.ZipFile(dest,'w',compression=zipfile.ZIP_DEFLATED,compresslevel=9) as z:
  for name in files:
   data=subprocess.run(['git','show','HEAD:'+name],cwd=ROOT,capture_output=True,check=True).stdout;audit.inspect(name,data);info=zipfile.ZipInfo(name,date_time=(1980,1,1,0,0,0));info.external_attr=0o100644<<16;info.compress_type=zipfile.ZIP_DEFLATED;z.writestr(info,data)
 with tempfile.TemporaryDirectory(prefix='iv4-release-check-') as temp:
  folder=Path(temp)/'package';folder.mkdir()
  with zipfile.ZipFile(dest) as z:
   assert z.testzip() is None
   for i in z.infolist():assert not Path(i.filename).is_absolute() and '..' not in Path(i.filename).parts
   z.extractall(folder)
  subprocess.run([sys.executable,'-X','utf8',str(folder/'tools/manage.py'),'validate'],cwd=folder,check=True,capture_output=True)
  parent=Path(temp)/'skills'
  subprocess.run([sys.executable,'-X','utf8',str(folder/'tools/manage.py'),'install','--skills-dir',str(parent)],cwd=folder,check=True,capture_output=True)
  result=subprocess.run([sys.executable,'-I','-S',str(parent/'keyence-iv4/scripts/lookup.py'),'--command','PR','--family','IV4'],cwd=temp,check=True,capture_output=True,text=True,encoding='utf-8')
  assert json.loads(result.stdout)['total_matches']==1
  subprocess.run([sys.executable,'-X','utf8',str(folder/'tools/manage.py'),'uninstall','--skills-dir',str(parent)],cwd=folder,check=True,capture_output=True)
 digest=hashlib.sha256(dest.read_bytes()).hexdigest();(output/'SHA256SUMS.txt').write_text(digest+'  '+dest.name+'\n',encoding='utf-8')
 commit=subprocess.run(['git','rev-parse','HEAD'],cwd=ROOT,capture_output=True,text=True,check=True).stdout.strip()
 metrics={'version':version,'source_commit':commit,'public_files':len(files),'archive':dest.name,'bytes':dest.stat().st_size,'sha256':digest,'isolated_zip_install_lookup_uninstall':'PASS','hardware_test':False}
 (output/'release-metrics.json').write_text(json.dumps(metrics,indent=2)+'\n',encoding='utf-8');print(json.dumps(metrics,indent=2))
if __name__=='__main__':
 p=argparse.ArgumentParser(description=__doc__);p.add_argument('--output',type=Path,required=True);a=p.parse_args();build(a.output)
