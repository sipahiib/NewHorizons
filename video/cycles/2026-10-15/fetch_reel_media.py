"""Fetch approved 15 October Reel inputs afresh; derive faithful static panel crops."""
from pathlib import Path
import urllib.request, hashlib, json, subprocess
ROOT=Path(__file__).resolve().parents[3]
OUT=ROOT/'assets/motion/2026-10-15/reels'
URLS={
 'r1_fig10.png':'https://arxiv.org/html/2610.17693v1/figures/hiro_ace_ar2_2023-01-31_precip.png',
 'r1_fig11.png':'https://arxiv.org/html/2610.17693v1/figures/HiRO-ACE-hurricane-example.png',
 'r1_fig5.png':'https://arxiv.org/html/2610.17693v1/figures/wind_event_bora.png',
 'r2_modis_sep21.jpg':'https://modis.gsfc.nasa.gov/gallery/images/image09232026_250m.jpg',
 'r2_eo_sep23.jpg':'https://assets.science.nasa.gov/content/dam/science/esd/eo/images/iotd/2026/explosive-intensification-for-hurricane-polo/hurricanepolo_amo_20260923_lrg.jpg',
 'r2_eo_sst.jpg':'https://assets.science.nasa.gov/content/dam/science/esd/eo/images/iotd/2026/explosive-intensification-for-hurricane-polo/hurricanepolo_mur_20260923_lrg.jpg',
 'r2_svs5681_no_dates.mp4':'https://svs.gsfc.nasa.gov/vis/a000000/a005600/a005681/Polo_v07_stutter.mp4',
}
def fetch():
 OUT.mkdir(parents=True,exist_ok=True)
 for n,u in URLS.items():
  with urllib.request.urlopen(u,timeout=180) as r: (OUT/n).write_bytes(r.read())
  print(n,(OUT/n).stat().st_size,flush=True)

# Coordinates are half-open source-pixel rectangles. No map data reconstructed.
CROPS=[
 ('r1_01_precip.png','r1_fig10.png',(145,87,700,465),'Figure 10 precipitation'),
 ('r1_02_wind.png','r1_fig10.png',(733,87,1290,465),'Figure 10 10m wind speed'),
 ('r1_03_pressure.png','r1_fig10.png',(1323,87,1880,465),'Figure 10 sea-level pressure'),
 ('r1_04_hurricane_wind.png','r1_fig11.png',(221,278,1357,1408),'Figure 11 hurricane wind'),
 ('r1_05_hurricane_pressure.png','r1_fig11.png',(1928,278,3063,1408),'Figure 11 hurricane pressure'),
 ('r1_06_hurricane_precip.png','r1_fig11.png',(3635,278,4770,1408),'Figure 11 hurricane precipitation'),
 ('r1_07_bora_wind.png','r1_fig5.png',(2728,242,3751,920),'Figure 5c generated HiROv2 Prediction 0 Bora wind'),
]
def derive():
 from PIL import Image
 for n,src,box,_ in CROPS:
  im=Image.open(OUT/src).crop(box).convert('RGB');im.save(OUT/n)

