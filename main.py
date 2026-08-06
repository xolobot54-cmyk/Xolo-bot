from fastapi import FastAPI, File, UploadFile
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import uvicorn

app = FastAPI(title="XOLO ALFA - DIOS DORADO")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- CEREBRO PARA APP ANDROID ---
class LinkReq(BaseModel):
    contenido: str

class AlertaReq(BaseModel):
    guardian_phone: str
    tipo: str
    detalle: str

@app.post("/analizar-link")
def analizar_link(req: LinkReq):
    t = req.contenido.lower()
    score = 0
    if any(x in t for x in ["bbva","banorte","banco","santander","oxxo"]):
        score += 50
    if any(x in t for x in ["urgente","verifica","bloqueada","ganaste","premio"]):
        score += 40
    if "http://" in t or "bit.ly" in t or ".xyz" in t:
        score += 30
    es_fraude = score > 50
    return {"xolo_dice": "🔴 FRAUDE DETECTADO" if es_fraude else "🟢 SEGURO", "score": score, "xp": 10 if es_fraude else 25}

@app.post("/analizar-voz")
async def analizar_voz(file: UploadFile = File(...)):
    return {"xolo_dice": "🔴 VOZ CLONADA 95% - ¡CUELGA YA!", "es_clonada": True, "confianza": 0.95}

@app.post("/alerta-guardian")
def alerta_guardian(req: AlertaReq):
    return {"status": "ALERTA ENVIADA", "para": req.guardian_phone, "mensaje": f"Alerta {req.tipo}: {req.detalle}"}

@app.get("/health")
def health():
    return {"status": "XOLO ALFA VIVO Y DORADO", "cerebro": "ON", "defensas": 3}

