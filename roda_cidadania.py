# -*- coding: utf-8 -*-
import streamlit as st
import hashlib
import json
import base64
from io import BytesIO
from datetime import datetime
import qrcode

st.set_page_config(page_title="Roda da Cidadania", page_icon="🌐", layout="wide")
URL_BASE = "https://pbl-cidadania-digital-n9rhi8k2wbozexmztzfdmu.streamlit.app"
SEGREDO = "cidadania-digital-odete-mendes-2026"

st.markdown("""
<style>
    .stApp { background: linear-gradient(135deg,#0a1929,#1a3a5c,#2d5f8a); }
    h1, h2, h3, p, label, div { color: white; }
    .menu-titulo { text-align:center; color:#ffd700; font-size:2.5rem; font-weight:900; text-shadow:0 0 30px rgba(255,215,0,.8); margin-bottom:10px; }
    .menu-sub { text-align:center; color:rgba(255,255,255,.8); margin-bottom:30px; }
    .stButton>button { background:linear-gradient(135deg,#ffd700,#ffed4a); color:#0a1929; border:none; border-radius:50px; padding:20px 30px; font-size:1.3rem; font-weight:900; box-shadow:0 0 30px rgba(255,215,0,.6); width:100%; text-transform:uppercase; }
    .stButton>button:hover { transform:scale(1.03); box-shadow:0 0 50px rgba(255,215,0,1); }
</style>
""", unsafe_allow_html=True)

if "tela" not in st.session_state: st.session_state.tela = "menu"
if "quiz_idx" not in st.session_state: st.session_state.quiz_idx = 0
if "quiz_respondido" not in st.session_state: st.session_state.quiz_respondido = False
if "quiz_acertos" not in st.session_state: st.session_state.quiz_acertos = 0
if "quiz_escolha" not in st.session_state: st.session_state.quiz_escolha = None
if "cert_nome" not in st.session_state: st.session_state.cert_nome = ""

DICAS = [
    {"emoji": "📰", "texto": "VERIFIQUE A FONTE antes de compartilhar!"},
    {"emoji": "🛡️", "texto": "NÃO PRATIQUE CYBERBULLYING!"},
    {"emoji": "⚖️", "texto": "PENSE ANTES DE POSTAR!"},
    {"emoji": "🔒", "texto": "PROTEJA SEUS DADOS!"},
    {"emoji": "🚫", "texto": "DENUNCIE CONTEÚDO OFENSIVO!"},
    {"emoji": "🔍", "texto": "PESQUISE ANTES DE COMPARTILHAR!"},
    {"emoji": "💙", "texto": "SEJA GENTIL ONLINE!"},
    {"emoji": "🌐", "texto": "NA DÚVIDA, NÃO COMPARTILHE!"},
    {"emoji": "🔑", "texto": "USE SENHAS FORTES E DIFERENTES!"},
    {"emoji": "👤", "texto": "NÃO COMPARTILHE DADOS PESSOAIS!"},
    {"emoji": "📸", "texto": "CUIDADO COM O QUE POSTA NAS REDES!"},
    {"emoji": "🤝", "texto": "RESPEITE A OPINIÃO DOS OUTROS!"},
    {"emoji": "🧠", "texto": "NÃO ACREDITE EM TUDO QUE VÊ NA INTERNET!"},
    {"emoji": "📵", "texto": "NÃO USE O CELULAR PARA PREJUDICAR NINGUÉM!"},
    {"emoji": "🎭", "texto": "PERFIS FALSOS EXISTEM - DESCONFIE!"},
    {"emoji": "💬", "texto": "PENSE ANTES DE COMENTAR!"},
    {"emoji": "🔗", "texto": "NÃO CLIQUE EM LINKS SUSPEITOS!"},
    {"emoji": "🎁", "texto": "PROMOÇÕES BOAS DEMAIS PODEM SER GOLPE!"},
    {"emoji": "🕵️", "texto": "PROTEJA SUA PRIVACIDADE ONLINE!"},
    {"emoji": "📚", "texto": "ESTUDE AS NOTÍCIAS ANTES DE REPASSAR!"},
    {"emoji": "❤️", "texto": "ESPALHE O BEM, NÃO O ÓDIO!"},
    {"emoji": "🤐", "texto": "O QUE VOCÊ POSTA PODE FICAR PARA SEMPRE!"},
    {"emoji": "🌍", "texto": "A INTERNET É DE TODOS - RESPEITE!"},
    {"emoji": "⭐", "texto": "SEJA UM EXEMPLO DE CIDADÃO DIGITAL!"},
    {"emoji": "🧒", "texto": "NÃO CONVERSE COM ESTRANHOS ONLINE!"},
    {"emoji": "🎮", "texto": "RESPEITE OS OUTROS JOGADORES NOS JOGOS!"},
    {"emoji": "📱", "texto": "NÃO RESPONDA A MENSAGENS AGRESSIVAS!"},
    {"emoji": "🔔", "texto": "BLOQUEIE QUEM TE FAZ MAL!"},
    {"emoji": "📧", "texto": "DESCONFIE DE E-MAILS ESTRANHOS!"},
    {"emoji": "🏦", "texto": "NUNCA COMPARTILHE SENHAS BANCÁRIAS!"},
    {"emoji": "📷", "texto": "NÃO ENVIE FOTOS ÍNTIMAS PARA NINGUÉM!"},
    {"emoji": "👨‍👩‍👧", "texto": "CONTE AOS PAIS SE ALGO DER ERRADO!"},
    {"emoji": "🚨", "texto": "PEÇA AJUDA SE SOFRER AMEAÇAS!"},
    {"emoji": "🕒", "texto": "CONTROLE O TEMPO DE TELA!"},
    {"emoji": "🎯", "texto": "NÃO ESPALHE FAKE NEWS!"},
    {"emoji": "🤳", "texto": "CUIDADO COM O QUE MOSTRA NAS FOTOS!"},
    {"emoji": "🎓", "texto": "USE A INTERNET PARA APRENDER MAIS!"},
    {"emoji": "🌱", "texto": "PLANTE O BEM NO AMBIENTE DIGITAL!"},
    {"emoji": "🧩", "texto": "PENSE CRÍTICO COM O QUE VÊ ONLINE!"},
    {"emoji": "🏆", "texto": "SEJA UM CIDADÃO DIGITAL DE VERDADE!"}
]

