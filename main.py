from fastapi import FastAPI
from fastapi.responses import HTMLResponse
import uvicorn

app = FastAPI(title="XOLO ANTI FRAUDE")

HTML_PAGE = """
<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>XOLO - DIOS XOLOTL | Anti Fraude</title>
<style>
  *{margin:0;padding:0;box-sizing:border-box}
  body{background:#0a0a0a;color:#fff;font-family:system-ui;display:flex;flex-direction:column;align-items:center;min-height:100vh;overflow-x:hidden}
  h1{font-size:2.2rem;margin:20px 0 5px;letter-spacing:3px;text-align:center;background:linear-gradient(90deg,#FFD700,#ff8c00);-webkit-background-clip:text;-webkit-text-fill-color:transparent}
  .xp-container{width:90%;max-width:500px;background:#222;border-radius:20px;height:28px;overflow:hidden;border:2px solid #333;margin:10px 0}
  .xp-bar{height:100%;background:linear-gradient(90deg,#FFD700,#ffaa00);width:0%;transition:width 0.6s ease;display:flex;align-items:center;justify-content:center;font-weight:900;color:#000;font-size:14px}
  .xp-text{font-size:1.1rem;margin:5px;color:#FFD700;font-weight:700}
  .xolo-stage{font-size:1rem;color:#aaa;letter-spacing:2px;margin-bottom:10px}
  .xolo-wrapper{width:100%;display:flex;justify-content:center;align-items:center;flex:1;min-height:55vh;position:relative}
  .xolo{width:280px;height:380px;transition:all 0.8s ease;filter:drop-shadow(0 0 20px rgba(255,215,0,0.3))}
  @media(min-width:768px){.xolo{width:400px;height:520px}}
  .breathe{animation:breathe 3s ease-in-out infinite}
  @keyframes breathe{0%,100%{transform:scale(1)}50%{transform:scale(1.02)}}
  .tail{animation:tail 0.8s ease-in-out infinite;transform-origin:top center}
  @keyframes tail{0%,100%{transform:rotate(-8deg)}50%{transform:rotate(8deg)}}
  .eye{animation:blink 4s infinite}
  @keyframes blink{0%,96%,100%{transform:scaleY(1)}97%,99%{transform:scaleY(0.1)}}
  .aura{animation:pulse 2s ease-in-out infinite}
  @keyframes pulse{0%,100%{opacity:0.6;transform:scale(1)}50%{opacity:1;transform:scale(1.05)}}
  .controls{width:90%;max-width:500px;display:flex;flex-direction:column;gap:12px;margin:20px 0 40px}
  input{padding:16px;border-radius:14px;border:2px solid #333;background:#1a1a1a;color:#fff;font-size:1rem;outline:none}
  input:focus{border-color:#FFD700}
  button{padding:16px;border-radius:14px;border:none;background:linear-gradient(90deg,#FFD700,#ff8c00);color:#000;font-weight:900;font-size:1.1rem;cursor:pointer;transition:transform 0.1s}
  button:active{transform:scale(0.97)}
  .result{padding:14px;border-radius:12px;text-align:center;font-weight:700;display:none}
  .safe{background:#0f3d1f;color:#4ade80;border:1px solid #16a34a}
  .danger{background:#4a1111;color:#f87171;border:1px solid #dc2626}
  .evolving{position:fixed;top:0;left:0;width:100%;height:100%;background:#000;display:none;align-items:center;justify-content:center;z-index:999;flex-direction:column}
  .evolving h2{font-size:3rem;color:#FFD700;animation:pulse 0.8s infinite}
</style>
</head>
<body>
<h1 id="title">XOLO - DIOS XOLOTL</h1>
<div class="xolo-stage" id="stage">CACHORRO</div>
<div class="xp-container"><div class="xp-bar" id="xpbar">0%</div></div>
<div class="xp-text" id="xptext">0 XP / 899 XP PARA SER DIOS</div>

<div class="xolo-wrapper" id="wrapper">
  <div class="xolo breathe" id="xolo"></div>
</div>

<div class="controls">
  <input id="inputFraude" placeholder="Pega link, mensaje o número sospechoso...">
  <button onclick="analizar()">🔍 ANALIZAR CON XOLO</button>
  <div class="result" id="result"></div>
</div>

<div class="evolving" id="evolving"><h2>¡EVOLUCIONANDO!</h2><p style="margin-top:20px;color:#fff">Tu Xolo está creciendo...</p></div>

<script>
let xp = parseInt(localStorage.getItem('xolo_xp')||'0');
const xolvl = [
 {min:0,max:99,name:'CACHORRO',desc:'Pequeño, orejas enormes, ojos ámbar'},
 {min:100,max:299,name:'JOVEN',desc:'Más alto, cuello alargado'},
 {min:300,max:599,name:'ADULTO',desc:'Elegante, arrugas en cuello, definición muscular'},
 {min:600,max:9999,name:'DIOS XOLOTL',desc:'Pezado cabeza dorado, collar con gemas, rayos dorados, aura divina'}
];

function getStage(x){return xololvl.find(s=>x>=s.min&&x<=s.max)}
function renderXolo(){
 const st = getStage(xp);
 document.getElementById('stage').innerText = st.name + ' - ' + st.desc;
 document.getElementById('xptext').innerText = xp+' XP / 899 XP PARA SER DIOS';
 document.getElementById('xpbar').style.width = Math.min((xp/899)*100,100)+'%';
 document.getElementById('xpbar').innerText = Math.floor((xp/899)*100)+'%';
 
 let svg = '';
 if(xp<100){ // CACHORRO
   svg = `<svg viewBox="0 0 200 280" width="100%" height="100%"><g><ellipse cx="100" cy="250" rx="70" ry="15" fill="#111"/><path d="M60 200 Q100 120 140 200" fill="#1a1a1a"/><circle cx="75" cy="90" r="18" fill="#1a1a1a" class="eye"/><circle cx="125" cy="90" r="18" fill="#1a1a1a" class="eye"/><circle cx="75" cy="92" r="6" fill="#ffb86c"/><circle cx="125" cy="92" r="6" fill="#ffb86c"/><path d="M40 70 L30 30 L65 55" fill="#1a1a1a"/><path d="M160 70 L170 30 L135 55" fill="#1a1a1a"/><path d="M85 110 Q100 125 115 110" stroke="#333" fill="none" stroke-width="3"/><g class="tail"><path d="M100 180 Q110 210 100 240" stroke="#1a1a1a" stroke-width="12" fill="none" stroke-linecap="round"/></g></g></svg>`;
 } else if(xp<300){ // JOVEN
   svg = `<svg viewBox="0 0 200 300" width="100%" height="100%"><g><ellipse cx="100" cy="270" rx="75" ry="15" fill="#111"/><path d="M55 220 Q100 90 145 220" fill="#151515"/><circle cx="72" cy="85" r="20" fill="#151515" class="eye"/><circle cx="128" cy="85" r="20" fill="#151515" class="eye"/><circle cx="72" cy="88" r="7" fill="#ffcc66"/><circle cx="128" cy="88" r="7" fill="#ffcc66"/><path d="M35 65 L25 15 L65 50" fill="#151515"/><path d="M165 65 L175 15 L135 50" fill="#151515"/><g class="tail"><path d="M100 190 Q125 220 110 260" stroke="#151515" stroke-width="14" fill="none"/></g></g></svg>`;
 } else if(xp<600){ // ADULTO
   svg = `<svg viewBox="0 0 200 320" width="100%" height="100%"><g><ellipse cx="100" cy="290" rx="80" ry="18" fill="#111"/><path d="M50 230 Q100 70 150 230" fill="#111"/><path d="M60 160 Q100 140 140 160" stroke="#222" stroke-width="2" fill="none"/><circle cx="70" cy="80" r="22" fill="#111" class="eye"/><circle cx="130" cy="80" r="22" fill="#111" class="eye"/><circle cx="70" cy="84" r="8" fill="#FFD700"/><circle cx="130" cy="84" r="8" fill="#FFD700"/><path d="M30 60 L18 5 L62 45" fill="#111"/><path d="M170 60 L182 5 L138 45" fill="#111"/><g class="tail"><path d="M100 200 Q135 230 120 280" stroke="#111" stroke-width="16" fill="none"/></g></g></svg>`;
 } else { // DIOS XOLOTL
   svg = `<svg viewBox="0 0 200 340" width="100%" height="100%"><g class="aura"><circle cx="100" cy="160" r="110" fill="none" stroke="#FFD700" stroke-width="2" opacity="0.4"/><circle cx="100" cy="160" r="90" fill="none" stroke="#FFD700" stroke-width="1" opacity="0.3"/></g><ellipse cx="100" cy="310" rx="85" ry="20" fill="#221a00"/><g><path d="M45 250 Q100 50 155 250" fill="#0d0d0d" stroke="#FFD700" stroke-width="2"/><path d="M60 160 Q100 140 140 160" stroke="#333" stroke-width="2" fill="none"/><circle cx="68" cy="75" r="24" fill="#0d0d0d" class="eye" stroke="#FFD700" stroke-width="1"/><circle cx="132" cy="75" r="24" fill="#0d0d0d" class="eye" stroke="#FFD700" stroke-width="1"/><circle cx="68" cy="80" r="10" fill="#FFD700"/><circle cx="132" cy="80" r="10" fill="#FFD700"/><path d="M25 55 L12 0 L60 40" fill="#0d0d0d" stroke="#FFD700" stroke-width="1.5"/><path d="M175 55 L188 0 L140 40" fill="#0d0d0d" stroke="#FFD700" stroke-width="1.5"/><path d="M60 30 L100 5 L140 30 L100 15 Z" fill="#FFD700"/><circle cx="100" cy="180" r="18" fill="#111" stroke="#FFD700" stroke-width="2"/><circle cx="100" cy="180" r="6" fill="#FFD700"/><g class="tail"><path d="M100 210 Q145 240 125 300" stroke="#0d0d0d" stroke-width="18" fill="none" stroke-linecap="round"/><circle cx="125" cy="300" r="8" fill="#FFD700"/></g></g></svg>`;
 }
 document.getElementById('xolo').innerHTML = svg;
 playSound(st.name);
}
function playSound(level){
 try{
  const ctx = new (window.AudioContext||window.webkitAudioContext)();
  const osc = ctx.createOscillator(); const gain = ctx.createGain();
  osc.connect(gain); gain.connect(ctx.destination);
  if(level==='CACHORRO'){osc.frequency.value=500;gain.gain.value=0.2;osc.start();osc.stop(ctx.currentTime+0.15)}
  else if(level==='JOVEN'){osc.frequency.value=350;gain.gain.value=0.25;osc.start();osc.stop(ctx.currentTime+0.3)}
  else if(level==='ADULTO'){osc.frequency.value=220;gain.gain.value=0.3;osc.start();osc.stop(ctx.currentTime+0.4)}
  else{osc.frequency.value=110;gain.gain.value=0.4; osc.type='sawtooth'; osc.start(); let o2=ctx.createOscillator(); o2.frequency.value=440; o2.connect(gain); o2.start(); o2.stop(ctx.currentTime+0.8); osc.stop(ctx.currentTime+0.8); if(navigator.vibrate)navigator.vibrate([100,50,100])}
 }catch(e){}
}
function analizar(){
 const val = document.getElementById('inputFraude').value.trim();
 if(!val){alert('¡Pega un mensaje sospechoso, Xolo lo olfateará!');return}
 const result = document.getElementById('result');
 result.style.display='block';
 const sospechoso = ['ganaste','premio','urgente','bitcoin','inversion','transferencia','banco','verifica','http://','.xyz','oferta'];
 let score = sospechoso.filter(w=>val.toLowerCase().includes(w)).length;
 if(score>=2 || val.includes('http://')){
   result.className='result danger'; result.innerText='🚨 ¡ALERTA! XOLO DETECTA POSIBLE FRAUDE. No compartas datos.';
   playSound('ADULTO'); if(navigator.vibrate)navigator.vibrate([200,100,200]);
   xp+=10;
 } else {
   result.className='result safe'; result.innerText='✅ Parece seguro, pero Xolo sigue vigilando.';
   xp+=25;
 }
 let oldStage = getStage(xp-25).name; let newStage = getStage(xp).name;
 if(oldStage!==newStage){document.getElementById('evolving').style.display='flex'; setTimeout(()=>{document.getElementById('evolving').style.display='none'},2000)}
 localStorage.setItem('xolo_xp',xp); renderXolo();
}
renderXolo();
</script>
</body>
</html>
"""

@app.get("/", response_class=HTMLResponse)
def home():
    return HTML_PAGE

@app.get("/health")
def health():
    return {"status":"XOLO VIVO", "xp_system":"activo"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
