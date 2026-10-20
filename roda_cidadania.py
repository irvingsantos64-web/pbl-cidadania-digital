# -*- coding: utf-8 -*-
import streamlit as st
import hashlib
import base64
from io import BytesIO
from datetime import datetime
import qrcode
import json

st.set_page_config(page_title="Cidadania Digital", page_icon="🌐", layout="wide")

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
    {"emoji": "📰", "texto": "VERIFIQUE A FONTE antes de compartilhar!"}, {"emoji": "🛡️", "texto": "NÃO PRATIQUE CYBERBULLYING!"},
    {"emoji": "⚖️", "texto": "PENSE ANTES DE POSTAR!"}, {"emoji": "🔒", "texto": "PROTEJA SEUS DADOS!"},
    {"emoji": "🚫", "texto": "DENUNCIE CONTEÚDO OFENSIVO!"}, {"emoji": "🔍", "texto": "PESQUISE ANTES DE COMPARTILHAR!"},
    {"emoji": "💙", "texto": "SEJA GENTIL ONLINE!"}, {"emoji": "🌐", "texto": "NA DÚVIDA, NÃO COMPARTILHE!"},
    {"emoji": "🔑", "texto": "USE SENHAS FORTES E DIFERENTES!"}, {"emoji": "👤", "texto": "NÃO COMPARTILHE DADOS PESSOAIS!"},
    {"emoji": "📸", "texto": "CUIDADO COM O QUE POSTA NAS REDES!"}, {"emoji": "🤝", "texto": "RESPEITE A OPINIÃO DOS OUTROS!"},
    {"emoji": "🧠", "texto": "NÃO ACREDITE EM TUDO QUE VÊ NA INTERNET!"}, {"emoji": "📵", "texto": "NÃO USE O CELULAR PARA PREJUDICAR NINGUÉM!"},
    {"emoji": "🎭", "texto": "PERFIS FALSOS EXISTEM - DESCONFIE!"}, {"emoji": "💬", "texto": "PENSE ANTES DE COMENTAR!"},
    {"emoji": "🔗", "texto": "NÃO CLIQUE EM LINKS SUSPEITOS!"}, {"emoji": "🎁", "texto": "PROMOÇÕES BOAS DEMAIS PODEM SER GOLPE!"},
    {"emoji": "🕵️", "texto": "PROTEJA SUA PRIVACIDADE ONLINE!"}, {"emoji": "📚", "texto": "ESTUDE AS NOTÍCIAS ANTES DE REPASSAR!"},
    {"emoji": "❤️", "texto": "ESPALHE O BEM, NÃO O ÓDIO!"}, {"emoji": "🤐", "texto": "O QUE VOCÊ POSTA PODE FICAR PARA SEMPRE!"},
    {"emoji": "🌍", "texto": "A INTERNET É DE TODOS - RESPEITE!"}, {"emoji": "⭐", "texto": "SEJA UM EXEMPLO DE CIDADÃO DIGITAL!"},
    {"emoji": "🧒", "texto": "NÃO CONVERSE COM ESTRANHOS ONLINE!"}, {"emoji": "🎮", "texto": "RESPEITE OS OUTROS JOGADORES NOS JOGOS!"},
    {"emoji": "📱", "texto": "NÃO RESPONDA A MENSAGENS AGRESSIVAS!"}, {"emoji": "🔔", "texto": "BLOQUEIE QUEM TE FAZ MAL!"},
    {"emoji": "📧", "texto": "DESCONFIE DE E-MAILS ESTRANHOS!"}, {"emoji": "🏦", "texto": "NUNCA COMPARTILHE SENHAS BANCÁRIAS!"},
    {"emoji": "📷", "texto": "NÃO ENVIE FOTOS ÍNTIMAS PARA NINGUÉM!"}, {"emoji": "👨‍👩‍👧", "texto": "CONTE AOS PAIS SE ALGO DER ERRADO!"},
    {"emoji": "🚨", "texto": "PEÇA AJUDA SE SOFRER AMEAÇAS!"}, {"emoji": "🕒", "texto": "CONTROLE O TEMPO DE TELA!"},
    {"emoji": "🎯", "texto": "NÃO ESPALHE FAKE NEWS!"}, {"emoji": "🤳", "texto": "CUIDADO COM O QUE MOSTRA NAS FOTOS!"},
    {"emoji": "🎓", "texto": "USE A INTERNET PARA APRENDER MAIS!"}, {"emoji": "🌱", "texto": "PLANTE O BEM NO AMBIENTE DIGITAL!"},
    {"emoji": "🧩", "texto": "PENSE CRÍTICO COM O QUE VÊ ONLINE!"}, {"emoji": "🏆", "texto": "SEJA UM CIDADÃO DIGITAL DE VERDADE!"}
]

