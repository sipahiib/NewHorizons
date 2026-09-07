// Original procedural animation. No external footage, photographs or stock images.
import fs from 'node:fs/promises';
import path from 'node:path';
import {spawn} from 'node:child_process';
import {once} from 'node:events';
import {createRequire} from 'node:module';
const require=createRequire(import.meta.url);
const sharp=require('../.tools-node/node_modules/sharp');
const ROOT = path.resolve(import.meta.dirname,'..');
const OUT = path.join(ROOT,'assets/motion/2026-09-07/main-illustrative');
const FPS=60, SECONDS=11, W=1920, H=1080;
sharp.concurrency(1);
export const scenes = [
  ['01-liftoff','A NEW ROUTE TO SPACE'],
  ['02-coastal-ascent','LAUNCHING FROM NORWAY'],
  ['03-flight-path','FROM ASCENT TO ORBIT'],
  ['04-propulsion','TURNING ENERGY INTO MOTION'],
  ['05-stage-separation','LEAVING A STAGE BEHIND'],
  ['06-upper-stage','CONTINUING THE CLIMB'],
  ['07-fairing-release','UNCOVERING THE PAYLOAD'],
  ['08-payload-deployment','RELEASING SATELLITES'],
  ['09-ground-contact','WAITING FOR CONFIRMATION'],
  ['10-launch-options','MORE WAYS TO REACH SPACE'],
];
const clamp=x=>Math.max(0,Math.min(1,x));
const ease=x=>{x=clamp(x);return x*x*(3-2*x);};
const line=(x1,y1,x2,y2,color='#66dfef',width=2,extra='')=>`<line x1="${x1}" y1="${y1}" x2="${x2}" y2="${y2}" stroke="${color}" stroke-width="${width}" ${extra}/>`;
const text=(x,y,s,size=14,color='#e0f4ff',extra='')=>`<text x="${x}" y="${y}" font-family="Arial,sans-serif" font-size="${size}" fill="${color}" ${extra}>${s}</text>`;
function stars(t) {return Array.from({length:105},(_,i)=>{
  const x=(i*139.713+t*(2+i%4))%980-10,y=(i*i*29.17)%470;
  return `<circle cx="${x}" cy="${y}" r="${i%7===0?1.4:.65}" fill="#c8edff" opacity="${.15+.25*(1+Math.sin(i+t*.5))/2}"/>`;
}).join('');}
function plume(t,length=135) {
  const f=1+.05*Math.sin(t*71)+.04*Math.sin(t*103);
  return `<path d="M-13 70 Q-24 110 0 ${70+length*f} Q24 110 13 70Z" fill="url(#flame)"/><path d="M-5 70 Q-9 100 0 ${70+length*.58*f} Q9 100 5 70Z" fill="#eafcff"/>`;
}
function rocket(t,{upper=false,fire=true,nose=true}={}) {
  return `<g>${fire?plume(t,upper?90:145):''}<path d="M-17 ${upper?-35:-95} L-17 57 L-25 70 L25 70 L17 57 L17 ${upper?-35:-95}Z" fill="url(#metal)" stroke="#79aebc" stroke-width=".8"/>${nose?`<path d="M-17 ${upper?-35:-95} Q-13 ${upper?-64:-129} 0 ${upper?-78:-143} Q13 ${upper?-64:-129} 17 ${upper?-35:-95}Z" fill="url(#metal)"/>`:''}<rect x="-17" y="-9" width="34" height="5" fill="#1c394a"/>${!upper?'<path d="M-17 26 L-32 67 L-17 58 M17 26 L32 67 L17 58" fill="#3b7286"/>':''}<rect x="-12" y="60" width="24" height="10" rx="2" fill="#304856"/><path d="M-8 -65 V-28" stroke="#fff" opacity=".55" stroke-width="2"/></g>`;
}
function satellite(t,scale=1) {return `<g transform="scale(${scale}) rotate(${Math.sin(t*.4)*5})"><rect x="-15" y="-17" width="30" height="34" rx="3" fill="url(#gold)" stroke="#f7e5a4"/><path d="M-15 0 H-64 M15 0 H64" stroke="#b2d7df" stroke-width="3"/><g fill="#124a71" stroke="#62bfd9" stroke-width="1"><rect x="-75" y="-21" width="52" height="42"/><rect x="23" y="-21" width="52" height="42"/></g>${[-62,-49,-36,36,49,62].map(x=>line(x,-21,x,21,'#48a8cc',.6)).join('')}${line(-75,0,-23,0,'#48a8cc',.6)}${line(23,0,75,0,'#48a8cc',.6)}<path d="M0 -17 V-33 L10 -40" fill="none" stroke="#e5edf0" stroke-width="2"/></g>`;}
function earth(t,x=480,y=665,r=340) {
  return `<g><defs><clipPath id="localEarth"><circle cx="${x}" cy="${y}" r="${r}"/></clipPath></defs><circle cx="${x}" cy="${y}" r="${r+8}" fill="none" stroke="#4bd5ff" stroke-width="5" opacity=".15"/><circle cx="${x}" cy="${y}" r="${r}" fill="url(#earth)"/><g clip-path="url(#localEarth)">${Array.from({length:7},(_,i)=>`<path d="M${x-r} ${y-r+45+i*55} Q${x+70*Math.sin(t*.07+i)} ${y-r+i*55-55} ${x+r} ${y-r+i*55+45}" fill="none" stroke="#428696" stroke-width="${8+i%3*5}" opacity=".23"/>`).join('')}</g></g>`;
}
function svg(index,t) {
  const p=t/SECONDS,u=ease(p); let body='';
  if(index===0) {
    const y=392-165*ease(p), x=475+10*Math.sin(p);
    body=`<path d="M0 430 L160 368 L259 414 L368 383 L455 430 L659 375 L820 421 L960 397 V540 H0Z" fill="#102d3a"/><rect y="449" width="960" height="91" fill="#071c29"/>${Array.from({length:18},(_,i)=>line(0,468+i*4,960,465+i*4,'#315062',.5,'opacity=".25"')).join('')}<g transform="translate(385 430)"><path d="M0 0 V-200 H22 V0 M0 -190 L22 -165 L0 -140 L22 -115 L0 -90 L22 -65 L0 -40 L22 -15" fill="none" stroke="#47626d" stroke-width="5"/></g><path d="M432 448 H520 L542 461 H416Z" fill="#486270"/>${Array.from({length:22},(_,i)=>{const age=(t*.18+i*.047)%1;return `<ellipse cx="${475+(i%2?1:-1)*(18+age*150)}" cy="${448-age*12}" rx="${12+age*53}" ry="${9+age*20}" fill="#b5c3c5" opacity="${.22*(1-age)}"/>`;}).join('')}<g transform="translate(${x} ${y}) scale(.78)">${rocket(t)}</g>`;
  } else if(index===1) {
    body=`<path d="M0 ${405+t*5} Q160 ${320+t*5} 280 ${435+t*5} T600 ${415+t*5} T960 ${400+t*5} V620 H0Z" fill="#173947"/><path d="M0 ${442+t*5} Q230 ${390+t*5} 430 ${470+t*5} T960 ${456+t*5} V640 H0Z" fill="#10293b"/>${Array.from({length:8},(_,i)=>`<ellipse cx="${(i*179-t*24+1100)%1100-60}" cy="${250+(i*61+t*18)%340}" rx="${90+i*6}" ry="12" fill="#a5c4d6" opacity=".055"/>`).join('')}<g transform="translate(${470+65*u} ${262-36*u}) rotate(12) scale(.95)">${rocket(t)}</g>`;
  } else if(index===2) {
    body=earth(t);const angle=-2.5+u*1.6,x=480+430*Math.cos(angle),y=665+430*Math.sin(angle);
    body+=`<path d="M135 445 Q220 122 585 241 T887 464" fill="none" stroke="#73e1ee" stroke-width="2" opacity=".35" stroke-dasharray="5 10"/><g transform="translate(${x} ${y}) rotate(${angle*180/Math.PI+180}) scale(.29)">${rocket(t)}</g><circle cx="${x}" cy="${y}" r="16" fill="none" stroke="#8eedf0" opacity=".5"/>`;
  } else if(index===3) {
    body=`<g transform="translate(480 252)"><path d="M-80 -118 H80 V-54 L40 -10 V55 H-40 V-10 L-80 -54Z" fill="url(#metal)" stroke="#96d8e1"/><path d="M-34 35 Q-36 84 -76 123 H76 Q36 84 34 35Z" fill="#284b60" stroke="#a6d4dc" stroke-width="2"/><path d="M-15 -110 V40 M15 -110 V40" stroke="#40d4df" stroke-width="7" fill="none"/>${Array.from({length:12},(_,i)=>{const y=-115+(t*95+i*19)%155;return `<circle cx="${i%2?15:-15}" cy="${y}" r="4" fill="#defcff"/>`;}).join('')}<g transform="translate(0 51) scale(3 .95)">${plume(t,175)}</g><ellipse cy="120" rx="65" ry="8" fill="#cbf7ff" opacity=".55"/></g>`;
  } else if(index===4) {
    const sep=100*ease((t-2)/7);
    body=earth(t,480,825,400)+`<g transform="translate(480 255) rotate(35)"><g transform="translate(0 ${sep})"><path d="M-24 0 H24 V166 L32 181 H-32 L-24 166Z" fill="url(#metal)"/><rect x="-24" y="7" width="48" height="8" fill="#234758"/></g><g transform="translate(0 ${-sep*.7}) scale(1.05)">${rocket(t,{upper:true,fire:false})}</g>${sep>4?line(-23,70-sep*.7,23,70-sep*.7,'#73e4e9',2):''}</g>`;
  } else if(index===5) {
    body=earth(t,480,810,420)+`<g transform="translate(${440+90*u} ${255-35*u}) rotate(65) scale(1.2)">${rocket(t,{upper:true})}</g>${Array.from({length:12},(_,i)=>line((i*111-t*24+1200)%1100-100,80+i*28,(i*111-t*24+1200)%1100-35,80+i*28,'#7fbdcf',.7,'opacity=".12"')).join('')}`;
  } else if(index===6) {
    const split=145*ease((t-1)/8);
    body=earth(t,480,835,400)+`<g transform="translate(480 275) rotate(22)"><path d="M-26 20 H26 V155 H-26Z" fill="url(#metal)"/><g transform="translate(0 -16)">${satellite(t,.56)}</g><g transform="translate(${-split} ${-split*.25}) rotate(${-split*.12})"><path d="M0 -137 Q-36 -101 -37 -69 V16 H0Z" fill="url(#metal)" stroke="#8ac4cf"/></g><g transform="translate(${split} ${-split*.25}) rotate(${split*.12})"><path d="M0 -137 Q36 -101 37 -69 V16 H0Z" fill="url(#metal)" stroke="#8ac4cf"/></g></g>`;
  } else if(index===7) {
    const drift=ease((t-1)/9);
    body=earth(t,480,850,410)+`<g transform="translate(${360-45*drift} ${340+30*drift}) rotate(50)"><path d="M-28 -70 H28 V120 H-28Z" fill="url(#metal)"/><ellipse cy="-70" rx="28" ry="8" fill="#263f4d"/><path d="M-18 120 L-28 147 H28 L18 120" fill="#385566"/></g><g transform="translate(${425+210*drift} ${252-70*drift}) rotate(${15+drift*20})">${satellite(t,.85)}</g>`;
  } else if(index===8) {
    const sx=585+90*Math.sin(t*.12),sy=165+12*Math.cos(t*.2),gx=300,gy=443;
    body=earth(t,480,817,400)+`<g transform="translate(${sx} ${sy}) rotate(-12)">${satellite(t,.7)}</g><g transform="translate(${gx} ${gy})"><path d="M-40 -34 Q0 25 40 -34 Q0 -13 -40 -34Z" fill="url(#metal)"/><path d="M0 -9 V29 M-27 30 H27 M0 -17 L17 -52" fill="none" stroke="#b4dce4" stroke-width="5"/></g>${line(sx,sy+35,gx+15,gy-50,'#67dfea',1,'opacity=".25"')}${Array.from({length:5},(_,i)=>{const q=(t*.12+i/5)%1;return `<circle cx="${sx+(gx+15-sx)*q}" cy="${sy+35+(gy-50-sy-35)*q}" r="${2+q*3}" fill="#8cecf3" opacity="${Math.sin(q*Math.PI)}"/>`;}).join('')}`;
  } else {
    body=earth(t,480,705,365);
    for(let i=0;i<3;i++) {
      const a=-2.8+i*.64+u*.45,x=480+(430+i*17)*Math.cos(a),y=705+(430+i*17)*Math.sin(a);
      body+=`<path d="M${115+i*94} 449 Q${120+i*270} ${75+i*28} ${805+i*36} ${360+i*28}" fill="none" stroke="${['#58d9e8','#aacbe9','#e5bd79'][i]}" stroke-width="1.4" opacity=".35" stroke-dasharray="${5+i} 8"/><g transform="translate(${x} ${y}) rotate(${i*18+t*1.2})">${satellite(t+i,.3)}</g>`;
    }
  }
  const titleOpacity=ease(t/.6)*(1-ease((t-4)/.8));
  return `<svg xmlns="http://www.w3.org/2000/svg" width="${W}" height="${H}" viewBox="0 0 960 540"><defs><linearGradient id="sky" x2="0" y2="1"><stop stop-color="#030c1a"/><stop offset="1" stop-color="#15364a"/></linearGradient><linearGradient id="metal"><stop stop-color="#618493"/><stop offset=".36" stop-color="#f3f8f8"/><stop offset=".63" stop-color="#cedfe2"/><stop offset="1" stop-color="#416476"/></linearGradient><linearGradient id="gold"><stop stop-color="#9b6b2a"/><stop offset=".5" stop-color="#ecd696"/><stop offset="1" stop-color="#a27231"/></linearGradient><linearGradient id="flame" x2="0" y2="1"><stop stop-color="#efffff"/><stop offset=".25" stop-color="#8deaff"/><stop offset=".65" stop-color="#fbb669"/><stop offset="1" stop-color="#eb6842" stop-opacity="0"/></linearGradient><radialGradient id="earth" cx=".35" cy=".05" r=".85"><stop stop-color="#3886a4"/><stop offset=".25" stop-color="#1b5578"/><stop offset=".7" stop-color="#0b263e"/><stop offset="1" stop-color="#030b18"/></radialGradient><clipPath id="globeClip"><circle cx="480" cy="665" r="340"/></clipPath></defs><rect width="960" height="540" fill="url(#sky)"/>${stars(t)}${body}<g opacity="${titleOpacity}">${line(48,57,80,57,'#69dbe8',3)}${text(94,63,scenes[index][1],18,'#e3f5fa','letter-spacing="2"')}</g><rect x="638" y="484" width="278" height="32" rx="5" fill="#03101e" opacity=".88"/>${text(900,505,'Illustrative animation · Not to scale',13,'#c6e2eb','text-anchor="end"')}</svg>`;
}
await fs.mkdir(OUT,{recursive:true});
if(process.argv.includes('--preview')) {
  const tiles=[];
  for(let i=0;i<10;i++) {
    const b=await sharp(Buffer.from(svg(i,5.5))).resize(480,270).png().toBuffer();
    tiles.push({input:b,left:(i%2)*480,top:Math.floor(i/2)*270});
  }
  const preview=path.join(ROOT,'build/video/main-motion-preview.jpg');
  await fs.mkdir(path.dirname(preview),{recursive:true});
  await sharp({create:{width:960,height:1350,channels:3,background:'#071525'}}).composite(tiles).jpeg({quality:90}).toFile(preview);
  console.log(preview);
} else {
  const ids=process.argv.slice(2).map(Number);
  if(!ids.length || ids.some(i=>!Number.isInteger(i)||i<1||i>10)) throw new Error('Pass scene numbers 1–10 or --preview');
  for(const num of ids) {
    const index=num-1, target=path.join(OUT,scenes[index][0]+'.mp4');
    const proc=spawn('ffmpeg',['-nostdin','-n','-v','error','-f','rawvideo','-pix_fmt','rgb24','-s',`${W}x${H}`,'-r',String(FPS),'-i','pipe:0','-an','-c:v','libx264','-preset','veryfast','-crf','19','-threads','2','-pix_fmt','yuv420p','-color_primaries','bt709','-color_trc','bt709','-colorspace','bt709','-movflags','+faststart',target],{stdio:['pipe','inherit','inherit']});
    let pipeError;
    proc.stdin.on('error',e=>{pipeError=e;});
    const done=once(proc,'close');
    for(let frame=0;frame<FPS*SECONDS;frame++) {
      if(pipeError) throw pipeError;
      const raw=await sharp(Buffer.from(svg(index,frame/FPS))).removeAlpha().raw().toBuffer();
      if(!proc.stdin.write(raw)) await once(proc.stdin,'drain');
    }
    proc.stdin.end();
    const [code]=await done;if(code!==0) throw new Error(`ffmpeg failed: ${code}`);
    console.log(`DONE ${scenes[index][0]} ${SECONDS}s ${W}x${H} ${FPS}fps`);
  }
}