QUIZ = [
    {"pergunta": "Você recebeu uma notícia bombástica no WhatsApp. O que faz?", "opcoes": ["Compartilho com todos, é urgente!", "Verifico a fonte antes de compartilhar.", "Acredito, se está na internet é verdade.", "Repasso só para os amigos próximos."], "correta": 1, "explicacao": "Sempre verifique a fonte antes de compartilhar. Fake news se espalham rápido!"},
    {"pergunta": "O que é cyberbullying?", "opcoes": ["Uma brincadeira normal na internet.", "Agressão, humilhação ou perseguição feita online.", "Um jogo virtual.", "Um tipo de vírus de computador."], "correta": 1, "explicacao": "Cyberbullying é violência online. Não pratique e denuncie!"},
    {"pergunta": "Um desconhecido pede seus dados pessoais online. O que faz?", "opcoes": ["Envio, pode ser importante.", "Envio só o nome e idade.", "Não envio nada e conto a um adulto.", "Envio se ele parecer legal."], "correta": 2, "explicacao": "Nunca compartilhe dados pessoais com estranhos. Conte a um adulto de confiança!"},
    {"pergunta": "Qual senha é mais segura?", "opcoes": ["123456", "minhasenha", "MeuNome2010", "X7#kL9$mP2!q"], "correta": 3, "explicacao": "Senhas fortes misturam letras maiúsculas, minúsculas, números e símbolos!"},
    {"pergunta": "Um amigo está sofrendo bullying online. O que faz?", "opcoes": ["Rio junto para não ser a próxima vítima.", "Fico quieto, não é meu problema.", "Apoio ele e denuncio o agressor.", "Compartilho para os outros verem."], "correta": 2, "explicacao": "Apoie a vítima e denuncie. Ser um cidadão digital é defender quem precisa!"}
]

def gerar_codigo_certificado(nome: str, data: str) -> dict:
    base = f"{nome.strip().lower()}|{data}"
    assinatura = hashlib.sha256((base + SEGREDO).encode()).hexdigest()[:10].upper()
    codigo = f"CD-{data.replace('-','')}-{assinatura}"
    return {"nome": nome.strip(), "data": data, "codigo": codigo}

