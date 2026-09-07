// Original code-native paper-rotor illustrations; not measured experiment footage.
import fs from 'node:fs/promises';
import path from 'node:path';
import {spawn,execFileSync} from 'node:child_process';
import {once} from 'node:events';
import {createRequire} from 'node:module';
const require=createRequire(import.meta.url),sharp=require('../.tools-node/node_modules/sharp');
sharp.concurrency(1);
const ROOT=path.resolve(import.meta.dirname,'..'),OUT=path.join(ROOT,'assets/motion/2026-09-07/reels/paper-illustrative');
const W=1920,H=1080,FPS=60,D=7;
const names=['01-rotor-drop','02-cut-lines','03-opposite-folds','04-equal-height','05-repeat-and-time'];
const titles=['AIR SLOWS THE FALL','CUT THE TEMPLATE','FOLD IN OPPOSITE DIRECTIONS','START AT THE SAME HEIGHT','REPEAT. OBSERVE. COMPARE.'];
const txt=(x,y,s,size=22,fill='#e1f2ef',extra='')=>`<text x="${x}" y="${y}" font-family="Arial,sans-serif" font-size="${size}" fill="${fill}" ${extra}>${s}</text>`;
const line=(x,y,X,Y,c='#72c8c0',extra='')=>`<line x1="${x}" y1="${y}" x2="${X}" y2="${Y}" stroke="${c}" stroke-width="2" ${extra}/>`;
const ease=p=>{p=Math.min(1,Math.max(0,p));return p*p*(3-2*p);};
function rotor(x,y,a,fold=1,s=1,color='#f5e8bb'){
 const f=fold*Math.PI*.48;
 const proj=([X,Y,Z])=>{const xx=X*Math.cos(a)+Z*Math.sin(a),zz=-X*Math.sin(a)+Z*Math.cos(a);return [xx,Y*.83-zz*.46];};
 const poly=(pts,c)=>`<polygon points="${pts.map(p=>proj(p).join(',')).join(' ')}" fill="${c}" stroke="#766f54" stroke-width="1.2"/>`;
 const blade=(side)=>{const X=side<0?-28:0,Z=side*Math.sin(f)*120,Y=-Math.cos(f)*120;return [[X,0,0],[X+28,0,0],[X+28,Y,Z],[X,Y,Z]];};
 const shapes=[{p:[[-28,0,0],[28,0,0],[17,119,5],[-17,119,5]],c:color},{p:blade(-1),c:'#fff4cf'},{p:blade(1),c:'#d9c98e'},{p:[[-17,104,5],[17,104,5],[17,124,11],[-17,124,11]],c:'#bcae7b'}];
 shapes.sort((p,q)=>p.p.reduce((v,r)=>v-r[0]*Math.sin(a)+r[2]*Math.cos(a),0)/p.p.length-q.p.reduce((v,r)=>v-r[0]*Math.sin(a)+r[2]*Math.cos(a),0)/q.p.length);
 return `<g transform="translate(${x} ${y}) scale(${s})">${shapes.map(p=>poly(p.p,p.c)).join('')}</g>`;
}
export function svg(i,t){let b='';const p=t/D;
 if(i===0){const y=146+220*ease(p);b=`<ellipse cx="480" cy="465" rx="${46-17*p}" ry="10" fill="#030d12" opacity=".5"/>${Array.from({length:8},(_,j)=>{let yy=150+(j*47-t*24+400)%290;return line(350+j%2*260,yy,350+j%2*260,yy-19,'#65b9b6','opacity=".22"');}).join('')}${rotor(480+12*Math.sin(t),y,t*4.4,1,1.2)}`;}
 if(i===1){const cut=ease(t/5);b=`<g transform="translate(480 285) rotate(${4*Math.sin(t*.4)})"><path d="M-72 -142 H72 V145 H-72Z" fill="#f3e7bc" stroke="#9d916c" stroke-width="2"/>${line(0,-142,0,-12,'#467d82','stroke-dasharray="8 5"')}${line(-72,22,-28,22,'#467d82','stroke-dasharray="8 5"')}${line(28,22,72,22,'#467d82','stroke-dasharray="8 5"')}<path d="M0 -142 V${-142+130*cut}" stroke="#133e48" stroke-width="4"/><circle cx="0" cy="${-142+130*cut}" r="5" fill="#55c7c0"/><path d="M-72 22 H${-72+44*cut} M72 22 H${72-44*cut}" stroke="#133e48" stroke-width="3"/><path d="M-28 23 V145 M28 23 V145" stroke="#497d80" stroke-width="2" stroke-dasharray="6 5"/></g>${txt(480,488,'Side panels stay attached and fold inward',15,'#acd0cb','text-anchor="middle"')}`;}
 if(i===2){const f=ease((t-.4)/5);b=rotor(480,289,.35+.25*Math.sin(t*.4),f,1.65)+`<path d="M310 237 Q277 285 335 330 M335 330 L322 311 M335 330 L311 332" fill="none" stroke="#7ee3d4" stroke-width="3" transform="translate(0 ${Math.sin(t*2)*5})"/><path d="M650 331 Q690 283 628 238 M628 238 L651 240 M628 238 L641 258" fill="none" stroke="#eecb75" stroke-width="3" transform="translate(0 ${-Math.sin(t*2)*5})"/>`;}
 if(i===3){const q=ease(p);b=line(180,155,780,155,'#a2dad1','stroke-dasharray="6 8"')+rotor(325,175+205*q,t*4,1,1.1)+rotor(635,175+187*q,t*3.7+.4,1,1.1,'#dae7d5')+txt(480,130,'SAME RELEASE HEIGHT',15,'#b6e1d8','text-anchor="middle"')+txt(480,474,'Compare designs · no measured result shown',16,'#aaccc9','text-anchor="middle"');}
 if(i===4){const q=(t%2.3)/2.3,ang=q*Math.PI*2; b=rotor(369,170+230*ease(q),q*10,1,1.04)+`<g transform="translate(659 289)"><circle r="71" fill="#0c2d38" stroke="#9dd8ce" stroke-width="4"/><rect x="-13" y="-92" width="26" height="15" rx="4" fill="#9dd8ce"/>${Array.from({length:12},(_,j)=>line(Math.sin(j*Math.PI/6)*57,-Math.cos(j*Math.PI/6)*57,Math.sin(j*Math.PI/6)*63,-Math.cos(j*Math.PI/6)*63,'#73a8a5')).join('')}${line(0,0,Math.sin(ang)*51,-Math.cos(ang)*51,'#edd08c')}<circle r="5" fill="#edd08c"/></g>${txt(659,399,'Observe elapsed time',17,'#c7e5df','text-anchor="middle"')}${txt(659,425,'Illustrative clock · no numeric result',13,'#9cbbb8','text-anchor="middle"')}`;}
 return `<svg xmlns="http://www.w3.org/2000/svg" width="${W}" height="${H}" viewBox="0 0 960 540"><defs><linearGradient id="bg" x2="0" y2="1"><stop stop-color="#08202e"/><stop offset="1" stop-color="#17404b"/></linearGradient></defs><rect width="960" height="540" fill="url(#bg)"/>${Array.from({length:18},(_,j)=>line(j*60,92,j*60,475,'#a3c9c5','opacity=".025"')).join('')}${txt(48,63,titles[i],23,'#e4f6ef','letter-spacing="2"')}${b}<rect x="624" y="500" width="304" height="27" rx="4" fill="#071923"/>${txt(916,519,'Illustrative animation · Not to scale',14,'#c4ded8','text-anchor="end"')}</svg>`;
}
await fs.mkdir(OUT,{recursive:true});
if(process.argv.includes('--preview')){const tiles=[];for(let i=0;i<5;i++)tiles.push({input:await sharp(Buffer.from(svg(i,3.4))).resize(480,270).png().toBuffer(),left:0,top:i*270});await sharp({create:{width:480,height:1350,channels:3,background:'#08202e'}}).composite(tiles).jpeg().toFile('/private/tmp/newhorizons-paper-original-preview.jpg');}
else {for(let i=0;i<5;i++){if(process.argv.includes('--scene-2')&&i!==1)continue;const target=path.join(OUT,names[i]+'.mp4');const proc=spawn('ffmpeg',['-nostdin','-n','-v','error','-f','rawvideo','-pix_fmt','rgb24','-s',`${W}x${H}`,'-r',`${FPS}`,'-i','pipe:0','-an','-c:v','libx264','-preset','veryfast','-crf','19','-threads','2','-pix_fmt','yuv420p','-movflags','+faststart',target],{stdio:['pipe','inherit','inherit']});let error;proc.stdin.on('error',e=>error=e);const done=once(proc,'close');for(let f=0;f<FPS*D;f++){if(error)throw error;const raw=await sharp(Buffer.from(svg(i,f/FPS))).removeAlpha().raw().toBuffer();if(!proc.stdin.write(raw))await once(proc.stdin,'drain');}proc.stdin.end();const [code]=await done;if(code)throw Error(`ffmpeg ${code}`);console.log(target);}}