QUIZ = [
    {"pergunta": "Você recebeu uma notícia bombástica no WhatsApp. O que faz?", "opcoes": ["Compartilho com todos, é urgente!", "Verifico a fonte antes de compartilhar.", "Acredito, se está na internet é verdade.", "Repasso só para os amigos próximos."], "correta": 1, "explicacao": "Sempre verifique a fonte antes de compartilhar. Fake news se espalham rápido!"},
    {"pergunta": "O que é cyberbullying?", "opcoes": ["Uma brincadeira normal na internet.", "Agressão, humilhação ou perseguição feita online.", "Um jogo virtual.", "Um tipo de vírus de computador."], "correta": 1, "explicacao": "Cyberbullying é violência online. Não pratique e denuncie!"},
    {"pergunta": "Um desconhecido pede seus dados pessoais online. O que faz?", "opcoes": ["Envio, pode ser importante.", "Envio só o nome e idade.", "Não envio nada e conto a um adulto.", "Envio se ele parecer legal."], "correta": 2, "explicacao": "Nunca compartilhe dados pessoais com estranhos. Conte a um adulto de confiança!"},
    {"pergunta": "Qual senha é mais segura?", "opcoes": ["123456", "minhasenha", "MeuNome2010", "X7#kL9$mP2!q"], "correta": 3, "explicacao": "Senhas fortes misturam letras maiúsculas, minúsculas, números e símbolos!"},
    {"pergunta": "Um amigo está sofrendo bullying online. O que faz?", "opcoes": ["Rio junto para não ser a próxima vítima.", "Fico quieto, não é meu problema.", "Apoio ele e denuncio o agressor.", "Compartilho para os outros verem."], "correta": 2, "explicacao": "Apoie a vítima e denuncie. Ser um cidadão digital é defender quem precisa!"}
]

def gerar_codigo_certificado(nome, data):
    base = f"{nome.strip().lower()}|{data}"
    assinatura = hashlib.sha256((base + SEGREDO).encode()).hexdigest()[:10].upper()
    return {"nome": nome.strip(), "data": data, "codigo": f"CD-{data.replace('-','')}-{assinatura}"}

def gerar_qr_base64(url):
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
        if st.button("🎡\n\nRODA\n\nDescubra uma dica"): st.session_state.tela = "roda"; st.rerun()
    with col2:
        if st.button("🧠\n\nQUIZ\n\nTeste seu conhecimento"):
            st.session_state.tela = "quiz"; st.session_state.quiz_idx = 0; st.session_state.quiz_acertos = 0; st.session_state.quiz_respondido = False; st.session_state.quiz_escolha = None; st.rerun()
    with col3:
        if st.button("🏆\n\nCERTIFICADO\n\nGanhe seu diploma"): st.session_state.tela = "certificado"; st.rerun()