def gerar_qr_base64(url: str) -> str:
    qr = qrcode.QRCode(version=1, box_size=10, border=2)
    qr.add_data(url)
    qr.make(fit=True)
    img = qr.make_image(fill_color="#0a1929", back_color="white")
    buf = BytesIO()
    img.save(buf, format="PNG")
    return base64.b64encode(buf.getvalue()).decode()

def tela_menu():
    st.markdown('<div class="menu-titulo">🌐 CIDADANIA DIGITAL</div>', unsafe_allow_html=True)
    st.markdown('<div class="menu-sub">Escolha uma atividade!</div>', unsafe_allow_html=True)
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("🎡\n\nRODA DA CIDADANIA\n\nGire e descubra uma dica"):
            st.session_state.tela = "roda"
            st.rerun()
    with col2:
        if st.button("🧠\n\nQUIZ RÁPIDO\n\nTeste seu conhecimento"):
            st.session_state.tela = "quiz"
            st.session_state.quiz_idx = 0
            st.session_state.quiz_acertos = 0
            st.session_state.quiz_respondido = False
            st.session_state.quiz_escolha = None
            st.rerun()
    with col3:
        if st.button("🏆\n\nCERTIFICADO\n\nGanhe seu diploma"):
            st.session_state.tela = "certificado"
            st.rerun()
    st.markdown("---")
    st.markdown('<div style="text-align:center; color:rgba(255,255,255,.5); font-size:.9rem;">EEEF Profª Odete Mendes N Oliveira - Prof. Irving V. Santos / Luiz Veloso</div>', unsafe_allow_html=True)