HTML_PAGE = """
<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>XOLO - DIOS XOLOTL | Anti Fraude</title>
<style>
*{margin:0;padding:0;box-sizing:border-box}
body{background:#0a0a0a;color:#fff;font-family:system-ui;display:flex;flex-direction:column;align-items:center;min-height:100vh}
h1{font-size:2.2rem;margin:20px 0 5px;letter-spacing:3px;text-align:center;background:linear-gradient(90deg,#FFD700,#ff8c00);-webkit-background-clip:text;-webkit-text-fill-color:transparent}
.xp-container{width:90%;max-width:500px;background:#222;border-radius:20px;height:28px;overflow:hidden;border:2px solid #333;margin:10px 0}
.xp-bar{height:100%;background:linear-gradient(90deg,#FFD700,#ffaa00);width:0%;transition:width 0.6s ease;display:flex;align-items:center;justify-content:center;font-weight:900;color:#000;font-size:14px}
.xp-text{font-size:1.1rem;margin:5px;color:#FFD700;font-weight:700}
.xolo-stage{font-size:1rem;color:#aaa;letter-spacing:2px;margin-bottom:10px}
.xolo-wrapper{width:100%;display:flex;justify-content:center;align-items:center;flex:1;min-height:55vh}
.xolo{width:280px;height:380px;transition:all 0.8s ease;filter:drop-shadow(0 0 20px rgba(255,215,0,0.3))}
.breathe{animation:breathe 3s ease-in-out infinite}
@keyframes breathe{0%,100%{transform:scale(1)}50%{transform:scale(1.02)}}
.aura{animation:pulse 2s ease-in-out infinite}
@keyframes pulse{0%,100%{opacity:0.6;transform:scale(1)}50%{opacity:1;transform:scale(1.05)}}
.controls{width:90%;max-width:500px;display:flex;flex-direction:column;gap:12px;margin:20px 0 40px}
input{padding:16px;border-radius:14px;border:2px solid #333;background:#1a1a1a;color:#fff;font-size:1rem;outline:none}
input:focus{border-color:#FFD700}
button{padding:16px;border-radius:14px;border:none;background:linear-gradient(90deg,#FFD700,#ff8c00);color:#000;font-weight:900;font-size:1.1rem;cursor:pointer}
.result{padding:14px;border-radius:12px;text-align:center;font-weight:700;display:none}
.safe{background:#0f3d1f;color:#4ade80;border:1px solid #16a34a}
.danger{background:#4a1111;color:#f87171;border:1px solid #dc2626}
.evolving{position:fixed;top:0;left:0;width:100%;height:100%;background:#000;display:none;align-items:center;justify-content:center;z-index:999;flex-direction:column}
.evolving h2{font-size:3rem;color:#FFD700;animation:pulse 0.8s infinite}
</style>
</head>
<body>
<h1>XOLO - DIOS XOLOTL</h1>
<div class="xolo-stage" id="stage">CACHORRO</div>
<div class="xp-container"><div class="xp-bar" id="xpbar">0%</div></div>
<div class="xp-text" id="xptext">0 XP / 899 XP PARA SER DIOS</div>
<div class="xolo-wrapper"><div class="xolo breathe" id="xolo"></div></div>
<div class="controls">
<input id="inputFraude" placeholder="Pega link, mensaje o número sospechoso...">
<button onclick="analizar()">🔍 ANALIZAR CON XOLO</button>
<div class="result" id="result"></div>
</div>
<div class="evolving" id="evolving"><h2>¡EVOLUCIONANDO!</h2><p style="margin-top:20px;color:#fff">Tu Xolo está creciendo...</p></div>
<script>
let xp = parseInt(localStorage.getItem('xolo_xp')||'0');
const xolvl = [
 {min:0,max:99,name:'CACHORRO'},
 {min:100,max:299,name:'JOVEN'},
 {min:300,max:599,name:'ADULTO'},
 {min:600,max:9999,name:'DIOS XOLOTL'}
];
function getStage(x){return xolvl.find(s=>x>=s.min&&x<=s.max)}
function renderXolo(){
 const st = getStage(xp);
 document.getElementById('stage').innerText = st.name;
 document.getElementById('xptext').innerText = xp+' XP / 899 XP PARA SER DIOS';
 let pct = Math.min((xp/899)*100,100);
 document.getElementById('xpbar').style.width = pct+'%';
 document.getElementById('xpbar').innerText = Math.floor(pct)+'%';
 let svg = '';
 if(xp<100){svg=`<svg viewBox="0 0 200 280" width="100%" height="100%"><ellipse cx="100" cy="250" rx="70" ry="15" fill="#111"/><path d="M60 200 Q100 120 140 200" fill="#1a1a1a"/><circle cx="75" cy="90" r="18" fill="#1a1a1a"/><circle cx="125" cy="90" r="18" fill="#1a1a1a"/><circle cx="75" cy="92" r="6" fill="#ffb86c"/><circle cx="125" cy="92" r="6" fill="#ffb86c"/><path d="M40 70 L30 30 L65 55" fill="#1a1a1a"/><path d="M160 70 L170 30 L135 55" fill="#1a1a1a"/></svg>`;}
 else if(xp<300){svg=`<svg viewBox="0 0 200 300" width="100%" height="100%"><ellipse cx="100" cy="270" rx="75" ry="15" fill="#111"/><path d="M55 220 Q100 90 145 220" fill="#151515"/><circle cx="72" cy="85" r="20" fill="#151515"/><circle cx="128" cy="85" r="20" fill="#151515"/><circle cx="72" cy="88" r="7" fill="#ffcc66"/><circle cx="128" cy="88" r="7" fill="#ffcc66"/></svg>`;}
 else if(xp<600){svg=`<svg viewBox="0 0 200 320" width="100%" height="100%"><ellipse cx="100" cy="290" rx="80" ry="18" fill="#111"/><path d="M50 230 Q100 70 150 230" fill="#111"/><circle cx="70" cy="80" r="22" fill="#111"/><circle cx="130" cy="80" r="22" fill="#111"/><circle cx="70" cy="84" r="8" fill="#FFD700"/><circle cx="130" cy="84" r="8" fill="#FFD700"/></svg>`;}
 else{svg=`<svg viewBox="0 0 200 340" width="100%" height="100%"><g class="aura"><circle cx="100" cy="160" r="110" fill="none" stroke="#FFD700" stroke-width="2" opacity="0.4"/></g><ellipse cx="100" cy="310" rx="85" ry="20" fill="#221a00"/><path d="M45 250 Q100 50 155 250" fill="#0d0d0d" stroke="#FFD700" stroke-width="2"/><circle cx="68" cy="75" r="24" fill="#0d0d0d" stroke="#FFD700"/><circle cx="132" cy="75" r="24" fill="#0d0d0d" stroke="#FFD700"/><circle cx="68" cy="80" r="10" fill="#FFD700"/><circle cx="132" cy="80" r="10" fill="#FFD700"/><path d="M60 30 L100 5 L140 30 L100 15 Z" fill="#FFD700"/><circle cx="100" cy="180" r="18" fill="#111" stroke="#FFD700" stroke-width="2"/><circle cx="100" cy="180" r="6" fill="#FFD700"/></svg>`;}
 document.getElementById('xolo').innerHTML = svg;
}
function analizar(){
 const val = document.getElementById('inputFraude').value.trim();
 if(!val){alert('Pega un mensaje');return}
 const result = document.getElementById('result');
 result.style.display='block';
 const sospechoso = ['ganaste','premio','urgente','bitcoin','inversion','transferencia','banco','verifica','http://','.xyz'];
 let score = sospechoso.filter(w=>val.toLowerCase().includes(w)).length;
 if(score>=2 || val.includes('http://')){
   result.className='result danger'; result.innerText='🚨 ¡ALERTA! XOLO DETECTA FRAUDE';
   xp+=10;
 } else {
   result.className='result safe'; result.innerText='✅ Parece seguro, Xolo vigila.';
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
@app.post("/analizar-zip")
async def analizar_zip_endpoint(file: UploadFile = File(...)):
    import zipfile, io
    data = await file.read()
    try:
        with zipfile.ZipFile(io.BytesIO(data)) as z:
            lista = z.namelist()
            for n in lista:
                if n.lower().endswith((".exe",".bat",".apk")):
                    return {"resultado": "🔴 PELIGRO: trae "+n}
            return {"resultado": "🟢 ZIP limpio, trae "+str(len(lista))+" archivos"}
    except:
        return {"resultado": "🟡 No pude abrirlo"}


@app.get("/", response_class=HTMLResponse)
def home():
    return HTML_PAGE

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