def tela_roda():
    col1, col2 = st.columns([1, 6])
    with col1:
        if st.button("⬅️ Voltar"): st.session_state.tela = "menu"; st.rerun()
    dicas_js = json.dumps(DICAS, ensure_ascii=False)
    html = """
    <!DOCTYPE html><html><head><style>
    body { background: #0a1929; display:flex; flex-direction:column; align-items:center; color:white; font-family:sans-serif; padding:10px; }
    .roda { width:300px; height:300px; border-radius:50%; border:5px solid #ffd700; transition:transform 3s cubic-bezier(0.2,0.8,0.2,1); }
    .btn { background:#ffd700; color:#0a1929; padding:10px 30px; border:none; border-radius:20px; font-weight:bold; cursor:pointer; margin-top:20px; }
    </style></head><body>
    <div class="roda" id="roda"></div>
    <button class="btn" onclick="girar()">GIRAR</button>
    <script>
    const dicas = __DICAS__; let girando = false; let angulo = 0;
    function girar() {
        if (girando) return; girando = true;
        document.getElementById('roda').style.transform = 'rotate(' + (angulo += 1080) + 'deg)';
        setTimeout(() => { alert(dicas[Math.floor(Math.random()*dicas.length)].texto); girando = false; }, 3000);
    }
    </script></body></html>
    """.replace("__DICAS__", dicas_js).replace("'", "\\'")
    st.components.v1.html(html, height=500)

def tela_quiz():
    with st.sidebar: st.write("")
    col1, col2 = st.columns([1, 6])
    with col1:
        if st.button("⬅️ Voltar"): st.session_state.tela = "menu"; st.rerun()
    idx = st.session_state.quiz_idx
    if idx >= len(QUIZ):
        st.markdown(f'<div class="menu-titulo">🎉 Fim! Você acertou {st.session_state.quiz_acertos} de {len(QUIZ)}</div>', unsafe_allow_html=True)
        if st.button("Jogar Novamente"): st.session_state.quiz_idx = 0; st.session_state.quiz_acertos = 0; st.session_state.quiz_respondido = False; st.session_state.quiz_escolha = None; st.rerun()
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
    nome = st.text_input("Seu nome completo:")
    st.session_state.cert_nome = nome
    if nome.strip():
        hoje = datetime.now().strftime("%Y-%m-%d")
        cert = gerar_codigo_certificado(nome, hoje)
        from urllib.parse import quote
        url = f"{URL_BASE}/?verificar={cert['codigo']}&nome={quote(nome.strip())}"
        qr = gerar_qr_base64(url)
        col_c, col_q = st.columns([3, 1])
        with col_c:
            st.markdown(f'<div style="background:#ffed4a; padding:40px; border-radius:20px; text-align:center; color:#0a1929;"><h1>CERTIFICADO</h1><h2>{cert["nome"]}</h2><p>Participou das atividades de Cidadania Digital.</p><p><b>Código:</b> {cert["codigo"]}</p></div>', unsafe_allow_html=True)
        with col_q:
            st.markdown(f'<img src="data:image/png;base64,{qr}" style="width:100%;">', unsafe_allow_html=True)

def tela_verificacao(codigo, nome):
    st.markdown('<div class="menu-titulo">🔍 Certificado</div>', unsafe_allow_html=True)
    st.markdown(f'<div style="background:#00b894; padding:30px; border-radius:20px; text-align:center; color:white;"><h2>✅ AUTÊNTICO</h2><p>Nome: {nome}</p><p>Código: {codigo}</p></div>', unsafe_allow_html=True)
    st.markdown('<div style="text-align:center; font-size:1.2rem; margin-top:20px;">📸 Tire um print desta tela!</div>', unsafe_allow_html=True)

query_params = st.query_params
if "verificar" in query_params and "nome" in query_params:
    tela_verificacao(query_params["verificar"], query_params["nome"])
elif st.session_state.tela == "menu": tela_menu()
elif st.session_state.tela == "roda": tela_roda()
elif st.session_state.tela == "quiz": tela_quiz()
elif st.session_state.tela == "certificado": tela_certificado()