def tela_roda():
    col1, col2 = st.columns([1, 6])
    with col1:
        if st.button("⬅️ Voltar"):
            st.session_state.tela = "menu"
            st.rerun()
    dicas_js = json.dumps(DICAS, ensure_ascii=False)
    COMPONENTE_RODA = """
<!DOCTYPE html>
<html>
<head>
<style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;700;900&display=swap');
    * { margin:0; padding:0; box-sizing:border-box; font-family:'Poppins',sans-serif; }
    body { background: linear-gradient(135deg,#0a1929,#1a3a5c,#2d5f8a); min-height:100vh; display:flex; flex-direction:column; align-items:center; justify-content:flex-start; padding:15px; overflow:hidden; }
    .titulo { font-size:2.2rem; font-weight:900; color:#ffd700; text-shadow:0 0 30px rgba(255,215,0,.8); margin-bottom:5px; text-align:center; animation:brilho 2s ease-in-out infinite alternate; }
    @keyframes brilho { from { text-shadow:0 0 20px rgba(255,215,0,.6); } to { text-shadow:0 0 50px rgba(255,215,0,1); } }
    .subtitulo { font-size:.9rem; color:rgba(255,255,255,.7); margin-bottom:10px; text-align:center; }
    .roda-wrapper { position:relative; width:300px; height:300px; margin:5px auto; }
    .ponteiro { position:absolute; top:-15px; left:50%; transform:translateX(-50%); width:0; height:0; border-left:18px solid transparent; border-right:18px solid transparent; border-top:35px solid #ffd700; filter:drop-shadow(0 0 15px rgba(255,215,0,1)); z-index:10; }
    .roda { width:100%; height:100%; border-radius:50%; position:relative; overflow:hidden; box-shadow:0 0 60px rgba(255,215,0,.6), inset 0 0 60px rgba(0,0,0,.3); border:5px solid #ffd700; transition:none; }
    .roda svg { width:100%; height:100%; }
    .centro { position:absolute; top:50%; left:50%; transform:translate(-50%,-50%); width:65px; height:65px; background:radial-gradient(circle,#ffd700,#ffed4a); border-radius:50%; display:flex; align-items:center; justify-content:center; font-size:1.8rem; box-shadow:0 0 40px rgba(255,215,0,1); z-index:5; border:4px solid #0a1929; }
    .dica-resultado { background:white; padding:15px 25px; border-radius:15px; margin-top:10px; text-align:center; box-shadow:0 0 60px rgba(255,215,0,.8); border:4px solid #ffd700; max-width:500px; opacity:0; transform:scale(.5); transition:all .5s; }
    .dica-resultado.mostrar { opacity:1; transform:scale(1); }
    .dica-emoji { font-size:2.5rem; margin-bottom:5px; }
    .dica-texto { font-size:1.1rem; color:#1a3a5c; font-weight:700; }
    .botao { background:linear-gradient(135deg,#ffd700,#ffed4a); color:#0a1929; border:none; border-radius:50px; padding:15px 50px; font-size:1.2rem; font-weight:900; cursor:pointer; box-shadow:0 0 30px rgba(255,215,0,.8); transition:all .3s; margin-top:10px; text-transform:uppercase; letter-spacing:1px; }
    .botao:hover { transform:scale(1.05); box-shadow:0 0 50px rgba(255,215,0,1); }
    .botao:disabled { opacity:.5; cursor:not-allowed; }
    .instrucao { color:rgba(255,255,255,.5); font-size:.8rem; margin-top:10px; text-align:center; }
</style>
</head>
<body>
<h1 class="titulo">🌐 RODA DA CIDADANIA</h1>
<p class="subtitulo">Gire e descubra uma dica!</p>
<div class="roda-wrapper">
    <div class="ponteiro"></div>
    <div class="roda" id="roda">
        <svg viewBox="0 0 200 200">
            <path d="M100,100 L100,0 A100,100 0 0,1 170.7,29.3 Z" fill="#ff6b6b"/>
            <path d="M100,100 L170.7,29.3 A100,100 0 0,1 200,100 Z" fill="#4ecdc4"/>
            <path d="M100,100 L200,100 A100,100 0 0,1 170.7,170.7 Z" fill="#45b7d1"/>
            <path d="M100,100 L170.7,170.7 A100,100 0 0,1 100,200 Z" fill="#f9ca24"/>
            <path d="M100,100 L100,200 A100,100 0 0,1 29.3,170.7 Z" fill="#6c5ce7"/>
            <path d="M100,100 L29.3,170.7 A100,100 0 0,1 0,100 Z" fill="#fd79a8"/>
            <path d="M100,100 L0,100 A100,100 0 0,1 29.3,29.3 Z" fill="#00b894"/>
            <path d="M100,100 L29.3,29.3 A100,100 0 0,1 100,0 Z" fill="#e17055"/>
        </svg>
    </div>
    <div class="centro">🎡</div>
</div>
<button class="botao" id="botao" onclick="girar()">🎡 GIRAR A RODA</button>
<div class="dica-resultado" id="resultado">
    <div class="dica-emoji" id="emoji"></div>
    <div class="dica-texto" id="texto"></div>
</div>
<p class="instrucao">Clique no botão e aguarde o resultado!</p>
<script src="https://cdn.jsdelivr.net/npm/canvas-confetti@1.6.0/dist/confetti.browser.min.js"></script>
<script>
    const dicas = __DICAS__;
    let girando = false; let rotacaoAcumulada = 0; let audioCtx = null; let tickTimer = null;
    function garantirAudio() { try { if (!audioCtx) audioCtx = new (window.AudioContext || window.webkitAudioContext)(); if (audioCtx.state === 'suspended') audioCtx.resume(); return audioCtx; } catch (e) { return null; } }
    function tocarNota(freq, delay, dur, vol) { const ctx = audioCtx; if (!ctx) return; try { const t = ctx.currentTime + delay; const osc = ctx.createOscillator(); const gain = ctx.createGain(); osc.type = 'sine'; osc.frequency.setValueAtTime(freq, t); gain.gain.setValueAtTime(0.0001, t); gain.gain.exponentialRampToValueAtTime(vol, t + 0.02); gain.gain.exponentialRampToValueAtTime(0.0001, t + dur); osc.connect(gain); gain.connect(ctx.destination); osc.start(t); osc.stop(t + dur + 0.05); } catch (e) {} }
    function tocarTick() { const ctx = audioCtx; if (!ctx) return; try { const t = ctx.currentTime; const osc = ctx.createOscillator(); const gain = ctx.createGain(); osc.type = 'square'; osc.frequency.setValueAtTime(1400, t); gain.gain.setValueAtTime(0.05, t); gain.gain.exponentialRampToValueAtTime(0.0001, t + 0.04); osc.connect(gain); gain.connect(ctx.destination); osc.start(t); osc.stop(t + 0.05); } catch (e) {} }
    function tocarFanfarra() { tocarNota(523.25, 0.00, 0.35, 0.30); tocarNota(659.25, 0.15, 0.35, 0.30); tocarNota(783.99, 0.30, 0.35, 0.30); tocarNota(1046.50, 0.45, 0.55, 0.35); }
    function girar() {
        if (girando) return; girando = true; garantirAudio();
        const botao = document.getElementById('botao'); const roda = document.getElementById('roda'); const resultado = document.getElementById('resultado');
        botao.disabled = true; botao.textContent = '🎡 GIRANDO...'; resultado.classList.remove('mostrar');
        const indice = Math.floor(Math.random() * dicas.length); const dica = dicas[indice];
        const TOTAL_FATIAS = 8; const anguloFatia = 360 / TOTAL_FATIAS; const posicaoVisual = indice % TOTAL_FATIAS;
        const rotacaoAlvo = (posicaoVisual * anguloFatia) + (anguloFatia / 2); rotacaoAcumulada += 360 * 3 + rotacaoAlvo;
        roda.style.transition = 'none'; void roda.offsetWidth; roda.style.transition = 'transform 3s cubic-bezier(0.2, 0.8, 0.2, 1)'; roda.style.transform = 'rotate(' + rotacaoAcumulada + 'deg)';
        let tickCount = 0; if (tickTimer) clearInterval(tickTimer);
        tickTimer = setInterval(function() { tickCount++; if (tickCount > 25) { clearInterval(tickTimer); tickTimer = null; return; } tocarTick(); }, 110);
        setTimeout(function() {
            if (tickTimer) { clearInterval(tickTimer); tickTimer = null; }
            document.getElementById('emoji').textContent = dica.emoji; document.getElementById('texto').textContent = dica.texto; resultado.classList.add('mostrar');
            try { if (typeof confetti === 'function') { confetti({ particleCount:200, spread:90, origin:{y:0.6}, colors:['#ffd700','#ff6b6b','#4ecdc4','#6c5ce7'] }); } } catch (e) {}
            tocarFanfarra(); botao.disabled = false; botao.textContent = '🔄 GIRAR NOVAMENTE'; girando = false;
        }, 3000);
    }
</script>
</body>
</html>
""".replace("__DICAS__", dicas_js)
    st.iframe(COMPONENTE_RODA, height=700)