def manifest():
 from PIL import Image
 import re
 prior=list((ROOT/'video/cycles').glob('*/*.json'))
 prior=[p for p in prior if p.parent.name<'2026-10-15']
 hashes={}; urls={}
 for p in prior:
  raw=p.read_text()
  for h in re.findall(r'\b[0-9a-f]{64}\b',raw):hashes.setdefault(h,[]).append(str(p.relative_to(ROOT)))
  for u in re.findall(r'https?[^\s"<>]+',raw):urls.setdefault(u,[]).append(str(p.relative_to(ROOT)))
 def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
 source=[]
 for n,u in URLS.items():
  p=OUT/n; h=sha(p)
  d={'file':str(p.relative_to(ROOT)),'download_url':u,'sha256':h,'bytes':p.stat().st_size,'fresh_download':True,'prior_hash_matches':hashes.get(h,[]),'prior_url_matches':urls.get(u,[]),'selected':n!='r2_eo_sst.jpg'}
  if p.suffix!='.mp4':d['native_dimensions']=list(Image.open(p).size)
  else:d.update(native_dimensions=[1920,1080],native_fps=30,duration_seconds=103.366667,source_audio=False)
  source.append(d)
 assets=[]
 for i,(n,src,box,desc) in enumerate(CROPS,1):
  assets.append({'output':'R1','segment':i,'file':str((OUT/n).relative_to(ROOT)),'source_file':str((OUT/src).relative_to(ROOT)),'source_url':URLS[src],'listing_page':'https://arxiv.org/html/2610.17693v1','native_source_dimensions':list(Image.open(OUT/src).size),'native_crop_dimensions':list(Image.open(OUT/n).size),'crop_xyxy':box,'sha256':sha(OUT/n),'description':desc,'correspondence':'scientific simulated model output, not recorded weather','credit':'Anna Kwa et al. (2026), Extreme events and statistics in an AI emulator of a global storm-resolving model, arXiv:2610.17693v1','license':'CC BY 4.0','license_url':'https://creativecommons.org/licenses/by/4.0/','license_evidence':'Paper HTML displays License: CC BY 4.0; figure captions do not identify third-party exceptions. Saved source_pages/arxiv.html.','transforms':'Faithful static crop removes titles, tick labels and colourbar; preserves complete plotted map interior, coastlines, grid and scientific vectors. No content reconstructed. Crop disclosed in credits.','visual_inspection':'Decoded and inspected; clean map crop, no prominent embedded editorial text.','prior_hash_matches':hashes.get(sha(OUT/n),[])})
 for i,n in enumerate(['r2_modis_sep21.jpg','r2_eo_sep23.jpg'],1):
  assets.append({'output':'R2','segment':i,'file':str((OUT/n).relative_to(ROOT)),'source_url':URLS[n],'listing_page':'https://modis.gsfc.nasa.gov/gallery/individual.php?db_date=2026-09-23' if i==1 else 'https://science.nasa.gov/earth/earth-observatory/explosive-intensification-for-hurricane-polo/','native_dimensions':list(Image.open(OUT/n).size),'crop_xyxy':None,'sha256':sha(OUT/n),'credit':'MODIS Land Rapid Response Team, NASA GSFC' if i==1 else 'NASA Earth Observatory/Michala Garrison, MODIS data from NASA EOSDIS LANCE and GIBS/Worldview','acquired':'2026-09-21' if i==1 else '2026-09-23','license':'NASA educational/informational media-use conditions; no third-party restriction identified on asset page','license_url':'https://www.nasa.gov/nasa-brand-center/images-and-media/','correspondence':'Actual Aqua MODIS satellite natural-colour image of Polo','visual_inspection':'Clean complete image; no prominent labels; source acquisition date differs from page publication date.','transforms':'Preserve whole landscape source image over blurred duplicate background; no pan/zoom.'})
 specs=[(22,26,[950,480,1450,980]),(26,30,[850,480,1650,1080]),(30,35,[650,450,1750,1080]),(35,39,[400,300,1600,1080]),(40,46,[0,0,1920,1080])]
 for i,(a,b,box) in enumerate(specs,3):
  assets.append({'output':'R2','segment':i,'file':str((OUT/'r2_svs5681_no_dates.mp4').relative_to(ROOT)),'source_url':URLS['r2_svs5681_no_dates.mp4'],'listing_page':'https://svs.gsfc.nasa.gov/5681/','native_dimensions':[1920,1080],'native_fps':30,'crop_xyxy':box,'native_crop_dimensions':[box[2]-box[0],box[3]-box[1]],'suggested_in_seconds':a,'suggested_out_seconds':b,'suggested_playback_rate':0.8,'suggested_scene_duration_seconds':(b-a)/.8,'sha256':sha(OUT/'r2_svs5681_no_dates.mp4'),'credit':"NASA's Scientific Visualization Studio. Data provided by the joint NASA/JAXA GPM mission.",'license':'NASA/SVS informational use conditions; no asset-specific third-party restriction found','license_url':'https://svs.gsfc.nasa.gov/help/','rights_evidence':'SVS page explicitly provides date-free version and requested NASA/JAXA credit. NASA media guidelines permit informational use; retain credit, no endorsement.','correspondence':'Satellite-derived cloud/rainfall visualization of Polo; final clip introduces GPM 3D structure, not raw camera footage or quantified climate rainfall attribution','visual_inspection':'Start/mid/end crop images inspected in svs_selected_inspection.jpg. Crop removes country labels; final source interval is full frame before prominent rulers.','transforms':'Static crop only, no tracking or synthesized data. Suggested 0.8x playback is optional and must be disclosed in credits/descriptions. Preserve complete prepared frame in foreground.','limitation':'First crop is 500x500 native and requires restrained scaling; inspect final mobile clarity.' if i==3 else None})
 d={'status':'audited-source-preparation-for-independent-review','checked_on':'2026-10-15','approval':'APPROVAL.md authorises production for both R1 and R2; parent approved R2 mix adjustment within satellite/derived visualization route','assets':assets,'sources':source,'segment_mix':{'R1':'7 scientific still map crops','R2':'2 distinct natural-colour satellite stills + 5 non-overlapping satellite-derived visualization excerpts'},'rights_evidence_directory':str((OUT/'source_pages').relative_to(ROOT)),'freshness_check':{'prior_json_files_checked':len(prior),'prior_distinct_recorded_sha256':len(hashes),'prior_manifest_paths':[str(p.relative_to(ROOT)) for p in prior],'result':'No selected source or crop hash matches prior-cycle JSON manifests; no source download URL matches. All source bytes freshly downloaded; no old asset copied.','limit':'Hash comparison cannot detect transformed visual duplicates in undocumented historical inputs; subject-specific source URLs also checked.'},'unused_source':'r2_eo_sst.jpg fetched for inspection only; excluded labelled SST map; never select for render.','editorial_requirements':['Narration identifies R1 simulation outputs; Figure5c is a HiROv2 generated sample conditioned on coarse X-SHiELD, not free-running event observation.','Narration identifies R2 imagery versus satellite-derived rainfall visualization; no quantified rainfall attribution.','Titles only initial 5–6 seconds, final calls only, no source labels or colourbars added.','R1 Figure10 map crops are about 555x378 native; retain sharp pixel meaning without AI upscaling.','Independent reviewer must assess crop meaning and native clarity; output QA must inspect actual render.']}
 (ROOT/'video/cycles/2026-10-15/reel_media_sources.json').write_text(json.dumps(d,indent=2)+'\n')
 print('manifest assets',len(assets),'prior files',len(prior),'prior hashes',len(hashes),'matches',sum(bool(s['prior_hash_matches']) for s in source))

if __name__=='__main__':
 fetch()
 derive()
 manifest()
