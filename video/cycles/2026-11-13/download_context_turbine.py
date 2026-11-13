import io,urllib.request,zipfile
url='https://mhkdr.openei.org/files/599/Event_OpticalandSonarVideos.zip'; size=1731078530
class Remote(io.RawIOBase):
 def __init__(self):self.pos=0
 def readable(self):return True
 def seekable(self):return True
 def tell(self):return self.pos
 def seek(self,offset,whence=0):
  self.pos=(offset if whence==0 else self.pos+offset if whence==1 else size+offset);return self.pos
 def read(self,n=-1):
  if n<0:n=size-self.pos
  if n==0:return b''
  req=urllib.request.Request(url,headers={'Range':f'bytes={self.pos}-{min(size-1,self.pos+n-1)}','User-Agent':'NewHorizonsEditorial/1.0'});r=urllib.request.urlopen(req,timeout=30)
  if r.status!=206:raise RuntimeError(f'Range unsupported: {r.status}')
  b=r.read();self.pos+=len(b);return b
z=zipfile.ZipFile(Remote())
from pathlib import Path
out=Path("assets/motion/2026-11-13/main");out.mkdir(parents=True,exist_ok=True)
names=["Event_OpticalandSonarVideos/Bird_2023_11_02_21_17_07/Bird_2023_11_02_21_17_07_Opt.avi","Event_OpticalandSonarVideos/Bird_2023_11_19_20_42_18/Bird_2023_11_19_20_42_18_Opt.avi","Event_OpticalandSonarVideos/Bird_2023_12_01_18_16_47/Bird_2023_12_01_18_16_47_Opt.avi"]
for i,n in enumerate(names,1):
 p=out/f"sequim-turbine-{i:02}.avi";p.write_bytes(z.read(n));print(n,p,p.stat().st_size,flush=True)
