import subprocess,json,concurrent.futures,pathlib
p=pathlib.Path(__file__).parent
def get(row):
 n,u=row
 r=subprocess.run(['curl','-L','--fail','-sS',u,'-o',str(p/n)],capture_output=True)
 return n,r.returncode,(p/n).stat().st_size if (p/n).exists() else 0,r.stderr.decode()[:100]
with concurrent.futures.ThreadPoolExecutor(max_workers=3) as ex:
 for r in ex.map(get,json.loads((p/'downloads.json').read_text())):print(r,flush=True)