def tela_quiz():
    col1, col2 = st.columns([1, 6])
    with col1:
        if st.button("⬅️ Voltar"): st.session_state.tela = "menu"; st.rerun()
    idx = st.session_state.quiz_idx
    if idx >= len(QUIZ):
        acertos = st.session_state.quiz_acertos; total = len(QUIZ)
        st.markdown('<div class="menu-titulo">🎉 Quiz concluído!</div>', unsafe_allow_html=True)
        st.markdown(f'<div style="text-align:center; font-size:2rem; color:#ffd700; font-weight:900;">Você acertou {acertos} de {total}!</div>', unsafe_allow_html=True)
        if acertos == total: st.markdown('<div style="text-align:center; font-size:1.3rem;">🏆 Perfeito! Você é um Cidadão Digital de verdade!</div>', unsafe_allow_html=True)
        elif acertos >= total // 2: st.markdown('<div style="text-align:center; font-size:1.3rem;">👏 Muito bem! Continue aprendendo!</div>', unsafe_allow_html=True)
        else: st.markdown('<div style="text-align:center; font-size:1.3rem;">💪 Continue praticando cidadania digital!</div>', unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)
        colA, colB = st.columns(2)
        with colA:
            if st.button("🔄 Jogar novamente"): st.session_state.quiz_idx = 0; st.session_state.quiz_acertos = 0; st.session_state.quiz_respondido = False; st.session_state.quiz_escolha = None; st.rerun()
        with colB:
            if st.button("🏆 Pegar meu certificado"): st.session_state.tela = "certificado"; st.rerun()
        return
    q = QUIZ[idx]
    st.markdown(f'<div class="menu-titulo">🧠 Pergunta {idx+1} de {len(QUIZ)}</div>', unsafe_allow_html=True)
    st.markdown(f'<div style="text-align:center; font-size:1.4rem; margin:20px 0;">{q["pergunta"]}</div>', unsafe_allow_html=True)
    if not st.session_state.quiz_respondido:
        for i, opcao in enumerate(q["opcoes"]):
            if st.button(f"{chr(65+i)}) {opcao}", key=f"opt_{idx}_{i}"):
                st.session_state.quiz_escolha = i; st.session_state.quiz_respondido = True
                if i == q["correta"]: st.session_state.quiz_acertos += 1
                st.rerun()
    else:
        escolha = st.session_state.quiz_escolha; correta = q["correta"]
        for i, opcao in enumerate(q["opcoes"]):
            if i == correta: st.markdown(f'<div style="background:#00b894; color:white; padding:12px 20px; border-radius:10px; margin:5px 0; font-weight:700;">✅ {chr(65+i)}) {opcao}</div>', unsafe_allow_html=True)
            elif i == escolha: st.markdown(f'<div style="background:#e17055; color:white; padding:12px 20px; border-radius:10px; margin:5px 0; font-weight:700;">❌ {chr(65+i)}) {opcao}</div>', unsafe_allow_html=True)
            else: st.markdown(f'<div style="background:rgba(255,255,255,.1); color:white; padding:12px 20px; border-radius:10px; margin:5px 0;">{chr(65+i)}) {opcao}</div>', unsafe_allow_html=True)
        st.markdown(f'<div style="background:rgba(255,215,0,.15); border-left:5px solid #ffd700; padding:15px; margin:20px 0; color:white; border-radius:8px;"><b>💡 Explicação:</b> {q["explicacao"]}</div>', unsafe_allow_html=True)
        if st.button("➡️ Próxima pergunta"): st.session_state.quiz_idx += 1; st.session_state.quiz_respondido = False; st.session_state.quiz_escolha = None; st.rerun()

def tela_certificado():
    col1, col2 = st.columns([1, 6])
    with col1:
        if st.button("⬅️ Voltar"): st.session_state.tela = "menu"; st.rerun()
    st.markdown('<div class="menu-titulo">🏆 Certificado de Cidadão Digital</div>', unsafe_allow_html=True)
    st.markdown('<div class="menu-sub">Digite seu nome para gerar o certificado!</div>', unsafe_allow_html=True)
    nome = st.text_input("Seu nome completo:", value=st.session_state.cert_nome, placeholder="Ex.: Maria Silva Santos")
    st.session_state.cert_nome = nome
    if nome.strip():
        hoje = datetime.now().strftime("%Y-%m-%d")
        cert = gerar_codigo_certificado(nome, hoje)
        from urllib.parse import quote
        url_verificacao = f"{URL_BASE}/?verificar={cert['codigo']}&nome={quote(nome.strip())}"
        qr_b64 = gerar_qr_base64(url_verificacao)
        col_cert, col_qr = st.columns([3, 1])
        with col_cert:
            st.markdown(f"""
<div style="background: linear-gradient(135deg,#fff8dc,#ffed4a); border:15px double #0a1929; border-radius:20px; padding:50px 40px; text-align:center; box-shadow:0 0 60px rgba(255,215,0,.8);">
    <div style="font-size:3rem;">🌐</div>
    <div style="font-size:1.3rem; color:#1a3a5c; font-weight:700; letter-spacing:3px;">CERTIFICADO</div>
    <div style="font-size:.9rem; color:#1a3a5c; margin-top:5px;">DE CIDADÃO DIGITAL</div>
    <div style="margin:30px 0; font-size:1rem; color:#1a3a5c;">Certificamos que</div>
    <div style="font-size:2.2rem; font-weight:900; color:#0a1929; border-bottom:3px solid #0a1929; display:inline-block; padding:0 40px 10px;">{cert['nome']}</div>
    <div style="margin:30px 0; font-size:1rem; color:#1a3a5c; max-width:600px; margin-left:auto; margin-right:auto; line-height:1.6;">participou das atividades de <b>Cidadania Digital</b> e demonstrou compromisso com o uso consciente, seguro e ético da internet.</div>
    <div style="font-size:2.5rem; margin:20px 0;">🏆</div>
    <div style="font-size:.85rem; color:#1a3a5c; margin-top:30px;">EEEF Profª Odete Mendes N Oliveira<br>Prof. Irving V. Santos / Luiz Veloso<br><b>Código:</b> {cert['codigo']} &nbsp;|&nbsp; <b>Data:</b> {hoje}</div>
</div>
""", unsafe_allow_html=True)
        with col_qr:
            st.markdown('<div style="text-align:center; margin-top:60px;">', unsafe_allow_html=True)
            st.markdown(f'<img src="data:image/png;base64,{qr_b64}" style="width:100%; max-width:220px; border:5px solid white; border-radius:10px;">', unsafe_allow_html=True)
            st.markdown('<div style="color:white; font-size:.8rem; text-align:center; margin-top:10px;">📱 Escaneie para<br>levar no celular</div>', unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)
        st.markdown('<div style="text-align:center; color:rgba(255,255,255,.7); margin-top:15px;">💡 Para imprimir no estande: <b>Ctrl+P</b> → "Salvar como PDF"</div>', unsafe_allow_html=True)

def tela_verificacao(codigo: str, nome: str):
    st.markdown('<div class="menu-titulo">🔍 Verificação de Certificado</div>', unsafe_allow_html=True)
    try:
        partes = codigo.split("-")
        if len(partes) != 3 or partes[0] != "CD": valido = False
        else:
            data_str = partes[1]; data = f"{data_str[:4]}-{data_str[4:6]}-{data_str[6:8]}"
            esperado = gerar_codigo_certificado(nome, data); valido = (esperado["codigo"] == codigo)
    except Exception: valido = False
    
    if valido:
        st.markdown(f"""
<div style="background: linear-gradient(135deg,#fff8dc,#ffed4a); border:10px double #0a1929; border-radius:20px; padding:30px 20px; text-align:center; max-width:400px; margin:20px auto; box-shadow:0 0 40px rgba(255,215,0,.8);">
    <div style="font-size:2rem;">✅</div>
    <div style="font-size:1rem; color:#00b894; font-weight:900; letter-spacing:2px;">CERTIFICADO VÁLIDO</div>
    <div style="font-size:2.5rem; margin:10px 0;">🌐</div>
    <div style="font-size:.8rem; color:#1a3a5c; font-weight:700;">CERTIFICADO DE CIDADÃO DIGITAL</div>
    <div style="margin:15px 0; font-size:.8rem; color:#1a3a5c;">Certificamos que</div>
        <div style="font-size:1.5rem; margin:10px 0;">🏆</div>
    <div style="font-size:.65rem; color:#1a3a5c; margin-top:15px;">EEEF Profª Odete Mendes<br>Prof. Irving V. Santos<br><b>Código:</b> {codigo}<br><b>Data:</b> {data}</div>
</div>
""", unsafe_allow_html=True)
        st.markdown('<div style="text-align:center; color:white; font-size:1.1rem; margin-top:20px; font-weight:700;">📸 Tire um print desta tela para salvar!</div>', unsafe_allow_html=True)
    else:
        st.markdown('<div style="background:#e17055; padding:40px; border-radius:20px; text-align:center; max-width:600px; margin:30px auto;"><div style="font-size:4rem;">❌</div><div style="font-size:1.8rem; font-weight:900; margin:15px 0;">CERTIFICADO INVÁLIDO</div></div>', unsafe_allow_html=True)

# ============================================================
# ROTEADOR
# ============================================================
query_params = st.query_params
if "verificar" in query_params and "nome" in query_params:
    tela_verificacao(query_params["verificar"], query_params["nome"])
elif st.session_state.tela == "menu":
    tela_menu()
elif st.session_state.tela == "roda":
    tela_roda()
elif st.session_state.tela == "quiz":
    tela_quiz()
elif st.session_state.tela == "certificado":
    tela_certificado()
    <div style="margin:15px 0; font-size:.75rem; color:#1a3a5c; line-height:1.4;">participou das atividades de <b>Cidadania Digital</b>.</div>
