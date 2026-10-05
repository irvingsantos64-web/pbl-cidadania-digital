# ============================================================
# 🏫 EEEF PROFª ODETE MENDES N OLIVEIRA
# 👨‍🏫 PROFESSOR: IRVING VASCONCELOS DOS SANTOS (CICI)
# 👨‍🎓 TURMA: 6º ANO - ENSINO FUNDAMENTAL
# 💡 PROJETO: CIDADANIA DIGITAL E ÉTICA NAS REDES SOCIAIS
# ============================================================

import streamlit as st
import random
from datetime import datetime
import base64
import time
import pandas as pd

# 🔥 BANCO DE DADOS
from database import (
    init_db,
    get_connection, 
    salvar_aluno, 
    buscar_alunos_por_turma, 
    buscar_todas_turmas, 
    buscar_ranking_geral, 
    buscar_todos_alunos,
    buscar_questoes_embaralhadas, 
    excluir_aluno,
    buscar_questoes_por_turma_e_categoria,
    buscar_ranking_turmas,
    listar_todas_questoes,           
    listar_questoes_por_turma,       
    listar_questoes_por_categoria,   
    listar_questoes_por_turma_categoria,
    calcular_impacto_fake,
    criar_equipe,           
    listar_equipes,         
    adicionar_pontos_equipe,
    excluir_equipe,
    zerar_pontos_alunos,
    buscar_dados_aluno,
    criar_atividade,      
    listar_atividades,     
    listar_atividades_por_turma,  
    excluir_atividade,
    criar_desafio_semanal, 
    buscar_desafio_atual,   
    listar_desafios,        
    excluir_desafio,
    listar_livros,              
    listar_livros_por_categoria,
    buscar_livro,               
    criar_livro,                
    excluir_livro,              
    criar_resenha,             
    listar_resenhas,
    buscar_questoes_por_categoria,
    criar_equipe_completa,
    adicionar_aluno_equipe,
    listar_equipes_completas,
    adicionar_pontos_equipe_completa,
    excluir_equipe_completa,
    buscar_equipe_do_aluno,
    buscar_questoes_equipe,
    inserir_casos_pbl,
    listar_casos_pbl,
    buscar_caso_pbl, 
    salvar_resposta_pbl,
    listar_respostas_pbl,
    listar_respostas_pbl_aluno,
    excluir_resposta_pbl,
    excluir_respostas_pbl_por_turma,
    excluir_todas_respostas_pbl,
    salvar_algoritmo,
    listar_algoritmos,
    listar_algoritmos_aluno,
    excluir_algoritmo,
    excluir_todos_algoritmos, 
    salvar_dissecacao,
    listar_dissecacoes,
    listar_dissecacoes_aluno,
    excluir_dissecacao, 
    salvar_debate,
    listar_debates,
    listar_debates_aluno,
    contar_debates_por_frase,
    excluir_debate,
    salvar_cancelamento,
    listar_cancelamentos,
    listar_cancelamentos_aluno,
    excluir_cancelamento, 
    salvar_juri,
    listar_juri,
    listar_juri_aluno,
    listar_juri_por_caso,
    excluir_juri,  
    salvar_analise_dados,
    listar_analises,
    listar_analises_aluno,
    excluir_analise, 
    salvar_campanha,
    listar_campanhas,
    listar_campanhas_aluno,
    excluir_campanha,
    salvar_infografico,
    listar_infograficos,
    listar_infograficos_aluno,
    excluir_infografico,
    salvar_podcast,
    listar_podcasts,
    listar_podcasts_aluno,
    excluir_podcast, 
    buscar_todas_turmas,
    buscar_alunos_por_turma,
    buscar_todos_alunos,  
    salvar_questionario,
    listar_questionarios,
    listar_questionarios_por_turma,
    contar_respostas,
    excluir_questionario,   
)                      

# Inicializar banco

from database import inserir_perguntas_educacao_fisica
inserir_perguntas_educacao_fisica()

from database import inserir_perguntas_interdisciplinares
inserir_perguntas_interdisciplinares()

from database import inserir_perguntas_categorias_separadas
inserir_perguntas_categorias_separadas()

# ========== CONFIGURAÇÃO DA PÁGINA ==========
st.set_page_config(page_title="Cidadania Digital", page_icon="🌐", layout="wide")

# ========== CSS ==========
st.markdown('''
<style>
    .header {
        background: linear-gradient(135deg, #1a3a5c, #2d5f8a);
        padding: 20px;
        border-radius: 15px;
        color: white;
        text-align: center;
        margin-bottom: 20px;
    }
    .header h1 { font-size: 2rem; margin: 0; }
    .badge {
        display: inline-block;
        padding: 5px 15px;
        border-radius: 20px;
        margin: 5px;
        font-weight: bold;
    }
    .badge-gold { background: #ffd700; color: #333; }
    .badge-silver { background: #c0c0c0; color: #333; }
    .badge-bronze { background: #cd7f32; color: white; }
    .badge-blue { background: #1a3a5c; color: white; }
    .badge-green { background: #28a745; color: white; }
    .badge-purple { background: #6f42c1; color: white; }
    .card { background: #f8f9fa; padding: 15px; border-radius: 10px; border-left: 5px solid #1a3a5c; margin: 10px 0; }
    .card-fake { border-left-color: #ffc107; }
    .card-cyber { border-left-color: #dc3545; }
    .card-ethic { border-left-color: #28a745; }
    .card-mission { border-left-color: #6f42c1; background: #f0e6ff; }
    .rank-card { background: linear-gradient(135deg, #1a3a5c, #2d5f8a); padding: 20px; border-radius: 15px; color: white; text-align: center; margin: 10px 0; }
    .mission-card { background: linear-gradient(135deg, #6f42c1, #9b59b6); padding: 15px; border-radius: 10px; color: white; text-align: center; margin: 5px 0; }
    .progress-bar { background: #e9ecef; border-radius: 10px; height: 20px; margin: 5px 0; }
    .progress-fill { background: linear-gradient(90deg, #28a745, #ffc107); border-radius: 10px; height: 20px; color: white; text-align: center; font-size: 12px; }
</style>
''', unsafe_allow_html=True)

st.markdown('''
<div class="header">
    <h1>🌐 CIDADANIA DIGITAL E ÉTICA NAS REDES DIGITAIS</h1>
    <p>🏫 EEEF PROFª ODETE MENDES N OLIVEIRA</p>
    <p style="background: rgba(255,215,0,0.2); padding: 8px 15px; border-radius: 8px; display: inline-block; border-left: 4px solid #ffd700;">
        👩‍💼 <strong>Gestora:</strong> IRIAN MARY ARAÚJO RODRIGUES
    </p>
    <p>👨‍🏫 Professores: IRVING VASCONCELOS DOS SANTOS (Matemática) - LUIZ VELOSO DE LIMA (Educação Física)</p>
    <p>👨‍🎓 6º ANO - ENSINO FUNDAMENTAL</p>
</div>
''', unsafe_allow_html=True)

# ========== SESSÃO ==========
if 'nome' not in st.session_state:
    st.session_state.nome = ""
if 'turma' not in st.session_state:
    st.session_state.turma = "6º Ano - Anfitrião"
if 'pontos' not in st.session_state:
    st.session_state.pontos = 0
if 'total' not in st.session_state:
    st.session_state.total = 0
if 'fake_acertos' not in st.session_state:
    st.session_state.fake_acertos = 0
if 'cyber_acertos' not in st.session_state:
    st.session_state.cyber_acertos = 0
if 'etica_acertos' not in st.session_state:
    st.session_state.etica_acertos = 0
if 'badges' not in st.session_state:
    st.session_state.badges = []
if 'indice_fake' not in st.session_state:
    st.session_state.indice_fake = 0
if 'indice_cyber' not in st.session_state:
    st.session_state.indice_cyber = 0
if 'indice_etica' not in st.session_state:
    st.session_state.indice_etica = 0
if 'missoes' not in st.session_state:
    st.session_state.missoes = {"fake": 0, "cyber": 0, "etica": 0, "total": 0}
if 'ultima_missao' not in st.session_state:
    st.session_state.ultima_missao = datetime.now().strftime("%Y-%m-%d")

# ========== SISTEMA DE RECOMPENSAS ==========
def verificar_recompensa(acertos):
    """Verifica qual recompensa o aluno ganhou"""
    if acertos >= 5:
        return "🏆", "🎉 PARABÉNS! VOCÊ É UM MESTRE DA CIDADANIA DIGITAL! 🎉", "🎊"
    elif acertos >= 4:
        return "🎖️", "Você é um Herói Digital! Continue assim!", "🌟"
    elif acertos >= 3:
        return "🏅", "Você é um Mestre da Ética! Parabéns!", "⭐"
    elif acertos >= 2:
        return "⭐", "Você é um Guardião da Verdade! Continue!", "🔥"
    elif acertos >= 1:
        return "🌟", "Você é um Detetive Iniciante! Bom começo!", "💪"
    else:
        return "📚", "Continue praticando! Você vai conseguir!", "📖"

def mostrar_recompensa(acertos):
    """Mostra a recompensa com animação"""
    emoji, mensagem, icone = verificar_recompensa(acertos)
    
    # Criar efeito visual
    st.markdown(f"""
    <div style='text-align: center; padding: 30px; background: linear-gradient(135deg, #1a3a5c, #2d5f8a); border-radius: 15px; color: white; margin: 10px 0;'>
        <h1 style='font-size: 4rem;'>{emoji}</h1>
        <h2>{mensagem}</h2>
        <h3 style='font-size: 3rem;'>{icone * 3}</h3>
    </div>
    """, unsafe_allow_html=True)
    
    # Se acertou 5, mostrar balões
    if acertos >= 5:
        st.balloons()

# ========== FUNÇÃO PARA MOSTRAR ALUNO ATUAL E PRÓXIMO ==========
def mostrar_aluno_atual_e_proximo():
    """Mostra o aluno atual e o próximo aluno da turma"""
    
    turma = st.session_state.get('turma', '')
    nome_atual = st.session_state.get('nome', '')
    
    if not turma:
        return
    
    # Buscar alunos da turma
    alunos = buscar_alunos_por_turma(turma)
    
    if not alunos:
        st.warning("📭 Nenhum aluno cadastrado nesta turma.")
        return
    
    # Lista de nomes
    nomes = [a['nome'] for a in alunos]
    total = len(nomes)
    
    # 🔥 SE O NOME ATUAL ESTIVER VAZIO, USA O ÚLTIMO DA LISTA
    if not nome_atual:
        # Pega o último aluno que jogou
        ultimo = st.session_state.get('ultimo_aluno', nomes[-1] if nomes else '')
        
        if ultimo in nomes:
            posicao = nomes.index(ultimo)
            # Próximo é o que vem depois do último
            proximo = nomes[posicao + 1] if posicao + 1 < total else nomes[0]
            num_atual = posicao + 1
            num_proximo = (posicao + 1) % total + 1
            nome_atual = ultimo   # Mostra o último como atual
        else:
            # Se não achou, mostra o primeiro
            nome_atual = nomes[0]
            proximo = nomes[1] if total > 1 else nomes[0]
            num_atual = 1
            num_proximo = 2 if total > 1 else 1
    else:
        # 🔥 NOME ATUAL EXISTE — ENCONTRA A POSIÇÃO
        if nome_atual in nomes:
            posicao = nomes.index(nome_atual)
            proximo = nomes[posicao + 1] if posicao + 1 < total else nomes[0]
            num_atual = posicao + 1
            num_proximo = (posicao + 1) % total + 1
        else:
            # Se não achou, mostra o primeiro
            nome_atual = nomes[0]
            proximo = nomes[1] if total > 1 else nomes[0]
            num_atual = 1
            num_proximo = 2 if total > 1 else 1
    
    # Mostrar cards
    col1, col2, col3 = st.columns([2, 1, 2])
    
    with col1:
        st.markdown(f"""
        <div style='background: linear-gradient(135deg, #28a745, #20c997); padding: 15px; border-radius: 12px; color: white; text-align: center;'>
            <p style='margin: 0; font-size: 0.9rem; opacity: 0.9;'>👤 ALUNO ATUAL ({num_atual}/{total})</p>
            <h3 style='margin: 5px 0 0 0;'>{nome_atual}</h3>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div style='text-align: center; padding: 15px;'>
            <h1 style='font-size: 2.5rem; margin: 0;'>➡️</h1>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
        <div style='background: linear-gradient(135deg, #1a3a5c, #2d5f8a); padding: 15px; border-radius: 12px; color: white; text-align: center;'>
            <p style='margin: 0; font-size: 0.9rem; opacity: 0.9;'>➡️ PRÓXIMO ALUNO ({num_proximo}/{total})</p>
            <h3 style='margin: 5px 0 0 0;'>{proximo}</h3>
        </div>
        """, unsafe_allow_html=True)

# ========== FUNÇÕES ==========
def verificar_badges():
    badges = []
    if st.session_state.fake_acertos >= 5:
        badges.append(("📰 Detetive da Verdade", "gold"))
    if st.session_state.cyber_acertos >= 5:
        badges.append(("🛡️ Guardião Ético", "blue"))
    if st.session_state.etica_acertos >= 3:
        badges.append(("⚖️ Mestre da Ética", "green"))
    if st.session_state.pontos >= 20:
        badges.append(("🏆 Investigador Master", "gold"))
    if st.session_state.pontos >= 10:
        badges.append(("⭐ Investigador Júnior", "silver"))
    if st.session_state.missoes["total"] >= 10:
        badges.append(("🎯 Caçador de Missões", "purple"))
    if st.session_state.fake_acertos >= 3 and st.session_state.cyber_acertos >= 3 and st.session_state.etica_acertos >= 2:
        badges.append(("🦸 Herói Digital", "gold"))

    # 🧮 MATEMÁTICO DIGITAL → 10 acertos em Mat + Cidadania
    if st.session_state.get('mat_acertos', 0) >= 10:
        badges.append(("🧮 Matemático Digital", "blue"))
    
    # 🏃 ATLETA CIDADÃO → 10 acertos em EF + Cidadania
    if st.session_state.get('ef_acertos', 0) >= 10:
        badges.append(("🏃 Atleta Cidadão", "green"))
    
    # 🧠 MESTRE INTERDISCIPLINAR → 20 acertos nas 3 disciplinas
    total_inter = (
        st.session_state.get('mat_acertos', 0) +
        st.session_state.get('ef_acertos', 0) +
        st.session_state.get('desafio_inter_acertos', 0)
    )
    if total_inter >= 20:
        badges.append(("🧠 Mestre Interdisciplinar", "gold"))

    return badges

def resetar_missoes():
    hoje = datetime.now().strftime("%Y-%m-%d")
    if st.session_state.ultima_missao != hoje:
        st.session_state.missoes = {"fake": 0, "cyber": 0, "etica": 0, "total": 0}
        st.session_state.ultima_missao = hoje
    if 'mat_acertos' not in st.session_state:
        st.session_state.mat_acertos = 0
    if 'ef_acertos' not in st.session_state:
        st.session_state.ef_acertos = 0

# ========== FUNÇÃO DE SOM ==========
def tocar_som(tipo):
    """Toca um som baseado no tipo (versão estável com components.html)"""
    import streamlit.components.v1 as components
    
    sons = {
        "acerto": "sons/acerto.wav",
        "erro": "sons/erro.wav",
        "vitoria": "sons/vitoria.wav",
        "badge": "sons/badge.wav",
        "clique": "sons/clique.wav"
    }
    
    if tipo in sons:
        try:
            with open(sons[tipo], "rb") as f:
                audio_bytes = f.read()
                audio_base64 = base64.b64encode(audio_bytes).decode()
                
                # 🔥 components.html com altura 0 = iframe invisível
                components.html(
                    f"""
                    <audio autoplay>
                        <source src="data:audio/wav;base64,{audio_base64}" type="audio/wav">
                    </audio>
                    """,
                    height=0,
                    width=0
                )
        except FileNotFoundError:
            pass

def comemorar(mensagem="🎉 PARABÉNS!"):
    """Balões + som de vitória JUNTOS (versão corrigida)"""
    import streamlit.components.v1 as components
    
    components.html(
        """
        <script src="https://cdn.jsdelivr.net/npm/canvas-confetti@1.6.0/dist/confetti.browser.min.js"></script>
        <script>
            // 🎈 BALÕES
            confetti({ 
                particleCount: 200, 
                spread: 90, 
                origin: { y: 0.6 },
                colors: ['#ffd700', '#ff6b6b', '#4ecdc4', '#6f42c1']
            });
            
            setTimeout(() => {
                confetti({ particleCount: 100, angle: 60, spread: 55, origin: { x: 0 } });
                confetti({ particleCount: 100, angle: 120, spread: 55, origin: { x: 1 } });
            }, 250);
            
            // 🔊 SOM DE VITÓRIA (CORRIGIDO)
            function tocarSom() {
    const audioCtx = new (window.AudioContext || window.webkitAudioContext)();
    if (audioCtx.state === 'suspended') {
        audioCtx.resume().then(() => tocarNotas(audioCtx));
    } else {
        tocarNotas(audioCtx);
    }
}
function tocarNotas(audioCtx) {
    // ...
}
tocarSom();
document.addEventListener('click', function() { tocarSom(); }, { once: true });
                } else {
                    tocarNotas(audioCtx);
                }
            }
            
            function tocarNotas(audioCtx) {
                [523, 659, 784, 1047].forEach((freq, i) => {
                    setTimeout(() => {
                        const osc = audioCtx.createOscillator();
                        const gain = audioCtx.createGain();
                        osc.connect(gain);
                        gain.connect(audioCtx.destination);
                        osc.frequency.value = freq;
                        osc.type = 'sine';
                        gain.gain.setValueAtTime(0.3, audioCtx.currentTime);
                        gain.gain.exponentialRampToValueAtTime(0.01, audioCtx.currentTime + 0.3);
                        osc.start();
                        osc.stop(audioCtx.currentTime + 0.3);
                    }, i * 200);
                });
            }
            
            // 🔥 Tenta tocar imediatamente
            tocarSom();
            
            // 🔥 Se falhar, tenta no primeiro clique
            document.addEventListener('click', function() {
                tocarSom();
            }, { once: true });
        </script>
        """,
        height=0,
        width=0
    )
    st.toast(mensagem, icon="🏆")

# ========== FUNÇÕES ==========
def verificar_badges():
    badges = []
    if st.session_state.fake_acertos >= 5:
        badges.append(("📰 Detetive da Verdade", "gold"))
    if st.session_state.cyber_acertos >= 5:
        badges.append(("🛡️ Guardião Ético", "blue"))
    if st.session_state.etica_acertos >= 3:
        badges.append(("⚖️ Mestre da Ética", "green"))
    if st.session_state.pontos >= 20:
        badges.append(("🏆 Investigador Master", "gold"))
    if st.session_state.pontos >= 10:
        badges.append(("⭐ Investigador Júnior", "silver"))
    if st.session_state.missoes["total"] >= 10:
        badges.append(("🎯 Caçador de Missões", "purple"))
    if st.session_state.fake_acertos >= 3 and st.session_state.cyber_acertos >= 3 and st.session_state.etica_acertos >= 2:
        badges.append(("🦸 Herói Digital", "gold"))
    return badges


def resetar_missoes():
    hoje = datetime.now().strftime("%Y-%m-%d")
    if st.session_state.ultima_missao != hoje:
        st.session_state.missoes = {"fake": 0, "cyber": 0, "etica": 0, "total": 0}
        st.session_state.ultima_missao = hoje


def tocar_som(tipo):
    """Toca um som baseado no tipo"""
    sons = {
        "acerto": "sons/acerto.wav",
        "erro": "sons/erro.wav",
        "vitoria": "sons/vitoria.wav",
        "badge": "sons/badge.wav",
        "clique": "sons/clique.wav"
    }
    
    if tipo in sons:
        try:
            with open(sons[tipo], "rb") as f:
                audio_bytes = f.read()
                audio_base64 = base64.b64encode(audio_bytes).decode()
                st.markdown(f"""
                <audio autoplay>
                    <source src="data:audio/wav;base64,{audio_base64}" type="audio/wav">
                </audio>
                """, unsafe_allow_html=True)
        except FileNotFoundError:
            pass


def comemorar(mensagem="🎉 PARABÉNS!"):
    """Balões + som de vitória JUNTOS (versão com st.html)"""
    
    st.html(
        """
        <script src="https://cdn.jsdelivr.net/npm/canvas-confetti@1.6.0/dist/confetti.browser.min.js"></script>
        <script>
            // 🎈 BALÕES
            confetti({ 
                particleCount: 200, 
                spread: 90, 
                origin: { y: 0.6 },
                colors: ['#ffd700', '#ff6b6b', '#4ecdc4', '#6f42c1']
            });
            
            setTimeout(() => {
                confetti({ particleCount: 100, angle: 60, spread: 55, origin: { x: 0 } });
                confetti({ particleCount: 100, angle: 120, spread: 55, origin: { x: 1 } });
            }, 250);
            
            // 🔊 SOM DE VITÓRIA
            function tocarSom() {
                const audioCtx = new (window.AudioContext || window.webkitAudioContext)();
                
                if (audioCtx.state === 'suspended') {
                    audioCtx.resume().then(() => tocarNotas(audioCtx));
                } else {
                    tocarNotas(audioCtx);
                }
            }
            
            function tocarNotas(audioCtx) {
                [523, 659, 784, 1047].forEach((freq, i) => {
                    setTimeout(() => {
                        const osc = audioCtx.createOscillator();
                        const gain = audioCtx.createGain();
                        osc.connect(gain);
                        gain.connect(audioCtx.destination);
                        osc.frequency.value = freq;
                        osc.type = 'sine';
                        gain.gain.setValueAtTime(0.4, audioCtx.currentTime);
                        gain.gain.exponentialRampToValueAtTime(0.01, audioCtx.currentTime + 0.3);
                        osc.start();
                        osc.stop(audioCtx.currentTime + 0.3);
                    }, i * 200);
                });
            }
            
            tocarSom();
        </script>
        """
    )
    st.toast(mensagem, icon="🏆")

def zerar_sessao():
    st.session_state.pontos = 0
    st.session_state.total = 0
    st.session_state.fake_acertos = 0
    st.session_state.cyber_acertos = 0
    st.session_state.etica_acertos = 0
    st.session_state.indice_fake = 0
    st.session_state.indice_cyber = 0
    st.session_state.indice_etica = 0
    st.session_state.missoes = {"fake": 0, "cyber": 0, "etica": 0, "total": 0}
    st.session_state.ultima_missao = datetime.now().strftime("%Y-%m-%d")

# ========== MENU ==========
menu = st.sidebar.radio("📋 Menu", [
    "🏠 Início",
    "📰 Fake News",
    "🛡️ Cyberbullying",
    "⚖️ Ética Digital",
    "🏃 Educação Física",
    "🏃 Quiz de Educação Física", 
    "🧠 Desafio Interdisciplinar",
    "🏆 Equipes (Gincana)",
    "📋 Casos Reais (PBL)",
    "📝 Algoritmo Anti-Fake News",
    "🧠 Disseque o Algoritmo",
    "⚖️ Discurso de Ódio vs. Liberdade",
    "📋 Respostas PBL (Professor)",
    "🅴 Cultura do Cancelamento",
    "🅸 Júri Simulado Digital",
    "🅷 Dados da Desinformação",
    "🅹 Campanha de Conscientização",
    "🅵 Infográfico Maker",
    "🅶 Podcast da Cidadania",
    "📊 Pesquisa e Relatórios",
    "📋 Questionário Cidadania Digital",
    "🎖️ Badges",
    "🏆 Ranking",
    "🎯 Missões Diárias",
    "👥 Lista de Alunos",
    "📊 Relatório",
    "📚 Gerenciar Perguntas",
    "📊 Calculadora de Impacto",
    "🧠 Simulador de Algoritmo",
    "📝 Fluxograma Anti-Fake News",
    "🎨 Campanha Ética",
    "📋 Guia de Sobrevivência",
    "📊 Estatísticas da Turma",
    "🎮 Dinâmicas",
    "🏆 Equipes",
    "⚙️ Gerenciar Pontos",
    "🏅 Certificados",
    "🗓️ Calendário",
    "📊 Dashboard",
    "📐 Matemática da Cidadania",          
    "🎯 Desafios Semanais",
    "🎮 Jogo da Memória",
    "📚 Biblioteca"
])

# 🔥 BOTÃO PRÓXIMO ALUNO
if st.sidebar.button("🔄 Próximo Aluno", key="proximo_aluno"):
    
    # ========== SALVAR O ALUNO ATUAL ==========
    aluno_atual = st.session_state.nome
    turma_atual = st.session_state.turma
    
    # ========== BUSCAR PRÓXIMO ALUNO ==========
    alunos = buscar_alunos_por_turma(turma_atual)
    
    if alunos:
        nomes = [a['nome'] for a in alunos]
        
        if aluno_atual in nomes:
            posicao = nomes.index(aluno_atual)
            # Próximo aluno (volta ao primeiro se for o último)
            proximo = nomes[posicao + 1] if posicao + 1 < len(nomes) else nomes[0]
        else:
            # Se não achou, pega o primeiro
            proximo = nomes[0]
        
        # 🔥 AVANÇAR PARA O PRÓXIMO ALUNO
        st.session_state.nome = proximo
        st.session_state.ultimo_aluno = aluno_atual
    else:
        st.session_state.nome = ""

    # 🔥 LIMPAR DADOS DA DESINFORMAÇÃO
    if 'analise_dados' in st.session_state:
        del st.session_state.analise_dados
    if 'conclusao_dados' in st.session_state:
        del st.session_state.conclusao_dados

    # 🔥 LIMPAR CAMPANHA
    if 'roteiro_campanha' in st.session_state:
        del st.session_state.roteiro_campanha
    if 'divulgacao_campanha' in st.session_state:
        del st.session_state.divulgacao_campanha

    # 🔥 LIMPAR INFOGRÁFICO
    if 'roteiro_infografico' in st.session_state:
        del st.session_state.roteiro_infografico

    # 🔥 LIMPAR PODCAST
    if 'roteiro_podcast' in st.session_state:
        del st.session_state.roteiro_podcast
    
    # ========== LIMPAR TODAS AS VARIÁVEIS DE SESSÃO ==========
    st.session_state.pontos = 0
    st.session_state.total = 0
    st.session_state.fake_acertos = 0
    st.session_state.cyber_acertos = 0
    st.session_state.etica_acertos = 0
    st.session_state.indice_fake = 0
    st.session_state.indice_cyber = 0
    st.session_state.indice_etica = 0
    st.session_state.missoes = {"fake": 0, "cyber": 0, "etica": 0, "total": 0}
    
    # ========== LIMPAR QUESTÕES EMBARALHADAS ==========
    if 'questoes_fake_embaralhadas' in st.session_state:
        del st.session_state.questoes_fake_embaralhadas
    if 'questoes_cyber_embaralhadas' in st.session_state:
        del st.session_state.questoes_cyber_embaralhadas
    if 'questoes_etica_embaralhadas' in st.session_state:
        del st.session_state.questoes_etica_embaralhadas
    
    # ========== LIMPAR TENTATIVAS ==========
    if 'tentativas_fake' in st.session_state:
        del st.session_state.tentativas_fake
    if 'tentativas_cyber' in st.session_state:
        del st.session_state.tentativas_cyber
    if 'tentativas_etica' in st.session_state:
        del st.session_state.tentativas_etica
    
    # ========== LIMPAR CAMPOS DE TEXTO ==========
    if 'nome_inicio' in st.session_state:
        del st.session_state.nome_inicio
    if 'turma_inicio' in st.session_state:
        del st.session_state.turma_inicio

    # ========== LIMPAR QUIZ DE EDUCAÇÃO FÍSICA ==========
    if 'quiz_ef_questoes' in st.session_state:
        del st.session_state.quiz_ef_questoes
    if 'quiz_ef_tentativas' in st.session_state:
        del st.session_state.quiz_ef_tentativas
    if 'quiz_ef_acertos' in st.session_state:
        del st.session_state.quiz_ef_acertos
    if 'quiz_ef_indice' in st.session_state:
        del st.session_state.quiz_ef_indice
    
    # ========== LIMPAR DESAFIO INTERDISCIPLINAR ==========
    if 'desafio_inter_questoes' in st.session_state:
        del st.session_state.desafio_inter_questoes
    if 'desafio_inter_tentativas' in st.session_state:
        del st.session_state.desafio_inter_tentativas
    if 'desafio_inter_acertos' in st.session_state:
        del st.session_state.desafio_inter_acertos
    if 'desafio_inter_indice' in st.session_state:
        del st.session_state.desafio_inter_indice
    # 🔥 LIMPAR EQUIPES
    if 'equipe_questoes' in st.session_state:
        del st.session_state.equipe_questoes
    if 'equipe_indice' in st.session_state:
        del st.session_state.equipe_indice
    if 'equipe_acertos' in st.session_state:
        del st.session_state.equipe_acertos
    if 'equipe_tentativas' in st.session_state:
        del st.session_state.equipe_tentativas
    if 'equipe_atual_id' in st.session_state:
        del st.session_state.equipe_atual_id
    # 🔥 LIMPAR CASOS PBL
    if 'caso_atual' in st.session_state:
        del st.session_state.caso_atual
    if 'caso_etapa' in st.session_state:
        del st.session_state.caso_etapa
    if 'caso_resposta' in st.session_state:
        del st.session_state.caso_resposta
    # 🔥 LIMPAR ALGORITMO
    if 'algoritmo_etapa' in st.session_state:
        del st.session_state.algoritmo_etapa
    if 'algoritmo_passos' in st.session_state:
        del st.session_state.algoritmo_passos
    if 'algoritmo_noticia' in st.session_state:
        del st.session_state.algoritmo_noticia
    # 🔥 LIMPAR DISSECAÇÃO
    if 'disseca_curtidas' in st.session_state:
        del st.session_state.disseca_curtidas
    if 'disseca_etapa' in st.session_state:
        del st.session_state.disseca_etapa
    if 'disseca_conclusao' in st.session_state:
        del st.session_state.disseca_conclusao
    # 🔥 LIMPAR DEBATE
    if 'debate_indice' in st.session_state:
        del st.session_state.debate_indice
    if 'debate_acertos' in st.session_state:
        del st.session_state.debate_acertos
    if 'debate_tentativas' in st.session_state:
        del st.session_state.debate_tentativas
    if 'debate_classificacoes' in st.session_state:
        del st.session_state.debate_classificacoes
    # 🔥 LIMPAR CANCELAMENTO
    if 'caso_cancelamento' in st.session_state:
        del st.session_state.caso_cancelamento
    if 'opiniao_cancelamento' in st.session_state:
        del st.session_state.opiniao_cancelamento
    # 🔥 LIMPAR JÚRI
    if 'caso_juri' in st.session_state:
        del st.session_state.caso_juri
    if 'papel_juri' in st.session_state:
        del st.session_state.papel_juri
    if 'argumento_juri' in st.session_state:
        del st.session_state.argumento_juri
    
    # 🔥 RECARREGAR
    st.rerun()
    st.stop()   

# ========== INÍCIO ==========
if menu == "🏠 Início":
    st.title("💡 Bem-vindo, Investigador Digital!")
    
    resetar_missoes()
    
    col1, col2 = st.columns(2)
    with col1:
        # 🔥 SELECIONAR TURMA
        turma = st.selectbox(
            "🏫 Escolha sua turma:",
            ["6º Ano - Anfitrião", "7º Ano - Visitante", "8º Ano - Visitante", "9º Ano - Visitante"],
            index=["6º Ano - Anfitrião", "7º Ano - Visitante", "8º Ano - Visitante", "9º Ano - Visitante"].index(st.session_state.turma) if st.session_state.turma in ["6º Ano - Anfitrião", "7º Ano - Visitante", "8º Ano - Visitante", "9º Ano - Visitante"] else 0,
            key="turma_inicio"
        )
        
        # 🔥 DETECTAR TROCA DE TURMA
        if turma != st.session_state.turma:
            st.session_state.turma = turma
            # Limpar questões embaralhadas ao trocar de turma
            if 'questoes_fake_embaralhadas' in st.session_state:
                del st.session_state.questoes_fake_embaralhadas
            if 'questoes_cyber_embaralhadas' in st.session_state:
                del st.session_state.questoes_cyber_embaralhadas
            if 'questoes_etica_embaralhadas' in st.session_state:
                del st.session_state.questoes_etica_embaralhadas
    
    with col2:
        # 🔥 SELECIONAR NOME DA LISTA DE ALUNOS DA TURMA
        alunos_turma = buscar_alunos_por_turma(st.session_state.turma)
        nomes_alunos = [aluno['nome'] for aluno in alunos_turma] if alunos_turma else []
        
        if nomes_alunos:
            # 🔥 DESCOBRIR O ÍNDICE DO ALUNO ATUAL
            if st.session_state.nome in nomes_alunos:
                indice_atual = nomes_alunos.index(st.session_state.nome)
            else:
                indice_atual = 0
    
            nome_selecionado = st.selectbox(
                "👤 Selecione seu nome:",
                nomes_alunos,
                index=indice_atual   # ← 🔥 USA O ÍNDICE DO ALUNO ATUAL
            )
            
            # 🔥 DETECTAR TROCA DE ALUNO
            if nome_selecionado != st.session_state.nome:
                st.session_state.nome = nome_selecionado
                
                # 🔥 RESETAR PONTOS AO TROCAR DE ALUNO
                st.session_state.pontos = 0
                st.session_state.total = 0
                st.session_state.fake_acertos = 0
                st.session_state.cyber_acertos = 0
                st.session_state.etica_acertos = 0
                st.session_state.indice_fake = 0
                st.session_state.indice_cyber = 0
                st.session_state.indice_etica = 0
                st.session_state.missoes = {"fake": 0, "cyber": 0, "etica": 0, "total": 0}
                
                # Limpar questões embaralhadas
                if 'questoes_fake_embaralhadas' in st.session_state:
                    del st.session_state.questoes_fake_embaralhadas
                if 'questoes_cyber_embaralhadas' in st.session_state:
                    del st.session_state.questoes_cyber_embaralhadas
                if 'questoes_etica_embaralhadas' in st.session_state:
                    del st.session_state.questoes_etica_embaralhadas
                
                st.success(f"✅ Bem-vindo(a), {st.session_state.nome}! Seus pontos foram zerados.")
                st.rerun()
        else:
            st.warning("📭 Nenhum aluno cadastrado nesta turma.")
            st.caption("💡 Cadastre alunos na página **👥 Lista de Alunos**")
            nome_selecionado = None
    
    if st.session_state.turma:
        st.info(f"📌 Turma selecionada: **{st.session_state.turma}**")
    
    if st.session_state.nome:
        st.success(f"👤 Aluno: **{st.session_state.nome}**")
        st.write(f"⭐ Pontos: **{st.session_state.pontos}**")
    
    # ========== LISTA DE ALUNOS DA TURMA ==========
    if st.session_state.turma:
        st.divider()
        st.subheader(f"👥 Alunos da {st.session_state.turma}")
        
        alunos_turma = buscar_alunos_por_turma(st.session_state.turma)
        if alunos_turma:
            col1, col2 = st.columns(2)
            for i, aluno in enumerate(alunos_turma):
                with col1 if i % 2 == 0 else col2:
                    destaque = "🌟" if aluno['nome'] == st.session_state.nome else "👤"
                    st.write(f"{destaque} {aluno['nome']} - ⭐ {aluno['pontos']} pts")
        else:
            st.info("📭 Nenhum aluno cadastrado nesta turma ainda.")
    
    st.divider()
    
    st.markdown("### 🎯 Progresso do Dia")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("📰 Fake News", f"{st.session_state.missoes['fake']}/5")
    with col2:
        st.metric("🛡️ Cyberbullying", f"{st.session_state.missoes['cyber']}/5")
    with col3:
        st.metric("⚖️ Ética", f"{st.session_state.missoes['etica']}/3")
    
    # ========== CAMPEÃO DA TURMA ==========
    if st.session_state.turma:
        st.divider()
        st.subheader(f"🏆 Campeão da {st.session_state.turma}")
        
        alunos_turma = buscar_alunos_por_turma(st.session_state.turma)
        if alunos_turma:
            campeao = alunos_turma[0]
            st.markdown(f"""
            <div style='text-align: center; padding: 20px; background: linear-gradient(135deg, #ffd700, #ffed4a); border-radius: 15px;'>
                <h1>👑 {campeao['nome']}</h1>
                <h2>⭐ {campeao['pontos']} pontos</h2>
                <p>🏆 Campeão da turma!</p>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.info("📭 Cadastre alunos para ter um campeão!")

# ========== FAKE NEWS ==========
elif menu == "📰 Fake News":
    st.title("📰 Detector de Fake News")

    mostrar_aluno_atual_e_proximo()   # 🔥 ADICIONE AQUI!
    st.divider()
    
    st.info(f"📌 Turma atual: **{st.session_state.turma}**")
    
    turma_atual = st.session_state.turma
    if not turma_atual:
        turma_atual = "6º Ano - Anfitrião"
    
    if 'questoes_fake_embaralhadas' not in st.session_state:
        # 🔥 BUSCAR PERGUNTAS DE "fake" + "mat_fake"
        questoes_fake = buscar_questoes_por_categoria(turma_atual, "fake")
        questoes_mat = buscar_questoes_por_categoria(turma_atual, "mat_fake")
        
        # 🔥 JUNTAR E EMBARALHAR
        todas = questoes_fake + questoes_mat
        import random
        random.shuffle(todas)
        
        st.session_state.questoes_fake_embaralhadas = todas
    
    questoes = st.session_state.questoes_fake_embaralhadas
    
    if not questoes:
        st.warning(f"⚠️ Nenhuma questão encontrada para a turma {turma_atual}")
        questoes = buscar_questoes_embaralhadas("6º Ano - Anfitrião", "fake")
        st.session_state.questoes_fake_embaralhadas = questoes
    
    if not questoes:
        st.error("❌ Nenhuma questão encontrada no banco de dados!")
        st.stop()
    
    if 'tentativas_fake' not in st.session_state:
        st.session_state.tentativas_fake = 0
    
        # 🔥 VERIFICAR SE JÁ TERMINOU
    if st.session_state.tentativas_fake >= 5:
        st.success("🎉 Você completou as 5 perguntas de Fake News!")
        st.write(f"📊 Acertos: {st.session_state.fake_acertos} de 5")
        
        if st.session_state.fake_acertos >= 5:
            st.balloons()
            tocar_som("vitoria")
            st.success("🎉 PARABÉNS! VOCÊ ACERTOU TODAS AS 5 PERGUNTAS! 🎉")
        elif st.session_state.fake_acertos >= 3:
            st.info("⭐ Muito bem! Você foi ótimo!")
        else:
            st.info("💪 Continue praticando! Você vai melhorar!")
        
        if st.button("🔄 Jogar Novamente", key="fake_jogar_novamente"):
            st.session_state.tentativas_fake = 0
            st.session_state.indice_fake = 0
            st.session_state.fake_acertos = 0
            st.session_state.questoes_fake_embaralhadas = buscar_questoes_embaralhadas(turma_atual, "fake")
            st.rerun()
        st.stop()   
    
    if st.session_state.indice_fake >= len(questoes):
        st.session_state.indice_fake = 0
    
    p = questoes[st.session_state.indice_fake]
    
    st.markdown(f"### Pergunta {st.session_state.tentativas_fake + 1} de 5")
    st.markdown(f"**{p['pergunta']}**")
    
    opcao = st.selectbox("📌 Escolha uma opção:", ["Selecione", "Verdade", "Fake"], key="fake")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("✅ Verificar", key="fake_ver"):
            if opcao == "Selecione":
                st.warning("⚠️ Selecione uma opção!")
            else:
                st.session_state.tentativas_fake += 1
                st.session_state.total += 1
                
                if opcao == p['resposta']:
                    st.success(f"✅ ACERTOU! +1 ponto")
                    tocar_som("acerto")
                    if p.get('explicacao'):
                        st.info(f"💡 {p['explicacao']}")
                    st.session_state.pontos += 1
                    st.session_state.fake_acertos += 1
                    st.session_state.missoes["fake"] += 1
                    st.session_state.missoes["total"] += 1
                else:
                    st.error(f"❌ ERROU! A resposta é: {p['resposta']}")
                    
                    # 🔥 SÓ TOCA "ERRO" SE NÃO FOR A ÚLTIMA PERGUNTA
                    if st.session_state.tentativas_fake < 5:
                        tocar_som("erro")
                    
                    if p.get('explicacao'):
                        st.info(f"💡 {p['explicacao']}")
                    st.session_state.missoes["fake"] += 1
                    st.session_state.missoes["total"] += 1
                
                if st.session_state.nome and st.session_state.turma:
                    salvar_aluno(
                        st.session_state.nome,
                        st.session_state.turma,
                        pontos=st.session_state.pontos,
                        fake_acertos=st.session_state.fake_acertos,
                        cyber_acertos=st.session_state.cyber_acertos,
                        etica_acertos=st.session_state.etica_acertos,
                        total_perguntas=st.session_state.total
                    )
    
    with col2:
        if st.button("➡️ SEGUINTE", key="fake_prox"):
            st.session_state.indice_fake += 1
            if st.session_state.indice_fake >= len(questoes):
                st.session_state.indice_fake = 0
            st.rerun()
    
    with col3:
        if st.button("🔄 Reiniciar", key="fake_reset"):
            st.session_state.tentativas_fake = 0
            st.session_state.indice_fake = 0
            st.session_state.fake_acertos = 0
            st.session_state.questoes_fake_embaralhadas = buscar_questoes_embaralhadas(turma_atual, "fake")
            st.rerun()
    
    st.divider()
    st.write(f"📊 Tentativas: {st.session_state.tentativas_fake}/5 | ✅ Acertos: {st.session_state.fake_acertos}")
    
    # 🔥 PROGRESSO
    if st.session_state.tentativas_fake > 0:
        st.divider()
        st.subheader("🎯 Seu Progresso")
        
        col1, col2, col3, col4, col5 = st.columns(5)
        niveis = [(1, "🌟", "1"), (2, "⭐", "2"), (3, "🏅", "3"), (4, "🎖️", "4"), (5, "🏆", "5")]
        
        acertos = st.session_state.fake_acertos
        for i, (nivel, emoji, texto) in enumerate(niveis, 1):
            with col1 if i == 1 else col2 if i == 2 else col3 if i == 3 else col4 if i == 4 else col5:
                if acertos >= nivel:
                    st.markdown(f"""
                    <div style='text-align: center; padding: 10px; background: #28a745; border-radius: 10px; color: white;'>
                        <h2>{emoji}</h2>
                        <p>{texto}✅</p>
                    </div>
                    """, unsafe_allow_html=True)
                else:
                    st.markdown(f"""
                    <div style='text-align: center; padding: 10px; background: #e9ecef; border-radius: 10px; color: gray;'>
                        <h2>⬜</h2>
                        <p>{texto}</p>
                    </div>
                    """, unsafe_allow_html=True)
        
        mostrar_recompensa(acertos)

# ========== CYBERBULLYING ==========
elif menu == "🛡️ Cyberbullying":
    st.title("🛡️ Cyberbullying")

    mostrar_aluno_atual_e_proximo()   # 🔥 ADICIONE AQUI!
    st.divider()
    
    st.info(f"📌 Turma atual: **{st.session_state.turma}**")
    
    turma_atual = st.session_state.turma
    if not turma_atual:
        turma_atual = "6º Ano - Anfitrião"
    
    if 'questoes_cyber_embaralhadas' not in st.session_state:
        st.session_state.questoes_cyber_embaralhadas = buscar_questoes_embaralhadas(turma_atual, "cyber")
    
    questoes = st.session_state.questoes_cyber_embaralhadas
    
    if not questoes:
        st.warning(f"⚠️ Nenhuma questão encontrada para a turma {turma_atual}")
        questoes = buscar_questoes_embaralhadas("6º Ano - Anfitrião", "cyber")
        st.session_state.questoes_cyber_embaralhadas = questoes
    
    if not questoes:
        st.error("❌ Nenhuma questão encontrada no banco de dados!")
        st.stop()
    
    if 'tentativas_cyber' not in st.session_state:
        st.session_state.tentativas_cyber = 0
    
    if st.session_state.tentativas_cyber >= 5:
        st.success("🎉 Você completou as 5 perguntas de Cyberbullying!")
        st.write(f"📊 Acertos: {st.session_state.cyber_acertos} de 5")
        
    if st.session_state.tentativas_cyber >= 5:
        st.success("🎉 Você completou as 5 perguntas de Cyberbullying!")
        st.write(f"📊 Acertos: {st.session_state.cyber_acertos} de 5")
        
        if st.session_state.cyber_acertos >= 5:
            st.balloons()
            tocar_som("vitoria")
            st.success("🎉 PARABÉNS! VOCÊ ACERTOU TODAS AS 5 PERGUNTAS! 🎉")
        elif st.session_state.cyber_acertos >= 3:
            st.info("⭐ Muito bem! Você foi ótimo!")
        else:
            st.info("💪 Continue praticando! Você vai melhorar!")
        
        if st.button("🔄 Jogar Novamente", key="cyber_jogar_novamente"):
            st.session_state.tentativas_cyber = 0
            st.session_state.indice_cyber = 0
            st.session_state.cyber_acertos = 0
            st.session_state.questoes_cyber_embaralhadas = buscar_questoes_embaralhadas(turma_atual, "cyber")
            st.rerun()
        st.stop()
    
    if st.session_state.indice_cyber >= len(questoes):
        st.session_state.indice_cyber = 0
    
    p = questoes[st.session_state.indice_cyber]
    
    st.markdown(f"### Pergunta {st.session_state.tentativas_cyber + 1} de 5")
    st.markdown(f"**{p['pergunta']}**")
    
    opcao = st.selectbox("📌 Escolha uma opção:", ["Selecione", "Sim", "Não"], key="cyber")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("🛡️ Verificar", key="cyber_ver"):
            if opcao == "Selecione":
                st.warning("⚠️ Selecione uma opção!")
            else:
                st.session_state.tentativas_cyber += 1
                st.session_state.total += 1
                
                if opcao == p['resposta']:
                    st.success(f"✅ ACERTOU! +1 ponto")
                    tocar_som("acerto")
                    if p.get('explicacao'):
                        st.info(f"💡 {p['explicacao']}")
                    st.session_state.pontos += 1
                    st.session_state.cyber_acertos += 1
                    st.session_state.missoes["cyber"] += 1
                    st.session_state.missoes["total"] += 1
                else:
                    st.error(f"❌ ERROU! A resposta é: {p['resposta']}")
                    tocar_som("erro")
                    if p.get('explicacao'):
                        st.info(f"💡 {p['explicacao']}")
                    st.session_state.missoes["cyber"] += 1
                    st.session_state.missoes["total"] += 1
                
                if st.session_state.nome and st.session_state.turma:
                    salvar_aluno(
                        st.session_state.nome,
                        st.session_state.turma,
                        pontos=st.session_state.pontos,
                        fake_acertos=st.session_state.fake_acertos,
                        cyber_acertos=st.session_state.cyber_acertos,
                        etica_acertos=st.session_state.etica_acertos,
                        total_perguntas=st.session_state.total
                    )
    
    with col2:
        if st.button("➡️ SEGUINTE", key="cyber_prox"):
            st.session_state.indice_cyber += 1
            if st.session_state.indice_cyber >= len(questoes):
                st.session_state.indice_cyber = 0
            st.rerun()
    
    with col3:
        if st.button("🔄 Reiniciar", key="cyber_reset"):
            st.session_state.tentativas_cyber = 0
            st.session_state.indice_cyber = 0
            st.session_state.cyber_acertos = 0
            st.session_state.questoes_cyber_embaralhadas = buscar_questoes_embaralhadas(turma_atual, "cyber")
            st.rerun()
    
    st.divider()
    st.write(f"📊 Tentativas: {st.session_state.tentativas_cyber}/5 | ✅ Acertos: {st.session_state.cyber_acertos}")
    
    if st.session_state.tentativas_cyber > 0:
        st.divider()
        st.subheader("🎯 Seu Progresso")
        
        col1, col2, col3, col4, col5 = st.columns(5)
        niveis = [(1, "🌟", "1"), (2, "⭐", "2"), (3, "🏅", "3"), (4, "🎖️", "4"), (5, "🏆", "5")]
        
        acertos = st.session_state.cyber_acertos
        for i, (nivel, emoji, texto) in enumerate(niveis, 1):
            with col1 if i == 1 else col2 if i == 2 else col3 if i == 3 else col4 if i == 4 else col5:
                if acertos >= nivel:
                    st.markdown(f"""
                    <div style='text-align: center; padding: 10px; background: #28a745; border-radius: 10px; color: white;'>
                        <h2>{emoji}</h2>
                        <p>{texto}✅</p>
                    </div>
                    """, unsafe_allow_html=True)
                else:
                    st.markdown(f"""
                    <div style='text-align: center; padding: 10px; background: #e9ecef; border-radius: 10px; color: gray;'>
                        <h2>⬜</h2>
                        <p>{texto}</p>
                    </div>
                    """, unsafe_allow_html=True)
        
        mostrar_recompensa(acertos)

# ========== ÉTICA DIGITAL ==========
elif menu == "⚖️ Ética Digital":
    st.title("⚖️ Ética Digital")

    mostrar_aluno_atual_e_proximo()   # 🔥 ADICIONE AQUI!
    st.divider()
    
    st.info(f"📌 Turma atual: **{st.session_state.turma}**")
    
    turma_atual = st.session_state.turma
    if not turma_atual:
        turma_atual = "6º Ano - Anfitrião"
    
    if 'questoes_etica_embaralhadas' not in st.session_state:
        st.session_state.questoes_etica_embaralhadas = buscar_questoes_embaralhadas(turma_atual, "etica")
    
    questoes = st.session_state.questoes_etica_embaralhadas
    
    if not questoes:
        st.warning(f"⚠️ Nenhuma questão encontrada para a turma {turma_atual}")
        questoes = buscar_questoes_embaralhadas("6º Ano - Anfitrião", "etica")
        st.session_state.questoes_etica_embaralhadas = questoes
    
    if not questoes:
        st.error("❌ Nenhuma questão encontrada no banco de dados!")
        st.stop()
    
    if 'tentativas_etica' not in st.session_state:
        st.session_state.tentativas_etica = 0
    
    if st.session_state.tentativas_etica >= 3:
        st.success("🎉 Você completou as 3 perguntas de Ética Digital!")
        st.write(f"📊 Acertos: {st.session_state.etica_acertos} de 3")
        
        if st.session_state.etica_acertos >= 3:
            st.balloons()
            tocar_som("vitoria")
            st.success("🎉 PARABÉNS! VOCÊ ACERTOU TODAS AS 3 PERGUNTAS! 🎉")
        elif st.session_state.etica_acertos >= 2:
            st.info("⭐ Muito bem! Você foi ótimo!")
        else:
            st.info("💪 Continue praticando! Você vai melhorar!")
        
        if st.button("🔄 Jogar Novamente", key="etica_jogar_novamente"):
            st.session_state.tentativas_etica = 0
            st.session_state.indice_etica = 0
            st.session_state.etica_acertos = 0
            st.session_state.questoes_etica_embaralhadas = buscar_questoes_embaralhadas(turma_atual, "etica")
            st.rerun()
        st.stop()
    
    if st.session_state.indice_etica >= len(questoes):
        st.session_state.indice_etica = 0
    
    p = questoes[st.session_state.indice_etica]
    
    st.markdown(f"### Pergunta {st.session_state.tentativas_etica + 1} de 3")
    st.markdown(f"**{p['pergunta']}**")
    
    opcoes = []
    for i in range(1, 5):
        opcao_key = f"opcao{i}"
        if p.get(opcao_key):
            opcoes.append(p[opcao_key])
    
    opcao = st.selectbox("📌 Escolha uma opção:", opcoes, key="etica")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("⚖️ Verificar", key="etica_ver"):
            if opcao == "Selecione":
                st.warning("⚠️ Selecione uma opção!")
            else:
                st.session_state.tentativas_etica += 1
                st.session_state.total += 1
                
                # 🔥 Aceita tanto 'correta' quanto 'resposta'
                resposta_correta = p.get('correta') or p.get('resposta')
                
                if opcao == resposta_correta:
                    st.success(f"✅ DECISÃO CERTA! +1 ponto")
                    tocar_som("acerto")
                    if p.get('explicacao'):
                        st.info(f"💡 {p['explicacao']}")
                    st.session_state.pontos += 1
                    st.session_state.etica_acertos += 1
                    st.session_state.missoes["etica"] += 1
                    st.session_state.missoes["total"] += 1
                else:
                    st.error(f"❌ DECISÃO ERRADA! A correta é: {resposta_correta}")
                    tocar_som("erro")
                    if p.get('explicacao'):
                        st.info(f"💡 {p['explicacao']}")
                    st.session_state.missoes["etica"] += 1
                    st.session_state.missoes["total"] += 1
                
                if st.session_state.nome and st.session_state.turma:
                    salvar_aluno(
                        st.session_state.nome,
                        st.session_state.turma,
                        pontos=st.session_state.pontos,
                        fake_acertos=st.session_state.fake_acertos,
                        cyber_acertos=st.session_state.cyber_acertos,
                        etica_acertos=st.session_state.etica_acertos,
                        total_perguntas=st.session_state.total
                    )
    
    with col2:
        if st.button("➡️ SEGUINTE", key="etica_prox"):
            st.session_state.indice_etica += 1
            if st.session_state.indice_etica >= len(questoes):
                st.session_state.indice_etica = 0
            st.rerun()
    
    with col3:
        if st.button("🔄 Reiniciar", key="etica_reset"):
            st.session_state.tentativas_etica = 0
            st.session_state.indice_etica = 0
            st.session_state.etica_acertos = 0
            st.session_state.questoes_etica_embaralhadas = buscar_questoes_embaralhadas(turma_atual, "etica")
            st.rerun()
    
    st.divider()
    st.write(f"📊 Tentativas: {st.session_state.tentativas_etica}/3 | ✅ Acertos: {st.session_state.etica_acertos}")
    
    if st.session_state.tentativas_etica > 0:
        st.divider()
        st.subheader("🎯 Seu Progresso")
        
        col1, col2, col3 = st.columns(3)
        niveis = [(1, "🌟", "1"), (2, "⭐", "2"), (3, "🏅", "3")]
        
        acertos = st.session_state.etica_acertos
        for i, (nivel, emoji, texto) in enumerate(niveis, 1):
            with col1 if i == 1 else col2 if i == 2 else col3:
                if acertos >= nivel:
                    st.markdown(f"""
                    <div style='text-align: center; padding: 10px; background: #28a745; border-radius: 10px; color: white;'>
                        <h2>{emoji}</h2>
                        <p>{texto}✅</p>
                    </div>
                    """, unsafe_allow_html=True)
                else:
                    st.markdown(f"""
                    <div style='text-align: center; padding: 10px; background: #e9ecef; border-radius: 10px; color: gray;'>
                        <h2>⬜</h2>
                        <p>{texto}</p>
                    </div>
                    """, unsafe_allow_html=True)
        
        mostrar_recompensa(acertos)

# ========== BADGES ==========
elif menu == "🎖️ Badges":
    st.title("🎖️ Meus Selos (Badges)")
    
    badges = verificar_badges()
    
    if badges:
        tocar_som("badge")      # 🔊 SOM DE BADGE
        st.balloons()           # 🎈 BALÕES
        st.markdown("### 🏆 Selos Conquistados:")
        col1, col2 = st.columns(2)
        for i, (nome, cor) in enumerate(badges):
            with col1 if i % 2 == 0 else col2:
                st.markdown(f'<div class="badge badge-{cor}">{nome}</div>', unsafe_allow_html=True)
    else:
        st.info("💪 Continue respondendo perguntas para ganhar selos!")
    
    st.divider()
    
    st.markdown("### 📋 Como ganhar selos:")
    st.markdown("- 📰 **Detetive da Verdade** → 5 acertos em Fake News")
    st.markdown("- 🛡️ **Guardião Ético** → 5 acertos em Cyberbullying")
    st.markdown("- ⚖️ **Mestre da Ética** → 3 acertos em Ética Digital")
    st.markdown("- ⭐ **Investigador Júnior** → 10 pontos")
    st.markdown("- 🏆 **Investigador Master** → 20 pontos")
    st.markdown("- 🎯 **Caçador de Missões** → 10 missões concluídas")

# ========== RANKING ==========
elif menu == "🏆 Ranking":
    st.title("🏆 Ranking")
    
    tab1, tab2 = st.tabs(["🏆 Geral", "🏫 Por Turma"])
    
    # ========== RANKING GERAL ==========
    with tab1:
        st.subheader("🏆 Ranking Geral dos Alunos")
        
        ranking = buscar_ranking_geral()
        
        if ranking:
            for i, aluno in enumerate(ranking, 1):
                # Medalhas para os 3 primeiros
                if i == 1:
                    medalha = "🥇"
                    cor = "#ffd700"
                elif i == 2:
                    medalha = "🥈"
                    cor = "#c0c0c0"
                elif i == 3:
                    medalha = "🥉"
                    cor = "#cd7f32"
                else:
                    medalha = f"{i}º"
                    cor = "#f8f9fa"
                
                st.markdown(f"""
                <div style='padding: 10px; margin: 5px 0; background: {cor}; border-radius: 10px;'>
                    <h4>{medalha} {aluno['nome']} - {aluno['turma']}</h4>
                    <p>⭐ {aluno['pontos']} pontos | 📰 {aluno['fake_acertos']} | 🛡️ {aluno['cyber_acertos']} | ⚖️ {aluno['etica_acertos']}</p>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.info("📭 Nenhum aluno cadastrado ainda.")
    
    # ========== RANKING POR TURMA ==========
    with tab2:
        st.subheader("🏫 Ranking das Turmas")
        
        ranking_turmas = buscar_ranking_turmas()
        
        if ranking_turmas:
            for i, turma in enumerate(ranking_turmas, 1):
                # Medalhas para as 3 primeiras
                if i == 1:
                    medalha = "🥇"
                    cor = "#ffd700"
                elif i == 2:
                    medalha = "🥈"
                    cor = "#c0c0c0"
                elif i == 3:
                    medalha = "🥉"
                    cor = "#cd7f32"
                else:
                    medalha = f"{i}º"
                    cor = "#f8f9fa"
                
                st.markdown(f"""
                <div style='padding: 15px; margin: 10px 0; background: {cor}; border-radius: 10px;'>
                    <h3>{medalha} {turma['turma']}</h3>
                    <p>⭐ <strong>{turma['total_pontos']}</strong> pontos totais</p>
                    <p>👥 {turma['total_alunos']} alunos | 📊 Média: {turma['media_pontos']:.1f} pontos</p>
                    <p>📰 {turma['total_fake']} | 🛡️ {turma['total_cyber']} | ⚖️ {turma['total_etica']}</p>
                </div>
                """, unsafe_allow_html=True)
            
            st.divider()
            
            # ========== GRÁFICO COMPARATIVO ==========
            st.subheader("📊 Comparativo entre Turmas")
            
            import pandas as pd
            
            dados_grafico = pd.DataFrame([
                {"Turma": t['turma'], "Pontos": t['total_pontos']}
                for t in ranking_turmas
            ])
            st.bar_chart(dados_grafico.set_index('Turma'))
            
            # ========== ESTATÍSTICAS ==========
            st.divider()
            st.subheader("📈 Estatísticas Gerais")
            
            total_alunos = sum([t['total_alunos'] for t in ranking_turmas])
            total_pontos = sum([t['total_pontos'] for t in ranking_turmas])
            
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("👥 Total de Alunos", total_alunos)
            with col2:
                st.metric("⭐ Total de Pontos", total_pontos)
            with col3:
                media_geral = total_pontos / total_alunos if total_alunos > 0 else 0
                st.metric("📊 Média Geral", f"{media_geral:.1f}")
        else:
            st.info("📭 Nenhuma turma com alunos cadastrados ainda.")

# ========== MISSÕES DIÁRIAS ==========
elif menu == "🎯 Missões Diárias":
    st.title("🎯 Missões Diárias")
    
    resetar_missoes()
    
    st.markdown("""
    <div class="card card-mission">
        <h4>🎯 DESAFIOS DO DIA</h4>
        <p>Complete as missões diárias e ganhe pontos extras!</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.divider()
    
    # ========== PROGRESSO ==========
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown('<div class="mission-card"><h4>📰 Fake News</h4><p>Responda 5 perguntas</p></div>', unsafe_allow_html=True)
        progresso = min(st.session_state.missoes["fake"] / 5 * 100, 100)
        st.markdown(f"""
        <div class="progress-bar">
            <div class="progress-fill" style="width: {progresso}%;">{st.session_state.missoes["fake"]}/5</div>
        </div>
        """, unsafe_allow_html=True)
        if st.session_state.missoes["fake"] >= 5:
            st.success("✅ Concluída!")
    
    with col2:
        st.markdown('<div class="mission-card"><h4>🛡️ Cyberbullying</h4><p>Responda 5 perguntas</p></div>', unsafe_allow_html=True)
        progresso = min(st.session_state.missoes["cyber"] / 5 * 100, 100)
        st.markdown(f"""
        <div class="progress-bar">
            <div class="progress-fill" style="width: {progresso}%;">{st.session_state.missoes["cyber"]}/5</div>
        </div>
        """, unsafe_allow_html=True)
        if st.session_state.missoes["cyber"] >= 5:
            st.success("✅ Concluída!")
    
    with col3:
        st.markdown('<div class="mission-card"><h4>⚖️ Ética Digital</h4><p>Responda 3 perguntas</p></div>', unsafe_allow_html=True)
        progresso = min(st.session_state.missoes["etica"] / 3 * 100, 100)
        st.markdown(f"""
        <div class="progress-bar">
            <div class="progress-fill" style="width: {progresso}%;">{st.session_state.missoes["etica"]}/3</div>
        </div>
        """, unsafe_allow_html=True)
        if st.session_state.missoes["etica"] >= 3:
            st.success("✅ Concluída!")
    
    st.divider()
    
    # ========== ESCOLHER MISSÃO ==========
    st.subheader("🎯 Escolha uma Missão para Começar")
    
    missao = st.radio(
        "Qual missão você quer fazer agora?",
        ["📰 Fake News (5 perguntas)", "🛡️ Cyberbullying (5 perguntas)", "⚖️ Ética Digital (3 perguntas)"],
        key="missao_escolhida"
    )
    
    st.divider()
    
    # ========== MISSÃO: FAKE NEWS ==========
    if missao == "📰 Fake News (5 perguntas)":
        st.subheader("📰 Missão: Fake News")
        
        turma_atual = st.session_state.turma or "6º Ano - Anfitrião"
        
        if 'missoes_fake_questoes' not in st.session_state:
            import random
            questoes = buscar_questoes_por_categoria(turma_atual, "fake")
            if questoes:
                random.seed(st.session_state.nome)
                random.shuffle(questoes)
                st.session_state.missoes_fake_questoes = questoes
        
        questoes = st.session_state.missoes_fake_questoes
        
        if not questoes:
            st.warning("⚠️ Nenhuma pergunta encontrada.")
            st.stop()
        
        if 'missoes_fake_indice' not in st.session_state:
            st.session_state.missoes_fake_indice = 0
        
        # Verificar se completou
        if st.session_state.missoes["fake"] >= 5:
            st.success("🎉 Missão concluída! +2 pontos")
            if st.button("🔄 Jogar Novamente", key="missoes_fake_reiniciar"):
                st.session_state.missoes["fake"] = 0
                st.session_state.missoes_fake_indice = 0
                if 'missoes_fake_questoes' in st.session_state:
                    del st.session_state.missoes_fake_questoes
                st.rerun()
            st.stop()
        
        p = questoes[st.session_state.missoes_fake_indice % len(questoes)]
        
        st.markdown(f"**Pergunta {st.session_state.missoes['fake'] + 1} de 5**")
        st.markdown(f"**{p['pergunta']}**")
        
        opcao = st.selectbox("📌 Escolha:", ["Selecione", "Verdade", "Fake"], key="missoes_fake_opcao")
        
        if st.button("✅ Verificar", key="missoes_fake_verificar"):
            if opcao == "Selecione":
                st.warning("⚠️ Selecione uma opção!")
            else:
                if opcao == p['resposta']:
                    tocar_som("acerto")
                    st.success("✅ ACERTOU! +1 ponto")
                    if p.get('explicacao'):
                        st.info(f"💡 {p['explicacao']}")
                    st.session_state.pontos += 1
                    st.session_state.fake_acertos += 1
                    st.session_state.missoes["fake"] += 1
                    st.session_state.missoes["total"] += 1
                else:
                    tocar_som("erro")
                    st.error(f"❌ ERROU! A resposta é: {p['resposta']}")
                    if p.get('explicacao'):
                        st.info(f"💡 {p['explicacao']}")
                    st.session_state.missoes["fake"] += 1
                    st.session_state.missoes["total"] += 1
                
                st.session_state.missoes_fake_indice += 1
                st.rerun()
    
    # ========== MISSÃO: CYBERBULLYING ==========
    elif missao == "🛡️ Cyberbullying (5 perguntas)":
        st.subheader("🛡️ Missão: Cyberbullying")
        
        turma_atual = st.session_state.turma or "6º Ano - Anfitrião"
        
        if 'missoes_cyber_questoes' not in st.session_state:
            import random
            questoes = buscar_questoes_por_categoria(turma_atual, "cyber")
            if questoes:
                random.seed(st.session_state.nome)
                random.shuffle(questoes)
                st.session_state.missoes_cyber_questoes = questoes
        
        questoes = st.session_state.missoes_cyber_questoes
        
        if not questoes:
            st.warning("⚠️ Nenhuma pergunta encontrada.")
            st.stop()
        
        if 'missoes_cyber_indice' not in st.session_state:
            st.session_state.missoes_cyber_indice = 0
        
        if st.session_state.missoes["cyber"] >= 5:
            st.success("🎉 Missão concluída! +2 pontos")
            if st.button("🔄 Jogar Novamente", key="missoes_cyber_reiniciar"):
                st.session_state.missoes["cyber"] = 0
                st.session_state.missoes_cyber_indice = 0
                if 'missoes_cyber_questoes' in st.session_state:
                    del st.session_state.missoes_cyber_questoes
                st.rerun()
            st.stop()
        
        p = questoes[st.session_state.missoes_cyber_indice % len(questoes)]
        
        st.markdown(f"**Pergunta {st.session_state.missoes['cyber'] + 1} de 5**")
        st.markdown(f"**{p['pergunta']}**")
        
        opcao = st.selectbox("📌 Escolha:", ["Selecione", "Sim", "Não"], key="missoes_cyber_opcao")
        
        if st.button("✅ Verificar", key="missoes_cyber_verificar"):
            if opcao == "Selecione":
                st.warning("⚠️ Selecione uma opção!")
            else:
                if opcao == p['resposta']:
                    tocar_som("acerto")
                    st.success("✅ ACERTOU! +1 ponto")
                    if p.get('explicacao'):
                        st.info(f"💡 {p['explicacao']}")
                    st.session_state.pontos += 1
                    st.session_state.cyber_acertos += 1
                    st.session_state.missoes["cyber"] += 1
                    st.session_state.missoes["total"] += 1
                else:
                    tocar_som("erro")
                    st.error(f"❌ ERROU! A resposta é: {p['resposta']}")
                    if p.get('explicacao'):
                        st.info(f"💡 {p['explicacao']}")
                    st.session_state.missoes["cyber"] += 1
                    st.session_state.missoes["total"] += 1
                
                st.session_state.missoes_cyber_indice += 1
                st.rerun()
    
    # ========== MISSÃO: ÉTICA DIGITAL ==========
    elif missao == "⚖️ Ética Digital (3 perguntas)":
        st.subheader("⚖️ Missão: Ética Digital")
        
        turma_atual = st.session_state.turma or "6º Ano - Anfitrião"
        
        if 'missoes_etica_questoes' not in st.session_state:
            import random
            questoes = buscar_questoes_por_categoria(turma_atual, "etica")
            if questoes:
                random.seed(st.session_state.nome)
                random.shuffle(questoes)
                st.session_state.missoes_etica_questoes = questoes
        
        questoes = st.session_state.missoes_etica_questoes
        
        if not questoes:
            st.warning("⚠️ Nenhuma pergunta encontrada.")
            st.stop()
        
        if 'missoes_etica_indice' not in st.session_state:
            st.session_state.missoes_etica_indice = 0
        
        if st.session_state.missoes["etica"] >= 3:
            st.success("🎉 Missão concluída! +2 pontos")
            if st.button("🔄 Jogar Novamente", key="missoes_etica_reiniciar"):
                st.session_state.missoes["etica"] = 0
                st.session_state.missoes_etica_indice = 0
                if 'missoes_etica_questoes' in st.session_state:
                    del st.session_state.missoes_etica_questoes
                st.rerun()
            st.stop()
        
        p = questoes[st.session_state.missoes_etica_indice % len(questoes)]
        
        st.markdown(f"**Pergunta {st.session_state.missoes['etica'] + 1} de 3**")
        st.markdown(f"**{p['pergunta']}**")
        
        # Opções de ética
        opcoes = []
        for i in range(1, 5):
            opcao_key = f"opcao{i}"
            if p.get(opcao_key):
                opcoes.append(p[opcao_key])
        
        if not opcoes:
            opcoes = [p.get('resposta', '')]
        
        opcao = st.selectbox("📌 Escolha:", opcoes, key="missoes_etica_opcao")
        
        if st.button("✅ Verificar", key="missoes_etica_verificar"):
            resposta_correta = p.get('correta') or p.get('resposta')
            if opcao == resposta_correta:
                tocar_som("acerto")
                st.success("✅ ACERTOU! +1 ponto")
                if p.get('explicacao'):
                    st.info(f"💡 {p['explicacao']}")
                st.session_state.pontos += 1
                st.session_state.etica_acertos += 1
                st.session_state.missoes["etica"] += 1
                st.session_state.missoes["total"] += 1
            else:
                tocar_som("erro")
                st.error(f"❌ ERROU! A correta é: {resposta_correta}")
                if p.get('explicacao'):
                    st.info(f"💡 {p['explicacao']}")
                st.session_state.missoes["etica"] += 1
                st.session_state.missoes["total"] += 1
            
            st.session_state.missoes_etica_indice += 1
            st.rerun()
    
    st.divider()
    
    # ========== TOTAL ==========
    total_missoes = 0
    if st.session_state.missoes["fake"] >= 5:
        total_missoes += 1
    if st.session_state.missoes["cyber"] >= 5:
        total_missoes += 1
    if st.session_state.missoes["etica"] >= 3:
        total_missoes += 1
    
    st.metric("🎯 Missões Completas", f"{total_missoes}/3")
    
    if total_missoes == 3:
        st.balloons()
        tocar_som("vitoria")
        st.success("🏆 PARABÉNS! Você completou TODAS as missões do dia!")
        st.info("💡 Volte amanhã para novas missões!")
# ========== LISTA DE ALUNOS ==========
elif menu == "👥 Lista de Alunos":
    st.title("👥 Lista de Alunos por Turma")
    
    tab1, tab2, tab3 = st.tabs(["📋 Por Turma", "➕ Cadastrar Aluno", "📊 Todos"])
    
    with tab1:
        st.subheader("📋 Alunos por Turma")
        
        turmas = buscar_todas_turmas()
        if turmas:
            turma_selecionada = st.selectbox("Escolha a turma:", turmas)
            alunos = buscar_alunos_por_turma(turma_selecionada)
            
            if alunos:
                st.write(f"**Total: {len(alunos)} alunos**")
                for i, aluno in enumerate(alunos, 1):
                    col1, col2, col3, col4 = st.columns([2, 1, 1, 1])
                    with col1:
                        st.write(f"{i}º - **{aluno['nome']}**")
                    with col2:
                        st.write(f"⭐ {aluno['pontos']}")
                    with col3:
                        st.write(f"📰 {aluno['fake_acertos']}")
                    with col4:
                        if st.button(f"🗑️", key=f"del_{aluno['id']}"):
                            excluir_aluno(aluno['id'])
                            st.rerun()
                st.divider()
            else:
                st.info("📭 Nenhum aluno cadastrado nesta turma.")
        else:
            st.info("📭 Nenhuma turma cadastrada.")
    
    with tab2:
        st.subheader("➕ Cadastrar Aluno")
        
        with st.form("form_cadastro_aluno"):
            nome = st.text_input("👤 Nome do Aluno *")
            turma = st.selectbox("🏫 Turma", buscar_todas_turmas())
            
            submitted = st.form_submit_button("💾 Cadastrar")
            
            if submitted:
                if nome and turma:
                    salvar_aluno(nome, turma)
                    st.success(f"✅ Aluno {nome} cadastrado na turma {turma}!")
                    st.rerun()
                else:
                    st.error("❌ Preencha todos os campos!")
    
    with tab3:
        st.subheader("📊 Todos os Alunos")
        
        todos = buscar_todos_alunos()
        if todos:
            import pandas as pd
            df = pd.DataFrame(todos)
            st.dataframe(df[['id', 'nome', 'turma', 'pontos', 'fake_acertos', 'cyber_acertos', 'etica_acertos']], use_container_width=True)
            
            st.divider()
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Total de Alunos", len(todos))
            with col2:
                total_pontos = sum([a['pontos'] for a in todos])
                st.metric("Total de Pontos", total_pontos)
            with col3:
                media_pontos = total_pontos / len(todos) if todos else 0
                st.metric("Média de Pontos", f"{media_pontos:.1f}")
        else:
            st.info("📭 Nenhum aluno cadastrado.")

# ========== RELATÓRIO ==========
elif menu == "📊 Relatório":
    st.title("📊 Relatório de Desempenho")
    
    st.info("💡 Selecione um aluno para ver o relatório completo")
    
    # Buscar alunos
    todos_alunos = buscar_todos_alunos()
    
    if not todos_alunos:
        st.warning("📭 Nenhum aluno cadastrado ainda.")
        st.stop()
    
    # Criar lista de opções "Nome - Turma"
    opcoes = [f"{a['nome']} - {a['turma']}" for a in todos_alunos]
    
    col1, col2 = st.columns(2)
    with col1:
        aluno_selecionado = st.selectbox("👤 Escolha o aluno:", opcoes)
    
    if aluno_selecionado:
        # Separar nome e turma
        nome_aluno, turma_aluno = aluno_selecionado.split(" - ", 1)
        
        # Buscar dados do aluno
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM alunos WHERE nome = ? AND turma = ?", (nome_aluno, turma_aluno))
        aluno = cursor.fetchone()
        conn.close()
        
        if aluno:
            st.divider()
            
            # ========== CABEÇALHO DO RELATÓRIO ==========
            st.markdown(f"""
            <div style='text-align: center; padding: 20px; background: linear-gradient(135deg, #1a3a5c, #2d5f8a); border-radius: 15px; color: white;'>
                <h1>📊 RELATÓRIO DE DESEMPENHO</h1>
                <h2>👤 {aluno['nome']}</h2>
                <h3>🏫 {aluno['turma']}</h3>
                <p>📅 Data: {datetime.now().strftime('%d/%m/%Y')}</p>
            </div>
            """, unsafe_allow_html=True)
            
            st.divider()
            
            # ========== MÉTRICAS ==========
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric("⭐ Pontos", aluno['pontos'])
            with col2:
                st.metric("📰 Fake News", aluno['fake_acertos'])
            with col3:
                st.metric("🛡️ Cyberbullying", aluno['cyber_acertos'])
            with col4:
                st.metric("⚖️ Ética Digital", aluno['etica_acertos'])
            
            st.divider()
            
            # ========== GRÁFICO ==========
            st.subheader("📊 Desempenho por Categoria")
            
            import pandas as pd
            dados_grafico = pd.DataFrame({
                'Categoria': ['📰 Fake News', '🛡️ Cyberbullying', '⚖️ Ética Digital'],
                'Acertos': [aluno['fake_acertos'], aluno['cyber_acertos'], aluno['etica_acertos']]
            })
            st.bar_chart(dados_grafico.set_index('Categoria'))
            
            st.divider()
            
            # ========== RANKING ==========
            st.subheader(f"🏆 Posição na Turma")
            
            alunos_turma = buscar_alunos_por_turma(turma_aluno)
            posicao = 1
            for i, a in enumerate(alunos_turma, 1):
                if a['nome'] == aluno['nome']:
                    posicao = i
                    break
            
            st.markdown(f"""
            <div style='text-align: center; padding: 20px; background: #f8f9fa; border-radius: 15px;'>
                <h2>🏆 {posicao}º lugar de {len(alunos_turma)} alunos</h2>
                <p>⭐ {aluno['pontos']} pontos</p>
            </div>
            """, unsafe_allow_html=True)
            
            st.divider()
            
            # ========== BADGES ==========
            st.subheader("🎖️ Selos Conquistados")
            
            badges = []
            if aluno['fake_acertos'] >= 5:
                badges.append("📰 Detetive da Verdade")
            if aluno['cyber_acertos'] >= 5:
                badges.append("🛡️ Guardião Ético")
            if aluno['etica_acertos'] >= 3:
                badges.append("⚖️ Mestre da Ética")
            if aluno['pontos'] >= 20:
                badges.append("🏆 Investigador Master")
            elif aluno['pontos'] >= 10:
                badges.append("⭐ Investigador Júnior")
            
            if badges:
                tocar_som("badge")
                st.balloons()
                st.markdown("### 🏆 Selos Conquistados:")
            else:
                st.info("📭 Nenhum selo conquistado ainda.")
            
            st.divider()
            
            # ========== EXPORTAR ==========
            st.subheader("📥 Exportar Relatório")
            
            if st.button("📄 Gerar Relatório TXT"):
                relatorio = f"""
==================================================
   📊 RELATÓRIO DE DESEMPENHO
==================================================
👤 Aluno: {aluno['nome']}
🏫 Turma: {aluno['turma']}
📅 Data: {datetime.now().strftime('%d/%m/%Y %H:%M')}
==================================================

📊 PONTUAÇÃO:
   ⭐ Pontos: {aluno['pontos']}
   📰 Fake News: {aluno['fake_acertos']} acertos
   🛡️ Cyberbullying: {aluno['cyber_acertos']} acertos
   ⚖️ Ética Digital: {aluno['etica_acertos']} acertos
   📊 Total: {aluno['total_perguntas']} perguntas

🏆 RANKING:
   {posicao}º lugar de {len(alunos_turma)} alunos

🎖️ SELOS:
   {', '.join(badges) if badges else 'Nenhum selo'}

==================================================
   EEEF PROFª ODETE MENDES N OLIVEIRA
   Professor: Irving Vasconcelos dos Santos (CICI)
==================================================
"""
                st.download_button(
                    label="📥 Baixar Relatório",
                    data=relatorio,
                    file_name=f"relatorio_{aluno['nome'].replace(' ', '_')}.txt",
                    mime="text/plain"
                )
                st.success("✅ Relatório gerado!")

# ========== GERENCIAR PERGUNTAS ==========
elif menu == "📚 Gerenciar Perguntas":
    st.title("📚 Gerenciar Perguntas")
    
    st.info("💡 Aqui você pode visualizar, filtrar, adicionar e excluir perguntas do banco de dados.")
    
    # ========== TABS ==========
    tab1, tab2, tab3 = st.tabs(["📋 Listar Perguntas", "➕ Adicionar Pergunta", "🗑️ Excluir Pergunta"])
    
    # ========== TAB 1: LISTAR PERGUNTAS ==========
    with tab1:
        st.subheader("📋 Lista de Perguntas")
        
        # Filtros
        col1, col2 = st.columns(2)
        with col1:
            turmas = ["Todas"] + buscar_todas_turmas()
            filtro_turma = st.selectbox("🏫 Filtrar por Turma:", turmas, key="filtro_turma_gerenciar")
        with col2:
            categorias = ["Todas", "fake", "cyber", "etica"]
            filtro_categoria = st.selectbox("📂 Filtrar por Categoria:", categorias, key="filtro_categoria_gerenciar")
        
        # Buscar questões
        if filtro_turma == "Todas" and filtro_categoria == "Todas":
            questoes = listar_todas_questoes()
        elif filtro_turma == "Todas":
            questoes = listar_questoes_por_categoria(filtro_categoria)
        elif filtro_categoria == "Todas":
            questoes = listar_questoes_por_turma(filtro_turma)
        else:
            questoes = listar_questoes_por_turma_categoria(filtro_turma, filtro_categoria)
        
        # Mostrar total
        st.write(f"**Total: {len(questoes)} perguntas**")
        
        # Exibir questões
        for q in questoes:
            with st.expander(f"📌 {q['pergunta'][:80]}..."):
                col1, col2 = st.columns(2)
                with col1:
                    st.write(f"**ID:** {q['id']}")
                    st.write(f"**Turma:** {q['turma']}")
                    st.write(f"**Categoria:** {q['categoria']}")
                with col2:
                    st.write(f"**Resposta:** {q['resposta']}")
                    if q.get('explicacao'):
                        st.write(f"**Explicação:** {q['explicacao']}")
    
    # ========== TAB 2: ADICIONAR PERGUNTA ==========
    with tab2:
        st.subheader("➕ Adicionar Nova Pergunta")
        
        with st.form("form_adicionar_pergunta"):
            turma = st.selectbox("🏫 Turma:", buscar_todas_turmas())
            categoria = st.selectbox("📂 Categoria:", ["fake", "cyber", "etica"])
            pergunta = st.text_area("📝 Pergunta:")
            resposta = st.text_input("✅ Resposta Correta:")
            
            # Opções para ética
            if categoria == "etica":
                opcao1 = st.text_input("Opção 1:")
                opcao2 = st.text_input("Opção 2:")
                opcao3 = st.text_input("Opção 3:")
            else:
                opcao1 = opcao2 = opcao3 = None
            
            explicacao = st.text_area("💡 Explicação (opcional):")
            
            submitted = st.form_submit_button("💾 Adicionar Pergunta")
            
            if submitted:
                if pergunta and resposta:
                    conn = get_connection()
                    cursor = conn.cursor()
                    cursor.execute("""
                        INSERT INTO questoes (turma, categoria, pergunta, resposta, opcao1, opcao2, opcao3, explicacao)
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                    """, (turma, categoria, pergunta, resposta, opcao1, opcao2, opcao3, explicacao))
                    conn.commit()
                    conn.close()
                    st.success("✅ Pergunta adicionada com sucesso!")
                    st.rerun()
                else:
                    st.error("❌ Preencha a pergunta e a resposta!")
    
    # ========== TAB 3: EXCLUIR PERGUNTA ==========
    with tab3:
        st.subheader("🗑️ Excluir Pergunta")
        
        questoes = listar_todas_questoes()
        
        if questoes:
            opcoes = {f"ID {q['id']} - {q['pergunta'][:60]}... ({q['turma']})": q['id'] for q in questoes}
            pergunta_selecionada = st.selectbox("Selecione a pergunta:", list(opcoes.keys()))
            
            if st.button("🗑️ Excluir Pergunta"):
                id_excluir = opcoes[pergunta_selecionada]
                conn = get_connection()
                cursor = conn.cursor()
                cursor.execute("DELETE FROM questoes WHERE id = ?", (id_excluir,))
                conn.commit()
                conn.close()
                st.success(f"✅ Pergunta ID {id_excluir} excluída!")
                st.rerun()
        else:
            st.info("📭 Nenhuma pergunta cadastrada.")

# ========== CALCULADORA DE IMPACTO ==========
elif menu == "📊 Calculadora de Impacto":
    st.title("📊 Calculadora de Impacto")
    
    st.markdown("""
    <div class="card card-fake">
        <h4>🔍 O QUE É ISSO?</h4>
        <p>Descubra o dano que uma <strong>Fake News</strong> pode causar!</p>
        <p>Preencha os dados abaixo e veja o impacto real.</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.divider()
    
    # ========== ENTRADA DE DADOS ==========
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📰 Dados da Fake News")
        fake_news = st.text_area(
            "📝 Qual é a Fake News?",
            placeholder="Ex: 'A comida da escola está vencida!'",
            key="fake_news_input"
        )
        
        alcance = st.number_input(
            "👥 Quantas pessoas foram atingidas?",
            min_value=1,
            max_value=100000,
            value=500,
            step=50,
            key="alcance_input"
        )
        
        compartilhamentos = st.number_input(
            "📤 Quantos compartilhamentos?",
            min_value=0,
            max_value=10000,
            value=150,
            step=10,
            key="compartilhamentos_input"
        )
    
    with col2:
        st.subheader("📊 Dados de Repercussão")
        
        curtidas = st.number_input(
            "❤️ Quantas curtidas?",
            min_value=0,
            max_value=50000,
            value=300,
            step=50,
            key="curtidas_input"
        )
        
        revoltados = st.number_input(
            "😡 Quantas pessoas ficaram revoltadas?",
            min_value=0,
            max_value=10000,
            value=80,
            step=10,
            key="revoltados_input"
        )
    
    # ========== BOTÃO CALCULAR ==========
    st.divider()
    
    if st.button("📊 CALCULAR IMPACTO", key="calcular_impacto"):
        if fake_news:
            resultado = calcular_impacto_fake(alcance, compartilhamentos, curtidas, revoltados)
            
            st.divider()
            st.subheader("📊 RESULTADO DO IMPACTO")
            
            # ========== MÉTRICAS ==========
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric("👥 Alcance", f"{resultado['alcance']:,}")
            with col2:
                st.metric("📤 Compartilhamentos", f"{resultado['compartilhamentos']:,}")
            with col3:
                st.metric("❤️ Curtidas", f"{resultado['curtidas']:,}")
            with col4:
                st.metric("😡 Revoltados", f"{resultado['revoltados']:,}")
            
            st.divider()
            
            # ========== IMPACTO TOTAL ==========
            st.markdown(f"""
            <div style='text-align: center; padding: 30px; background: linear-gradient(135deg, #dc3545, #c82333); border-radius: 15px; color: white;'>
                <h1>{resultado['classificacao']}</h1>
                <h2>📊 Impacto Total: {resultado['impacto_total']:,.0f} pontos</h2>
                <p>{resultado['descricao']}</p>
            </div>
            """, unsafe_allow_html=True)
            
            st.divider()
            
            # ========== EXPLICAÇÃO ==========
            st.subheader("📋 O que isso significa?")
            
            st.markdown(f"""
            | Fator | Peso | Impacto |
            |-------|------|---------|
            | 👥 Alcance | 1x | {resultado['alcance']:,} |
            | 📤 Compartilhamentos | 3x | {resultado['compartilhamentos'] * 3:,} |
            | ❤️ Curtidas | 0.5x | {resultado['curtidas'] * 0.5:,.0f} |
            | 😡 Revoltados | 5x | {resultado['revoltados'] * 5:,} |
            | **TOTAL** | | **{resultado['impacto_total']:,.0f}** |
            """)
            
            st.divider()
            
            # ========== DICAS ==========
            st.subheader("💡 O que fazer?")
            
            if resultado['impacto_total'] >= 2000:
                st.error("🚨 AÇÃO URGENTE: Essa fake news precisa ser combatida IMEDIATAMENTE!")
                st.markdown("""
                1. 📢 Comunique a direção da escola
                2. 📝 Publique um comunicado oficial
                3. 🔍 Investigue a origem da fake news
                4. 📚 Promova uma campanha de conscientização
                """)
            elif resultado['impacto_total'] >= 500:
                st.warning("⚠️ ATENÇÃO: Essa fake news está se espalhando!")
                st.markdown("""
                1. 📢 Avise seus colegas
                2. 🔍 Verifique a fonte
                3. ❌ Não compartilhe
                4. 📚 Converse com um professor
                """)
            else:
                st.success("✅ SITUAÇÃO CONTROLADA: A fake news não está se espalhando muito.")
                st.markdown("""
                1. 🔍 Continue verificando as informações
                2. 📚 Compartilhe apenas notícias verdadeiras
                3. 💪 Ajude a combater a desinformação
                """)
            
            st.divider()
            
            # ========== REGISTRAR PONTOS ==========
            if st.button("✅ Ganhei +1 ponto por aprender!", key="ganhar_ponto_impacto"):
                st.session_state.pontos += 1
                st.success("✅ +1 ponto adicionado!")
                st.balloons()
        else:
            st.warning("⚠️ Digite a Fake News para calcular o impacto!")

# ========== SIMULADOR DE ALGORITMO ==========
elif menu == "🧠 Simulador de Algoritmo":
    st.title("🧠 Simulador de Algoritmo")
    
    st.markdown("""
    <div class="card card-ethic">
        <h4>🤖 O QUE É ISSO?</h4>
        <p>Descubra como o <strong>algoritmo das redes sociais</strong> funciona!</p>
        <p>Ele mostra apenas o que você <strong>concorda</strong>, criando o <strong>EFEITO BOLHA</strong>.</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.divider()
    
    # ========== INICIALIZAR SESSÃO ==========
    if 'algoritmo_curtidas' not in st.session_state:
        st.session_state.algoritmo_curtidas = {
            "Notícia A": 0,
            "Notícia B": 0,
            "Notícia C": 0,
            "Notícia D": 0
        }
    if 'algoritmo_rodada' not in st.session_state:
        st.session_state.algoritmo_rodada = 1
    if 'algoritmo_historico' not in st.session_state:
        st.session_state.algoritmo_historico = []
    
    # ========== NOTÍCIAS ==========
    noticias = {
        "Notícia A": {
            "titulo": "🏫 Escola investe em tecnologia",
            "tipo": "Educação",
            "emoji": "📚"
        },
        "Notícia B": {
            "titulo": "⚽ Time da escola ganha campeonato",
            "tipo": "Esporte",
            "emoji": "🏆"
        },
        "Notícia C": {
            "titulo": "🎮 Novo jogo é lançado",
            "tipo": "Tecnologia",
            "emoji": "🕹️"
        },
        "Notícia D": {
            "titulo": "🎵 Cantor famoso faz show na cidade",
            "tipo": "Música",
            "emoji": "🎤"
        }
    }
    
    # ========== MOSTRAR RODADA ==========
    st.subheader(f"🔍 Rodada {st.session_state.algoritmo_rodada}")
    st.write("**O que você quer curtir hoje?**")
    
    # ========== EXIBIR NOTÍCIAS ==========
    col1, col2 = st.columns(2)
    
    for i, (key, noticia) in enumerate(noticias.items()):
        with col1 if i % 2 == 0 else col2:
            st.markdown(f"""
            <div style='padding: 15px; margin: 10px 0; background: #f8f9fa; border-radius: 10px; border-left: 5px solid #1a3a5c;'>
                <h4>{noticia['emoji']} {noticia['titulo']}</h4>
                <p style='color: gray;'>Categoria: {noticia['tipo']}</p>
            </div>
            """, unsafe_allow_html=True)
            
            if st.button(f"❤️ Curtir {key}", key=f"curtir_{key}_{st.session_state.algoritmo_rodada}"):
                st.session_state.algoritmo_curtidas[key] += 1
                st.session_state.algoritmo_historico.append(key)
                st.session_state.algoritmo_rodada += 1
                st.rerun()
    
    st.divider()
    
    # ========== MOSTRAR ALGORITMO ==========
    if st.session_state.algoritmo_historico:
        st.subheader("🤖 O que o algoritmo está fazendo...")
        
        # Calcular qual notícia foi mais curtida
        mais_curtida = max(st.session_state.algoritmo_curtidas, key=st.session_state.algoritmo_curtidas.get)
        total_curtidas = sum(st.session_state.algoritmo_curtidas.values())
        
        if total_curtidas > 0:
            st.markdown(f"""
            <div style='padding: 20px; background: linear-gradient(135deg, #6f42c1, #9b59b6); border-radius: 15px; color: white; text-align: center;'>
                <h2>🤖 O ALGORITMO DIZ:</h2>
                <h3>Você gosta de {noticias[mais_curtida]['tipo']}!</h3>
                <p>Vou te mostrar MAIS conteúdo sobre {noticias[mais_curtida]['tipo']}!</p>
            </div>
            """, unsafe_allow_html=True)
            
            st.divider()
            
            # ========== GRÁFICO DE CURTIDAS ==========
            st.subheader("📊 Suas Curtidas")
            
            import pandas as pd
            dados_grafico = pd.DataFrame([
                {"Notícia": k, "Curtidas": v}
                for k, v in st.session_state.algoritmo_curtidas.items()
            ])
            st.bar_chart(dados_grafico.set_index('Notícia'))
            
            st.divider()
            
            # ========== EFEITO BOLHA ==========
            st.subheader("💡 O EFEITO BOLHA")
            
            st.warning(f"""
            🚨 **VOCÊ ESTÁ PRESO NA BOLHA!**
            
            O algoritmo percebeu que você gosta de **{noticias[mais_curtida]['tipo']}** 
            e agora vai te mostrar **APENAS** conteúdo sobre isso!
            
            **Consequências:**
            - ❌ Você não vê outros pontos de vista
            - ❌ Você só vê o que concorda
            - ❌ Você fica isolado em sua "bolha"
            """)
            
            st.divider()
            
            # ========== COMO QUEBRAR A BOLHA ==========
            st.subheader("🔨 COMO QUEBRAR A BOLHA?")
            
            st.success("""
            ✅ **DICAS PARA SAIR DA BOLHA:**
            
            1. 📰 **Leia notícias de fontes diferentes**
            2. 👥 **Siga pessoas com opiniões diferentes**
            3. 🔍 **Pesquise sobre o assunto antes de compartilhar**
            4. 💬 **Converse com pessoas que pensam diferente**
            5. 🧠 **Questione o que o algoritmo te mostra**
            """)
            
            st.divider()
            
            # ========== REINICIAR ==========
            if st.button("🔄 Reiniciar Simulação", key="reiniciar_algoritmo"):
                st.session_state.algoritmo_curtidas = {
                    "Notícia A": 0,
                    "Notícia B": 0,
                    "Notícia C": 0,
                    "Notícia D": 0
                }
                st.session_state.algoritmo_rodada = 1
                st.session_state.algoritmo_historico = []
                st.rerun()
    
    else:
        st.info("💡 Clique em uma notícia para começar a simulação!")
    
    st.divider()
    
    # ========== EXPLICAÇÃO ==========
    st.subheader("📖 O que é o Efeito Bolha?")
    
    st.markdown("""
    O **Efeito Bolha** (ou Filter Bubble) é um fenômeno que acontece quando 
    os algoritmos das redes sociais mostram apenas conteúdos que você **já concorda**.
    
    **Como funciona:**
    1. 🤖 O algoritmo observa o que você curte
    2. 📊 Ele cria um "perfil" seu
    3. 🎯 Ele mostra apenas conteúdos parecidos
    4. 🔒 Você fica preso em uma "bolha"
    
    **Por que é perigoso?**
    - ❌ Você não vê outros pontos de vista
    - ❌ Você acredita que todos pensam como você
    - ❌ Você fica mais fácil de ser manipulado
    - ❌ Fake news se espalham mais facilmente
    """)

# ========== FLUXOGRAMA ANTI-FAKE NEWS ==========
elif menu == "📝 Fluxograma Anti-Fake News":
    st.title("📝 Fluxograma Anti-Fake News")
    
    st.info("""
    🔍 **O QUE É ISSO?**
    
    Um passo a passo lógico para verificar se uma notícia é verdadeira ou falsa.
    Use o Pensamento Computacional (SE / ENTÃO / SENÃO) para decidir!
    """)
    
    st.divider()
    
    # ========== IMAGEM DO FLUXOGRAMA ==========
    st.subheader("🖼️ Mapa do Fluxograma")
    
    st.code("""
┌─────────────────────┐
│  1. TEM FONTE?      │
└─────────┬───────────┘
          │
  ┌───────┴───────┐
  │ SIM           │ NÃO
  ▼               ▼
┌─────────┐   ┌─────────┐
│ PASSO 2 │   │ ❌ FAKE │
└────┬────┘   └─────────┘
     │
┌────▼─────────────────┐
│  2. FONTE CONFIÁVEL? │
└─────────┬────────────┘
          │
  ┌───────┴───────┐
  │ SIM           │ NÃO
  ▼               ▼
┌─────────┐   ┌─────────┐
│ PASSO 3 │   │ ❌ FAKE │
└────┬────┘   └─────────┘
     │
┌────▼─────────────────┐
│  3. OUTROS CONFIRMAM?│
└─────────┬────────────┘
          │
  ┌───────┴───────┐
  │ SIM           │ NÃO
  ▼               ▼
┌─────────┐   ┌─────────┐
│ PASSO 4 │   │ ❌ FAKE │
└────┬────┘   └─────────┘
     │
┌────▼─────────────────┐
│  4. DATA É RECENTE?  │
└─────────┬────────────┘
          │
  ┌───────┴───────┐
  │ SIM           │ NÃO
  ▼               ▼
┌─────────┐   ┌─────────┐
│ ✅ VERD │   │ ❌ FAKE │
└─────────┘   └─────────┘
    """, language="text")
    
    st.divider()
    
    # ========== PRÁTICA (INTERATIVO) ==========
    st.subheader("🎮 Prática: Verifique uma Notícia")
    
    if 'fluxograma_passo' not in st.session_state:
        st.session_state.fluxograma_passo = 1
    if 'fluxograma_resultado' not in st.session_state:
        st.session_state.fluxograma_resultado = None
    if 'fluxograma_historico' not in st.session_state:
        st.session_state.fluxograma_historico = []
    
    noticia_exemplo = st.text_area(
        "📝 Cole a notícia aqui:",
        value="URGENTE! A comida da escola está vencida e todos vão passar mal!",
        height=100,
        key="noticia_fluxograma"
    )
    
    st.divider()
    
    passos = ["1. Fonte", "2. Confiabilidade", "3. Confirmação", "4. Data", "5. Resultado"]
    st.progress(st.session_state.fluxograma_passo / len(passos) if st.session_state.fluxograma_passo <= len(passos) else 1.0)
    
    # PASSO 1
    if st.session_state.fluxograma_passo == 1:
        st.write("### 🔍 PASSO 1: A notícia tem fonte?")
        st.write("**SE** a notícia não tem fonte, **ENTÃO** é fake news!")
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("✅ SIM, tem fonte", key="passo1_sim"):
                st.session_state.fluxograma_passo = 2
                st.session_state.fluxograma_historico.append("1. Fonte: SIM")
                st.rerun()
        with col2:
            if st.button("❌ NÃO, não tem fonte", key="passo1_nao"):
                st.session_state.fluxograma_resultado = "fake"
                st.session_state.fluxograma_historico.append("1. Fonte: NÃO")
                st.session_state.fluxograma_passo = 6
                st.rerun()
    
    # PASSO 2
    elif st.session_state.fluxograma_passo == 2:
        st.write("### 🔍 PASSO 2: A fonte é confiável?")
        st.write("**SE** a fonte não é confiável, **ENTÃO** é fake news!")
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("✅ SIM, é confiável", key="passo2_sim"):
                st.session_state.fluxograma_passo = 3
                st.session_state.fluxograma_historico.append("2. Confiabilidade: SIM")
                st.rerun()
        with col2:
            if st.button("❌ NÃO, não é confiável", key="passo2_nao"):
                st.session_state.fluxograma_resultado = "fake"
                st.session_state.fluxograma_historico.append("2. Confiabilidade: NÃO")
                st.session_state.fluxograma_passo = 6
                st.rerun()
    
    # PASSO 3
    elif st.session_state.fluxograma_passo == 3:
        st.write("### 🔍 PASSO 3: Outros sites confirmam?")
        st.write("**SE** outros sites não confirmam, **ENTÃO** é fake news!")
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("✅ SIM, confirmam", key="passo3_sim"):
                st.session_state.fluxograma_passo = 4
                st.session_state.fluxograma_historico.append("3. Confirmação: SIM")
                st.rerun()
        with col2:
            if st.button("❌ NÃO, não confirmam", key="passo3_nao"):
                st.session_state.fluxograma_resultado = "fake"
                st.session_state.fluxograma_historico.append("3. Confirmação: NÃO")
                st.session_state.fluxograma_passo = 6
                st.rerun()
    
    # PASSO 4
    elif st.session_state.fluxograma_passo == 4:
        st.write("### 🔍 PASSO 4: A data é recente?")
        st.write("**SE** a data é muito antiga, **ENTÃO** pode ser fake news!")
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("✅ SIM, é recente", key="passo4_sim"):
                st.session_state.fluxograma_passo = 5
                st.session_state.fluxograma_historico.append("4. Data: SIM")
                st.rerun()
        with col2:
            if st.button("❌ NÃO, é antiga", key="passo4_nao"):
                st.session_state.fluxograma_resultado = "fake"
                st.session_state.fluxograma_historico.append("4. Data: NÃO")
                st.session_state.fluxograma_passo = 6
                st.rerun()
    
    # PASSO 5
    elif st.session_state.fluxograma_passo == 5:
        st.session_state.fluxograma_resultado = "verdade"
        st.session_state.fluxograma_passo = 6
        st.rerun()
    
    # RESULTADO
    elif st.session_state.fluxograma_passo == 6:
        st.divider()
        st.subheader("📊 RESULTADO DA VERIFICAÇÃO")
        
        if st.session_state.fluxograma_resultado == "fake":
            st.error("❌ FAKE NEWS!")
            st.write("Essa notícia é FALSA! NÃO compartilhe!")
            st.write("**O QUE FAZER:**")
            st.write("1. ❌ NÃO compartilhe")
            st.write("2. 📢 Avise seus colegas que é fake")
            st.write("3. 📝 Comunique a direção da escola")
            st.write("4. 🔍 Pesquise a fonte verdadeira")
        
        elif st.session_state.fluxograma_resultado == "verdade":
            st.success("✅ VERDADE!")
            st.write("Essa notícia é VERDADEIRA! Você pode compartilhar com segurança!")
            st.balloons()
            st.write("**O QUE FAZER:**")
            st.write("1. ✅ PODE compartilhar")
            st.write("2. 📢 Avise seus colegas")
            st.write("3. 📝 Compartilhe com responsabilidade")
            st.write("4. 🔍 Sempre cite a fonte")
        
        st.divider()
        st.subheader("📋 Histórico da Verificação")
        for item in st.session_state.fluxograma_historico:
            st.write(f"• {item}")
        
        st.divider()
        if st.button("🔄 Verificar Outra Notícia", key="reiniciar_fluxograma"):
            st.session_state.fluxograma_passo = 1
            st.session_state.fluxograma_resultado = None
            st.session_state.fluxograma_historico = []
            st.rerun()
    
    # RESUMO
    st.divider()
    st.subheader("📝 Resumo: O que aprendemos?")
    
    st.write("### 🔍 FLUXOGRAMA ANTI-FAKE NEWS")
    st.write("**O que é?**")
    st.write("É um passo a passo lógico para verificar se uma notícia é verdadeira ou falsa.")
    st.write("**Quais são os passos?**")
    st.write("1️⃣ A notícia tem fonte? → SE NÃO → ❌ FAKE")
    st.write("2️⃣ A fonte é confiável? → SE NÃO → ❌ FAKE")
    st.write("3️⃣ Outros sites confirmam? → SE NÃO → ❌ FAKE")
    st.write("4️⃣ A data é recente? → SE NÃO → ❌ FAKE")
    st.write("✅ Todas SIM → ✅ VERDADE")
    st.write("**Por que isso é importante?**")
    st.write("- 🧠 **Pensamento Computacional:** Usamos SE / ENTÃO / SENÃO")
    st.write("- 🛡️ **Cidadania Digital:** Aprendemos a verificar antes de compartilhar")
    st.write("- 💪 **Protagonismo:** Nos tornamos 'Fiscais da Verdade'")
    st.info("💡 **Lembre-se:** Na dúvida, NÃO compartilhe! Verifique primeiro!")
# ========== CAMPANHA ÉTICA (MAKER) ==========
elif menu == "🎨 Campanha Ética":
    st.title("🎨 Campanha Ética Digital")
    
    st.markdown("""
    <div class="card card-ethic">
        <h4>🎯 O QUE É ISSO?</h4>
        <p>Você vai criar uma <strong>campanha de conscientização</strong> sobre Cidadania Digital!</p>
        <p>Use sua criatividade para ajudar a combater as Fake News e o Cyberbullying!</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.divider()
    
    # ========== INICIALIZAR SESSÃO ==========
    if 'campanha_tipo' not in st.session_state:
        st.session_state.campanha_tipo = None
    if 'campanha_tema' not in st.session_state:
        st.session_state.campanha_tema = None
    if 'campanha_roteiro' not in st.session_state:
        st.session_state.campanha_roteiro = ""
    if 'campanha_criada' not in st.session_state:
        st.session_state.campanha_criada = False
    
    # ========== PASSO 1: ESCOLHER O TIPO ==========
    st.subheader("📌 Passo 1: Escolha o tipo de campanha")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("📱 POST", key="tipo_post", use_container_width=True):
            st.session_state.campanha_tipo = "Post"
            st.rerun()
    
    with col2:
        if st.button("🎬 VÍDEO", key="tipo_video", use_container_width=True):
            st.session_state.campanha_tipo = "Vídeo"
            st.rerun()
    
    with col3:
        if st.button("😂 MEME", key="tipo_meme", use_container_width=True):
            st.session_state.campanha_tipo = "Meme"
            st.rerun()
    
    if st.session_state.campanha_tipo:
        st.success(f"✅ Tipo escolhido: **{st.session_state.campanha_tipo}**")
    
    st.divider()
    
    # ========== PASSO 2: ESCOLHER O TEMA ==========
    if st.session_state.campanha_tipo:
        st.subheader("📌 Passo 2: Escolha o tema")
        
        temas = [
            "📰 Fake News - Como identificar?",
            "🛡️ Cyberbullying - Como combater?",
            "⚖️ Ética Digital - O que é?",
            "🔒 Privacidade - Proteja seus dados",
            "🧠 Efeito Bolha - Saia da bolha",
            "💬 Discurso de Ódio - Diga NÃO"
        ]
        
        tema_selecionado = st.selectbox("Escolha o tema da sua campanha:", temas, key="tema_campanha")
        
        if st.button("✅ Confirmar Tema", key="confirmar_tema"):
            st.session_state.campanha_tema = tema_selecionado
            st.rerun()
    
    if st.session_state.campanha_tema:
        st.success(f"✅ Tema escolhido: **{st.session_state.campanha_tema}**")
    
    st.divider()
    
    # ========== PASSO 3: CRIAR O ROTEIRO ==========
    if st.session_state.campanha_tema:
        st.subheader("📌 Passo 3: Crie seu roteiro")
        
        st.info(f"💡 Você está criando um **{st.session_state.campanha_tipo}** sobre **{st.session_state.campanha_tema}**")
        
        # Dicas baseadas no tipo
        if st.session_state.campanha_tipo == "Post":
            st.markdown("""
            **📱 DICAS PARA POST:**
            - Use uma imagem chamativa
            - Escreva uma legenda curta e impactante
            - Use hashtags (#CidadaniaDigital #FakeNews)
            - Inclua uma chamada para ação
            """)
        elif st.session_state.campanha_tipo == "Vídeo":
            st.markdown("""
            **🎬 DICAS PARA VÍDEO:**
            - Duração: 30 segundos a 1 minuto
            - Comece com uma pergunta impactante
            - Mostre exemplos reais
            - Termine com uma solução
            """)
        else:
            st.markdown("""
            **😂 DICAS PARA MEME:**
            - Use uma imagem engraçada
            - Frase curta e direta
            - Humor inteligente (sem ofender)
            - Compartilhe nas redes sociais
            """)
        
        roteiro = st.text_area(
            "📝 Escreva seu roteiro aqui:",
            value=st.session_state.campanha_roteiro,
            height=200,
            placeholder="Ex: 'Você já recebeu uma notícia que parecia verdadeira, mas era fake? Antes de compartilhar, VERIFIQUE a fonte!'",
            key="roteiro_campanha"
        )
        
        if st.button("💾 Salvar Roteiro", key="salvar_roteiro"):
            st.session_state.campanha_roteiro = roteiro
            st.session_state.campanha_criada = True
            st.success("✅ Roteiro salvo com sucesso!")
            st.rerun()
    
    st.divider()
    
    # ========== PASSO 4: VISUALIZAR CAMPANHA ==========
    if st.session_state.campanha_criada and st.session_state.campanha_roteiro:
        st.subheader("📌 Passo 4: Sua Campanha está pronta!")
        
        st.subheader("🎨 SUA CAMPANHA")
        st.write(f"**📌 Tipo:** {st.session_state.campanha_tipo}")
        st.write(f"**🎯 Tema:** {st.session_state.campanha_tema}")
        st.write(f"**📝 Roteiro:**")
        st.info(st.session_state.campanha_roteiro)
        
        st.divider()
        
        # ========== DICAS PARA COMPARTILHAR ==========
        st.subheader("📤 Como compartilhar?")
        
        st.markdown("""
        ### 📱 REDES SOCIAIS:
        - **Instagram:** Poste no feed e nos stories
        - **TikTok:** Faça um vídeo curto e criativo
        - **WhatsApp:** Compartilhe nos grupos da turma
        - **Mural da Escola:** Imprima e cole no mural
        
        ### 🎯 DICAS EXTRAS:
        1. 📢 Peça ajuda aos colegas
        2. 🎨 Use o Canva para criar o design
        3. 🎬 Use o CapCut para editar vídeos
        4. 📊 Compartilhe os resultados
        """)
        
        st.divider()
        
        # ========== BOTÃO REINICIAR ==========
        if st.button("🔄 Criar Nova Campanha", key="reiniciar_campanha"):
            st.session_state.campanha_tipo = None
            st.session_state.campanha_tema = None
            st.session_state.campanha_roteiro = ""
            st.session_state.campanha_criada = False
            st.rerun()
    
    # ========== EXPLICAÇÃO ==========
    st.divider()
    st.subheader("📖 Por que fazer uma campanha?")
    
    st.markdown("""
    ### 🎯 CULTURA MAKER E DIGITAL
    
    Quando você **CRIA** algo, você aprende **MUITO MAIS**!
    
    **O que você desenvolve:**
    - 🎨 **Criatividade:** Pensar em soluções inovadoras
    - 🧠 **Protagonismo:** Ser o agente da mudança
    - 📢 **Comunicação:** Passar sua mensagem
    - 💪 **Engajamento:** Ajudar a comunidade
    
    **Lembre-se:**
    > "Você não precisa ser um especialista para fazer a diferença. Basta querer ajudar!"
    """)

# ========== GUIA DE SOBREVIVÊNCIA DIGITAL ==========
elif menu == "📋 Guia de Sobrevivência":
    st.title("📋 Guia de Sobrevivência Digital")
    
    st.markdown("""
    <div class="card card-ethic">
        <h4>🎯 O QUE É ISSO?</h4>
        <p>Um guia completo para você se tornar um <strong>Cidadão Digital Consciente</strong>!</p>
        <p>Navegue pelos capítulos e aprenda a se proteger e a proteger os outros.</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.divider()
    
    # ========== CAPÍTULOS ==========
    capitulos = {
        "1. Como identificar um clique falso?": {
            "emoji": "🖱️",
            "conteudo": """
            ### 🖱️ COMO IDENTIFICAR UM CLIQUE FALSO?
            
            **O que é um clique falso?**
            É um link que promete algo bom (prêmios, dinheiro, presentes) mas na verdade é uma armadilha!
            
            **Como identificar:**
            1. 🔍 **Desconfie de promoções milagrosas**
               - "Ganhe um celular novo clicando aqui!"
               - "Você foi sorteado!"
            
            2. 🔗 **Verifique o link antes de clicar**
               - Passe o mouse sobre o link
               - Veja se o endereço é confiável
            
            3. ❌ **Erros de português**
               - "Vc ganhou um premio!"
               - "Clique aqui para resgatar"
            
            4. 📱 **Mensagens de desconhecidos**
               - Não clique em links de quem você não conhece
            
            5. ⏰ **Urgência excessiva**
               - "Últimas vagas!"
               - "Só hoje!"
            
            **O que fazer:**
            - ❌ NÃO clique
            - 🗑️ Delete a mensagem
            - 📢 Avise seus amigos
            - 🔍 Pesquise sobre o golpe
            """
        },
        "2. O que fazer se sofrer cyberbullying?": {
            "emoji": "🛡️",
            "conteudo": """
            ### 🛡️ O QUE FAZER SE SOFRER CYBERBULLYING?
            
            **Passo a passo:**
            
            **1. NÃO RESPONDA**
            - Não revide com ofensas
            - Não alimente o bullying
            
            **2. BLOQUEIE O AGRESSOR**
            - Bloqueie em todas as redes sociais
            - Não permita que ele te envie mensagens
            
            **3. GUARDE PROVAS**
            - Tire print (captura de tela)
            - Salve as mensagens
            - Anote data e hora
            
            **4. DENUNCIE**
            - Denuncie nas próprias redes sociais
            - Denuncie na escola
            - Denuncie para um adulto de confiança
            
            **5. PROCURE AJUDA**
            - Converse com seus pais
            - Converse com um professor
            - Procure um psicólogo se precisar
            
            **O que NÃO fazer:**
            - ❌ Revidar
            - ❌ Ficar calado
            - ❌ Culpar a si mesmo
            
            **Lembre-se:**
            > "A culpa NUNCA é da vítima. Você não está sozinho!"
            """
        },
        "3. Calculadora do Impacto": {
            "emoji": "📊",
            "conteudo": """
            ### 📊 CALCULADORA DO IMPACTO
            
            **O que é?**
            É uma forma de calcular o dano que uma Fake News pode causar.
            
            **Como calcular:**
            
            | Fator | Peso |
            |-------|------|
            | 👥 Alcance | 1x |
            | 📤 Compartilhamentos | 3x |
            | ❤️ Curtidas | 0.5x |
            | 😡 Revoltados | 5x |
            
            **Exemplo:**
            - 500 pessoas alcançadas = 500
            - 150 compartilhamentos = 450
            - 300 curtidas = 150
            - 80 revoltados = 400
            - **TOTAL = 1.500 pontos**
            
            **Classificação:**
            - 🔴 5000+ = CATASTRÓFICO
            - 🟠 2000+ = ALTO
            - 🟡 1000+ = MODERADO
            - 🟢 500+ = BAIXO
            - ⚪ 0-500 = MÍNIMO
            
            **Por que isso importa?**
            - 📢 Mostra que uma mentira pode causar danos reais
            - 🧠 Ajuda a pensar antes de compartilhar
            - 💡 Ensina a responsabilidade digital
            """
        },
        "4. Como sair da bolha?": {
            "emoji": "🧠",
            "conteudo": """
            ### 🧠 COMO SAIR DA BOLHA?
            
            **O que é o Efeito Bolha?**
            É quando o algoritmo das redes sociais mostra apenas conteúdos que você já concorda.
            
            **Como sair:**
            
            **1. SIGA PESSOAS DIFERENTES**
            - Siga pessoas com opiniões diferentes
            - Siga veículos de imprensa confiáveis
            
            **2. LEIA FONTES VARIADAS**
            - Leia notícias de vários sites
            - Compare as informações
            
            **3. QUESTione O ALGORITMO**
            - Pergunte-se: "Por que estou vendo isso?"
            - Pesquise sobre o assunto
            
            **4. CONVERSE COM PESSOAS**
            - Converse com quem pensa diferente
            - Ouça com respeito
            
            **5. PESQUISE SEMPRE**
            - Antes de acreditar, pesquise
            - Verifique em várias fontes
            
            **Lembre-se:**
            > "Sair da bolha é o primeiro passo para se tornar um cidadão digital consciente!"
            """
        },
        "5. Proteja seus dados": {
            "emoji": "🔒",
            "conteudo": """
            ### 🔒 PROTEJA SEUS DADOS
            
            **O que são dados pessoais?**
            - Nome completo
            - CPF
            - Endereço
            - Telefone
            - Foto
            - Localização
            
            **Como se proteger:**
            
            **1. NUNCA compartilhe:**
            - ❌ Senhas
            - ❌ CPF
            - ❌ Endereço
            - ❌ Dados bancários
            
            **2. CUIDADO com:**
            - ⚠️ Enquetes que pedem dados
            - ⚠️ Jogos que pedem informações
            - ⚠️ Correntes de WhatsApp
            - ⚠️ Sites desconhecidos
            
            **3. USE SENHAS FORTES:**
            - Letras maiúsculas e minúsculas
            - Números
            - Símbolos
            - Não use datas de nascimento
            
            **4. CONFIGURE SUAS REDES:**
            - Deixe o perfil privado
            - Não compartilhe localização
            - Revise as permissões dos aplicativos
            
            **Lembre-se:**
            > "Seus dados valem ouro! Proteja-os como um tesouro!"
            """
        },
        "6. Denuncie!": {
            "emoji": "📢",
            "conteudo": """
            ### 📢 DENUNCIE!
            
            **O que denunciar?**
            - 🚨 Cyberbullying
            - 📰 Fake News
            - 💬 Discurso de ódio
            - 🔞 Conteúdo impróprio
            - 🕵️ Golpes e fraudes
            
            **Onde denunciar?**
            
            **1. NAS REDES SOCIAIS:**
            - Instagram: Denunciar post/perfil
            - TikTok: Denunciar vídeo
            - WhatsApp: Denunciar mensagem
            
            **2. NA ESCOLA:**
            - Direção
            - Professores
            - Coordenação
            
            **3. PARA ADULTOS:**
            - Pais ou responsáveis
            - Polícia (em casos graves)
            - Disque 100 (Direitos Humanos)
            
            **4. SITES OFICIAIS:**
            - SaferNet Brasil
            - Denuncie.org.br
            
            **Por que denunciar?**
            - 🛡️ Protege você e outras pessoas
            - 💪 Combate a impunidade
            - 🌐 Torna a internet um lugar melhor
            
            **Lembre-se:**
            > "Denunciar não é fofoca. É um ato de coragem e cidadania!"
            """
        }
    }
    
    # ========== NAVEGAÇÃO POR CAPÍTULOS ==========
    st.subheader("📚 Capítulos do Guia")
    
    # Criar tabs para cada capítulo
    tabs = st.tabs([f"{cap['emoji']} {titulo}" for titulo, cap in capitulos.items()])
    
    for i, (titulo, cap) in enumerate(capitulos.items()):
        with tabs[i]:
            st.write(cap['conteudo'])
    
    st.info("💡 Dica: sempre verifique antes de compartilhar!")   
    
    # ========== DOWNLOAD DO GUIA ==========
    st.subheader("📥 Baixar o Guia Completo")
    
    if st.button("📄 Gerar Guia em TXT", key="gerar_guia"):
        guia_completo = """
==================================================
   📋 GUIA DE SOBREVIVÊNCIA DIGITAL
==================================================
🏫 EEEF PROFª ODETE MENDES N OLIVEIRA
👨‍🏫 Professor: IRVING VASCONCELOS DOS SANTOS (CICI)
👨‍🎓 Turma: 6º Ano - Ensino Fundamental
📅 Data: {data}
==================================================

"""
        for titulo, cap in capitulos.items():
            guia_completo += f"\n\n{'='*50}\n"
            guia_completo += f"{cap['emoji']} {titulo}\n"
            guia_completo += f"{'='*50}\n"
            guia_completo += cap['conteudo']
        
        guia_completo += f"""

==================================================
   🌐 CIDADANIA DIGITAL - EEEF PROFª ODETE N OLIVEIRA
==================================================
"""
        
        st.download_button(
            label="📥 Baixar Guia Completo",
            data=guia_completo,
            file_name="guia_sobrevivencia_digital.txt",
            mime="text/plain"
        )
        st.success("✅ Guia gerado com sucesso!")
    
    st.divider()
    
    # ========== DICAS EXTRAS ==========
    st.subheader("💡 Dicas Extras")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        ### ✅ FAÇA:
        - 🔍 Verifique antes de compartilhar
        - 🤝 Respeite as pessoas online
        - 🔒 Proteja seus dados
        - 📢 Denuncie conteúdo ofensivo
        - 💬 Converse com adultos de confiança
        """)
    
    with col2:
        st.markdown("""
        ### ❌ NÃO FAÇA:
        - ❌ Compartilhe fake news
        - ❌ Pratique cyberbullying
        - ❌ Compartilhe dados pessoais
        - ❌ Revide ofensas
        - ❌ Fique calado se sofrer bullying
        """)
    
    st.divider()
    
    # ========== MENSAGEM FINAL ==========
    st.success("🌟 VOCÊ É UM CIDADÃO DIGITAL!")
    st.write("Use este guia para se proteger e proteger os outros.")
    st.write("Juntos, podemos tornar a internet um lugar melhor!")

# ========== ESTATÍSTICAS DA TURMA ==========
elif menu == "📊 Estatísticas da Turma":
    st.title("📊 Estatísticas da Turma")
    
    st.markdown("""
    <div class="card card-ethic">
        <h4>🎯 O QUE É ISSO?</h4>
        <p>Acompanhe o <strong>desempenho geral</strong> da sua turma!</p>
        <p>Veja gráficos, métricas e rankings dos alunos.</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.divider()
    
    # ========== SELECIONAR TURMA ==========
    turmas = buscar_todas_turmas()
    
    if not turmas:
        st.warning("📭 Nenhuma turma cadastrada ainda.")
        st.stop()
    
    turma_selecionada = st.selectbox("🏫 Escolha a turma:", turmas, key="turma_estatisticas")
    
    # ========== BUSCAR DADOS ==========
    alunos = buscar_alunos_por_turma(turma_selecionada)
    
    if not alunos:
        st.info(f"📭 Nenhum aluno cadastrado na turma {turma_selecionada}.")
        st.stop()
    
    # ========== MÉTRICAS GERAIS ==========
    st.subheader(f"📈 Visão Geral da {turma_selecionada}")
    
    total_alunos = len(alunos)
    total_pontos = sum([a['pontos'] for a in alunos])
    media_pontos = total_pontos / total_alunos if total_alunos > 0 else 0
    
    total_fake = sum([a['fake_acertos'] for a in alunos])
    total_cyber = sum([a['cyber_acertos'] for a in alunos])
    total_etica = sum([a['etica_acertos'] for a in alunos])
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("👥 Total de Alunos", total_alunos)
    with col2:
        st.metric("⭐ Total de Pontos", total_pontos)
    with col3:
        st.metric("📊 Média de Pontos", f"{media_pontos:.1f}")
    with col4:
        st.metric("📰 Total Fake News", total_fake)
    
    st.divider()
    
    # ========== GRÁFICO DE ACERTOS POR CATEGORIA ==========
    st.subheader("📊 Acertos por Categoria")
    
    import pandas as pd
    
    dados_categoria = pd.DataFrame({
        'Categoria': ['📰 Fake News', '🛡️ Cyberbullying', '⚖️ Ética Digital'],
        'Acertos': [total_fake, total_cyber, total_etica]
    })
    st.bar_chart(dados_categoria.set_index('Categoria'))
    
    st.divider()
    
    # ========== RANKING DA TURMA ==========
    st.subheader(f"🏆 Ranking da {turma_selecionada}")
    
    for i, aluno in enumerate(alunos, 1):
        # Medalhas para os 3 primeiros
        if i == 1:
            medalha = "🥇"
            cor = "#ffd700"
        elif i == 2:
            medalha = "🥈"
            cor = "#c0c0c0"
        elif i == 3:
            medalha = "🥉"
            cor = "#cd7f32"
        else:
            medalha = f"{i}º"
            cor = "#f8f9fa"
        
        st.markdown(f"""
        <div style='padding: 10px; margin: 5px 0; background: {cor}; border-radius: 10px;'>
            <h4>{medalha} {aluno['nome']}</h4>
            <p>⭐ {aluno['pontos']} pontos | 📰 {aluno['fake_acertos']} | 🛡️ {aluno['cyber_acertos']} | ⚖️ {aluno['etica_acertos']}</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.divider()
    
    # ========== GRÁFICO DE DESEMPENHO POR ALUNO ==========
    st.subheader("📈 Desempenho por Aluno")
    
    dados_alunos = pd.DataFrame([
        {"Aluno": a['nome'], "Pontos": a['pontos']}
        for a in alunos
    ])
    st.bar_chart(dados_alunos.set_index('Aluno'))
    
    st.divider()
    
    # ========== ESTATÍSTICAS AVANÇADAS ==========
    st.subheader("📊 Estatísticas Avançadas")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 📰 Fake News")
        if total_fake > 0:
            st.write(f"• Total de acertos: {total_fake}")
            st.write(f"• Média por aluno: {total_fake/total_alunos:.1f}")
            st.write(f"• Maior acerto: {max([a['fake_acertos'] for a in alunos])}")
        else:
            st.write("Nenhum acerto ainda.")
        
        st.markdown("### 🛡️ Cyberbullying")
        if total_cyber > 0:
            st.write(f"• Total de acertos: {total_cyber}")
            st.write(f"• Média por aluno: {total_cyber/total_alunos:.1f}")
            st.write(f"• Maior acerto: {max([a['cyber_acertos'] for a in alunos])}")
        else:
            st.write("Nenhum acerto ainda.")
    
    with col2:
        st.markdown("### ⚖️ Ética Digital")
        if total_etica > 0:
            st.write(f"• Total de acertos: {total_etica}")
            st.write(f"• Média por aluno: {total_etica/total_alunos:.1f}")
            st.write(f"• Maior acerto: {max([a['etica_acertos'] for a in alunos])}")
        else:
            st.write("Nenhum acerto ainda.")
        
        st.markdown("### 🏆 Destaques")
        if alunos:
            melhor_aluno = alunos[0]
            st.write(f"• Melhor aluno: {melhor_aluno['nome']}")
            st.write(f"• Pontos: {melhor_aluno['pontos']}")
            st.write(f"• Posição: 1º lugar")
    
    st.divider()
    
    # ========== EXPORTAR RELATÓRIO ==========
    st.subheader("📥 Exportar Estatísticas")
    
    if st.button("📄 Gerar Relatório da Turma", key="gerar_relatorio_turma"):
        relatorio = f"""
==================================================
   📊 ESTATÍSTICAS DA TURMA
==================================================
🏫 Turma: {turma_selecionada}
📅 Data: {datetime.now().strftime('%d/%m/%Y %H:%M')}
==================================================

📈 VISÃO GERAL:
   👥 Total de Alunos: {total_alunos}
   ⭐ Total de Pontos: {total_pontos}
   📊 Média de Pontos: {media_pontos:.1f}
   📰 Fake News: {total_fake}
   🛡️ Cyberbullying: {total_cyber}
   ⚖️ Ética Digital: {total_etica}

🏆 RANKING DA TURMA:
"""
        # 🔥 CRIA a variável ANTES do for
        relatorio = ""
        relatorio += "=" * 55 + "\n"
        relatorio += "   📊 ESTATÍSTICAS DA TURMA\n"
        relatorio += "=" * 55 + "\n"
        relatorio += f"🏫 Turma: {turma_selecionada}\n"
        relatorio += f"📅 Data: {datetime.now().strftime('%d/%m/%Y %H:%M')}\n"
        relatorio += "=" * 55 + "\n\n"
        relatorio += "🏆 RANKING DA TURMA:\n"
        
        # 🔥 ADICIONA os alunos DENTRO do for
        for i, aluno in enumerate(alunos, 1):
            relatorio += f"   {i}º - {aluno['nome']} - ⭐ {aluno['pontos']} pontos\n"
        
        # 🔥 FECHA o relatório DEPOIS do for
        relatorio += "\n"
        relatorio += "=" * 55 + "\n"
        relatorio += "   EEEF PROFª ODETE MENDES N OLIVEIRA\n"
        relatorio += "   Professor: Irving Vasconcelos dos Santos (CICI)\n"
        relatorio += "=" * 55 + "\n"
        
        st.download_button(
            label="📥 Baixar Relatório",
            data=relatorio,
            file_name=f"estatisticas_{turma_selecionada.replace(' ', '_')}.txt",
            mime="text/plain"
        )
        st.success("✅ Relatório gerado!")
# ========== DINÂMICAS ==========
elif menu == "🎮 Dinâmicas":
    st.title("🎮 Dinâmicas de Sala de Aula")
    
    st.info("🎯 Atividades práticas para envolver os alunos usando o sistema!")
    
    st.divider()
    
    # ========== LISTA DE DINÂMICAS ==========
    dinamicas = {
        "🏆 Gincana Digital": {
            "objetivo": "Competição entre equipes para testar conhecimentos",
            "duracao": "1 aula (50 min)",
            "materiais": "Computadores ou celulares, sistema Cidadania Digital",
            "passos": [
                "Dividir a turma em 4 equipes",
                "Cada equipe escolhe um nome",
                "Professor abre o sistema na página Fake News",
                "Cada equipe responde 5 perguntas (1 minuto cada)",
                "Anotar os pontos de cada equipe",
                "A equipe com mais pontos ganha!"
            ],
            "premiacao": "🥇 Certificado 'Mestres da Cidadania Digital'",
            "modulo": "📰 Fake News + 🛡️ Cyberbullying"
        },
        "🎭 Teatro de Fake News": {
            "objetivo": "Dramatizar casos de fake news para entender as consequências",
            "duracao": "1 aula (50 min)",
            "materiais": "Roupas, cartazes, celular para gravar",
            "passos": [
                "Dividir a turma em grupos de 4 alunos",
                "Cada grupo escolhe uma fake news",
                "Criar um roteiro de 5 cenas",
                "Ensaiar por 15 minutos",
                "Apresentar para a turma",
                "Debater sobre o que aprenderam"
            ],
            "premiacao": "🎭 Certificado 'Artistas da Verdade'",
            "modulo": "🎨 Campanha Ética"
        },
        "🔍 Caça ao Fake": {
            "objetivo": "Identificar fake news reais na internet",
            "duracao": "30 min",
            "materiais": "Celulares ou computadores, folha de registro",
            "passos": [
                "Dividir a turma em duplas",
                "Cada dupla pesquisa 5 notícias na internet",
                "Usar o Fluxograma Anti-Fake News para verificar",
                "Anotar os resultados na folha",
                "Compartilhar as descobertas com a turma"
            ],
            "premiacao": "🔍 Certificado 'Detetives da Verdade'",
            "modulo": "📝 Fluxograma Anti-Fake News"
        },
        "🎨 Mural Colaborativo": {
            "objetivo": "Criar um mural sobre Cidadania Digital",
            "duracao": "1 aula (50 min)",
            "materiais": "Cartolina, canetões, post-its, Canva",
            "passos": [
                "Dividir a turma em grupos",
                "Cada grupo cria um post/meme sobre um tema",
                "Montar o mural na sala ou corredor",
                "Apresentar para a escola",
                "Tirar fotos e compartilhar"
            ],
            "premiacao": "🎨 Certificado 'Comunicadores Digitais'",
            "modulo": "🎨 Campanha Ética"
        },
        "🎤 Júri Simulado": {
            "objetivo": "Simular um julgamento de um caso de cyberbullying",
            "duracao": "1 aula (50 min)",
            "materiais": "Roupas, martelo de brinquedo, cartazes",
            "passos": [
                "Escolher um caso de cyberbullying",
                "Distribuir os papéis: Juiz, Advogados, Jurados, Testemunhas",
                "Cada parte prepara seus argumentos",
                "Simular o julgamento",
                "Jurados decidem o veredito",
                "Debater sobre a decisão"
            ],
            "premiacao": "🎤 Certificado 'Guardiões da Justiça'",
            "modulo": "⚖️ Ética Digital"
        },
        "📊 Gráfico Humano": {
            "objetivo": "Representar dados com o corpo",
            "duracao": "30 min",
            "materiais": "Espaço livre, perguntas",
            "passos": [
                "Professor faz uma pergunta (ex: Quem usa TikTok?)",
                "Alunos se posicionam em fileiras",
                "Formar um gráfico humano",
                "Registrar os dados no sistema",
                "Analisar os resultados"
            ],
            "premiacao": "📊 Certificado 'Estatísticos Digitais'",
            "modulo": "📊 Calculadora de Impacto"
        },
        "🎬 Criação de Vídeo": {
            "objetivo": "Produzir um vídeo sobre Cidadania Digital",
            "duracao": "2 aulas (100 min)",
            "materiais": "Celular, CapCut, TikTok",
            "passos": [
                "Dividir a turma em grupos",
                "Escolher um tema",
                "Criar o roteiro (1 minuto)",
                "Gravar o vídeo",
                "Editar no CapCut",
                "Apresentar para a turma"
            ],
            "premiacao": "🎬 Certificado 'Produtores de Conteúdo'",
            "modulo": "🎨 Campanha Ética"
        },
        "🎲 Quiz Relâmpago": {
            "objetivo": "Testar conhecimentos rapidamente",
            "duracao": "15 min",
            "materiais": "Placas verde/vermelha, perguntas",
            "passos": [
                "Professor faz uma pergunta",
                "Alunos levantam a placa (Verdade/Fake)",
                "Quem acertar ganha 1 ponto",
                "Quem errar sai da rodada",
                "O último que ficar ganha!"
            ],
            "premiacao": "🎲 Certificado 'Mestre do Quiz'",
            "modulo": "📰 Fake News"
        }
    }
    
    # ========== EXIBIR DINÂMICAS (SIMPLIFICADO) ==========
    for nome, info in dinamicas.items():
        with st.expander(f"{nome} - {info['duracao']}"):
            st.write(f"**🎯 Objetivo:** {info['objetivo']}")
            st.write(f"**⏰ Duração:** {info['duracao']}")
            st.write(f"**📦 Materiais:** {info['materiais']}")
            st.write(f"**📌 Módulo:** {info['modulo']}")
            st.write(f"**🏆 Premiação:** {info['premiacao']}")
            
            st.write("**📝 Passo a Passo:**")
            for i, passo in enumerate(info['passos'], 1):
                st.write(f"{i}. {passo}")
    
    st.divider()
    
    # ========== CRONOGRAMA ==========
    st.subheader("📅 Cronograma Sugerido")
    
    import pandas as pd
    cronograma = [
        {"Semana": "1", "Dinâmica": "🏆 Gincana Digital", "Duração": "1 aula"},
        {"Semana": "2", "Dinâmica": "🎭 Teatro de Fake News", "Duração": "1 aula"},
        {"Semana": "3", "Dinâmica": "🔍 Caça ao Fake", "Duração": "30 min"},
        {"Semana": "4", "Dinâmica": "🎨 Mural Colaborativo", "Duração": "1 aula"},
        {"Semana": "5", "Dinâmica": "🎤 Júri Simulado", "Duração": "1 aula"},
        {"Semana": "6", "Dinâmica": "📊 Gráfico Humano", "Duração": "30 min"},
        {"Semana": "7", "Dinâmica": "🎬 Criação de Vídeo", "Duração": "2 aulas"},
        {"Semana": "8", "Dinâmica": "🎲 Quiz Relâmpago", "Duração": "15 min"},
    ]
    df_cronograma = pd.DataFrame(cronograma)
    st.dataframe(df_cronograma, use_container_width=True)
    
    st.divider()
    
    # ========== DICAS PARA O PROFESSOR ==========
    st.subheader("💡 Dicas para o Professor")
    
    st.write("**📌 ANTES DA DINÂMICA:**")
    st.write("- ✅ Prepare o material com antecedência")
    st.write("- ✅ Teste o sistema no computador")
    st.write("- ✅ Divida a turma em grupos equilibrados")
    st.write("- ✅ Explique as regras claramente")
    
    st.write("**📌 DURANTE A DINÂMICA:**")
    st.write("- ✅ Circule pela sala e ajude os grupos")
    st.write("- ✅ Mantenha o tempo controlado")
    st.write("- ✅ Incentive a participação de todos")
    st.write("- ✅ Registre os momentos importantes")
    
    st.write("**📌 DEPOIS DA DINÂMICA:**")
    st.write("- ✅ Promova um debate sobre o que aprenderam")
    st.write("- ✅ Registre os resultados no sistema")
    st.write("- ✅ Parabenize os alunos pelo esforço")
    st.write("- ✅ Planeje a próxima dinâmica")
    
    # ========== MENSAGEM FINAL ==========
    st.markdown("""
    <div style='text-align: center; padding: 30px; background: linear-gradient(135deg, #1a3a5c, #2d5f8a); border-radius: 15px; color: white;'>
        <h1>🎮 DINÂMICAS EDUCACIONAIS</h1>
        <p>Aprender brincando é mais divertido!</p>
        <p>Use estas dinâmicas para envolver seus alunos!</p>
        <h2>🌟👨‍🏫🌟</h2>
    </div>
    """, unsafe_allow_html=True)

# ========== EQUIPES (GINCANA) ==========
elif menu == "🏆 Equipes":
    st.title("🏆 Gincana Digital - Equipes")
    
    tab1, tab2, tab3 = st.tabs(["📋 Listar Equipes", "➕ Criar Equipe", "🎮 Gincana"])
    
    with tab1:
        st.subheader("📋 Equipes Cadastradas")
        
        equipes = listar_equipes()
        if equipes:
            for equipe in equipes:
                col1, col2, col3 = st.columns([2, 1, 1])
                with col1:
                    st.write(f"**{equipe['nome']}** - {equipe['turma']}")
                with col2:
                    st.write(f"⭐ {equipe['pontos']} pontos")
                with col3:
                    if st.button(f"🗑️", key=f"del_equipe_{equipe['id']}"):
                        excluir_equipe(equipe['id'])
                        st.rerun()
        else:
            st.info("📭 Nenhuma equipe cadastrada.")
    
    with tab2:
        st.subheader("➕ Criar Nova Equipe")
        
        with st.form("form_criar_equipe"):
            nome_equipe = st.text_input("👥 Nome da Equipe:")
            turma_equipe = st.selectbox("🏫 Turma:", buscar_todas_turmas())
            
            if st.form_submit_button("💾 Criar Equipe"):
                if nome_equipe and turma_equipe:
                    criar_equipe(nome_equipe, turma_equipe)
                    st.success(f"✅ Equipe {nome_equipe} criada!")
                    st.rerun()
                else:
                    st.error("❌ Preencha todos os campos!")
    
    with tab3:
        st.subheader("🎮 Gincana Digital")
        
        equipes = listar_equipes()
        if not equipes:
            st.warning("⚠️ Crie equipes primeiro!")
            st.stop()
        
        # Escolher equipe
        opcoes_equipes = {f"{e['nome']} ({e['pontos']} pts)": e['id'] for e in equipes}
        equipe_selecionada = st.selectbox("🎯 Escolha a equipe:", list(opcoes_equipes.keys()))
        
        # Pontos
        pontos = st.number_input("⭐ Pontos a adicionar:", min_value=1, max_value=10, value=1)
        
        if st.button("✅ Adicionar Pontos"):
            adicionar_pontos_equipe(opcoes_equipes[equipe_selecionada], pontos)
            st.success(f"✅ +{pontos} pontos para {equipe_selecionada}!")
            st.rerun()
        
        st.divider()
        
        # Ranking
        st.subheader("🏆 Ranking das Equipes")
        equipes_atualizadas = listar_equipes()
        for i, equipe in enumerate(equipes_atualizadas, 1):
            medalha = "🥇" if i == 1 else "🥈" if i == 2 else "🥉" if i == 3 else f"{i}º"
            st.write(f"{medalha} {equipe['nome']} - ⭐ {equipe['pontos']} pontos")

# ========== MATEMÁTICA DA CIDADANIA ==========
elif menu == "📐 Matemática da Cidadania":
    st.title("📐 Matemática da Cidadania")
    
    st.info("""
    🎯 **O QUE É ISSO?**
    
    Atividades que unem **Matemática** e **Cidadania Digital**!
    Baseado na **BNCC** - Anos Finais do Ensino Fundamental.
    """)
    
    st.divider()
    
    # ========== TABS ==========
    tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
        "📊 Frações e Percentuais",
        "📈 Estatística",
        "📐 Ângulos e Polígonos",
        "🎲 Probabilidade",
        "📉 Funções e Gráficos",
        "🧮 Números Racionais"
    ])
    
    # ========== TAB 1: FRAÇÕES E PERCENTUAIS ==========
    with tab1:
        st.subheader("📊 Frações e Percentuais na Cidadania Digital")
        
        # Atividade 1: Tempo de Tela
        st.markdown("### 📱 Atividade 1: Tempo de Tela")
        st.write("Calcule a fração e o percentual do dia gasto em cada atividade.")
        
        col1, col2 = st.columns(2)
        with col1:
            horas_redes = st.number_input("Horas em redes sociais:", min_value=0.0, max_value=24.0, value=3.0, step=0.5)
            horas_estudo = st.number_input("Horas de estudo:", min_value=0.0, max_value=24.0, value=2.0, step=0.5)
        with col2:
            horas_sono = st.number_input("Horas de sono:", min_value=0.0, max_value=24.0, value=8.0, step=0.5)
            horas_outras = st.number_input("Outras atividades:", min_value=0.0, max_value=24.0, value=11.0, step=0.5)
        
        if st.button("Calcular Frações e Percentuais", key="calc_fracoes"):
            total = horas_redes + horas_estudo + horas_sono + horas_outras
            
            if total > 0:
                st.success(f"✅ Total de horas: {total:.1f}h")
                
                dados = {
                    "📱 Redes Sociais": horas_redes,
                    "📚 Estudo": horas_estudo,
                    "😴 Sono": horas_sono,
                    "🏃 Outras": horas_outras
                }
                
                for atividade, horas in dados.items():
                    if horas > 0:
                        fracao = horas / 24
                        percentual = (horas / 24) * 100
                        st.write(f"**{atividade}:** {horas:.1f}h = {horas:.1f}/24 = {fracao:.4f} = {percentual:.2f}%")
                
                st.info(f"🧮 **Verificação:** Soma das frações = {total/24:.4f} (deve ser 1.0000)")
            else:
                st.warning("⚠️ Digite valores maiores que zero!")
        
        st.divider()
        
        # Atividade 2: Fake News
        st.markdown("### 📰 Atividade 2: Razão e Proporção - Fake News")
        st.write("Calcule a razão entre fake news e notícias verdadeiras.")
        
        col1, col2 = st.columns(2)
        with col1:
            fake = st.number_input("Fake News:", min_value=0, value=30, key="fake_frac")
            verdadeiras = st.number_input("Notícias Verdadeiras:", min_value=0, value=70, key="verdadeiras_frac")
        with col2:
            total_noticias = fake + verdadeiras
            st.metric("Total de Notícias", total_noticias)
        
        if st.button("Calcular Razão", key="calc_razao"):
            if total_noticias > 0:
                razao = fake / verdadeiras if verdadeiras > 0 else 0
                percentual_fake = (fake / total_noticias) * 100
                percentual_verdade = (verdadeiras / total_noticias) * 100
                
                st.success(f"📊 **RAZÃO:** {fake}/{verdadeiras} = {razao:.4f}")
                st.write(f"**Proporção:** {fake} está para {verdadeiras}")
                st.write(f"**Percentual de Fake News:** {percentual_fake:.2f}%")
                st.write(f"**Percentual de Verdadeiras:** {percentual_verdade:.2f}%")
                
                if percentual_fake > 50:
                    st.error("🚨 ALERTA: Mais de 50% são fake news! Cuidado!")
                elif percentual_fake > 30:
                    st.warning("⚠️ Atenção: 30% são fake news!")
                else:
                    st.success("✅ Bom! Menos de 30% são fake news.")
            else:
                st.warning("⚠️ Total de notícias deve ser maior que zero!")
    
    # ========== TAB 2: ESTATÍSTICA ==========
    with tab2:
        st.subheader("📈 Estatística na Cidadania Digital")
        
        # Atividade 1: Média, Mediana e Moda
        st.markdown("### 📊 Atividade 1: Média, Mediana e Moda - Cyberbullying")
        st.write("Digite os casos de cyberbullying por mês:")
        
        meses = ["Jan", "Fev", "Mar", "Abr", "Mai", "Jun", "Jul", "Ago", "Set", "Out", "Nov", "Dez"]
        casos = []
        
        cols = st.columns(4)
        for i, mes in enumerate(meses):
            with cols[i % 4]:
                valor = st.number_input(f"{mes}:", min_value=0, value=0, key=f"caso_{mes}")
                casos.append(valor)
        
        if st.button("Calcular Estatísticas", key="calc_estatistica"):
            if sum(casos) > 0:
                import statistics
                media = statistics.mean(casos)
                mediana = statistics.median(casos)
                
                try:
                    moda = statistics.mode(casos)
                except:
                    moda = "Não há moda"
                
                st.success("📊 **RESULTADOS:**")
                st.write(f"**Média:** {media:.2f} casos/mês")
                st.write(f"**Mediana:** {mediana:.2f}")
                st.write(f"**Moda:** {moda}")
                st.write(f"**Total no ano:** {sum(casos)} casos")
                st.write(f"**Maior valor:** {max(casos)}")
                st.write(f"**Menor valor:** {min(casos)}")
                st.write(f"**Amplitude:** {max(casos) - min(casos)}")
            else:
                st.warning("⚠️ Digite alguns valores!")
        
        st.divider()
        
        # Atividade 2: Tabela de Frequência
        st.markdown("### 📊 Atividade 2: Tabela de Frequência - Tipos de Bullying")
        
        tipos = ["Xingamento", "Exclusão", "Ameaça", "Difamação", "Outros"]
        frequencias = []
        
        cols = st.columns(5)
        for i, tipo in enumerate(tipos):
            with cols[i]:
                freq = st.number_input(f"{tipo}:", min_value=0, value=0, key=f"freq_{tipo}")
                frequencias.append(freq)
        
        if st.button("Gerar Tabela", key="calc_tabela"):
            total = sum(frequencias)
            if total > 0:
                import pandas as pd
                df = pd.DataFrame({
                    'Tipo': tipos,
                    'Frequência': frequencias,
                    'Freq. Relativa': [f"{f/total:.4f}" for f in frequencias],
                    'Percentual': [f"{(f/total)*100:.2f}%" for f in frequencias]
                })
                st.dataframe(df, use_container_width=True)
                st.write(f"**TOTAL:** {total}")
            else:
                st.warning("⚠️ Digite alguns valores!")
    
    # ========== TAB 3: ÂNGULOS E POLÍGONOS ==========
    with tab3:
        st.subheader("📐 Ângulos e Polígonos na Cidadania Digital")
        
        # Atividade 1: Gráfico de Setores (Ângulos)
        st.markdown("### 📊 Atividade 1: Gráfico de Setores - Ângulos")
        st.write("Calcule os ângulos do gráfico de pizza para cada categoria.")
        
        categorias = ["Fake News", "Cyberbullying", "Ética Digital", "Privacidade", "Segurança"]
        valores = []
        
        cols = st.columns(5)
        for i, cat in enumerate(categorias):
            with cols[i]:
                val = st.number_input(f"{cat}:", min_value=0, value=0, key=f"cat_{cat}")
                valores.append(val)
        
        if st.button("Calcular Ângulos", key="calc_angulos"):
            total = sum(valores)
            if total > 0:
                st.success("📐 **ÂNGULOS CALCULADOS:**")
                for cat, val in zip(categorias, valores):
                    if val > 0:
                        angulo = (val / total) * 360
                        st.write(f"**{cat}:** {val}/{total} = {val/total:.4f} → {angulo:.2f}°")
                
                st.info(f"🧮 **Verificação:** Soma dos ângulos = 360°")
            else:
                st.warning("⚠️ Digite alguns valores!")
        
        st.divider()
        
        # Atividade 2: Polígonos de Segurança
        st.markdown("### 🔐 Atividade 2: Polígonos de Segurança")
        st.write("Cada camada de segurança é um polígono:")
        
        poligonos = {
            "🔺 Senha Forte": "Triângulo (3 lados)",
            "🟦 2FA": "Quadrado (4 lados)",
            "⬡ Antivírus": "Pentágono (5 lados)",
            "⭐ Criptografia": "Hexágono (6 lados)"
        }
        
        for nome, desc in poligonos.items():
            st.write(f"**{nome}:** {desc}")
        
        st.info("""
        🧮 **SOMA DOS ÂNGULOS INTERNOS:**
        - Triângulo: 180°
        - Quadrado: 360°
        - Pentágono: 540°
        - Hexágono: 720°
        
        **Fórmula:** S = (n - 2) × 180°
        """)
        
        # Calculadora de Polígonos
        st.markdown("### 🧮 Calculadora de Polígonos")
        n_lados = st.number_input("Número de lados:", min_value=3, max_value=20, value=3, key="n_lados")
        
        if n_lados >= 3:
            soma_angulos = (n_lados - 2) * 180
            angulo_interno = soma_angulos / n_lados
            
            st.success(f"📐 **POLÍGONO DE {n_lados} LADOS:**")
            st.write(f"**Soma dos ângulos internos:** {soma_angulos}°")
            st.write(f"**Cada ângulo interno:** {angulo_interno:.2f}°")
            
            if n_lados == 3:
                st.info("🔺 Triângulo - Nível 1 de Segurança")
            elif n_lados == 4:
                st.info("🟦 Quadrado - Nível 2 de Segurança")
            elif n_lados == 5:
                st.info("⬡ Pentágono - Nível 3 de Segurança")
            elif n_lados == 6:
                st.info("⭐ Hexágono - Nível 4 de Segurança")
            else:
                st.info(f"🔐 Polígono de {n_lados} lados - Nível {n_lados - 2} de Segurança")
    
    # ========== TAB 4: PROBABILIDADE ==========
    with tab4:
        st.subheader("🎲 Probabilidade na Cidadania Digital")
        
        st.markdown("### 🎲 Atividade: Probabilidade de Fake News")
        st.write("Calcule a probabilidade de receber uma fake news.")
        
        col1, col2 = st.columns(2)
        with col1:
            total_mensagens = st.number_input("Total de mensagens recebidas:", min_value=1, value=100, key="total_msg")
            fake_recebidas = st.number_input("Fake news recebidas:", min_value=0, value=30, key="fake_recebidas")
        with col2:
            verdadeiras = total_mensagens - fake_recebidas
            st.metric("Mensagens Verdadeiras", verdadeiras)
        
        if st.button("Calcular Probabilidade", key="calc_prob"):
            if total_mensagens > 0:
                prob_fake = fake_recebidas / total_mensagens
                prob_verdade = verdadeiras / total_mensagens
                
                st.success("🎲 **PROBABILIDADES:**")
                st.write(f"**P(Fake News) =** {fake_recebidas}/{total_mensagens} = {prob_fake:.4f} = {prob_fake*100:.2f}%")
                st.write(f"**P(Verdadeira) =** {verdadeiras}/{total_mensagens} = {prob_verdade:.4f} = {prob_verdade*100:.2f}%")
                st.write(f"**Soma das probabilidades:** {prob_fake + prob_verdade:.4f} (deve ser 1.0000)")
                
                if prob_fake > 0.5:
                    st.error("🚨 ALTA probabilidade de receber fake news!")
                elif prob_fake > 0.3:
                    st.warning("⚠️ MÉDIA probabilidade de receber fake news!")
                else:
                    st.success("✅ BAIXA probabilidade de receber fake news!")
    
    # ========== TAB 5: FUNÇÕES E GRÁFICOS ==========
    with tab5:
        st.subheader("📉 Funções e Gráficos na Cidadania Digital")
        
        st.markdown("### 📈 Atividade: Evolução dos Pontos")
        st.write("Acompanhe a evolução dos seus pontos ao longo do tempo.")
        
        dias = ["Seg", "Ter", "Qua", "Qui", "Sex", "Sáb", "Dom"]
        pontos = []
        
        cols = st.columns(7)
        for i, dia in enumerate(dias):
            with cols[i]:
                p = st.number_input(f"{dia}:", min_value=0, value=0, key=f"ponto_{dia}")
                pontos.append(p)
        
        if st.button("Gerar Gráfico", key="calc_grafico"):
            if sum(pontos) > 0:
                import pandas as pd
                df = pd.DataFrame({"Dia": dias, "Pontos": pontos})
                st.line_chart(df.set_index("Dia"))
                
                total = sum(pontos)
                media = total / len(pontos)
                crescimento = pontos[-1] - pontos[0]
                percentual_crescimento = (crescimento / pontos[0] * 100) if pontos[0] > 0 else 0
                
                st.success("📊 **ANÁLISE:**")
                st.write(f"**Total de pontos:** {total}")
                st.write(f"**Média diária:** {media:.2f}")
                st.write(f"**Crescimento:** {crescimento:+d} pontos")
                st.write(f"**Percentual de crescimento:** {percentual_crescimento:+.2f}%")
            else:
                st.warning("⚠️ Digite alguns valores!")
    
    # ========== TAB 6: NÚMEROS RACIONAIS ==========
    with tab6:
        st.subheader("🧮 Números Racionais na Cidadania Digital")
        
        st.markdown("### 🔢 Atividade: Frações, Decimais e Porcentagens")
        
        col1, col2 = st.columns(2)
        with col1:
            numerador = st.number_input("Numerador:", min_value=0, value=3, key="numerador")
            denominador = st.number_input("Denominador:", min_value=1, value=4, key="denominador")
        with col2:
            if denominador > 0:
                decimal = numerador / denominador
                percentual = decimal * 100
                st.metric("Decimal", f"{decimal:.4f}")
                st.metric("Percentual", f"{percentual:.2f}%")
        
        if st.button("Calcular", key="calc_racionais"):
            if denominador > 0:
                st.success("🧮 **REPRESENTAÇÕES:**")
                st.write(f"**Fração:** {numerador}/{denominador}")
                st.write(f"**Decimal:** {decimal:.4f}")
                st.write(f"**Percentual:** {percentual:.2f}%")
                st.write(f"**Fração simplificada:** {numerador//__import__('math').gcd(numerador, denominador)}/{denominador//__import__('math').gcd(numerador, denominador)}")
                
                # Contexto de Cidadania Digital
                st.info(f"""
                💡 **APLICAÇÃO NA CIDADANIA DIGITAL:**
                
                Se {numerador} em cada {denominador} mensagens são fake news,
                isso representa {percentual:.1f}% das mensagens!
                """)
            else:
                st.warning("⚠️ Denominador não pode ser zero!")

# ========== DASHBOARD (INCREMENTADO) ==========
elif menu == "📊 Painel":
    st.title("📊 Dashboard de Desempenho")
    
    alunos = buscar_todos_alunos()
    
    if not alunos:
        st.warning("📭 Nenhum aluno cadastrado ainda.")
        st.stop()
    
    # ========== MÉTRICAS GERAIS ==========
    st.subheader("📈 Métricas Gerais")
    
    total_alunos = len(alunos)
    total_pontos = sum([a['pontos'] for a in alunos])
    media_pontos = total_pontos / total_alunos if total_alunos > 0 else 0
    total_fake = sum([a['fake_acertos'] for a in alunos])
    total_cyber = sum([a['cyber_acertos'] for a in alunos])
    total_etica = sum([a['etica_acertos'] for a in alunos])
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("👥 Total de Alunos", total_alunos)
    with col2:
        st.metric("⭐ Total de Pontos", total_pontos)
    with col3:
        st.metric("📊 Média de Pontos", f"{media_pontos:.1f}")
    with col4:
        st.metric("✅ Total de Acertos", total_fake + total_cyber + total_etica)
    
    st.divider()
    
    # ========== GRÁFICOS ==========
    import pandas as pd
    import plotly.express as px
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📊 Acertos por Categoria")
        df_categoria = pd.DataFrame({
            'Categoria': ['📰 Fake News', '🛡️ Cyberbullying', '⚖️ Ética Digital'],
            'Acertos': [total_fake, total_cyber, total_etica]
        })
        fig = px.pie(df_categoria, values='Acertos', names='Categoria', 
                     color_discrete_sequence=['#ffc107', '#dc3545', '#28a745'],
                     title='Distribuição de Acertos')
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.subheader("📊 Pontos por Turma")
        turmas = {}
        for a in alunos:
            if a['turma'] not in turmas:
                turmas[a['turma']] = 0
            turmas[a['turma']] += a['pontos']
        df_turmas = pd.DataFrame([{"Turma": t, "Pontos": p} for t, p in turmas.items()])
        fig = px.bar(df_turmas, x='Turma', y='Pontos', color='Pontos',
                     color_continuous_scale='Blues',
                     title='Pontos por Turma')
        st.plotly_chart(fig, use_container_width=True)
    
    st.divider()
    
    # ========== GRÁFICO DE RADAR (POLÍGONO DE DESEMPENHO) ==========
    st.subheader("📊 Polígono de Desempenho (Radar)")
    
    # Calcular médias por categoria
    media_fake = total_fake / total_alunos if total_alunos > 0 else 0
    media_cyber = total_cyber / total_alunos if total_alunos > 0 else 0
    media_etica = total_etica / total_alunos if total_alunos > 0 else 0
    media_pontos = media_pontos
    
    # Criar gráfico de radar
    categorias_radar = ['Fake News', 'Cyberbullying', 'Ética Digital', 'Pontos', 'Participação']
    valores_radar = [
        min(media_fake / 5 * 100, 100),  # Normalizar para 0-100
        min(media_cyber / 5 * 100, 100),
        min(media_etica / 3 * 100, 100),
        min(media_pontos / 20 * 100, 100),
        75  # Participação fixa (exemplo)
    ]
    
    fig_radar = px.line_polar(
        r=valores_radar,
        theta=categorias_radar,
        line_close=True,
        title='Polígono de Desempenho da Turma',
        color_discrete_sequence=['#1a3a5c']
    )
    fig_radar.update_traces(fill='toself')
    st.plotly_chart(fig_radar, use_container_width=True)
    
    st.divider()

    # ========== GRÁFICO POR DISCIPLINA ==========
    st.subheader("📊 Desempenho por Disciplina")
    
    # Calcular acertos por disciplina (aproximado)
    # Cidadania Digital = fake + cyber + etica
    # Matemática = parte das perguntas de fake
    # Ed. Física = parte das perguntas de fake/etica
    
    total_acertos = total_fake + total_cyber + total_etica
    total_possivel = total_alunos * 13  # 5 fake + 5 cyber + 3 etica
    
    # Estimativa: 60% cidadania, 20% matemática, 20% ed. física
    acertos_cidadania = total_acertos
    acertos_matematica = int(total_acertos * 0.20)
    acertos_ef = int(total_acertos * 0.15)
    
    percentual_cidadania = (acertos_cidadania / total_possivel * 100) if total_possivel > 0 else 0
    percentual_matematica = (acertos_matematica / (total_possivel * 0.25) * 100) if total_possivel > 0 else 0
    percentual_ef = (acertos_ef / (total_possivel * 0.20) * 100) if total_possivel > 0 else 0
    
    # Mostrar métricas
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("🌐 Cidadania Digital", f"{acertos_cidadania} acertos", f"{percentual_cidadania:.0f}%")
    with col2:
        st.metric("🧮 Matemática", f"{acertos_matematica} acertos", f"{percentual_matematica:.0f}%")
    with col3:
        st.metric("🏃 Ed. Física", f"{acertos_ef} acertos", f"{percentual_ef:.0f}%")
    
    # Gráfico de barras
    import pandas as pd
    
    dados_disciplinas = pd.DataFrame({
        'Disciplina': ['🌐 Cidadania', '🧮 Matemática', '🏃 Ed. Física'],
        'Acertos': [acertos_cidadania, acertos_matematica, acertos_ef]
    })
    
    st.bar_chart(dados_disciplinas.set_index('Disciplina'))
    
    st.divider()
    
    # ========== GRÁFICO DE BARRAS - TOP 10 ==========
    st.subheader("🏆 Top 10 Alunos")
    
    top_alunos = sorted(alunos, key=lambda x: x['pontos'], reverse=True)[:10]
    df_top = pd.DataFrame([{"Aluno": a['nome'], "Pontos": a['pontos']} for a in top_alunos])
    fig = px.bar(df_top, x='Aluno', y='Pontos', color='Pontos',
                 color_continuous_scale='Greens',
                 title='Top 10 Alunos')
    st.plotly_chart(fig, use_container_width=True)
    
    st.divider()
    
    # ========== TABELA DETALHADA ==========
    st.subheader("📋 Tabela Detalhada")
    df = pd.DataFrame([{
        'Nome': a['nome'],
        'Turma': a['turma'],
        'Pontos': a['pontos'],
        'Fake News': a['fake_acertos'],
        'Cyberbullying': a['cyber_acertos'],
        'Ética Digital': a['etica_acertos']
    } for a in alunos])
    st.dataframe(df, use_container_width=True)
    
    st.divider()
    
    # ========== ESTATÍSTICAS MATEMÁTICAS ==========
    st.subheader("📐 Estatísticas Matemáticas")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("📊 Média", f"{media_pontos:.2f}")
    with col2:
        import statistics
        mediana = statistics.median([a['pontos'] for a in alunos])
        st.metric("📊 Mediana", f"{mediana:.2f}")
    with col3:
        try:
            moda = statistics.mode([a['pontos'] for a in alunos])
            st.metric("📊 Moda", f"{moda}")
        except:
            st.metric("📊 Moda", "Não há")

# ========== GERENCIAR PONTOS ==========
elif menu == "⚙️ Gerenciar Pontos":
    st.title("⚙️ Gerenciar Pontos")
    
    st.markdown("""
    <div class="card card-ethic">
        <h4>🎯 O QUE É ISSO?</h4>
        <p>Aqui você pode <strong>zerar os pontos</strong> dos alunos!</p>
        <p>Use quando quiser começar uma nova rodada de atividades.</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.divider()
    
    # ========== ZERAR SESSÃO ATUAL ==========
    st.subheader("🔄 Zerar Sessão Atual")
    
    st.warning("⚠️ Isso vai zerar os pontos da SESSÃO ATUAL (memória temporária).")
    
    if st.button("🔄 Zerar Sessão Atual", key="zerar_sessao"):
        zerar_sessao()
        st.success("✅ Sessão atual zerada!")
        st.rerun()
    
    st.divider()
    
        # ========== ZERAR PONTOS NO BANCO ==========
    st.subheader("🗄️ Zerar Pontos no Banco de Dados")
    st.error("⚠️ Isso vai zerar os pontos de TODOS os alunos no BANCO DE DADOS.")
    
    # 🔥 CHECKBOX DE CONFIRMAÇÃO
    confirmar = st.checkbox("⚠️ Confirmo que quero zerar TODOS os pontos", key="confirmar_zerar")
    
    turmas = buscar_todas_turmas()
    
    if turmas:
        opcao_turma = st.selectbox(
            "🏫 Escolha a turma:",
            ["Todas as turmas"] + turmas,
            key="turma_zerar"
        )
        
        if opcao_turma == "Todas as turmas":
            if st.button("🗑️ ZERAR TODOS OS PONTOS", key="zerar_todos", disabled=not confirmar):
                conn = get_connection()
                cursor = conn.cursor()
                cursor.execute("""
                    UPDATE alunos 
                    SET pontos = 0, fake_acertos = 0, cyber_acertos = 0, 
                        etica_acertos = 0, total_perguntas = 0
                """)
                conn.commit()
                linhas = cursor.rowcount
                conn.close()
                
                st.success(f"✅ {linhas} alunos zerados!")
        else:
            if st.button(f"🗑️ ZERAR PONTOS DA {opcao_turma.upper()}", key="zerar_turma", disabled=not confirmar):
                conn = get_connection()
                cursor = conn.cursor()
                cursor.execute("""
                    UPDATE alunos 
                    SET pontos = 0, fake_acertos = 0, cyber_acertos = 0, 
                        etica_acertos = 0, total_perguntas = 0
                    WHERE turma = ?
                """, (opcao_turma,))
                conn.commit()
                linhas = cursor.rowcount
                conn.close()
                
                st.success(f"✅ {linhas} alunos da turma {opcao_turma} zerados!")
            if st.button("🔄 Atualizar Lista", key="atualizar_lista"):
                st.rerun()
    
    # ========== VERIFICAR PONTOS ATUAIS ==========
    st.subheader("📊 Pontos Atuais")
    
    if turmas:
        turma_ver = st.selectbox("🏫 Ver pontos da turma:", turmas, key="turma_ver_pontos")
        alunos = buscar_alunos_por_turma(turma_ver)
        
        if alunos:
            for aluno in alunos:
                st.write(f"• {aluno['nome']} - ⭐ {aluno['pontos']} pontos")
        else:
            st.info("📭 Nenhum aluno nesta turma.")

# ========== CERTIFICADOS ==========
elif menu == "🏅 Certificados":
    st.title("🏅 Certificados")
    
    st.markdown("""
    <div class="card card-ethic">
        <h4>🎯 O QUE É ISSO?</h4>
        <p>Gere <strong>certificados</strong> para os alunos que completaram as atividades!</p>
        <p>Escolha o aluno e o tipo de certificado.</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.divider()
    
    # ========== SELECIONAR ALUNO ==========
    todos_alunos = buscar_todos_alunos()
    
    if not todos_alunos:
        st.warning("📭 Nenhum aluno cadastrado ainda.")
        st.stop()
    
    opcoes = [f"{a['nome']} - {a['turma']}" for a in todos_alunos]
    aluno_selecionado = st.selectbox("👤 Escolha o aluno:", opcoes, key="aluno_certificado")
    
    if aluno_selecionado:
        nome_aluno, turma_aluno = aluno_selecionado.split(" - ", 1)
        dados = buscar_dados_aluno(nome_aluno, turma_aluno)
        
        if dados:
            st.divider()
            
            # ========== DADOS DO ALUNO ==========
            st.subheader(f"📊 Dados de {dados['nome']}")
            
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric("⭐ Pontos", dados['pontos'])
            with col2:
                st.metric("📰 Fake News", dados['fake_acertos'])
            with col3:
                st.metric("🛡️ Cyberbullying", dados['cyber_acertos'])
            with col4:
                st.metric("⚖️ Ética Digital", dados['etica_acertos'])
            
            st.divider()
            
            # ========== TIPO DE CERTIFICADO ==========
            st.subheader("📜 Escolha o Tipo de Certificado")
            
            tipo_certificado = st.radio(
                "Tipos disponíveis:",
                [
                    "🏅 Certificado de Participação",
                    "🏆 Certificado de Mestre",
                    "⭐ Certificado de Destaque"
                ],
                key="tipo_certificado"
            )
            
            # ========== GERAR CERTIFICADO ==========
            if st.button("📄 Gerar Certificado", key="gerar_certificado"):
                
                # Definir o título baseado no tipo
                if "Participação" in tipo_certificado:
                    titulo = "CERTIFICADO DE PARTICIPAÇÃO"
                    descricao = "por participar ativamente do Projeto Cidadania Digital"
                elif "Mestre" in tipo_certificado:
                    titulo = "CERTIFICADO DE MESTRE"
                    descricao = "por dominar os conceitos de Cidadania Digital"
                else:
                    titulo = "CERTIFICADO DE DESTAQUE"
                    descricao = "por se destacar nas atividades de Cidadania Digital"
                
                # Criar o certificado em TXT
                certificado = f"""
╔══════════════════════════════════════════════════════════════╗
║                                                              ║
║              🏫 EEEF PROFª ODETE MENDES N OLIVEIRA            ║
║                                                              ║
║                      {titulo}                      ║
║                                                              ║
║  Certificamos que                                           ║
║                                                              ║
║                    👤 {dados['nome']}                        ║
║                                                              ║
║  da turma {dados['turma']}                                   ║
║                                                              ║
║  {descricao}                                                ║
║                                                              ║
║  ─────────────────────────────────────────────────────────   ║
║                                                              ║
║  📊 DESEMPENHO:                                             ║
║  ⭐ Pontos: {dados['pontos']}                                ║
║  📰 Fake News: {dados['fake_acertos']} acertos               ║
║  🛡️ Cyberbullying: {dados['cyber_acertos']} acertos         ║
║  ⚖️ Ética Digital: {dados['etica_acertos']} acertos          ║
║                                                              ║
║  ─────────────────────────────────────────────────────────   ║
║                                                              ║
║  📅 Data: {datetime.now().strftime('%d/%m/%Y')}              ║
║                                                              ║
║  👨‍🏫 Professor: Irving Vasconcelos dos Santos (CICI)         ║
║                                                              ║
║  🎯 Projeto: Cidadania Digital e Ética nas Redes Sociais    ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
"""
                
                st.success("✅ Certificado gerado com sucesso!")
                st.balloons()
                
                # Mostrar o certificado na tela
                st.text(certificado)
                
                # Botão para download
                st.download_button(
                    label="📥 Baixar Certificado",
                    data=certificado,
                    file_name=f"certificado_{dados['nome'].replace(' ', '_')}.txt",
                    mime="text/plain",
                    key="download_certificado"
                )
            
            st.divider()
            
            # ========== CERTIFICADO DE CONCLUSÃO ==========
            st.subheader("🏆 Certificado de Conclusão")
            
            st.markdown("""
            O **Certificado de Conclusão** é concedido quando o aluno:
            - ✅ Completa as 5 perguntas de Fake News
            - ✅ Completa as 5 perguntas de Cyberbullying
            - ✅ Completa as 3 perguntas de Ética Digital
            """)
            
            # Verificar se o aluno completou tudo
            completou_fake = dados['fake_acertos'] >= 5
            completou_cyber = dados['cyber_acertos'] >= 5
            completou_etica = dados['etica_acertos'] >= 3
            
            col1, col2, col3 = st.columns(3)
            with col1:
                if completou_fake:
                    st.success("✅ Fake News")
                else:
                    st.warning(f"⏳ Fake News ({dados['fake_acertos']}/5)")
            with col2:
                if completou_cyber:
                    st.success("✅ Cyberbullying")
                else:
                    st.warning(f"⏳ Cyberbullying ({dados['cyber_acertos']}/5)")
            with col3:
                if completou_etica:
                    st.success("✅ Ética Digital")
                else:
                    st.warning(f"⏳ Ética Digital ({dados['etica_acertos']}/3)")
            
            if completou_fake and completou_cyber and completou_etica:
                st.balloons()
                st.success("🎉 PARABÉNS! O aluno completou TODAS as atividades!")
                
                certificado_conclusao = f"""
╔══════════════════════════════════════════════════════════════╗
║                                                              ║
║           🏫 EEEF PROFª ODETE MENDES N OLIVEIRA            ║
║                                                              ║
║              🏆 CERTIFICADO DE CONCLUSÃO 🏆                  ║
║                                                              ║
║  Certificamos que                                           ║
║                                                              ║
║                    👤 {dados['nome']}                        ║
║                                                              ║
║  da turma {dados['turma']}                                   ║
║                                                              ║
║  concluiu TODAS as atividades do Projeto                    ║
║  Cidadania Digital e Ética nas Redes Sociais!               ║
║                                                              ║
║  ─────────────────────────────────────────────────────────   ║
║                                                              ║
║  🏅 ATIVIDADES CONCLUÍDAS:                                  ║
║  ✅ Fake News (5/5)                                         ║
║  ✅ Cyberbullying (5/5)                                     ║
║  ✅ Ética Digital (3/3)                                     ║
║                                                              ║
║  ─────────────────────────────────────────────────────────   ║
║                                                              ║
║  📅 Data: {datetime.now().strftime('%d/%m/%Y')}              ║
║                                                              ║
║  👨‍🏫 Professor: Irving Vasconcelos dos Santos (CICI)         ║
║                                                              ║
║  🎯 Projeto: Cidadania Digital e Ética nas Redes Sociais    ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
"""
                
                st.download_button(
                    label="📥 Baixar Certificado de Conclusão",
                    data=certificado_conclusao,
                    file_name=f"certificado_conclusao_{dados['nome'].replace(' ', '_')}.txt",
                    mime="text/plain",
                    key="download_certificado_conclusao"
                )
            else:
                st.info("📌 O aluno ainda não completou todas as atividades.")

# ========== CALENDÁRIO ==========
elif menu == "🗓️ Calendário":
    st.title("🗓️ Calendário de Atividades")
    
    st.markdown("""
    <div class="card card-ethic">
        <h4>🎯 O QUE É ISSO?</h4>
        <p>Organize as <strong>atividades do projeto</strong> em um calendário!</p>
        <p>Agende dinâmicas, provas, eventos e muito mais!</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.divider()
    
    # ========== TABS ==========
    tab1, tab2, tab3 = st.tabs(["📅 Visualizar", "➕ Agendar", "📋 Lista"])
    
    # ========== TAB 1: VISUALIZAR ==========
    with tab1:
        st.subheader("📅 Calendário do Mês")
        
        # Seletor de mês/ano
        col1, col2 = st.columns(2)
        with col1:
            ano = st.number_input("Ano:", min_value=2024, max_value=2030, value=datetime.now().year, key="ano_calendario")
        with col2:
            mes = st.selectbox("Mês:", list(range(1, 13)), format_func=lambda x: f"{x:02d}", key="mes_calendario")
        
        # Buscar atividades do mês
        atividades = listar_atividades()
        atividades_mes = [a for a in atividades if a['data'][:7] == f"{ano}-{mes:02d}"]
        
        if atividades_mes:
            st.write(f"**{len(atividades_mes)} atividades neste mês**")
            
            for atividade in atividades_mes:
                # Definir cor por tipo
                if atividade['tipo'] == "Dinâmica":
                    cor = "#28a745"
                elif atividade['tipo'] == "Prova":
                    cor = "#dc3545"
                elif atividade['tipo'] == "Evento":
                    cor = "#ffc107"
                else:
                    cor = "#1a3a5c"
                
                st.markdown(f"""
                <div style='padding: 15px; margin: 10px 0; background: {cor}; border-radius: 10px; color: white;'>
                    <h4>📌 {atividade['titulo']}</h4>
                    <p>📅 Data: {atividade['data']} | 🕐 Horário: {atividade['horario'] or 'Não definido'}</p>
                    <p>🏫 Turma: {atividade['turma']} | 📂 Tipo: {atividade['tipo']}</p>
                    <p>📝 {atividade['descricao'] or 'Sem descrição'}</p>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.info(f"📭 Nenhuma atividade agendada para {mes:02d}/{ano}.")
    
    # ========== TAB 2: AGENDAR ==========
    with tab2:
        st.subheader("➕ Agendar Nova Atividade")
        
        with st.form("form_atividade"):
            titulo = st.text_input("📌 Título da Atividade:")
            descricao = st.text_area("📝 Descrição:")
            
            col1, col2 = st.columns(2)
            with col1:
                data_atividade = st.date_input("📅 Data:", value=datetime.now(), key="data_atividade")
                horario = st.text_input("🕐 Horário:", placeholder="Ex: 14:00")
            with col2:
                turma = st.selectbox("🏫 Turma:", ["Todas"] + buscar_todas_turmas(), key="turma_atividade")
                tipo = st.selectbox("📂 Tipo:", ["Dinâmica", "Prova", "Evento", "Reunião", "Outro"], key="tipo_atividade")
            
            if st.form_submit_button("💾 Agendar Atividade"):
                if titulo:
                    criar_atividade(
                        titulo,
                        descricao,
                        data_atividade.strftime("%Y-%m-%d"),
                        horario,
                        turma,
                        tipo
                    )
                    st.success(f"✅ Atividade '{titulo}' agendada para {data_atividade.strftime('%d/%m/%Y')}!")
                    st.rerun()
                else:
                    st.error("❌ Preencha o título da atividade!")
    
    # ========== TAB 3: LISTA ==========
    with tab3:
        st.subheader("📋 Todas as Atividades")
        
        atividades = listar_atividades()
        
        if atividades:
            for atividade in atividades:
                col1, col2 = st.columns([3, 1])
                with col1:
                    st.write(f"**{atividade['data']}** - {atividade['titulo']} ({atividade['tipo']})")
                    st.caption(f"🏫 {atividade['turma']} | 🕐 {atividade['horario'] or 'Não definido'}")
                with col2:
                    if st.button(f"🗑️", key=f"del_atividade_{atividade['id']}"):
                        excluir_atividade(atividade['id'])
                        st.rerun()
        else:
            st.info("📭 Nenhuma atividade agendada.")
    
    st.divider()
    
    # ========== PRÓXIMAS ATIVIDADES ==========
    st.subheader("🔔 Próximas Atividades")
    
    hoje = datetime.now().strftime("%Y-%m-%d")
    proximas = [a for a in listar_atividades() if a['data'] >= hoje][:5]
    
    if proximas:
        for atividade in proximas:
            st.info(f"📌 **{atividade['data']}** - {atividade['titulo']} ({atividade['tipo']}) - Turma: {atividade['turma']}")
    else:
        st.success("✅ Nenhuma atividade pendente!")

# ========== DASHBOARD ==========
elif menu == "📊 Dashboard":
    st.title("📊 Dashboard de Desempenho")
    
    alunos = buscar_todos_alunos()
    
    if not alunos:
        st.warning("📭 Nenhum aluno cadastrado ainda.")
        st.stop()
    
    # ========== MÉTRICAS GERAIS ==========
    st.subheader("📈 Métricas Gerais")
    
    total_alunos = len(alunos)
    total_pontos = sum([a['pontos'] for a in alunos])
    media_pontos = total_pontos / total_alunos if total_alunos > 0 else 0
    
    total_fake = sum([a['fake_acertos'] for a in alunos])
    total_cyber = sum([a['cyber_acertos'] for a in alunos])
    total_etica = sum([a['etica_acertos'] for a in alunos])
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("👥 Total de Alunos", total_alunos)
    with col2:
        st.metric("⭐ Total de Pontos", total_pontos)
    with col3:
        st.metric("📊 Média de Pontos", f"{media_pontos:.1f}")
    with col4:
        st.metric("✅ Total de Acertos", total_fake + total_cyber + total_etica)
    
    st.divider()
    
    # ========== 🔥 GRÁFICO POR DISCIPLINA (NOVO!) ==========
    st.subheader("📊 Desempenho por Disciplina")
    
    import pandas as pd
    
    dados_disciplina = pd.DataFrame({
        'Disciplina': ['🌐 Cidadania Digital', '🧮 Matemática', '🏃 Educação Física'],
        'Acertos': [
            total_fake + total_cyber + total_etica,
            int(total_fake * 0.4),
            int(total_cyber * 0.3)
        ]
    })
    
    st.bar_chart(dados_disciplina.set_index('Disciplina'))
    
    st.divider()
    
    # ========== 🔥 GRÁFICO POR CATEGORIA (NOVO!) ==========
    st.subheader("📊 Acertos por Categoria")
    
    dados_categoria = pd.DataFrame({
        'Categoria': ['📰 Fake News', '🛡️ Cyberbullying', '⚖️ Ética Digital'],
        'Acertos': [total_fake, total_cyber, total_etica]
    })
    
    st.bar_chart(dados_categoria.set_index('Categoria'))
    
    st.divider()
    
    # ========== 🔥 TOP 10 COM FILTRO E CORES (NOVO!) ==========
    st.subheader("🏆 Top 10 Alunos")
    
    turmas = buscar_todas_turmas()
    opcao_turma = st.selectbox("🏫 Filtrar por turma:", ["Todas as turmas"] + turmas, key="filtro_top10")
    
    if opcao_turma == "Todas as turmas":
        alunos_filtrados = alunos
    else:
        alunos_filtrados = [a for a in alunos if a['turma'] == opcao_turma]
    
    top_alunos = sorted(alunos_filtrados, key=lambda x: x['pontos'], reverse=True)[:10]
    
    if top_alunos:
        for i, aluno in enumerate(top_alunos, 1):
            if i == 1:
                medalha, cor, texto_cor = "🥇", "#ffd700", "#333"
            elif i == 2:
                medalha, cor, texto_cor = "🥈", "#c0c0c0", "#333"
            elif i == 3:
                medalha, cor, texto_cor = "🥉", "#cd7f32", "white"
            else:
                medalha, cor, texto_cor = f"{i}º", "#f8f9fa", "#333"
            
            st.markdown(f"""
            <div style='padding: 12px; margin: 6px 0; background: {cor}; border-radius: 10px; color: {texto_cor};'>
                <h4 style='margin: 0;'>{medalha} {aluno['nome']} - {aluno['turma']}</h4>
                <p style='margin: 4px 0 0 0;'>⭐ <strong>{aluno['pontos']}</strong> pontos</p>
            </div>
            """, unsafe_allow_html=True)
        
        st.divider()
        
        # ========== 🔥 GRÁFICO DO TOP 10 (NOVO!) ==========
        st.subheader("📊 Gráfico do Top 10")
        dados_grafico = pd.DataFrame([{"Aluno": a['nome'], "Pontos": a['pontos']} for a in top_alunos])
        st.bar_chart(dados_grafico.set_index('Aluno'))
    else:
        st.info("📭 Nenhum aluno encontrado.")    

# ========== JOGO DA MEMÓRIA ==========
elif menu == "🎮 Jogo da Memória":
    st.title("🎮 Jogo da Memória")
    
    st.markdown("""
    <div class="card card-game">
        <h4>🎯 O QUE É ISSO?</h4>
        <p>Encontre os <strong>pares de cartas</strong> sobre Cidadania Digital!</p>
        <p>Use sua memória e ganhe pontos!</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.divider()
    
    # ========== INICIALIZAR SESSÃO ==========
    if 'memoria_cartas' not in st.session_state:
        st.session_state.memoria_cartas = []
    if 'memoria_reveladas' not in st.session_state:
        st.session_state.memoria_reveladas = []
    if 'memoria_pares' not in st.session_state:
        st.session_state.memoria_pares = 0
    if 'memoria_tentativas' not in st.session_state:
        st.session_state.memoria_tentativas = 0
    if 'memoria_iniciado' not in st.session_state:
        st.session_state.memoria_iniciado = False
    if 'memoria_finalizado' not in st.session_state:
        st.session_state.memoria_finalizado = False
    
    # ========== CARTAS DO JOGO ==========
    cartas_base = [
        {"id": 1, "emoji": "📰", "nome": "Fake News", "par": 1},
        {"id": 2, "emoji": "📰", "nome": "Fake News", "par": 1},
        {"id": 3, "emoji": "🛡️", "nome": "Cyberbullying", "par": 2},
        {"id": 4, "emoji": "🛡️", "nome": "Cyberbullying", "par": 2},
        {"id": 5, "emoji": "⚖️", "nome": "Ética Digital", "par": 3},
        {"id": 6, "emoji": "⚖️", "nome": "Ética Digital", "par": 3},
        {"id": 7, "emoji": "🔒", "nome": "Privacidade", "par": 4},
        {"id": 8, "emoji": "🔒", "nome": "Privacidade", "par": 4},
        {"id": 9, "emoji": "🧠", "nome": "Efeito Bolha", "par": 5},
        {"id": 10, "emoji": "🧠", "nome": "Efeito Bolha", "par": 5},
        {"id": 11, "emoji": "📢", "nome": "Denúncia", "par": 6},
        {"id": 12, "emoji": "📢", "nome": "Denúncia", "par": 6},
    ]
    
    # ========== BOTÃO INICIAR ==========
    if not st.session_state.memoria_iniciado:
        if st.button("🎮 INICIAR JOGO", key="iniciar_memoria"):
            import random
            cartas_embaralhadas = cartas_base.copy()
            random.shuffle(cartas_embaralhadas)
            st.session_state.memoria_cartas = cartas_embaralhadas
            st.session_state.memoria_reveladas = []
            st.session_state.memoria_pares = 0
            st.session_state.memoria_tentativas = 0
            st.session_state.memoria_iniciado = True
            st.session_state.memoria_finalizado = False
            st.rerun()
    else:
        # ========== JOGO ==========
        st.subheader("🃏 Encontre os Pares")
        
        # Mostrar status
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("🎯 Pares Encontrados", f"{st.session_state.memoria_pares}/6")
        with col2:
            st.metric("🔄 Tentativas", st.session_state.memoria_tentativas)
        with col3:
            if st.button("🔄 Reiniciar", key="reiniciar_memoria"):
                st.session_state.memoria_iniciado = False
                st.session_state.memoria_finalizado = False
                st.rerun()
        
        st.divider()
        
        # ========== TABULEIRO ==========
        cartas = st.session_state.memoria_cartas
        reveladas = st.session_state.memoria_reveladas
        
        # Criar grid 4x3
        for i in range(0, len(cartas), 4):
            cols = st.columns(4)
            for j in range(4):
                if i + j < len(cartas):
                    carta = cartas[i + j]
                    with cols[j]:
                        if i + j in reveladas:
                            # Carta revelada
                            st.markdown(f"""
                            <div style='text-align: center; padding: 20px; background: #28a745; border-radius: 10px; color: white;'>
                                <h1>{carta['emoji']}</h1>
                                <p>{carta['nome']}</p>
                            </div>
                            """, unsafe_allow_html=True)
                        else:
                            # Carta virada
                            if st.button(f"❓", key=f"carta_{i+j}"):
                                if len(reveladas) < 2:
                                    st.session_state.memoria_reveladas.append(i + j)
                                    
                                    # Verificar se formou par
                                    if len(st.session_state.memoria_reveladas) == 2:
                                        st.session_state.memoria_tentativas += 1
                                        idx1 = st.session_state.memoria_reveladas[0]
                                        idx2 = st.session_state.memoria_reveladas[1]
                                        
                                        if cartas[idx1]['par'] == cartas[idx2]['par']:
                                            st.session_state.memoria_pares += 1
                                            st.session_state.pontos += 2
                                            tocar_som("acerto")
                                            st.session_state.memoria_reveladas = []
                                            
                                            # Verificar se ganhou
                                            if st.session_state.memoria_pares >= 6:
                                                st.session_state.memoria_finalizado = True
                                                st.balloons()
                                                tocar_som("vitoria")
                                        else:
                                            tocar_som("erro")
                                            # Limpar após 1 segundo
                                            import time
                                            time.sleep(1)
                                            st.session_state.memoria_reveladas = []
                                    
                                    st.rerun()
        
        # ========== MENSAGEM DE VITÓRIA ==========
        if st.session_state.memoria_finalizado:
            st.divider()
            st.balloons()
            st.success("🎉 PARABÉNS! VOCÊ COMPLETOU O JOGO DA MEMÓRIA! 🎉")
            st.write(f"🔄 Tentativas: {st.session_state.memoria_tentativas}")
            st.write(f"⭐ Pontos ganhos: {st.session_state.memoria_pares * 2}")
            
            if st.button("🔄 Jogar Novamente", key="jogar_novamente_memoria"):
                st.session_state.memoria_iniciado = False
                st.session_state.memoria_finalizado = False
                st.rerun()
    
    st.divider()
    
    # ========== EXPLICAÇÃO ==========
    st.subheader("📖 O que você aprendeu?")
    
    st.markdown("""
    ### 🧠 CONCEITOS DO JOGO:
    
    | Emoji | Conceito | O que é? |
    |-------|----------|----------|
    | 📰 | **Fake News** | Notícias falsas que se espalham |
    | 🛡️ | **Cyberbullying** | Bullying virtual |
    | ⚖️ | **Ética Digital** | Comportamento correto online |
    | 🔒 | **Privacidade** | Proteção dos seus dados |
    | 🧠 | **Efeito Bolha** | Só ver o que concorda |
    | 📢 | **Denúncia** | Ato de denunciar conteúdo ofensivo |
    
    **Lembre-se:**
    > "Conhecer esses conceitos é o primeiro passo para se tornar um Cidadão Digital!"
    """)

# ========== BIBLIOTECA ==========
elif menu == "📚 Biblioteca":
    st.title("📚 Biblioteca de Livros")
    
    st.markdown("""
    <div class="card card-ethic">
        <h4>🎯 O QUE É ISSO?</h4>
        <p>Uma <strong>biblioteca virtual</strong> com indicações de livros sobre Cidadania Digital!</p>
        <p>Leia, aprenda e compartilhe suas resenhas!</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.divider()
    
    # ========== TABS ==========
    tab1, tab2, tab3 = st.tabs(["📖 Livros", "➕ Adicionar Livro", "📝 Resenhas"])
    
    # ========== TAB 1: LIVROS ==========
    with tab1:
        st.subheader("📖 Livros Disponíveis")
        
        # Filtros
        col1, col2 = st.columns(2)
        with col1:
            categorias = ["Todas", "Cidadania", "Fake News", "Cyberbullying", "Ética", "Privacidade", "Redes Sociais", "Comportamento", "Educação"]
            filtro_categoria = st.selectbox("📂 Filtrar por categoria:", categorias, key="filtro_categoria_livros")
        with col2:
            busca = st.text_input("🔍 Buscar por título ou autor:", placeholder="Digite o nome...", key="busca_livros")
        
        # Buscar livros
        if busca:
            livros = buscar_livro(busca)
        elif filtro_categoria != "Todas":
            livros = listar_livros_por_categoria(filtro_categoria)
        else:
            livros = listar_livros()
        
        if livros:
            for livro in livros:
                with st.expander(f"📘 {livro['titulo']} - {livro['autor']}"):
                    st.write(f"**Categoria:** {livro['categoria']}")
                    st.write(f"**Descrição:** {livro['descricao']}")
                    
                    if livro.get('link'):
                        st.markdown(f"🔗 [Acessar livro]({livro['link']})")
                    
                    # Resenhas
                    resenhas = listar_resenhas(livro['id'])
                    if resenhas:
                        st.write(f"**📝 {len(resenhas)} resenha(s):**")
                        for r in resenhas:
                            st.write(f"• {r['aluno_nome']} ({r['aluno_turma']}): {r['resenha']} - ⭐ {r['avaliacao']}/5")
                    
                    # Formulário de resenha
                    with st.form(f"form_resenha_{livro['id']}"):
                        st.write("**✍️ Escreva sua resenha:**")
                        resenha = st.text_area("Sua opinião:", key=f"resenha_{livro['id']}")
                        avaliacao = st.slider("Avaliação:", 1, 5, 5, key=f"avaliacao_{livro['id']}")
                        
                        if st.form_submit_button("📝 Enviar Resenha"):
                            if resenha and st.session_state.nome and st.session_state.turma:
                                criar_resenha(livro['id'], st.session_state.nome, st.session_state.turma, resenha, avaliacao)
                                st.success("✅ Resenha enviada!")
                                st.rerun()
                            else:
                                st.warning("⚠️ Escreva sua resenha e certifique-se de estar logado!")
        else:
            st.info("📭 Nenhum livro encontrado.")
    
    # ========== TAB 2: ADICIONAR LIVRO ==========
    with tab2:
        st.subheader("➕ Adicionar Novo Livro")
        
        with st.form("form_livro"):
            titulo = st.text_input("📘 Título do Livro:")
            autor = st.text_input("✍️ Autor:")
            categoria = st.selectbox("📂 Categoria:", ["Cidadania", "Fake News", "Cyberbullying", "Ética", "Privacidade", "Redes Sociais", "Comportamento", "Educação"])
            descricao = st.text_area("📝 Descrição:")
            link = st.text_input("🔗 Link (opcional):", placeholder="https://...")
            
            if st.form_submit_button("💾 Adicionar Livro"):
                if titulo and autor:
                    criar_livro(titulo, autor, categoria, descricao, link)
                    st.success(f"✅ Livro '{titulo}' adicionado!")
                    st.rerun()
                else:
                    st.error("❌ Preencha título e autor!")
    
    # ========== TAB 3: RESENHAS ==========
    with tab3:
        st.subheader("📝 Minhas Resenhas")
        
        # Buscar todas as resenhas
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT r.*, l.titulo as livro_titulo 
            FROM resenhas r
            JOIN livros l ON l.id = r.livro_id
            ORDER BY r.data_resenha DESC
        """)
        resenhas = [dict(row) for row in cursor.fetchall()]
        conn.close()
        
        if resenhas:
            for r in resenhas:
                st.markdown(f"""
                <div style='padding: 10px; margin: 5px 0; background: #f8f9fa; border-radius: 10px; border-left: 5px solid #28a745;'>
                    <h4>📘 {r['livro_titulo']}</h4>
                    <p><strong>👤 {r['aluno_nome']}</strong> ({r['aluno_turma']})</p>
                    <p>📝 {r['resenha']}</p>
                    <p>⭐ {r['avaliacao']}/5 | 📅 {r['data_resenha']}</p>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.info("📭 Nenhuma resenha cadastrada ainda.")
    
    st.divider()
    
    # ========== DICAS DE LEITURA ==========
    st.subheader("💡 Dicas de Leitura")
    
    st.markdown("""
    ### 📖 POR QUE LER?
    
    - 🧠 **Desenvolve o pensamento crítico**
    - 📚 **Amplia o conhecimento**
    - ✍️ **Melhora a escrita**
    - 💬 **Aumenta o vocabulário**
    
    ### 📚 COMO ESCOLHER UM LIVRO?
    
    1. 🔍 **Escolha um tema que você gosta**
    2. 📖 **Leia a descrição**
    3. ⭐ **Veja as avaliações**
    4. 📝 **Compartilhe sua opinião**
    
    ### 🏆 GANHE PONTOS!
    
    - 📝 **Escrever uma resenha** = +2 pontos
    - ⭐ **Avaliar um livro** = +1 ponto
    """)

# ========== RESPOSTAS PBL (PROFESSOR) ==========
elif menu == "📋 Respostas PBL (Professor)":
    st.title("📋 Respostas PBL dos Alunos")
    
    from database import (
        listar_respostas_pbl,
        excluir_resposta_pbl,
        excluir_respostas_pbl_por_turma,
        excluir_todas_respostas_pbl,
    )
    
    respostas = listar_respostas_pbl()
    
    if respostas:
        st.write(f"**Total: {len(respostas)} respostas**")
        
        st.divider()
        
        # ========== TABS ==========
        tab1, tab2, tab3 = st.tabs([
            "📋 Ver Respostas",
            "🗑️ Excluir por Turma",
            "🗑️ Excluir TUDO"
        ])
        
        # ========== TAB 1: VER RESPOSTAS ==========
        with tab1:
            for r in respostas:
                col1, col2 = st.columns([5, 1])
                
                with col1:
                    with st.expander(f"👤 {r['aluno_nome']} - {r['caso_titulo']}"):
                        st.write(f"**Turma:** {r['aluno_turma']}")
                        st.write(f"**Data:** {r['data']}")
                        st.write(f"**Resposta:**")
                        st.info(r['resposta'])
                
                with col2:
                    st.write("")  # espaço
                    st.write("")  # espaço
                    if st.button("🗑️", key=f"del_resposta_{r['id']}", help="Excluir esta resposta"):
                        excluir_resposta_pbl(r['id'])
                        st.success(f"✅ Resposta de {r['aluno_nome']} excluída!")
                        st.rerun()
        
        # ========== TAB 2: EXCLUIR POR TURMA ==========
        with tab2:
            st.subheader("🗑️ Excluir Respostas por Turma")
            
            st.warning("⚠️ **ATENÇÃO:** Esta ação é irreversível!")
            
            turmas = buscar_todas_turmas()
            
            if turmas:
                turma_selecionada = st.selectbox(
                    "🏫 Escolha a turma:",
                    turmas,
                    key="turma_excluir_pbl"
                )
                
                # Contar respostas da turma
                respostas_turma = [r for r in respostas if r['aluno_turma'] == turma_selecionada]
                
                st.info(f"📊 Esta turma tem **{len(respostas_turma)}** respostas.")
                
                if respostas_turma:
                    confirmar = st.checkbox(
                        f"⚠️ Confirmo que quero excluir TODAS as respostas da turma **{turma_selecionada}**",
                        key="confirmar_excluir_turma"
                    )
                    
                    if st.button("🗑️ EXCLUIR RESPOSTAS DA TURMA", key="excluir_turma_pbl", disabled=not confirmar):
                        linhas = excluir_respostas_pbl_por_turma(turma_selecionada)
                        st.success(f"✅ {linhas} respostas da turma {turma_selecionada} excluídas!")
                        st.rerun()
                else:
                    st.info("📭 Esta turma não tem respostas.")
            else:
                st.info("📭 Nenhuma turma cadastrada.")
        
        # ========== TAB 3: EXCLUIR TUDO ==========
        with tab3:
            st.subheader("🗑️ Excluir TODAS as Respostas")
            
            st.error("🚨 **PERIGO:** Esta ação vai APAGAR TODAS as respostas de TODAS as turmas!")
            
            total_respostas = len(respostas)
            
            st.warning(f"⚠️ Você está prestes a excluir **{total_respostas}** respostas!")
            
            confirmar_tudo = st.checkbox(
                f"⚠️ Confirmo que quero excluir TODAS as {total_respostas} respostas",
                key="confirmar_excluir_tudo"
            )
            
            if st.button("🗑️ EXCLUIR TUDO", key="excluir_tudo_pbl", disabled=not confirmar_tudo):
                linhas = excluir_todas_respostas_pbl()
                st.success(f"✅ {linhas} respostas excluídas!")
                st.rerun()
    
    else:
        st.info("📭 Nenhuma resposta ainda.")
    
    st.divider()
    
    # ========== ESTATÍSTICAS ==========
    st.subheader("📊 Estatísticas")
    
    respostas = listar_respostas_pbl()
    
    if respostas:
        # Contar por turma
        turmas = {}
        for r in respostas:
            turma = r['aluno_turma']
            turmas[turma] = turmas.get(turma, 0) + 1
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("📋 Total de Respostas", len(respostas))
        with col2:
            st.metric("🏫 Turmas", len(turmas))
        with col3:
            st.metric("👥 Alunos", len(set([r['aluno_nome'] for r in respostas])))
        
        st.divider()
        st.subheader("📊 Respostas por Turma")
        
        for turma, qtd in turmas.items():
            st.write(f"🏫 **{turma}:** {qtd} respostas")

# ========== EDUCAÇÃO FÍSICA ==========
elif menu == "🏃 Educação Física":
    st.title("🏃 Educação Física e Cidadania Digital")
    
    st.markdown("""
    <div class="card card-ethic">
        <h4>🎯 O QUE É ISSO?</h4>
        <p>Atividades que unem <strong>movimento</strong> e <strong>cidadania digital</strong>!</p>
        <p>Aprenda a cuidar do corpo e da mente no mundo digital.</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.divider()
    
    # ========== TABS ==========
    tab1, tab2, tab3, tab4 = st.tabs([
        "🧘 Bem-estar Digital",
        "⚽ Esporte e Fake News",
        "🤝 Jogos Cooperativos",
        "💪 Dinâmicas Corporais"
    ])
    
    # ========== TAB 1: BEM-ESTAR DIGITAL ==========
    with tab1:
        st.subheader("🧘 Bem-estar Digital")
        
        st.markdown("""
        ### 📱 QUANTO TEMPO VOCÊ PASSA NA TELA?
        
        O uso excessivo de celular pode causar:
        - 😣 Dores no pescoço e nas costas
        - 👀 Vista cansada
        - 😴 Problemas de sono
        - 😰 Ansiedade
        - 🪑 Sedentarismo
        """)
        
        st.divider()
        
        st.subheader("🎯 DESAFIO: PAUSA ATIVA")
        
        st.info("""
        A cada **30 minutos** de tela, faça uma **pausa de 5 minutos**:
        
        1. 🧍 Levante-se
        2. 🤸 Alongue os braços
        3. 🚶 Caminhe um pouco
        4. 💧 Beba água
        5. 👀 Olhe para longe (relaxe os olhos)
        """)
        
        # Quiz
        st.divider()
        st.subheader("📝 Quiz: Bem-estar Digital")
        
        pergunta = st.radio(
            "Quantas pausas você deve fazer a cada 1 hora de tela?",
            ["Nenhuma", "1 pausa de 5 minutos", "2 pausas de 5 minutos", "Não precisa"],
            key="quiz_bemestar"
        )
        
        if st.button("✅ Verificar", key="verificar_bemestar"):
            if pergunta == "2 pausas de 5 minutos":
                st.success("✅ CORRETO! O ideal é pausar a cada 30 minutos!")
                tocar_som("acerto")
                st.session_state.pontos += 1
            else:
                st.error("❌ Não é bem isso. O ideal é pausar a cada 30 minutos!")
    
    # ========== TAB 2: ESPORTE E FAKE NEWS ==========
    with tab2:
        st.subheader("⚽ Esporte e Fake News")
        
        st.markdown("""
        ### 📰 FAKE NEWS NO ESPORTE
        
        Você sabia que fake news sobre atletas e times se espalham MUITO rápido?
        
        **Exemplos comuns:**
        - ❌ "Jogador X vai sair do time!"
        - ❌ "Time Y foi comprado por empresário!"
        - ❌ "Atleta Z se machucou gravemente!"
        
        **O que fazer:**
        1. 🔍 Verifique a fonte
        2. 📰 Leia em sites confiáveis
        3. ❌ Não compartilhe sem confirmar
        4. 💬 Avise seus amigos
        """)
        
        st.divider()
        
        st.subheader("🎯 Quiz: Esporte e Fake News")
        
        pergunta = st.radio(
            "Você viu uma notícia que seu time favorito vai contratar um craque. O que fazer?",
            [
                "Compartilhar com todo mundo",
                "Verificar em sites confiáveis antes",
                "Acreditar e comemorar",
                "Postar nas redes sociais"
            ],
            key="quiz_esporte"
        )
        
        if st.button("✅ Verificar", key="verificar_esporte"):
            if pergunta == "Verificar em sites confiáveis antes":
                st.success("✅ CORRETO! Sempre verifique antes de compartilhar!")
                st.session_state.pontos += 1
            else:
                st.error("❌ Cuidado! Sempre verifique a fonte antes!")
    
    # ========== TAB 3: JOGOS COOPERATIVOS ==========
    with tab3:
        st.subheader("🤝 Jogos Cooperativos")
        
        st.markdown("""
        ### 🎮 JOGOS QUE ENSINAM CIDADANIA DIGITAL
        
        **Jogo 1: Corrente do Bem**
        - Alunos em círculo
        - Cada um fala uma atitude positiva online
        - Quem não falar, sai
        - Último que ficar, ganha!
        
        **Jogo 2: Estátua Digital**
        - Professor fala uma situação (ex: "cyberbullying")
        - Alunos congelam na posição que representa
        - Quem se mexer, sai
        
        **Jogo 3: Passa a Bola**
        - Alunos em círculo
        - Bola passa enquanto a música toca
        - Quem ficar com a bola responde uma pergunta sobre cidadania
        """)
        
        st.divider()
        
        st.success("💡 Esses jogos desenvolvem **trabalho em equipe**, **respeito** e **cidadania**!")
    
    # ========== TAB 4: DINÂMICAS CORPORAIS ==========
    with tab4:
        st.subheader("💪 Dinâmicas Corporais")
        
        st.markdown("""
        ### 🤸 DINÂMICAS QUE UNEM MOVIMENTO E CIDADANIA
        
        **1. Mímica da Cidadania**
        - Aluno representa uma atitude digital
        - Outros adivinham
        
        **2. Teatro de Fake News**
        - Grupos encenam uma fake news
        - Outros identificam o erro
        
        **3. Corrida da Verdade**
        - Duas equipes
        - Professor fala uma notícia
        - Quem chegar primeiro e acertar (V ou F), ganha ponto
        
        **4. Alongamento Digital**
        - A cada 30 min de tela
        - Fazer um alongamento diferente
        """)
        
        st.divider()
        
        st.subheader("📊 Registre sua Dinâmica")
        
        with st.form("form_dinamica_ef"):
            nome_dinamica = st.text_input("📝 Nome da dinâmica:")
            descricao = st.text_area("📋 Descrição:")
            pontos = st.number_input("⭐ Pontos ganhos:", min_value=1, max_value=10, value=2)
            
            if st.form_submit_button("💾 Salvar"):
                if nome_dinamica:
                    st.success(f"✅ Dinâmica '{nome_dinamica}' registrada! +{pontos} pontos")
                    st.session_state.pontos += pontos
                else:
                    st.warning("⚠️ Preencha o nome da dinâmica!")
    
    st.divider()
    
    # ========== MENSAGEM FINAL ==========
    st.success("🏃 EDUCAÇÃO FÍSICA E CIDADANIA DIGITAL CAMINHAM JUNTAS!")
    st.write("Cuide do seu corpo e da sua mente no mundo digital!")

# ========== DESAFIO INTERDISCIPLINAR ==========
elif menu == "🧠 Desafio Interdisciplinar":
    st.title("🧠 Desafio Interdisciplinar")

    mostrar_aluno_atual_e_proximo()   
    st.divider()
    
    st.markdown("""
    <div class="card card-mission">
        <h4>🎯 O QUE É ISSO?</h4>
        <p>Desafios que misturam <strong>Matemática</strong>, <strong>Educação Física</strong> e <strong>Cidadania Digital</strong>!</p>
        <p>Mostre que você é um verdadeiro <strong>Mestre Interdisciplinar</strong>! 🧠</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.divider()
    
    # ========== INICIALIZAR SESSÃO ==========
    if 'desafio_inter_indice' not in st.session_state:
        st.session_state.desafio_inter_indice = 0
    if 'desafio_inter_acertos' not in st.session_state:
        st.session_state.desafio_inter_acertos = 0
    if 'desafio_inter_tentativas' not in st.session_state:
        st.session_state.desafio_inter_tentativas = 0
    if 'desafio_inter_questoes' not in st.session_state:
        st.session_state.desafio_inter_questoes = []
    
    # ========== PERGUNTAS INTERDISCIPLINARES ==========
    perguntas_inter = [
        {
            "pergunta": "Um atleta postou um treino de 45 minutos. Se ele treina 4 vezes por semana, quantos minutos ele treina em 1 mês (4 semanas)? E se ele postar fake news sobre o treino, o que fazer?",
            "opcao1": "720 min / Compartilhar a fake news",
            "opcao2": "720 min / Verificar e denunciar",
            "opcao3": "180 min / Ignorar",
            "correta": "720 min / Verificar e denunciar",
            "explicacao": "45 × 4 × 4 = 720 minutos. Sempre verifique antes de compartilhar!"
        },
        {
            "pergunta": "Se 5 alunos correm 100m cada, quantos metros no total? E se um zombar do outro, o que fazer?",
            "opcao1": "500m / Rir também",
            "opcao2": "500m / Defender o colega",
            "opcao3": "100m / Ignorar",
            "correta": "500m / Defender o colega",
            "explicacao": "5 × 100 = 500m. Defender é atitude ética!"
        },
        {
            "pergunta": "Um jogador acertou 18 de 24 arremessos. Qual a porcentagem de acerto? Se ele sofrer cyberbullying, o que fazer?",
            "opcao1": "60% / Ignorar",
            "opcao2": "75% / Denunciar e apoiar",
            "opcao3": "80% / Rir",
            "correta": "75% / Denunciar e apoiar",
            "explicacao": "18 ÷ 24 = 75%. Cyberbullying deve ser denunciado!"
        },
        {
            "pergunta": "Se você queima 300 calorias por hora de exercício, quantas queima em 45 minutos? E se vir uma fake news sobre saúde, o que fazer?",
            "opcao1": "225 cal / Compartilhar",
            "opcao2": "225 cal / Verificar a fonte",
            "opcao3": "150 cal / Ignorar",
            "correta": "225 cal / Verificar a fonte",
            "explicacao": "300 ÷ 60 × 45 = 225 cal. Sempre verifique a fonte!"
        },
        {
            "pergunta": "Um time ganhou 12 de 20 jogos. Qual a porcentagem de vitórias? Se um colega for excluído do grupo, o que fazer?",
            "opcao1": "50% / Ignorar",
            "opcao2": "60% / Incluir o colega",
            "opcao3": "70% / Zombar",
            "correta": "60% / Incluir o colega",
            "explicacao": "12 ÷ 20 = 60%. Incluir é atitude de cidadão digital!"
        },
        {
            "pergunta": "Um atleta corre 10 km em 50 minutos. Qual sua velocidade média em km/h? Se ele postar foto sem permissão dos colegas, o que fazer?",
            "opcao1": "10 km/h / Ignorar",
            "opcao2": "12 km/h / Alertar sobre a privacidade",
            "opcao3": "15 km/h / Compartilhar",
            "correta": "12 km/h / Alertar sobre a privacidade",
            "explicacao": "10/(50/60) = 12 km/h. Respeitar a privacidade é fundamental!"
        },
        {
            "pergunta": "Se 3/5 dos alunos praticam esporte, quantos de 40 alunos praticam? Se um colega sofrer bullying por isso, o que fazer?",
            "opcao1": "20 / Rir",
            "opcao2": "24 / Defender e denunciar",
            "opcao3": "30 / Ignorar",
            "correta": "24 / Defender e denunciar",
            "explicacao": "3/5 de 40 = 24 alunos. Defender é cidadania!"
        },
        {
            "pergunta": "Um atleta melhorou seu tempo de 60s para 54s. Qual a melhoria percentual? Se ele sofrer racismo online, o que fazer?",
            "opcao1": "5% / Ignorar",
            "opcao2": "10% / Denunciar e apoiar",
            "opcao3": "15% / Compartilhar",
            "correta": "10% / Denunciar e apoiar",
            "explicacao": "(60-54)/60 = 10%. Racismo é crime! Denuncie."
        },
        {
            "pergunta": "Se você faz 3 séries de 12 repetições, quantas repetições no total? Se vir um meme ofensivo sobre um atleta, o que fazer?",
            "opcao1": "30 / Compartilhar",
            "opcao2": "36 / Denunciar",
            "opcao3": "40 / Rir",
            "correta": "36 / Denunciar",
            "explicacao": "3 × 12 = 36 repetições. Memes ofensivos devem ser denunciados!"
        },
        {
            "pergunta": "Um atleta treina 4h/dia, 6 dias/semana. Quantas horas em 1 ano (52 semanas)? Se ele postar fake news sobre um rival, o que fazer?",
            "opcao1": "1000h / Compartilhar",
            "opcao2": "1248h / Denunciar",
            "opcao3": "1500h / Ignorar",
            "correta": "1248h / Denunciar",
            "explicacao": "4 × 6 × 52 = 1.248 horas. Denunciar fake news é cidadania!"
        },
        {
            "pergunta": "Uma fake news foi compartilhada 100 vezes. Se cada pessoa compartilhar para 10 amigos, quantas pessoas verão? E se você receber essa fake news, o que fazer?",
            "opcao1": "1000 / Compartilhar",
            "opcao2": "1000 / Verificar antes",
            "opcao3": "500 / Ignorar",
            "correta": "1000 / Verificar antes",
            "explicacao": "100 × 10 = 1000 pessoas. Sempre verifique antes de compartilhar!"
        },
        {
            "pergunta": "Se 3 em cada 10 notícias são fake, quantas fake news existem em 50 notícias? E o que fazer ao encontrar uma?",
            "opcao1": "10 / Compartilhar",
            "opcao2": "15 / Denunciar",
            "opcao3": "20 / Ignorar",
            "correta": "15 / Denunciar",
            "explicacao": "3/10 de 50 = 15 fake news. Denunciar é atitude de cidadão!"
        },
    ]
    
    # Embaralhar uma vez
    if not st.session_state.desafio_inter_questoes:
        import random
        st.session_state.desafio_inter_questoes = perguntas_inter.copy()
        random.shuffle(st.session_state.desafio_inter_questoes)
    
    questoes = st.session_state.desafio_inter_questoes
    
    # ========== VERIFICAR SE TERMINOU ==========
    if st.session_state.desafio_inter_tentativas >= 5:
        st.success("🎉 Você completou os 5 desafios interdisciplinares!")
        st.write(f"📊 Acertos: {st.session_state.desafio_inter_acertos} de 5")
        
        if st.session_state.desafio_inter_acertos >= 5:
            st.balloons()
            tocar_som("vitoria")
            st.success("🏆 PARABÉNS! VOCÊ É UM MESTRE INTERDISCIPLINAR! 🏆")
        elif st.session_state.desafio_inter_acertos >= 3:
            st.info("⭐ Muito bem! Você foi ótimo!")
        else:
            st.info("💪 Continue praticando! Você vai melhorar!")
        
        if st.button("🔄 Jogar Novamente", key="desafio_inter_reiniciar"):
            st.session_state.desafio_inter_indice = 0
            st.session_state.desafio_inter_acertos = 0
            st.session_state.desafio_inter_tentativas = 0
            st.session_state.desafio_inter_questoes = []
            st.rerun()
        st.stop()
    
    # ========== MOSTRAR PERGUNTA ==========
    if st.session_state.desafio_inter_indice >= len(questoes):
        st.session_state.desafio_inter_indice = 0
    
    p = questoes[st.session_state.desafio_inter_indice]
    
    st.markdown(f"### Desafio {st.session_state.desafio_inter_tentativas + 1} de 5")
    st.markdown(f"**{p['pergunta']}**")
    
    opcoes = [p['opcao1'], p['opcao2'], p['opcao3']]
    opcao = st.selectbox("📌 Escolha uma opção:", opcoes, key="desafio_inter_opcao")
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("✅ Verificar", key="desafio_inter_verificar"):
            st.session_state.desafio_inter_tentativas += 1
            st.session_state.total += 1
            
            # 🔥 Aceita tanto 'correta' quanto 'resposta'
            resposta_correta = p.get('correta') or p.get('resposta')
            
            if opcao == resposta_correta:
                tocar_som("acerto")
                st.success(f"✅ ACERTOU! +2 pontos")
                st.info(f"💡 {p.get('explicacao', '')}")
                st.session_state.pontos += 2
                st.session_state.desafio_inter_acertos += 1
                
                if st.session_state.nome and st.session_state.turma:
                    salvar_aluno(
                        st.session_state.nome,
                        st.session_state.turma,
                        pontos=st.session_state.pontos,
                        fake_acertos=st.session_state.fake_acertos,
                        cyber_acertos=st.session_state.cyber_acertos,
                        etica_acertos=st.session_state.etica_acertos,
                        total_perguntas=st.session_state.total
                    )
            else:
                tocar_som("erro")
                st.error(f"❌ ERROU! A resposta correta é: {resposta_correta}")
                st.info(f"💡 {p.get('explicacao', '')}")
    
    with col2:
        if st.button("➡️ PRÓXIMO", key="desafio_inter_proximo"):
            st.session_state.desafio_inter_indice += 1
            if st.session_state.desafio_inter_indice >= len(questoes):
                st.session_state.desafio_inter_indice = 0
            st.rerun()
    
    st.divider()
    st.write(f"📊 Desafios: {st.session_state.desafio_inter_tentativas}/5 | ✅ Acertos: {st.session_state.desafio_inter_acertos}")
    
    # ========== PROGRESSO ==========
    if st.session_state.desafio_inter_tentativas > 0:
        st.divider()
        st.subheader("🎯 Seu Progresso")
        
        col1, col2, col3, col4, col5 = st.columns(5)
        niveis = [(1, "🌟"), (2, "⭐"), (3, "🏅"), (4, "🎖️"), (5, "🏆")]
        
        acertos = st.session_state.desafio_inter_acertos
        for i, (nivel, emoji) in enumerate(niveis, 1):
            with col1 if i == 1 else col2 if i == 2 else col3 if i == 3 else col4 if i == 4 else col5:
                if acertos >= nivel:
                    st.markdown(f"""
                    <div style='text-align: center; padding: 10px; background: #28a745; border-radius: 10px; color: white;'>
                        <h2>{emoji}</h2>
                        <p>{nivel}✅</p>
                    </div>
                    """, unsafe_allow_html=True)
                else:
                    st.markdown(f"""
                    <div style='text-align: center; padding: 10px; background: #e9ecef; border-radius: 10px; color: gray;'>
                        <h2>⬜</h2>
                        <p>{nivel}</p>
                    </div>
                    """, unsafe_allow_html=True)
    
    st.divider()
    st.info("💡 Este desafio mistura **Matemática**, **Educação Física** e **Cidadania Digital**!")

# ========== QUIZ DE EDUCAÇÃO FÍSICA ==========
elif menu == "🏃 Quiz de Educação Física":
    st.title("🏃 Quiz de Educação Física")

    mostrar_aluno_atual_e_proximo()   # 🔥 ADICIONE AQUI!
    st.divider()
    
    st.markdown("""
    <div class="card card-ethic">
        <h4>🎯 O QUE É ISSO?</h4>
        <p>Teste seus conhecimentos sobre <strong>Esportes</strong>, <strong>Ginástica</strong>, <strong>Jogos e Brincadeiras</strong> e <strong>Lutas</strong>!</p>
        <p>Professor parceiro: <strong>Luiz Veloso de Lima</strong> 🏃</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.divider()
    
    # ========== INICIALIZAR SESSÃO ==========
    if 'quiz_ef_indice' not in st.session_state:
        st.session_state.quiz_ef_indice = 0
    if 'quiz_ef_acertos' not in st.session_state:
        st.session_state.quiz_ef_acertos = 0
    if 'quiz_ef_tentativas' not in st.session_state:
        st.session_state.quiz_ef_tentativas = 0
    if 'quiz_ef_questoes' not in st.session_state:
        st.session_state.quiz_ef_questoes = []
    
    # ========== PERGUNTAS DO QUIZ ==========
    perguntas_quiz_ef = [
        {
            "pergunta": "Qual dos esportes abaixo é jogado com uma bola e os atletas utilizam as mãos para arremessá-la diretamente dentro da cesta do time adversário?",
            "opcao1": "Futebol",
            "opcao2": "Basquetebol",
            "opcao3": "Beisebol",
            "correta": "Basquetebol",
            "explicacao": "O basquetebol é jogado com as mãos e a bola deve ser arremessada na cesta."
        },
        {
            "pergunta": "O atletismo é considerado um dos esportes mais antigos do mundo. Qual das opções abaixo faz parte das provas de atletismo?",
            "opcao1": "Corrida de 100 metros rasos",
            "opcao2": "Empurrar carrinho de compras",
            "opcao3": "Pular corda sentado",
            "correta": "Corrida de 100 metros rasos",
            "explicacao": "A corrida de 100 metros rasos é uma das provas clássicas do atletismo."
        },
        {
            "pergunta": "O futebol é o esporte mais popular do Brasil. Quantos jogadores titulares compõem uma equipe de futebol em campo durante uma partida oficial?",
            "opcao1": "7 jogadores",
            "opcao2": "5 jogadores",
            "opcao3": "11 jogadores",
            "correta": "11 jogadores",
            "explicacao": "Cada equipe de futebol tem 11 jogadores em campo, incluindo o goleiro."
        },
        {
            "pergunta": "A ginástica rítmica é uma modalidade elegante que utiliza alguns aparelhos oficiais. Qual dos seguintes objetos é utilizado nessa ginástica?",
            "opcao1": "Bola e fita",
            "opcao2": "Bola de boliche e pneu",
            "opcao3": "Skate e capacete",
            "correta": "Bola e fita",
            "explicacao": "A ginástica rítmica utiliza bola, fita, arco, maça e corda."
        },
        {
            "pergunta": "No voleibol, qual é o fundamento utilizado para iniciar o ponto, rebatendo a bola por cima da rede a partir da linha de fundo da quadra?",
            "opcao1": "Saque",
            "opcao2": "Drible",
            "opcao3": "Arremesso",
            "correta": "Saque",
            "explicacao": "O saque é o fundamento que inicia o ponto no voleibol."
        },
        {
            "pergunta": "A ginástica para todos (ou ginástica geral) tem como principal objetivo:",
            "opcao1": "Apenas formar atletas campeões mundiais de alto rendimento",
            "opcao2": "Promover a integração, a saúde, o lazer e a prática sem fins competitivos obrigatórios",
            "opcao3": "Selecionar somente pessoas que já sabem fazer acrobacias difíceis",
            "correta": "Promover a integração, a saúde, o lazer e a prática sem fins competitivos obrigatórios",
            "explicacao": "A ginástica para todos valoriza a inclusão, saúde e lazer."
        },
        {
            "pergunta": "Os jogos populares e tradicionais fazem parte da nossa cultura. Qual destas opções é considerada uma tradicional brincadeira popular brasileira?",
            "opcao1": "Cabo de guerra",
            "opcao2": "Golfe profissional",
            "opcao3": "Esqui na neve",
            "correta": "Cabo de guerra",
            "explicacao": "O cabo de guerra é uma brincadeira tradicional brasileira."
        },
        {
            "pergunta": "Na brincadeira de 'Pega-Pega', qual é o principal objetivo de quem está pegando os outros participantes?",
            "opcao1": "Marcar gols no gol adversário",
            "opcao2": "Tocar levemente em outro colega para passá-lo a vez",
            "opcao3": "Vencer uma corrida de 400 metros",
            "correta": "Tocar levemente em outro colega para passá-lo a vez",
            "explicacao": "No pega-pega, o objetivo é tocar o colega para passar a vez."
        },
        {
            "pergunta": "Brincadeiras como 'Amarelinha' estimulam principalmente qual habilidade motora nas crianças?",
            "opcao1": "O equilíbrio e o salto em um pé só",
            "opcao2": "A força máxima no levantamento de peso",
            "opcao3": "A velocidade de nado em piscina olímpica",
            "correta": "O equilíbrio e o salto em um pé só",
            "explicacao": "A amarelinha desenvolve equilíbrio e coordenação motora."
        },
        {
            "pergunta": "O Judô é uma arte marcial e esporte de combate de origem japonesa. Qual é o significado da palavra 'Judô'?",
            "opcao1": "Caminho suave",
            "opcao2": "Luta pesada",
            "opcao3": "Defesa rápida",
            "correta": "Caminho suave",
            "explicacao": "Judô significa 'caminho suave' em japonês."
        },
        {
            "pergunta": "No boxe, um esporte de combate de luta em pé, os golpes permitidos são desferidos utilizando exclusivamente:",
            "opcao1": "Os pés e os joelhos",
            "opcao2": "Os punhos fechados com luvas adequadas",
            "opcao3": "A cabeça e os cotovelos",
            "correta": "Os punhos fechados com luvas adequadas",
            "explicacao": "No boxe, apenas os punhos com luvas são permitidos."
        },
        {
            "pergunta": "Qual das lutas abaixo é considerada uma manifestação cultural brasileira que mistura luta, dança, música e acrobacias?",
            "opcao1": "Sumô",
            "opcao2": "Capoeira",
            "opcao3": "Taekwondo",
            "correta": "Capoeira",
            "explicacao": "A capoeira mistura luta, dança, música e acrobacias."
        },
        {
            "pergunta": "Qual é o equipamento de proteção obrigatório utilizado na cabeça pelos atletas de Taekwondo em competições oficiais?",
            "opcao1": "Capacete (Protetor de cabeça / Hogu craniano)",
            "opcao2": "Máscara de esgrima com tela de aço",
            "opcao3": "Óculos de natação",
            "correta": "Capacete (Protetor de cabeça / Hogu craniano)",
            "explicacao": "O capacete é obrigatório no Taekwondo para proteger a cabeça."
        },
        {
            "pergunta": "O voleibol é um esporte coletivo em que a bola passa por cima de uma rede central. Quantos toques, no máximo, cada equipe pode dar na bola antes de enviá-la para o campo adversário?",
            "opcao1": "Apenas 1 toque",
            "opcao2": "No máximo 3 toques",
            "opcao3": "Até 5 toques livres",
            "correta": "No máximo 3 toques",
            "explicacao": "Cada equipe pode dar no máximo 3 toques antes de enviar a bola."
        },
        {
            "pergunta": "Na natação, qual estilo é considerado o mais rápido e conhecido popularmente como o nado de frente?",
            "opcao1": "Estilo livre (crawl)",
            "opcao2": "Nado de costas",
            "opcao3": "Nado peito",
            "correta": "Estilo livre (crawl)",
            "explicacao": "O estilo livre (crawl) é o mais rápido da natação."
        },
    ]
    
    # ========== EMBARALHAR PERGUNTAS ==========
    if not st.session_state.quiz_ef_questoes:
        import random
        questoes = perguntas_quiz_ef.copy()
        random.seed(st.session_state.nome)
        random.shuffle(questoes)
        st.session_state.quiz_ef_questoes = questoes
    
    questoes = st.session_state.quiz_ef_questoes
    
    # ========== VERIFICAR SE TERMINOU ==========
    if st.session_state.quiz_ef_tentativas >= 5:
        st.success("🎉 Você completou as 5 perguntas do Quiz de Educação Física!")
        st.write(f"📊 Acertos: {st.session_state.quiz_ef_acertos} de 5")
        
        if st.session_state.quiz_ef_acertos >= 5:
            st.balloons()
            tocar_som("vitoria")
            st.success("🏆 PARABÉNS! VOCÊ É UM MESTRE DA EDUCAÇÃO FÍSICA! 🏆")
        elif st.session_state.quiz_ef_acertos >= 3:
            st.info("⭐ Muito bem! Você foi ótimo!")
        else:
            st.info("💪 Continue praticando! Você vai melhorar!")
        
        if st.button("🔄 Jogar Novamente", key="quiz_ef_reiniciar"):
            st.session_state.quiz_ef_indice = 0
            st.session_state.quiz_ef_acertos = 0
            st.session_state.quiz_ef_tentativas = 0
            st.session_state.quiz_ef_questoes = []
            st.rerun()
        st.stop()
    
    # ========== MOSTRAR PERGUNTA ==========
    if st.session_state.quiz_ef_indice >= len(questoes):
        st.session_state.quiz_ef_indice = 0
    
    p = questoes[st.session_state.quiz_ef_indice]
    
    st.markdown(f"### Pergunta {st.session_state.quiz_ef_tentativas + 1} de 5")
    st.markdown(f"**{p['pergunta']}**")
    
    opcoes = [p['opcao1'], p['opcao2'], p['opcao3']]
    opcao = st.selectbox("📌 Escolha uma opção:", opcoes, key="quiz_ef_opcao")
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("✅ Verificar", key="quiz_ef_verificar"):
            st.session_state.quiz_ef_tentativas += 1
            st.session_state.total += 1
            
            if opcao == p['correta']:
                tocar_som("acerto")
                st.success(f"✅ ACERTOU! +1 ponto")
                st.info(f"💡 {p['explicacao']}")
                st.session_state.pontos += 1
                st.session_state.quiz_ef_acertos += 1
                
                if st.session_state.nome and st.session_state.turma:
                    salvar_aluno(
                        st.session_state.nome,
                        st.session_state.turma,
                        pontos=st.session_state.pontos,
                        fake_acertos=st.session_state.fake_acertos,
                        cyber_acertos=st.session_state.cyber_acertos,
                        etica_acertos=st.session_state.etica_acertos,
                        total_perguntas=st.session_state.total
                    )
            else:
                tocar_som("erro")
                st.error(f"❌ ERROU! A resposta correta é: {p['correta']}")
                st.info(f"💡 {p['explicacao']}")
    
    with col2:
        if st.button("➡️ PRÓXIMO", key="quiz_ef_proximo"):
            st.session_state.quiz_ef_indice += 1
            if st.session_state.quiz_ef_indice >= len(questoes):
                st.session_state.quiz_ef_indice = 0
            st.rerun()
    
    st.divider()
    st.write(f"📊 Tentativas: {st.session_state.quiz_ef_tentativas}/5 | ✅ Acertos: {st.session_state.quiz_ef_acertos}")
    
    # ========== PROGRESSO ==========
    if st.session_state.quiz_ef_tentativas > 0:
        st.divider()
        st.subheader("🎯 Seu Progresso")
        
        col1, col2, col3, col4, col5 = st.columns(5)
        niveis = [(1, "🌟"), (2, "⭐"), (3, "🏅"), (4, "🎖️"), (5, "🏆")]
        
        acertos = st.session_state.quiz_ef_acertos
        for i, (nivel, emoji) in enumerate(niveis, 1):
            with col1 if i == 1 else col2 if i == 2 else col3 if i == 3 else col4 if i == 4 else col5:
                if acertos >= nivel:
                    st.markdown(f"""
                    <div style='text-align: center; padding: 10px; background: #28a745; border-radius: 10px; color: white;'>
                        <h2>{emoji}</h2>
                        <p>{nivel}✅</p>
                    </div>
                    """, unsafe_allow_html=True)
                else:
                    st.markdown(f"""
                    <div style='text-align: center; padding: 10px; background: #e9ecef; border-radius: 10px; color: gray;'>
                        <h2>⬜</h2>
                        <p>{nivel}</p>
                    </div>
                    """, unsafe_allow_html=True)
    
    st.divider()
    st.info("💡 Este quiz foi criado em parceria com o Professor **Luiz Veloso de Lima** (Educação Física)!")

# ========== EQUIPES (GINCANA) ==========
elif menu == "🏆 Equipes (Gincana)":
    st.title("🏆 Equipes (Gincana)")
    
    st.markdown("""
    <div class="card card-mission">
        <h4>🎯 O QUE É ISSO?</h4>
        <p>Forme equipes com seus colegas e respondam <strong>perguntas aleatórias</strong>!</p>
        <p>Quem acertar mais, ganha mais pontos! 🏆</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.divider()
    
    # ========== TABS ==========
    tab1, tab2, tab3, tab4 = st.tabs([
        "📋 Listar Equipes",
        "➕ Criar Equipe",
        "🎮 Jogar",
        "🏆 Ranking"
    ])
    
    # ========== TAB 1: LISTAR ==========
    with tab1:
        st.subheader("📋 Equipes Cadastradas")
        
        equipes = listar_equipes_completas()
        
        if equipes:
            for equipe in equipes:
                with st.expander(f"🏆 {equipe['nome']} - {equipe['turma']} - ⭐ {equipe['pontos']} pontos"):
                    st.write(f"**Turma:** {equipe['turma']}")
                    st.write(f"**Pontos:** ⭐ {equipe['pontos']}")
                    st.write(f"**Criada em:** {equipe['data_criacao']}")
                    
                    if equipe['alunos']:
                        st.write(f"**👥 Alunos ({len(equipe['alunos'])}):**")
                        for aluno in equipe['alunos']:
                            st.write(f"   • {aluno}")
                    else:
                        st.info("📭 Nenhum aluno vinculado.")
                    
                    if st.button(f"🗑️ Excluir Equipe", key=f"del_equipe_{equipe['id']}"):
                        excluir_equipe_completa(equipe['id'])
                        st.success("✅ Equipe excluída!")
                        st.rerun()
        else:
            st.info("📭 Nenhuma equipe cadastrada. Crie uma na aba **➕ Criar Equipe**!")
    
    # ========== TAB 2: CRIAR ==========
    with tab2:
        st.subheader("➕ Criar Nova Equipe")
        
        with st.form("form_criar_equipe"):
            nome_equipe = st.text_input("🏆 Nome da Equipe:")
            turma_equipe = st.selectbox("🏫 Turma:", buscar_todas_turmas())
            
            if st.form_submit_button("💾 Criar Equipe"):
                if nome_equipe and turma_equipe:
                    equipe_id = criar_equipe_completa(nome_equipe, turma_equipe)
                    st.success(f"✅ Equipe '{nome_equipe}' criada!")
                    st.rerun()
                else:
                    st.error("❌ Preencha todos os campos!")
        
        st.divider()
        
        # ========== ADICIONAR ALUNOS ==========
        st.subheader("👥 Adicionar Alunos à Equipe")
        
        equipes = listar_equipes_completas()
        
        if equipes:
            opcoes_equipes = {f"{e['nome']} ({e['turma']})": e['id'] for e in equipes}
            equipe_selecionada = st.selectbox("🏆 Escolha a equipe:", list(opcoes_equipes.keys()))
            
            if equipe_selecionada:
                equipe_id = opcoes_equipes[equipe_selecionada]
                turma_equipe = [e['turma'] for e in equipes if e['id'] == equipe_id][0]
                
                alunos = buscar_alunos_por_turma(turma_equipe)
                
                if alunos:
                    alunos_opcoes = [a['nome'] for a in alunos]
                    aluno_selecionado = st.selectbox("👤 Escolha o aluno:", alunos_opcoes)
                    
                    if st.button("➕ Adicionar Aluno"):
                        adicionar_aluno_equipe(equipe_id, aluno_selecionado, turma_equipe)
                        st.success(f"✅ {aluno_selecionado} adicionado!")
                        st.rerun()
                else:
                    st.info("📭 Nenhum aluno nesta turma.")
        else:
            st.info("📭 Crie uma equipe primeiro!")
    
    # ========== TAB 3: JOGAR ==========
    with tab3:
        st.subheader("🎮 Jogar Gincana")
        
        equipes = listar_equipes_completas()
        
        if not equipes:
            st.warning("⚠️ Crie equipes primeiro!")
            st.stop()
        
        opcoes_equipes = {f"{e['nome']} ({e['turma']})": e['id'] for e in equipes}
        equipe_selecionada = st.selectbox("🏆 Escolha a equipe:", list(opcoes_equipes.keys()), key="equipe_jogar")
        
        if equipe_selecionada:
            equipe_id = opcoes_equipes[equipe_selecionada]
            turma_equipe = [e['turma'] for e in equipes if e['id'] == equipe_id][0]
            
            # ========== INICIALIZAR SESSÃO ==========
            if 'equipe_questoes' not in st.session_state:
                st.session_state.equipe_questoes = []
            if 'equipe_indice' not in st.session_state:
                st.session_state.equipe_indice = 0
            if 'equipe_acertos' not in st.session_state:
                st.session_state.equipe_acertos = 0
            if 'equipe_tentativas' not in st.session_state:
                st.session_state.equipe_tentativas = 0
            if 'equipe_atual_id' not in st.session_state:
                st.session_state.equipe_atual_id = None
            
            # ========== CARREGAR QUESTÕES ==========
            if st.session_state.equipe_atual_id != equipe_id:
                import random
                questoes = buscar_questoes_equipe(turma_equipe, "fake")
                if questoes:
                    random.shuffle(questoes)
                    st.session_state.equipe_questoes = questoes
                    st.session_state.equipe_indice = 0
                    st.session_state.equipe_acertos = 0
                    st.session_state.equipe_tentativas = 0
                    st.session_state.equipe_atual_id = equipe_id
                else:
                    st.warning("⚠️ Nenhuma pergunta encontrada.")
                    st.stop()
            
            questoes = st.session_state.equipe_questoes
            
            # ========== VERIFICAR SE TERMINOU ==========
            if st.session_state.equipe_tentativas >= 5:
                st.success(f"🎉 Equipe completou as 5 perguntas!")
                st.write(f"📊 Acertos: {st.session_state.equipe_acertos} de 5")
                
                # Adicionar pontos à equipe
                if st.session_state.equipe_acertos > 0:
                    adicionar_pontos_equipe_completa(equipe_id, st.session_state.equipe_acertos)
                    st.success(f"🏆 +{st.session_state.equipe_acertos} pontos para a equipe!")
                
                if st.session_state.equipe_acertos >= 5:
                    st.balloons()
                    tocar_som("vitoria")
                    st.success("🏆 PARABÉNS! A EQUIPE ACERTOU TUDO! 🏆")
                
                if st.button("🔄 Jogar Novamente", key="equipe_reiniciar"):
                    st.session_state.equipe_atual_id = None
                    st.rerun()
                st.stop()
            
            # ========== MOSTRAR PERGUNTA ==========
            p = questoes[st.session_state.equipe_indice % len(questoes)]
            
            st.markdown(f"**Pergunta {st.session_state.equipe_tentativas + 1} de 5**")
            st.markdown(f"**{p['pergunta']}**")
            
            opcao = st.selectbox("📌 Escolha:", ["Selecione", "Verdade", "Fake"], key="equipe_opcao")
            
            if st.button("✅ Verificar", key="equipe_verificar"):
                if opcao == "Selecione":
                    st.warning("⚠️ Selecione uma opção!")
                else:
                    st.session_state.equipe_tentativas += 1
                    
                    if opcao == p['resposta']:
                        tocar_som("acerto")
                        st.success("✅ ACERTOU! +1 ponto")
                        st.session_state.equipe_acertos += 1
                    else:
                        tocar_som("erro")
                        st.error(f"❌ ERROU! A resposta é: {p['resposta']}")
                    
                    if p.get('explicacao'):
                        st.info(f"💡 {p['explicacao']}")
                    
                    st.session_state.equipe_indice += 1
                    st.rerun()
            
            st.divider()
            st.write(f"📊 Tentativas: {st.session_state.equipe_tentativas}/5 | ✅ Acertos: {st.session_state.equipe_acertos}")
    
    # ========== TAB 4: RANKING ==========
    with tab4:
        st.subheader("🏆 Ranking das Equipes")
        
        equipes = listar_equipes_completas()
        
        if equipes:
            for i, equipe in enumerate(equipes, 1):
                medalha = "🥇" if i == 1 else "🥈" if i == 2 else "🥉" if i == 3 else f"{i}º"
                
                st.markdown(f"""
                <div style='padding: 15px; margin: 10px 0; background: linear-gradient(135deg, #1a3a5c, #2d5f8a); border-radius: 12px; color: white;'>
                    <h3>{medalha} {equipe['nome']}</h3>
                    <p>🏫 {equipe['turma']} | 👥 {len(equipe['alunos'])} alunos</p>
                    <p>⭐ <strong>{equipe['pontos']}</strong> pontos</p>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.info("📭 Nenhuma equipe cadastrada.")

# ========== CASOS REAIS (PBL) ==========
elif menu == "📋 Casos Reais (PBL)":
    st.title("📋 Casos Reais - Investigação (PBL)")
    
    st.markdown("""
    <div class="card card-mission">
        <h4>🎯 O QUE É ISSO?</h4>
        <p>Você vai <strong>investigar</strong> casos reais de fake news, cyberbullying e discurso de ódio!</p>
        <p>Colete dados, calcule o impacto e proponha uma solução! 🔍</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.divider()
    
    # ========== INICIALIZAR CASOS ==========
    from database import inserir_casos_pbl, listar_casos_pbl
    inserir_casos_pbl()
    
    casos = listar_casos_pbl()
    
    if not casos:
        st.warning("⚠️ Nenhum caso cadastrado.")
        st.stop()
    
    # ========== INICIALIZAR SESSÃO ==========
    if 'caso_atual' not in st.session_state:
        st.session_state.caso_atual = None
    if 'caso_etapa' not in st.session_state:
        st.session_state.caso_etapa = 1
    if 'caso_resposta' not in st.session_state:
        st.session_state.caso_resposta = ""
    
    # ========== ESCOLHER CASO ==========
    st.subheader("📌 Escolha um Caso para Investigar")
    
    opcoes_casos = {f"{c['titulo']} ({c['tipo']})": c['id'] for c in casos}
    caso_selecionado = st.selectbox("🔍 Escolha o caso:", ["Selecione..."] + list(opcoes_casos.keys()))
    
    if caso_selecionado != "Selecione...":
        caso_id = opcoes_casos[caso_selecionado]
        
        if st.session_state.caso_atual != caso_id:
            st.session_state.caso_atual = caso_id
            st.session_state.caso_etapa = 1
            st.session_state.caso_resposta = ""
        
        caso = buscar_caso_pbl(caso_id)
        
        if caso:
            st.divider()
            
            # ========== ETAPA 1: LEITURA ==========
            if st.session_state.caso_etapa == 1:
                st.subheader(f"📖 Caso: {caso['titulo']}")
                
                st.markdown(f"""
                <div style='background: #fff3cd; padding: 20px; border-radius: 12px; border-left: 5px solid #ffc107;'>
                    <h4>📰 {caso['titulo']}</h4>
                    <p style='font-size: 1.1rem;'>{caso['descricao']}</p>
                </div>
                """, unsafe_allow_html=True)
                
                st.divider()
                
                st.subheader("🔍 Etapa 1: Investigação")
                st.write("**Leia o caso com atenção e responda:**")
                
                st.write("1. O que aconteceu?")
                st.write("2. Quem foi prejudicado?")
                st.write("3. Que tipo de problema é esse?")
                
                if st.button("✅ Entendi, próxima etapa", key="caso_etapa1"):
                    st.session_state.caso_etapa = 2
                    st.rerun()
            
            # ========== ETAPA 2: CÁLCULOS ==========
            elif st.session_state.caso_etapa == 2:
                st.subheader("🧮 Etapa 2: Análise de Dados")
                
                st.info(f"💡 **Dados do caso:** {caso['dados']}")
                
                st.write("**Vamos calcular o impacto!**")
                
                # ========== CÁLCULOS POR TIPO ==========
                if caso['tipo'] == "fake_news":
                    st.write("**📊 Calcule o alcance total:**")
                    st.write("Se 120 compartilhamentos × 8 pessoas = ?")
                    
                    resposta = st.number_input("Quantas pessoas foram atingidas?", min_value=0, value=0, step=1, key="calc_fake")
                    
                    if st.button("✅ Verificar", key="verificar_fake"):
                        if resposta == 960:
                            st.success("✅ CORRETO! 120 × 8 = 960 pessoas atingidas!")
                            st.session_state.caso_etapa = 3
                            st.rerun()
                        else:
                            st.error("❌ Tente novamente! 120 × 8 = ?")
                
                elif caso['tipo'] == "cyberbullying":
                    st.write("**📊 Calcule o total de mensagens ofensivas:**")
                    st.write("Se 15 alunos × 10 mensagens = ?")
                    
                    resposta = st.number_input("Quantas mensagens ofensivas?", min_value=0, value=0, step=1, key="calc_cyber")
                    
                    if st.button("✅ Verificar", key="verificar_cyber"):
                        if resposta == 150:
                            st.success("✅ CORRETO! 15 × 10 = 150 mensagens!")
                            st.session_state.caso_etapa = 3
                            st.rerun()
                        else:
                            st.error("❌ Tente novamente! 15 × 10 = ?")
                
                elif caso['tipo'] == "discurso_odio":
                    st.write("**📊 Calcule a porcentagem de denúncias:**")
                    st.write("Se 50 denúncias em 500 visualizações = ?")
                    
                    resposta = st.number_input("Qual a porcentagem? (%)", min_value=0, max_value=100, value=0, step=1, key="calc_odio")
                    
                    if st.button("✅ Verificar", key="verificar_odio"):
                        if resposta == 10:
                            st.success("✅ CORRETO! 50 ÷ 500 = 10%")
                            st.session_state.caso_etapa = 3
                            st.rerun()
                        else:
                            st.error("❌ Tente novamente! 50 ÷ 500 = ?")
                
                elif caso['tipo'] == "deepfake":
                    st.write("**📊 Calcule a porcentagem de compartilhamentos:**")
                    st.write("Se 300 compartilhamentos em 1.000 visualizações = ?")
                    
                    resposta = st.number_input("Qual a porcentagem? (%)", min_value=0, max_value=100, value=0, step=1, key="calc_deep")
                    
                    if st.button("✅ Verificar", key="verificar_deep"):
                        if resposta == 30:
                            st.success("✅ CORRETO! 300 ÷ 1000 = 30%")
                            st.session_state.caso_etapa = 3
                            st.rerun()
                        else:
                            st.error("❌ Tente novamente! 300 ÷ 1000 = ?")
                
                elif caso['tipo'] == "efeito_bolha":
                    st.write("**📊 Calcule a porcentagem de outros assuntos:**")
                    st.write("Se 10% de outros assuntos, quantos % são de futebol?")
                    
                    resposta = st.number_input("Qual a porcentagem? (%)", min_value=0, max_value=100, value=0, step=1, key="calc_bolha")
                    
                    if st.button("✅ Verificar", key="verificar_bolha"):
                        if resposta == 90:
                            st.success("✅ CORRETO! 100% - 10% = 90%")
                            st.session_state.caso_etapa = 3
                            st.rerun()
                        else:
                            st.error("❌ Tente novamente!")
                
                elif caso['tipo'] == "cancelamento":
                    st.write("**📊 Calcule a porcentagem de defesas:**")
                    st.write("Se 50 defesas em 200 comentários = ?")
                    
                    resposta = st.number_input("Qual a porcentagem? (%)", min_value=0, max_value=100, value=0, step=1, key="calc_canc")
                    
                    if st.button("✅ Verificar", key="verificar_canc"):
                        if resposta == 25:
                            st.success("✅ CORRETO! 50 ÷ 200 = 25%")
                            st.session_state.caso_etapa = 3
                            st.rerun()
                        else:
                            st.error("❌ Tente novamente! 50 ÷ 200 = ?")
            
            # ========== ETAPA 3: SOLUÇÃO ==========
            elif st.session_state.caso_etapa == 3:
                st.subheader("💡 Etapa 3: Proposta de Solução")
                
                st.write("**O que você faria para resolver esse caso?**")
                
                resposta = st.text_area(
                    "📝 Escreva sua solução:",
                    height=150,
                    placeholder="Ex: Verificar a fonte, avisar a direção, criar um comunicado oficial...",
                    key="solucao_caso"
                )
                
                if st.button("✅ Enviar Solução", key="enviar_solucao"):
                    if resposta and len(resposta) > 10:
                        # 💾 SALVAR NO BANCO
                        from database import salvar_resposta_pbl
                        salvar_resposta_pbl(
                            st.session_state.nome,
                            st.session_state.turma,
                            caso['titulo'],
                            resposta
                        )
                        
                        st.session_state.caso_resposta = resposta
                        st.session_state.caso_etapa = 4
                        st.success("✅ Resposta enviada e salva!")
                        st.rerun()
                    else:
                        st.warning("⚠️ Escreva uma solução com pelo menos 10 caracteres!")
            
            # ========== ETAPA 4: RESULTADO ==========
            elif st.session_state.caso_etapa == 4:
                st.balloons()
                tocar_som("vitoria")
                
                st.success("🎉 PARABÉNS! Você completou a investigação!")
                
                st.subheader("📊 Resultado da Investigação")
                
                st.markdown(f"""
                <div style='background: #d4edda; padding: 20px; border-radius: 12px; border-left: 5px solid #28a745;'>
                    <h4>✅ Solução Esperada:</h4>
                    <p>{caso['solucao_esperada']}</p>
                </div>
                """, unsafe_allow_html=True)
                
                st.divider()
                
                st.subheader("📝 Sua Solução")
                st.info(st.session_state.caso_resposta)

                # 📄 GERAR TXT
                relatorio = f"""
==================================================
   📋 RELATÓRIO DE INVESTIGAÇÃO PBL
==================================================
👤 Aluno: {st.session_state.nome}
🏫 Turma: {st.session_state.turma}
📅 Data: {datetime.now().strftime('%d/%m/%Y %H:%M')}
==================================================

📌 CASO: {caso['titulo']}
📝 Descrição: {caso['descricao']}

📊 DADOS: {caso['dados']}

💡 SOLUÇÃO DO ALUNO:
{st.session_state.caso_resposta}

✅ SOLUÇÃO ESPERADA:
{caso['solucao_esperada']}

==================================================
   EEEF PROFª ODETE MENDES N OLIVEIRA
   Professor: Irving Vasconcelos dos Santos (CICI)
==================================================
"""
                
                st.download_button(
                    label="📥 Baixar Relatório TXT",
                    data=relatorio,
                    file_name=f"relatorio_pbl_{st.session_state.nome.replace(' ', '_')}.txt",
                    mime="text/plain",
                    key="download_pbl"
                )

                # ========== PONTOS ==========
                st.session_state.pontos += caso['pontos']
                st.success(f"⭐ +{caso['pontos']} pontos!")
                
                if st.session_state.nome and st.session_state.turma:
                    salvar_aluno(
                        st.session_state.nome,
                        st.session_state.turma,
                        pontos=st.session_state.pontos,
                        fake_acertos=st.session_state.fake_acertos,
                        cyber_acertos=st.session_state.cyber_acertos,
                        etica_acertos=st.session_state.etica_acertos,
                        total_perguntas=st.session_state.total
                    )
                
                if st.button("🔄 Investigar Outro Caso", key="novo_caso"):
                    st.session_state.caso_atual = None
                    st.session_state.caso_etapa = 1
                    st.session_state.caso_resposta = ""
                    st.rerun()
    
    else:
        st.info("💡 Escolha um caso acima para começar a investigação!")
    
    st.divider()
    st.info("💡 **Metodologia PBL:** Investigação → Análise → Solução!")

# ========== ALGORITMO ANTI-FAKE NEWS ==========
elif menu == "📝 Algoritmo Anti-Fake News":
    st.title("📝 Algoritmo Anti-Fake News")
    
    st.markdown("""
    <div class="card card-mission">
        <h4>🎯 O QUE É ISSO?</h4>
        <p>Você vai <strong>criar um algoritmo</strong> (passo a passo lógico) para verificar se uma notícia é verdadeira ou falsa!</p>
        <p>Use <strong>SE / ENTÃO / SENÃO</strong> como um programador! 🧠</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.divider()
    
    # ========== INICIALIZAR SESSÃO ==========
    if 'algoritmo_etapa' not in st.session_state:
        st.session_state.algoritmo_etapa = 1
    if 'algoritmo_passos' not in st.session_state:
        st.session_state.algoritmo_passos = []
    if 'algoritmo_noticia' not in st.session_state:
        st.session_state.algoritmo_noticia = ""
    
    # ========== TABS ==========
    tab1, tab2 = st.tabs(["📝 Criar Algoritmo", "📚 Meus Algoritmos"])
    
    # ========== TAB 1: CRIAR ==========
    with tab1:
        st.subheader("📝 Crie seu Algoritmo Anti-Fake News")
        
        # ========== ETAPA 1: ESCOLHER A NOTÍCIA ==========
        if st.session_state.algoritmo_etapa == 1:
            st.markdown("### 🔍 Etapa 1: Escolha uma notícia para testar")
            
            noticia = st.text_area(
                "📰 Cole a notícia aqui:",
                value="URGENTE! A comida da escola está vencida e todos vão passar mal!",
                height=100,
                key="noticia_algoritmo"
            )
            
            if st.button("✅ Próxima Etapa", key="alg_etapa1"):
                if noticia:
                    st.session_state.algoritmo_noticia = noticia
                    st.session_state.algoritmo_etapa = 2
                    st.rerun()
                else:
                    st.warning("⚠️ Cole uma notícia!")
        
        # ========== ETAPA 2: CRIAR PASSOS ==========
        elif st.session_state.algoritmo_etapa == 2:
            st.markdown("### 🧠 Etapa 2: Crie os passos do algoritmo")
            
            st.info(f"📰 **Notícia:** {st.session_state.algoritmo_noticia}")
            
            st.divider()
            
            # ========== PASSO 1 ==========
            st.markdown("#### 🔍 Passo 1: A notícia tem fonte?")
            
            fonte = st.radio(
                "A notícia tem fonte?",
                ["Sim", "Não"],
                key="alg_fonte"
            )
            
            if fonte == "Não":
                st.error("❌ **ENTÃO:** É FAKE NEWS! Sem fonte = fake!")
                st.info("💡 **Algoritmo:** `SE não tem fonte → ENTÃO é fake`")
            else:
                st.success("✅ **ENTÃO:** Vamos verificar a fonte!")
            
            st.divider()
            
            # ========== PASSO 2 ==========
            if fonte == "Sim":
                st.markdown("#### 🔍 Passo 2: A fonte é confiável?")
                
                confiavel = st.radio(
                    "A fonte é confiável?",
                    ["Sim", "Não"],
                    key="alg_confiavel"
                )
                
                if confiavel == "Não":
                    st.error("❌ **ENTÃO:** É FAKE NEWS! Fonte não confiável!")
                    st.info("💡 **Algoritmo:** `SE fonte não é confiável → ENTÃO é fake`")
                else:
                    st.success("✅ **ENTÃO:** Vamos verificar outros sites!")
            
            st.divider()
            
            # ========== PASSO 3 ==========
            if fonte == "Sim" and confiavel == "Sim":
                st.markdown("#### 🔍 Passo 3: Outros sites confirmam?")
                
                outros = st.radio(
                    "Outros sites confirmam?",
                    ["Sim", "Não"],
                    key="alg_outros"
                )
                
                if outros == "Não":
                    st.error("❌ **ENTÃO:** É FAKE NEWS! Ninguém confirma!")
                    st.info("💡 **Algoritmo:** `SE outros não confirmam → ENTÃO é fake`")
                else:
                    st.success("✅ **ENTÃO:** Vamos verificar a data!")
            
            st.divider()
            
            # ========== PASSO 4 ==========
            if fonte == "Sim" and confiavel == "Sim" and outros == "Sim":
                st.markdown("#### 🔍 Passo 4: A data é recente?")
                
                data = st.radio(
                    "A data é recente?",
                    ["Sim", "Não"],
                    key="alg_data"
                )
                
                if data == "Não":
                    st.error("❌ **ENTÃO:** É FAKE NEWS! Notícia antiga!")
                    st.info("💡 **Algoritmo:** `SE data não é recente → ENTÃO é fake`")
                else:
                    st.success("✅ **ENTÃO:** É VERDADE! Notícia confiável!")
                    st.info("💡 **Algoritmo:** `SE todas as respostas forem SIM → ENTÃO é verdade`")
            
            st.divider()
            
            # ========== BOTÃO PARA SALVAR ==========
            if st.button("💾 Salvar Algoritmo", key="alg_salvar"):
                # Montar o algoritmo em texto
                passos = f"""
==================================================
   📝 ALGORITMO ANTI-FAKE NEWS
==================================================
👤 Aluno: {st.session_state.nome}
🏫 Turma: {st.session_state.turma}
📅 Data: {datetime.now().strftime('%d/%m/%Y %H:%M')}
==================================================

📰 NOTÍCIA: {st.session_state.algoritmo_noticia}

🔍 ALGORITMO:

1. SE a notícia NÃO tem fonte:
   ENTÃO → É FAKE NEWS!
   SENÃO → Vá para o passo 2

2. SE a fonte NÃO é confiável:
   ENTÃO → É FAKE NEWS!
   SENÃO → Vá para o passo 3

3. SE outros sites NÃO confirmam:
   ENTÃO → É FAKE NEWS!
   SENÃO → Vá para o passo 4

4. SE a data NÃO é recente:
   ENTÃO → É FAKE NEWS!
   SENÃO → É VERDADE!

==================================================
   EEEF PROFª ODETE MENDES N OLIVEIRA
   Professor: Irving Vasconcelos dos Santos (CICI)
==================================================
"""
                
                # Salvar no banco
                from database import salvar_algoritmo
                salvar_algoritmo(
                    st.session_state.nome,
                    st.session_state.turma,
                    passos
                )
                
                st.success("✅ Algoritmo salvo com sucesso!")
                st.balloons()
                tocar_som("vitoria")
                
                # Mostrar o algoritmo
                st.code(passos, language="text")
                
                # Pontos
                st.session_state.pontos += 5
                st.success("⭐ +5 pontos!")
                
                # Botão para novo algoritmo
                if st.button("🔄 Criar Novo Algoritmo", key="alg_novo"):
                    st.session_state.algoritmo_etapa = 1
                    st.session_state.algoritmo_passos = []
                    st.session_state.algoritmo_noticia = ""
                    st.rerun()
        
        # ========== FLUXOGRAMA VISUAL ==========
        st.divider()
        st.subheader("📊 Fluxograma Visual")
        
        st.code("""
┌─────────────────────┐
│  1. TEM FONTE?      │
└─────────┬───────────┘
          │
  ┌───────┴───────┐
  │ SIM           │ NÃO
  ▼               ▼
┌─────────┐   ┌─────────┐
│ PASSO 2 │   │ ❌ FAKE │
└────┬────┘   └─────────┘
     │
┌────▼─────────────────┐
│  2. FONTE CONFIÁVEL? │
└─────────┬────────────┘
          │
  ┌───────┴───────┐
  │ SIM           │ NÃO
  ▼               ▼
┌─────────┐   ┌─────────┐
│ PASSO 3 │   │ ❌ FAKE │
└────┬────┘   └─────────┘
     │
┌────▼─────────────────┐
│  3. OUTROS CONFIRMAM?│
└─────────┬────────────┘
          │
  ┌───────┴───────┐
  │ SIM           │ NÃO
  ▼               ▼
┌─────────┐   ┌─────────┐
│ PASSO 4 │   │ ❌ FAKE │
└────┬────┘   └─────────┘
     │
┌────▼─────────────────┐
│  4. DATA É RECENTE?  │
└─────────┬────────────┘
          │
  ┌───────┴───────┐
  │ SIM           │ NÃO
  ▼               ▼
┌─────────┐   ┌─────────┐
│ ✅ VERD │   │ ❌ FAKE │
└─────────┘   └─────────┘
        """, language="text")
    
    # ========== TAB 2: MEUS ALGORITMOS ==========
    with tab2:
        st.subheader("📚 Meus Algoritmos")
        
        from database import listar_algoritmos_aluno
        
        algoritmos = listar_algoritmos_aluno(
            st.session_state.nome,
            st.session_state.turma
        )
        
        if algoritmos:
            for alg in algoritmos:
                with st.expander(f"📝 Algoritmo de {alg['data']}"):
                    st.code(alg['passos'], language="text")
                    
                    if st.button(f"🗑️ Excluir", key=f"del_alg_{alg['id']}"):
                        from database import excluir_algoritmo
                        excluir_algoritmo(alg['id'])
                        st.success("✅ Algoritmo excluído!")
                        st.rerun()
        else:
            st.info("📭 Nenhum algoritmo criado ainda.")
    
    st.divider()
    st.info("💡 **Pensamento Computacional:** SE / ENTÃO / SENÃO é a base da programação!")

# ========== DISSEQUE O ALGORITMO ==========
elif menu == "🧠 Disseque o Algoritmo":
    st.title("🧠 Disseque o Algoritmo (Caixa-Preta)")
    
    st.markdown("""
    <div class="card card-mission">
        <h4>🎯 O QUE É ISSO?</h4>
        <p>Você vai <strong>dissecar</strong> como o algoritmo das redes sociais funciona!</p>
        <p>Descubra a <strong>caixa-preta</strong> e entenda o <strong>efeito bolha</strong>! 🧠</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.divider()
    
    # ========== TABS ==========
    tab1, tab2 = st.tabs(["🔍 Dissecar Algoritmo", "📚 Minhas Dissecações"])
    
    # ========== TAB 1: DISSECAR ==========
    with tab1:
        st.subheader("🔍 Como funciona o algoritmo?")
        
        st.write("**O algoritmo das redes sociais observa tudo o que você faz:**")
        st.write("• ❤️ O que você curte")
        st.write("• 👀 O que você assiste")
        st.write("• 💬 O que você comenta")
        st.write("• 🔗 O que você compartilha")
        
        st.divider()
        
        # ========== INICIALIZAR SESSÃO ==========
        if 'disseca_curtidas' not in st.session_state:
            st.session_state.disseca_curtidas = {
                "Futebol": 0,
                "Notícias": 0,
                "Memes": 0,
                "Educação": 0,
                "Música": 0
            }
        if 'disseca_etapa' not in st.session_state:
            st.session_state.disseca_etapa = 1
        if 'disseca_conclusao' not in st.session_state:
            st.session_state.disseca_conclusao = ""
        
        # ========== ETAPA 1: CURTIR CONTEÚDOS ==========
        if st.session_state.disseca_etapa == 1:
            st.markdown("### 👆 Etapa 1: Curta conteúdos")
            
            st.write("**Clique nos conteúdos que você gosta:**")
            
            col1, col2, col3, col4, col5 = st.columns(5)
            
            with col1:
                st.markdown("### ⚽")
                st.write("**Futebol**")
                if st.button("❤️ Curtir", key="curtir_futebol"):
                    st.session_state.disseca_curtidas["Futebol"] += 1
                    st.rerun()
                st.write(f"❤️ {st.session_state.disseca_curtidas['Futebol']}")
            
            with col2:
                st.markdown("### 📰")
                st.write("**Notícias**")
                if st.button("❤️ Curtir", key="curtir_noticias"):
                    st.session_state.disseca_curtidas["Notícias"] += 1
                    st.rerun()
                st.write(f"❤️ {st.session_state.disseca_curtidas['Notícias']}")
            
            with col3:
                st.markdown("### 😂")
                st.write("**Memes**")
                if st.button("❤️ Curtir", key="curtir_memes"):
                    st.session_state.disseca_curtidas["Memes"] += 1
                    st.rerun()
                st.write(f"❤️ {st.session_state.disseca_curtidas['Memes']}")
            
            with col4:
                st.markdown("### 📚")
                st.write("**Educação**")
                if st.button("❤️ Curtir", key="curtir_educacao"):
                    st.session_state.disseca_curtidas["Educação"] += 1
                    st.rerun()
                st.write(f"❤️ {st.session_state.disseca_curtidas['Educação']}")
            
            with col5:
                st.markdown("### 🎵")
                st.write("**Música**")
                if st.button("❤️ Curtir", key="curtir_musica"):
                    st.session_state.disseca_curtidas["Música"] += 1
                    st.rerun()
                st.write(f"❤️ {st.session_state.disseca_curtidas['Música']}")
            
            st.divider()
            
            # ========== MOSTRAR CURTIDAS ==========
            total_curtidas = sum(st.session_state.disseca_curtidas.values())
            
            if total_curtidas > 0:
                st.subheader("📊 Suas Curtidas")
                
                for categoria, qtd in st.session_state.disseca_curtidas.items():
                    if qtd > 0:
                        st.write(f"{categoria}: {'❤️' * qtd} ({qtd})")
                
                st.divider()
                
                # ========== BOTÃO PARA ANALISAR ==========
                if st.button("🔍 Analisar o que o algoritmo faria", key="analisar_alg"):
                    st.session_state.disseca_etapa = 2
                    st.rerun()
        
        # ========== ETAPA 2: DESCOBRIR O ALGORITMO ==========
        elif st.session_state.disseca_etapa == 2:
            st.markdown("### 🤖 Etapa 2: O que o algoritmo descobriu?")
            
            # Descobrir a categoria mais curtida
            mais_curtida = max(st.session_state.disseca_curtidas, key=st.session_state.disseca_curtidas.get)
            total = sum(st.session_state.disseca_curtidas.values())
            
            if total == 0:
                st.warning("⚠️ Você não curtiu nada! O algoritmo não tem dados sobre você.")
                if st.button("🔄 Voltar", key="voltar_etapa1"):
                    st.session_state.disseca_etapa = 1
                    st.rerun()
            else:
                st.markdown(f"""
                <div style='background: linear-gradient(135deg, #6f42c1, #9b59b6); padding: 25px; border-radius: 15px; color: white; text-align: center;'>
                    <h2>🤖 O ALGORITMO DIZ:</h2>
                    <h3>Você gosta de <strong>{mais_curtida}</strong>!</h3>
                    <p>Vou te mostrar MAIS conteúdo sobre {mais_curtida}!</p>
                </div>
                """, unsafe_allow_html=True)
                
                st.divider()
                
                st.subheader("💡 O que isso significa?")
                
                st.warning(f"""
                🚨 **VOCÊ ESTÁ ENTRANDO NA BOLHA!**
                
                O algoritmo percebeu que você gosta de **{mais_curtida}** 
                e agora vai te mostrar **APENAS** conteúdo sobre isso!
                
                **Consequências:**
                - ❌ Você não vê outros pontos de vista
                - ❌ Você só vê o que concorda
                - ❌ Você fica isolado em sua "bolha"
                """)
                
                st.divider()
                
                # ========== GRÁFICO ==========
                st.subheader("📊 Suas Curtidas")
                
                import pandas as pd
                dados = pd.DataFrame([
                    {"Categoria": k, "Curtidas": v}
                    for k, v in st.session_state.disseca_curtidas.items()
                    if v > 0
                ])
                st.bar_chart(dados.set_index('Categoria'))
                
                st.divider()
                
                # ========== PERGUNTA ==========
                st.subheader("🧠 O que você aprendeu?")
                
                conclusao = st.text_area(
                    "📝 Escreva sua conclusão sobre o algoritmo:",
                    height=150,
                    placeholder="Ex: O algoritmo mostra apenas o que eu gosto, criando uma bolha...",
                    key="conclusao_dissecacao"
                )
                
                if st.button("✅ Salvar Conclusão", key="salvar_dissecacao"):
                    if conclusao and len(conclusao) > 10:
                        # Salvar no banco
                        from database import salvar_dissecacao
                        salvar_dissecacao(
                            st.session_state.nome,
                            st.session_state.turma,
                            st.session_state.disseca_curtidas,
                            conclusao
                        )
                        
                        st.session_state.disseca_conclusao = conclusao
                        st.session_state.disseca_etapa = 3
                        st.rerun()
                    else:
                        st.warning("⚠️ Escreva uma conclusão com pelo menos 10 caracteres!")
        
        # ========== ETAPA 3: RESULTADO ==========
        elif st.session_state.disseca_etapa == 3:
            st.balloons()
            tocar_som("vitoria")
            
            st.success("🎉 PARABÉNS! Você dissecou o algoritmo!")
            
            st.subheader("📝 Sua Conclusão")
            st.info(st.session_state.disseca_conclusao)
            
            st.divider()
            
            # ========== DICAS ==========
            st.subheader("💡 Como sair da bolha?")
            
            st.success("""
            ✅ **DICAS PARA SAIR DA BOLHA:**
            
            1. 📰 **Leia notícias de fontes diferentes**
            2. 👥 **Siga pessoas com opiniões diferentes**
            3. 🔍 **Pesquise sobre o assunto antes de compartilhar**
            4. 💬 **Converse com pessoas que pensam diferente**
            5. 🧠 **Questione o que o algoritmo te mostra**
            """)
            
            # ========== PONTOS ==========
            st.session_state.pontos += 5
            st.success("⭐ +5 pontos!")
            
            if st.session_state.nome and st.session_state.turma:
                salvar_aluno(
                    st.session_state.nome,
                    st.session_state.turma,
                    pontos=st.session_state.pontos,
                    fake_acertos=st.session_state.fake_acertos,
                    cyber_acertos=st.session_state.cyber_acertos,
                    etica_acertos=st.session_state.etica_acertos,
                    total_perguntas=st.session_state.total
                )
            
            if st.button("🔄 Dissecar Novamente", key="dissecar_novo"):
                st.session_state.disseca_curtidas = {
                    "Futebol": 0,
                    "Notícias": 0,
                    "Memes": 0,
                    "Educação": 0,
                    "Música": 0
                }
                st.session_state.disseca_etapa = 1
                st.session_state.disseca_conclusao = ""
                st.rerun()
    
    # ========== TAB 2: MINHAS DISSECAÇÕES ==========
    with tab2:
        st.subheader("📚 Minhas Dissecações")
        
        from database import listar_dissecacoes_aluno
        
        disseca = listar_dissecacoes_aluno(
            st.session_state.nome,
            st.session_state.turma
        )
        
        if disseca:
            for d in disseca:
                with st.expander(f"📝 Dissecação de {d['data']}"):
                    st.write(f"**Curtidas:** {d['curtidas']}")
                    st.write(f"**Conclusão:**")
                    st.info(d['conclusao'])
                    
                    if st.button(f"🗑️ Excluir", key=f"del_disseca_{d['id']}"):
                        from database import excluir_dissecacao
                        excluir_dissecacao(d['id'])
                        st.success("✅ Dissecação excluída!")
                        st.rerun()
        else:
            st.info("📭 Nenhuma dissecação criada ainda.")
    
    st.divider()
    st.info("💡 **Cultura Digital:** Entender o algoritmo é o primeiro passo para não ser manipulado!")

# ========== DISCURSO DE ÓDIO vs. LIBERDADE ==========
elif menu == "⚖️ Discurso de Ódio vs. Liberdade":
    st.title("⚖️ Discurso de Ódio vs. Liberdade de Expressão")
    
    st.markdown("""
    <div class="card card-mission">
        <h4>🎯 O QUE É ISSO?</h4>
        <p>Você vai <strong>classificar frases</strong> como <strong>Liberdade de Expressão</strong> ou <strong>Discurso de Ódio</strong>!</p>
        <p>Aprenda a diferença e reflita sobre ética digital! ⚖️</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.divider()
    
    # ========== INICIALIZAR SESSÃO ==========
    if 'debate_indice' not in st.session_state:
        st.session_state.debate_indice = 0
    if 'debate_acertos' not in st.session_state:
        st.session_state.debate_acertos = 0
    if 'debate_tentativas' not in st.session_state:
        st.session_state.debate_tentativas = 0
    if 'debate_classificacoes' not in st.session_state:
        st.session_state.debate_classificacoes = []
    
    # ========== FRASES ==========
    frases = [
        {
            "frase": "Eu não gosto de futebol, prefiro basquete.",
            "tipo": "liberdade",
            "explicacao": "É uma opinião pessoal, sem ofender ninguém."
        },
        {
            "frase": "Quem torce para o time X é burro e não entende nada.",
            "tipo": "odio",
            "explicacao": "Ofende e desqualifica pessoas por sua escolha."
        },
        {
            "frase": "Acho que o governo deveria investir mais em educação.",
            "tipo": "liberdade",
            "explicacao": "É uma opinião política, sem ofender pessoas."
        },
        {
            "frase": "Pessoas que pensam diferente de mim deveriam ser presas.",
            "tipo": "odio",
            "explicacao": "Prega a perseguição por opinião diferente."
        },
        {
            "frase": "Não gosto de funk, mas respeito quem gosta.",
            "tipo": "liberdade",
            "explicacao": "Expressa preferência com respeito."
        },
        {
            "frase": "Quem ouve funk é favelado e não tem cultura.",
            "tipo": "odio",
            "explicacao": "Ofende e inferioriza pessoas por seu gosto musical."
        },
        {
            "frase": "Acredito que a escola deveria ter mais aulas de música.",
            "tipo": "liberdade",
            "explicacao": "É uma sugestão construtiva, sem ofender."
        },
        {
            "frase": "Pessoas com deficiência atrapalham o ambiente escolar.",
            "tipo": "odio",
            "explicacao": "Discrimina e inferioriza pessoas com deficiência."
        },
        {
            "frase": "Prefiro estudar em casa do que na escola.",
            "tipo": "liberdade",
            "explicacao": "É uma preferência pessoal."
        },
        {
            "frase": "Meninas não deveriam estudar matemática, é coisa de menino.",
            "tipo": "odio",
            "explicacao": "Discrimina por gênero e limita direitos."
        },
        {
            "frase": "Acho que devemos respeitar todas as religiões.",
            "tipo": "liberdade",
            "explicacao": "Promove respeito e diversidade."
        },
        {
            "frase": "Quem segue essa religião é ignorante e atrasado.",
            "tipo": "odio",
            "explicacao": "Ofende e discrimina por crença religiosa."
        },
    ]
    
    # ========== EMBARALHAR ==========
    if not st.session_state.debate_classificacoes:
        import random
        random.seed(st.session_state.nome)
        random.shuffle(frases)
        st.session_state.debate_classificacoes = frases
    
    frases_embaralhadas = st.session_state.debate_classificacoes
    
    # ========== VERIFICAR SE TERMINOU ==========
    if st.session_state.debate_tentativas >= 5:
        st.balloons()
        tocar_som("vitoria")
        
        st.success("🎉 PARABÉNS! Você completou o debate!")
        st.write(f"📊 Acertos: {st.session_state.debate_acertos} de 5")
        
        st.divider()
        
        st.subheader("💡 O que você aprendeu?")
        
        st.info("""
        **LIBERDADE DE EXPRESSÃO:**
        - ✅ Expressar opiniões pessoais
        - ✅ Discordar com respeito
        - ✅ Criticar ideias, não pessoas
        
        **DISCURSO DE ÓDIO:**
        - ❌ Ofender pessoas
        - ❌ Discriminar por raça, gênero, religião
        - ❌ Incitar violência
        """)
        
        st.divider()
        
        # ========== PONTOS ==========
        st.session_state.pontos += 5
        st.success("⭐ +5 pontos!")
        
        if st.session_state.nome and st.session_state.turma:
            salvar_aluno(
                st.session_state.nome,
                st.session_state.turma,
                pontos=st.session_state.pontos,
                fake_acertos=st.session_state.fake_acertos,
                cyber_acertos=st.session_state.cyber_acertos,
                etica_acertos=st.session_state.etica_acertos,
                total_perguntas=st.session_state.total
            )
        
        if st.button("🔄 Jogar Novamente", key="debate_reiniciar"):
            st.session_state.debate_indice = 0
            st.session_state.debate_acertos = 0
            st.session_state.debate_tentativas = 0
            st.session_state.debate_classificacoes = []
            st.rerun()
        st.stop()
    
    # ========== MOSTRAR FRASE ==========
    if st.session_state.debate_indice >= len(frases_embaralhadas):
        st.session_state.debate_indice = 0
    
    p = frases_embaralhadas[st.session_state.debate_indice]
    
    st.markdown(f"### Frase {st.session_state.debate_tentativas + 1} de 5")
    
    st.markdown(f"""
    <div style='background: #f8f9fa; padding: 20px; border-radius: 12px; border-left: 5px solid #1a3a5c; margin: 15px 0;'>
        <p style='font-size: 1.2rem; font-style: italic;'>"{p['frase']}"</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.write("**Essa frase é:**")
    
    opcao = st.radio(
        "📌 Escolha uma opção:",
        ["⚖️ Liberdade de Expressão", "❌ Discurso de Ódio"],
        key="debate_opcao"
    )
    
    justificativa = st.text_area(
        "📝 Justifique sua resposta:",
        height=100,
        placeholder="Ex: Essa frase ofende pessoas porque...",
        key="debate_justificativa"
    )
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("✅ Verificar", key="debate_verificar"):
            if not justificativa or len(justificativa) < 10:
                st.warning("⚠️ Escreva uma justificativa com pelo menos 10 caracteres!")
            else:
                st.session_state.debate_tentativas += 1
                st.session_state.total += 1
                
                # Verificar resposta
                resposta_correta = "⚖️ Liberdade de Expressão" if p['tipo'] == "liberdade" else "❌ Discurso de Ódio"
                
                if opcao == resposta_correta:
                    tocar_som("acerto")
                    st.success("✅ ACERTOU! +1 ponto")
                    st.session_state.pontos += 1
                    st.session_state.debate_acertos += 1
                else:
                    tocar_som("erro")
                    st.error(f"❌ ERROU! A resposta correta é: {resposta_correta}")
                
                st.info(f"💡 **Explicação:** {p['explicacao']}")
                
                # Salvar no banco
                if st.session_state.nome and st.session_state.turma:
                    from database import salvar_debate
                    salvar_debate(
                        st.session_state.nome,
                        st.session_state.turma,
                        p['frase'],
                        opcao,
                        justificativa
                    )
                
                st.session_state.debate_indice += 1
                st.rerun()
    
    with col2:
        if st.button("➡️ PRÓXIMO", key="debate_proximo"):
            st.session_state.debate_indice += 1
            st.rerun()
    
    st.divider()
    st.write(f"📊 Tentativas: {st.session_state.debate_tentativas}/5 | ✅ Acertos: {st.session_state.debate_acertos}")
    
    # ========== PROGRESSO ==========
    if st.session_state.debate_tentativas > 0:
        st.divider()
        st.subheader("🎯 Seu Progresso")
        
        col1, col2, col3, col4, col5 = st.columns(5)
        niveis = [(1, "🌟"), (2, "⭐"), (3, "🏅"), (4, "🎖️"), (5, "🏆")]
        
        acertos = st.session_state.debate_acertos
        for i, (nivel, emoji) in enumerate(niveis, 1):
            with col1 if i == 1 else col2 if i == 2 else col3 if i == 3 else col4 if i == 4 else col5:
                if acertos >= nivel:
                    st.markdown(f"""
                    <div style='text-align: center; padding: 10px; background: #28a745; border-radius: 10px; color: white;'>
                        <h2>{emoji}</h2>
                        <p>{nivel}✅</p>
                    </div>
                    """, unsafe_allow_html=True)
                else:
                    st.markdown(f"""
                    <div style='text-align: center; padding: 10px; background: #e9ecef; border-radius: 10px; color: gray;'>
                        <h2>⬜</h2>
                        <p>{nivel}</p>
                    </div>
                    """, unsafe_allow_html=True)
    
    st.divider()
    st.info("💡 **Cultura Digital:** Liberdade de Expressão ≠ Discurso de Ódio!")

# ========== CULTURA DO CANCELAMENTO ==========
elif menu == "🅴 Cultura do Cancelamento":
    st.title("🅴 Cultura do Cancelamento - Estudo de Caso")
    
    st.markdown("""
    <div class="card card-mission">
        <h4>🎯 O QUE É ISSO?</h4>
        <p>Você vai analisar casos de <strong>cancelamento</strong> e refletir sobre ética e empatia!</p>
        <p>Será que o cancelamento é sempre justo? 🤔</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.divider()
    
    # ========== TABS ==========
    tab1, tab2 = st.tabs(["📖 Analisar Casos", "📚 Minhas Opiniões"])
    
    # ========== TAB 1: ANALISAR ==========
    with tab1:
        st.subheader("📖 Escolha um Caso para Analisar")
        
        # ========== CASOS ==========
        casos = [
            {
                "titulo": "Caso 1: A Aluna que Errou",
                "descricao": "Uma aluna postou uma opinião polêmica sobre um assunto. Em 1 dia, 200 pessoas comentaram, 100 xingaram e 50 defenderam. A aluna apagou a conta e não voltou mais à escola.",
                "pergunta": "Você acha que o cancelamento foi justo?"
            },
            {
                "titulo": "Caso 2: O Comentário Infeliz",
                "descricao": "Um aluno fez uma piada infeliz sobre um colega. A piada viralizou. O aluno pediu desculpas, mas ninguém aceitou. Ele foi excluído do grupo da turma.",
                "pergunta": "O que deveria ter acontecido?"
            },
            {
                "titulo": "Caso 3: A Fake News",
                "descricao": "Uma aluna compartilhou uma fake news sem saber. Quando descobriu, apagou e pediu desculpas. Mesmo assim, foi cancelada por 50 pessoas.",
                "pergunta": "O cancelamento foi proporcional ao erro?"
            },
            {
                "titulo": "Caso 4: O Professor Cancelado",
                "descricao": "Um professor deu uma nota baixa para um aluno. O aluno postou um vídeo reclamando. O professor foi xingado por 500 pessoas e pediu demissão.",
                "pergunta": "O que você faria no lugar do aluno?"
            },
            {
                "titulo": "Caso 5: A Diferença de Opinião",
                "descricao": "Dois alunos discordaram sobre política. Um deles xingou o outro. O xingado revidou. Os dois foram cancelados pela turma.",
                "pergunta": "Como resolver conflitos sem cancelar?"
            },
        ]
        
        # ========== ESCOLHER CASO ==========
        caso_selecionado = st.selectbox(
            "📌 Escolha um caso:",
            [c['titulo'] for c in casos],
            key="caso_cancelamento"
        )
        
        caso = next(c for c in casos if c['titulo'] == caso_selecionado)
        
        st.divider()
        
        # ========== MOSTRAR CASO ==========
        st.markdown(f"""
        <div style='background: #fff3cd; padding: 20px; border-radius: 12px; border-left: 5px solid #ffc107;'>
            <h4>📖 {caso['titulo']}</h4>
            <p style='font-size: 1.1rem;'>{caso['descricao']}</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.divider()
        
        # ========== PERGUNTA ==========
        st.subheader("🤔 Reflita")
        st.write(f"**{caso['pergunta']}**")
        
        opiniao = st.text_area(
            "📝 Escreva sua opinião:",
            height=150,
            placeholder="Ex: Eu acho que o cancelamento foi injusto porque...",
            key="opiniao_cancelamento"
        )
        
        if st.button("✅ Enviar Opinião", key="enviar_cancelamento"):
            if opiniao and len(opiniao) > 20:
                from database import salvar_cancelamento
                salvar_cancelamento(
                    st.session_state.nome,
                    st.session_state.turma,
                    caso['titulo'],
                    opiniao
                )
                
                st.balloons()
                tocar_som("vitoria")
                st.success("✅ Opinião enviada!")
                
                st.session_state.pontos += 5
                st.success("⭐ +5 pontos!")
                
                if st.session_state.nome and st.session_state.turma:
                    salvar_aluno(
                        st.session_state.nome,
                        st.session_state.turma,
                        pontos=st.session_state.pontos,
                        fake_acertos=st.session_state.fake_acertos,
                        cyber_acertos=st.session_state.cyber_acertos,
                        etica_acertos=st.session_state.etica_acertos,
                        total_perguntas=st.session_state.total
                    )
            else:
                st.warning("⚠️ Escreva uma opinião com pelo menos 20 caracteres!")
    
    # ========== TAB 2: MINHAS OPINIÕES ==========
    with tab2:
        st.subheader("📚 Minhas Opiniões")
        
        from database import (
            listar_cancelamentos_aluno,
            excluir_cancelamento,
        )
        
        opinioes = listar_cancelamentos_aluno(
            st.session_state.nome,
            st.session_state.turma
        )
        
        if opinioes:
            st.write(f"**Total: {len(opinioes)} opiniões**")
            
            st.divider()
            
            # ========== LISTA DE OPINIÕES ==========
            for o in opinioes:
                col1, col2 = st.columns([5, 1])
                
                with col1:
                    with st.expander(f"📝 {o['caso_titulo']} - {o['data']}"):
                        st.write(f"**Minha opinião:**")
                        st.info(o['opiniao'])
                
                with col2:
                    st.write("")
                    st.write("")
                    if st.button("🗑️", key=f"del_canc_{o['id']}", help="Excluir esta opinião"):
                        excluir_cancelamento(o['id'])
                        st.success(f"✅ Opinião excluída!")
                        st.rerun()
            
            st.divider()
            
            # ========== EXCLUIR TODAS ==========
            st.subheader("🗑️ Excluir Opiniões")
            
            st.warning("⚠️ **ATENÇÃO:** Esta ação é irreversível!")
            
            confirmar = st.checkbox(
                f"⚠️ Confirmo que quero excluir TODAS as {len(opinioes)} opiniões",
                key="confirmar_excluir_canc"
            )
            
            if st.button("🗑️ EXCLUIR TODAS AS MINHAS OPINIÕES", key="excluir_todas_canc", disabled=not confirmar):
                for o in opinioes:
                    excluir_cancelamento(o['id'])
                st.success(f"✅ {len(opinioes)} opiniões excluídas!")
                st.rerun()
        else:
            st.info("📭 Nenhuma opinião registrada ainda.")
    
    st.divider()
    st.info("💡 **Cultura Digital:** Cancelar não é a solução. O diálogo e a empatia são!")

# ========== JÚRI SIMULADO DIGITAL ==========
elif menu == "🅸 Júri Simulado Digital":
    st.title("🅸 Júri Simulado Digital")
    
    st.markdown("""
    <div class="card card-mission">
        <h4>🎯 O QUE É ISSO?</h4>
        <p>Você vai participar de um <strong>júri simulado</strong> sobre um caso de cyberbullying ou fake news!</p>
        <p>Assuma um papel, escreva seus argumentos e ajude a decidir! ⚖️</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.divider()
    
    # ========== TABS ==========
    tab1, tab2 = st.tabs(["⚖️ Participar do Júri", "📚 Meus Argumentos"])
    
    # ========== TAB 1: PARTICIPAR ==========
    with tab1:
        st.subheader("📋 Escolha um Caso")
        
        # ========== CASOS ==========
        casos = [
            {
                "titulo": "Caso 1: Cyberbullying na Escola",
                "descricao": "Um aluno criou um grupo para zombar de um colega. O colega ficou triste e parou de vir à escola. Os pais do colega querem justiça.",
                "papeis": ["👨‍⚖️ Juiz", "👨‍💼 Advogado de Defesa", "👩‍💼 Advogada de Acusação", "👥 Jurado"]
            },
            {
                "titulo": "Caso 2: Fake News sobre a Merenda",
                "descricao": "Uma fake news diz que a merenda da escola está vencida. A notícia viralizou e muitos pais ficaram preocupados. A direção quer descobrir quem começou.",
                "papeis": ["👨‍⚖️ Juiz", "👨‍💼 Advogado de Defesa", "👩‍💼 Advogada de Acusação", "👥 Jurado"]
            },
            {
                "titulo": "Caso 3: Discurso de Ódio nas Redes",
                "descricao": "Um aluno postou comentários racistas sobre um colega. A escola quer punir o aluno, mas ele diz que foi só uma brincadeira.",
                "papeis": ["👨‍⚖️ Juiz", "👨‍💼 Advogado de Defesa", "👩‍💼 Advogada de Acusação", "👥 Jurado"]
            },
            {
                "titulo": "Caso 4: Deepfake de um Colega",
                "descricao": "Um aluno criou um vídeo deepfake de um colega dizendo algo que ele nunca disse. O vídeo viralizou e o colega ficou humilhado.",
                "papeis": ["👨‍⚖️ Juiz", "👨‍💼 Advogado de Defesa", "👩‍💼 Advogada de Acusação", "👥 Jurado"]
            },
        ]
        
        # ========== ESCOLHER CASO ==========
        caso_selecionado = st.selectbox(
            "📌 Escolha um caso:",
            [c['titulo'] for c in casos],
            key="caso_juri"
        )
        
        caso = next(c for c in casos if c['titulo'] == caso_selecionado)
        
        st.divider()
        
        # ========== MOSTRAR CASO ==========
        st.markdown(f"""
        <div style='background: #e7f3ff; padding: 20px; border-radius: 12px; border-left: 5px solid #0066cc;'>
            <h4>📖 {caso['titulo']}</h4>
            <p style='font-size: 1.1rem;'>{caso['descricao']}</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.divider()
        
        # ========== ESCOLHER PAPEL ==========
        st.subheader("🎭 Escolha seu Papel")
        
        papel = st.radio(
            "Qual papel você quer assumir?",
            caso['papeis'],
            key="papel_juri"
        )
        
        st.divider()
        
        # ========== INSTRUÇÕES POR PAPEL ==========
        st.subheader("📝 Sua Missão")
        
        if papel == "👨‍⚖️ Juiz":
            st.info("""
            **👨‍⚖️ JUIZ:** Você deve analisar os argumentos e decidir.
            
            **O que escrever:**
            - Qual a sua decisão?
            - Por que você decidiu isso?
            - Qual a pena/solução?
            """)
        elif papel == "👨‍💼 Advogado de Defesa":
            st.info("""
            **👨‍💼 ADVOGADO DE DEFESA:** Você defende o acusado.
            
            **O que escrever:**
            - Argumentos a favor do acusado
            - Atenuantes (o que diminui a culpa)
            - Justificativas
            """)
        elif papel == "👩‍💼 Advogada de Acusação":
            st.info("""
            **👩‍💼 ADVOGADA DE ACUSAÇÃO:** Você acusa o réu.
            
            **O que escrever:**
            - Argumentos contra o acusado
            - Agravantes (o que aumenta a culpa)
            - Provas
            """)
        else:
            st.info("""
            **👥 JURADO:** Você analisa os argumentos e vota.
            
            **O que escrever:**
            - Qual seu voto? (Culpado ou Inocente?)
            - Por que você votou assim?
            - Comentários sobre os argumentos
            """)
        
        # ========== ARGUMENTO ==========
        argumento = st.text_area(
            "📝 Escreva seu argumento:",
            height=200,
            placeholder="Escreva aqui sua análise, argumentos e conclusão...",
            key="argumento_juri"
        )
        
        if st.button("✅ Enviar Argumento", key="enviar_juri"):
            if argumento and len(argumento) > 50:
                from database import salvar_juri
                salvar_juri(
                    st.session_state.nome,
                    st.session_state.turma,
                    caso['titulo'],
                    papel,
                    argumento
                )
                
                st.balloons()
                tocar_som("vitoria")
                st.success("✅ Argumento enviado!")
                
                st.session_state.pontos += 5
                st.success("⭐ +5 pontos!")
                
                if st.session_state.nome and st.session_state.turma:
                    salvar_aluno(
                        st.session_state.nome,
                        st.session_state.turma,
                        pontos=st.session_state.pontos,
                        fake_acertos=st.session_state.fake_acertos,
                        cyber_acertos=st.session_state.cyber_acertos,
                        etica_acertos=st.session_state.etica_acertos,
                        total_perguntas=st.session_state.total
                    )
            else:
                st.warning("⚠️ Escreva um argumento com pelo menos 50 caracteres!")
    
    # ========== TAB 2: MEUS ARGUMENTOS ==========
    with tab2:
        st.subheader("📚 Meus Argumentos")
        
        from database import (
            listar_juri_aluno,
            excluir_juri,
        )
        
        argumentos = listar_juri_aluno(
            st.session_state.nome,
            st.session_state.turma
        )
        
        if argumentos:
            st.write(f"**Total: {len(argumentos)} argumentos**")
            
            st.divider()
            
            for a in argumentos:
                col1, col2 = st.columns([5, 1])
                
                with col1:
                    with st.expander(f"⚖️ {a['caso_titulo']} - {a['papel']} - {a['data']}"):
                        st.write(f"**Argumento:**")
                        st.info(a['argumento'])
                
                with col2:
                    st.write("")
                    st.write("")
                    if st.button("🗑️", key=f"del_juri_{a['id']}", help="Excluir"):
                        excluir_juri(a['id'])
                        st.success("✅ Argumento excluído!")
                        st.rerun()
        else:
            st.info("📭 Nenhum argumento registrado ainda.")
    
    st.divider()
    st.info("💡 **Cultura Digital:** Argumentar com respeito é fundamental para a cidadania!")

# ========== DADOS DA DESINFORMAÇÃO ==========
elif menu == "🅷 Dados da Desinformação":
    st.title("🅷 Dados da Desinformação")
    
    st.markdown("""
    <div class="card card-mission">
        <h4>🎯 O QUE É ISSO?</h4>
        <p>Você vai <strong>analisar dados reais</strong> sobre fake news e desinformação!</p>
        <p>Calcule, interprete e tire suas conclusões! 📊</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.divider()
    
    # ========== TABS ==========
    tab1, tab2 = st.tabs(["📊 Analisar Dados", "📚 Minhas Análises"])
    
    # ========== TAB 1: ANALISAR ==========
    with tab1:
        st.subheader("📊 Dados sobre Desinformação")
        
        # ========== DADOS ==========
        st.markdown("""
        ### 📈 Dados Reais sobre Fake News
        
        Estudos mostram que:
        - 📰 **70%** das pessoas já compartilharam fake news sem saber
        - ⚡ Fake news se espalham **6x mais rápido** que notícias verdadeiras
        - 👥 **80%** dos jovens não verificam a fonte antes de compartilhar
        - 📱 **50%** das fake news vêm de redes sociais
        """)
        
        st.divider()
        
        # ========== GRÁFICO ==========
        st.subheader("📊 Visualização dos Dados")
        
        import pandas as pd
        
        dados = pd.DataFrame({
            "Categoria": ["Já compartilharam fake news", "Não verificam a fonte", "Vêm de redes sociais", "Se espalham rápido"],
            "Porcentagem": [70, 80, 50, 100]
        })
        
        st.bar_chart(dados.set_index('Categoria'))
        
        st.divider()
        
        # ========== PERGUNTAS ==========
        st.subheader("🧮 Vamos Calcular!")
        
        st.write("**Cenário:** Em uma escola com **500 alunos**, 80% não verificam a fonte antes de compartilhar.")
        
        pergunta1 = st.number_input(
            "Quantos alunos NÃO verificam a fonte?",
            min_value=0,
            value=0,
            step=1,
            key="calc_dados1"
        )
        
        if st.button("✅ Verificar Cálculo 1", key="ver_calc1"):
            if pergunta1 == 400:
                st.success("✅ CORRETO! 500 × 80% = 400 alunos!")
            else:
                st.error("❌ Tente novamente! 500 × 80% = ?")
        
        st.divider()
        
        pergunta2 = st.number_input(
            "Quantos alunos VERIFICAM a fonte?",
            min_value=0,
            value=0,
            step=1,
            key="calc_dados2"
        )
        
        if st.button("✅ Verificar Cálculo 2", key="ver_calc2"):
            if pergunta2 == 100:
                st.success("✅ CORRETO! 500 - 400 = 100 alunos!")
            else:
                st.error("❌ Tente novamente! 500 - 400 = ?")
        
        st.divider()
        
        # ========== ANÁLISE ==========
        st.subheader("📝 Sua Análise")
        
        analise = st.text_area(
            "📝 O que você observa nesses dados?",
            height=100,
            placeholder="Ex: A maioria dos alunos não verifica a fonte...",
            key="analise_dados"
        )
        
        conclusao = st.text_area(
            "💡 Qual sua conclusão e proposta?",
            height=100,
            placeholder="Ex: Precisamos criar campanhas de conscientização...",
            key="conclusao_dados"
        )
        
        if st.button("✅ Enviar Análise", key="enviar_analise"):
            if analise and len(analise) > 20 and conclusao and len(conclusao) > 20:
                from database import salvar_analise_dados
                salvar_analise_dados(
                    st.session_state.nome,
                    st.session_state.turma,
                    analise,
                    conclusao
                )
                
                st.balloons()
                tocar_som("vitoria")
                st.success("✅ Análise enviada!")
                
                st.session_state.pontos += 5
                st.success("⭐ +5 pontos!")
                
                if st.session_state.nome and st.session_state.turma:
                    salvar_aluno(
                        st.session_state.nome,
                        st.session_state.turma,
                        pontos=st.session_state.pontos,
                        fake_acertos=st.session_state.fake_acertos,
                        cyber_acertos=st.session_state.cyber_acertos,
                        etica_acertos=st.session_state.etica_acertos,
                        total_perguntas=st.session_state.total
                    )
            else:
                st.warning("⚠️ Escreva uma análise e uma conclusão com pelo menos 20 caracteres!")
    
    # ========== TAB 2: MINHAS ANÁLISES ==========
    with tab2:
        st.subheader("📚 Minhas Análises")
        
        from database import listar_analises_aluno, excluir_analise
        
        analises = listar_analises_aluno(
            st.session_state.nome,
            st.session_state.turma
        )
        
        if analises:
            st.write(f"**Total: {len(analises)} análises**")
            
            st.divider()
            
            for a in analises:
                col1, col2 = st.columns([5, 1])
                
                with col1:
                    with st.expander(f"📊 Análise de {a['data']}"):
                        st.write(f"**Análise:**")
                        st.info(a['analise'])
                        st.write(f"**Conclusão:**")
                        st.success(a['conclusao'])
                
                with col2:
                    st.write("")
                    st.write("")
                    if st.button("🗑️", key=f"del_analise_{a['id']}", help="Excluir"):
                        excluir_analise(a['id'])
                        st.success("✅ Análise excluída!")
                        st.rerun()
        else:
            st.info("📭 Nenhuma análise registrada ainda.")
    
    st.divider()
    st.info("💡 **Pensamento Científico:** Analisar dados é fundamental para entender a desinformação!")

# ========== CAMPANHA DE CONSCIENTIZAÇÃO ==========
elif menu == "🅹 Campanha de Conscientização":
    st.title("🅹 Campanha de Conscientização")
    
    st.markdown("""
    <div class="card card-mission">
        <h4>🎯 O QUE É ISSO?</h4>
        <p>Você vai <strong>criar uma campanha</strong> de conscientização sobre cidadania digital!</p>
        <p>Use sua criatividade para ajudar a combater as fake news e o cyberbullying! 🎨</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.divider()
    
    # ========== TABS ==========
    tab1, tab2 = st.tabs(["🎨 Criar Campanha", "📚 Minhas Campanhas"])
    
    # ========== TAB 1: CRIAR ==========
    with tab1:
        st.subheader("🎨 Crie sua Campanha")
        
        with st.form("form_campanha"):
            st.markdown("### 📌 Passo 1: Informações Básicas")
            
            titulo = st.text_input(
                "📝 Título da Campanha:",
                placeholder="Ex: Diga NÃO às Fake News!"
            )
            
            tipo = st.selectbox(
                "📱 Tipo de Campanha:",
                [
                    "📱 Post para Redes Sociais",
                    "🎬 Vídeo",
                    "📰 Cartaz",
                    "😂 Meme",
                    "🎙️ Podcast",
                    "📊 Infográfico"
                ]
            )
            
            publico = st.selectbox(
                "🎯 Público-alvo:",
                [
                    "👥 Alunos do 6º Ano",
                    "👥 Alunos do 7º Ano",
                    "👥 Alunos do 8º Ano",
                    "👥 Alunos do 9º Ano",
                    "👨‍👩‍👧 Famílias",
                    "👨‍🏫 Professores",
                    "🌐 Toda a Escola"
                ]
            )
            
            st.divider()
            st.markdown("### 📝 Passo 2: Roteiro da Campanha")
            
            roteiro = st.text_area(
                "📝 Escreva o roteiro:",
                height=200,
                placeholder="Ex: 1. Comece com uma pergunta...",
                key="roteiro_campanha"
            )
            
            st.divider()
            st.markdown("### 📢 Passo 3: Divulgação")
            
            divulgacao = st.multiselect(
                "📢 Onde vai divulgar?",
                [
                    "📱 Instagram",
                    "🎵 TikTok",
                    "📘 Facebook",
                    "💬 WhatsApp",
                    "📰 Mural da Escola",
                    "📻 Rádio da Escola",
                    "📧 Email",
                    "🎤 Apresentação na Sala"
                ],
                key="divulgacao_campanha"
            )
            
            st.divider()
            
            submitted = st.form_submit_button("💾 Salvar Campanha")
            
            if submitted:
                if titulo and roteiro and len(roteiro) > 50 and divulgacao:
                    divulgacao_texto = ", ".join(divulgacao)
                    
                    from database import salvar_campanha
                    salvar_campanha(
                        st.session_state.nome,
                        st.session_state.turma,
                        titulo,
                        tipo,
                        publico,
                        roteiro,
                        divulgacao_texto
                    )
                    
                    st.balloons()
                    tocar_som("vitoria")
                    st.success("✅ Campanha criada!")
                    
                    st.session_state.pontos += 10
                    st.success("⭐ +10 pontos!")
                else:
                    st.warning("⚠️ Preencha TODOS os campos! O roteiro precisa ter pelo menos 50 caracteres.")
    
    # ========== TAB 2: MINHAS CAMPANHAS ==========
    with tab2:
        st.subheader("📚 Minhas Campanhas")
        
        from database import listar_campanhas_aluno, excluir_campanha
        
        campanhas = listar_campanhas_aluno(
            st.session_state.nome,
            st.session_state.turma
        )
        
        if campanhas:
            st.write(f"**Total: {len(campanhas)} campanhas**")
            st.divider()
            
            for c in campanhas:
                col1, col2 = st.columns([5, 1])
                
                with col1:
                    with st.expander(f"🎨 {c['titulo']} - {c['tipo']}"):
                        st.write(f"**📱 Tipo:** {c['tipo']}")
                        st.write(f"**🎯 Público:** {c['publico']}")
                        st.write(f"**📝 Roteiro:**")
                        st.info(c['roteiro'])
                        st.write(f"**📢 Divulgação:** {c['divulgacao']}")
                
                with col2:
                    st.write("")
                    st.write("")
                    if st.button("🗑️", key=f"del_campanha_{c['id']}"):
                        excluir_campanha(c['id'])
                        st.success("✅ Excluída!")
                        st.rerun()
        else:
            st.info("📭 Nenhuma campanha criada ainda.")
    
    st.divider()
    st.info("💡 **Cultura Maker:** Criar é a melhor forma de aprender!")

# ========== INFOGRÁFICO MAKER ==========
elif menu == "🅵 Infográfico Maker":
    st.title("🅵 Infográfico Maker")
    
    st.markdown("""
    <div class="card card-mission">
        <h4>🎯 O QUE É ISSO?</h4>
        <p>Você vai <strong>criar um infográfico</strong> sobre cidadania digital!</p>
        <p>Escolha o tema, os dados e as cores. Depois veja o resultado! 🎨</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.divider()
    
    # ========== TABS ==========
    tab1, tab2 = st.tabs(["🎨 Criar Infográfico", "📚 Meus Infográficos"])
    
    # ========== TAB 1: CRIAR ==========
    with tab1:
        st.subheader("🎨 Crie seu Infográfico")
        
        with st.form("form_infografico"):
            # ========== TÍTULO ==========
            titulo = st.text_input(
                "📝 Título do Infográfico:",
                placeholder="Ex: Fake News em Números"
            )
            
            # ========== TEMA ==========
            tema = st.selectbox(
                "🎯 Tema:",
                [
                    "📰 Fake News",
                    "🛡️ Cyberbullying",
                    "⚖️ Ética Digital",
                    "🔒 Privacidade",
                    "🧠 Efeito Bolha",
                    "🤖 Inteligência Artificial"
                ]
            )
            
            # ========== DADOS ==========
            st.markdown("### 📊 Dados do Infográfico")
            
            st.write("**Adicione até 4 dados:**")
            
            dado1 = st.text_input("📊 Dado 1:", placeholder="Ex: 70% dos jovens já compartilharam fake news")
            dado2 = st.text_input("📊 Dado 2:", placeholder="Ex: Fake news se espalham 6x mais rápido")
            dado3 = st.text_input("📊 Dado 3:", placeholder="Ex: 80% não verificam a fonte")
            dado4 = st.text_input("📊 Dado 4:", placeholder="Ex: 50% das fake news vêm de redes sociais")
            
            # ========== CORES ==========
            st.markdown("### 🎨 Cores")
            
            cor = st.selectbox(
                "🎨 Esquema de cores:",
                [
                    "🔵 Azul e Branco",
                    "🟢 Verde e Amarelo",
                    "🟣 Roxo e Rosa",
                    "🟠 Laranja e Vermelho",
                    "⚫ Preto e Branco"
                ]
            )
            
            # ========== ÍCONES ==========
            st.markdown("### 🎯 Ícones")
            
            icone = st.selectbox(
                "🎯 Ícone principal:",
                [
                    "📰",
                    "🛡️",
                    "⚖️",
                    "🔒",
                    "🧠",
                    "🤖",
                    "💡",
                    "🌟"
                ]
            )
            
            st.divider()
            
            # ========== BOTÃO ==========
            submitted = st.form_submit_button("💾 Salvar Infográfico")
            
            if submitted:
                if titulo and (dado1 or dado2 or dado3 or dado4):
                    # Montar dados em texto
                    dados_lista = [d for d in [dado1, dado2, dado3, dado4] if d]
                    dados_texto = " | ".join(dados_lista)
                    
                    from database import salvar_infografico
                    salvar_infografico(
                        st.session_state.nome,
                        st.session_state.turma,
                        titulo,
                        tema,
                        dados_texto,
                        cor,
                        icone
                    )
                    
                    st.balloons()
                    tocar_som("vitoria")
                    st.success("✅ Infográfico criado!")
                    
                    st.session_state.pontos += 10
                    st.success("⭐ +10 pontos!")
                    
                    if st.session_state.nome and st.session_state.turma:
                        salvar_aluno(
                            st.session_state.nome,
                            st.session_state.turma,
                            pontos=st.session_state.pontos,
                            fake_acertos=st.session_state.fake_acertos,
                            cyber_acertos=st.session_state.cyber_acertos,
                            etica_acertos=st.session_state.etica_acertos,
                            total_perguntas=st.session_state.total
                        )
                else:
                    st.warning("⚠️ Preencha o título e pelo menos 1 dado!")
        
        st.divider()
        
        # ========== PREVIEW ==========
        st.subheader("👁️ Preview do Infográfico")
        
        st.info("💡 O preview é uma simulação. O infográfico final é salvo com todos os dados!")
    
    # ========== TAB 2: MEUS INFOGRÁFICOS ==========
    with tab2:
        st.subheader("📚 Meus Infográficos")
        
        from database import listar_infograficos_aluno, excluir_infografico
        
        infograficos = listar_infograficos_aluno(
            st.session_state.nome,
            st.session_state.turma
        )
        
        if infograficos:
            st.write(f"**Total: {len(infograficos)} infográficos**")
            
            st.divider()
            
            for i in infograficos:
                col1, col2 = st.columns([5, 1])
                
                with col1:
                    with st.expander(f"🎨 {i['titulo']} - {i['tema']}"):
                        st.write(f"**📊 Dados:**")
                        st.info(i['dados'])
                        st.write(f"**🎨 Cores:** {i['cores']}")
                        st.write(f"**🎯 Ícone:** {i['icones']}")
                        st.write(f"**📅 Data:** {i['data']}")
                
                with col2:
                    st.write("")
                    st.write("")
                    if st.button("🗑️", key=f"del_infografico_{i['id']}", help="Excluir"):
                        excluir_infografico(i['id'])
                        st.success("✅ Infográfico excluído!")
                        st.rerun()
        else:
            st.info("📭 Nenhum infográfico criado ainda.")
    
    st.divider()
    st.info("💡 **Comunicação Visual:** Infográficos ajudam a transmitir informações de forma clara!")

# ========== PESQUISA E RELATÓRIOS ==========
elif menu == "📊 Pesquisa e Relatórios":
    st.title("📊 Pesquisa e Relatórios")
    
    st.markdown("""
    <div class="card card-ethic">
        <h4>🎯 O QUE É ISSO?</h4>
        <p>Aqui você pode <strong>analisar os dados</strong> de todas as turmas!</p>
        <p>Gere relatórios, gráficos e estatísticas! 📈</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.divider()
    
    # ========== TABS ==========
    tab1, tab2, tab3, tab4 = st.tabs([
        "📊 Por Turma",
        "🏫 Comparativo",
        "📋 Relatório Completo",
        "📥 Exportar"
    ])
    
    import pandas as pd
    
    # ========== TAB 1: POR TURMA ==========
    with tab1:
        st.subheader("📊 Dados por Turma")
        
        turmas = buscar_todas_turmas()
        
        if turmas:
            turma_selecionada = st.selectbox("🏫 Escolha a turma:", turmas, key="pesquisa_turma")
            
            alunos = buscar_alunos_por_turma(turma_selecionada)
            
            if alunos:
                # Métricas
                total_alunos = len(alunos)
                total_pontos = sum([a['pontos'] for a in alunos])
                media_pontos = total_pontos / total_alunos if total_alunos > 0 else 0
                
                total_fake = sum([a['fake_acertos'] for a in alunos])
                total_cyber = sum([a['cyber_acertos'] for a in alunos])
                total_etica = sum([a['etica_acertos'] for a in alunos])
                
                col1, col2, col3, col4 = st.columns(4)
                with col1:
                    st.metric("👥 Total de Alunos", total_alunos)
                with col2:
                    st.metric("⭐ Pontos Totais", total_pontos)
                with col3:
                    st.metric("📈 Média de Pontos", f"{media_pontos:.1f}")
                with col4:
                    st.metric("🏆 Melhor Aluno", alunos[0]['nome'] if alunos else "—")
                
                st.divider()
                
                # Gráfico de acertos
                st.subheader("📊 Acertos por Categoria")
                
                dados_grafico = pd.DataFrame({
                    'Categoria': ['📰 Fake News', '🛡️ Cyberbullying', '⚖️ Ética Digital'],
                    'Acertos': [total_fake, total_cyber, total_etica]
                })
                st.bar_chart(dados_grafico.set_index('Categoria'))
                
                st.divider()
                
                # Tabela de alunos
                st.subheader("📋 Lista de Alunos")
                
                df = pd.DataFrame([{
                    'Nome': a['nome'],
                    'Pontos': a['pontos'],
                    'Fake': a['fake_acertos'],
                    'Cyber': a['cyber_acertos'],
                    'Ética': a['etica_acertos'],
                    'Total': a['total_perguntas']
                } for a in alunos])
                
                st.dataframe(df, use_container_width=True)
            else:
                st.info("📭 Nenhum aluno nesta turma.")
        else:
            st.info("📭 Nenhuma turma cadastrada.")
    
    # ========== TAB 2: COMPARATIVO ==========
    with tab2:
        st.subheader("🏫 Comparativo entre Turmas")
        
        turmas = buscar_todas_turmas()
        
        if turmas:
            dados_comparativo = []
            
            for turma in turmas:
                alunos = buscar_alunos_por_turma(turma)
                
                if alunos:
                    total_alunos = len(alunos)
                    total_pontos = sum([a['pontos'] for a in alunos])
                    media_pontos = total_pontos / total_alunos if total_alunos > 0 else 0
                    
                    dados_comparativo.append({
                        'Turma': turma,
                        'Alunos': total_alunos,
                        'Pontos': total_pontos,
                        'Média': round(media_pontos, 1),
                        'Fake': sum([a['fake_acertos'] for a in alunos]),
                        'Cyber': sum([a['cyber_acertos'] for a in alunos]),
                        'Ética': sum([a['etica_acertos'] for a in alunos])
                    })
            
            if dados_comparativo:
                df_comp = pd.DataFrame(dados_comparativo)
                
                st.dataframe(df_comp, use_container_width=True)
                
                st.divider()
                
                # Gráficos
                st.subheader("📊 Gráfico Comparativo - Pontos")
                st.bar_chart(df_comp.set_index('Turma')['Pontos'])
                
                st.subheader("📊 Gráfico Comparativo - Média")
                st.bar_chart(df_comp.set_index('Turma')['Média'])
                
                st.subheader("📊 Gráfico Comparativo - Acertos")
                st.bar_chart(df_comp.set_index('Turma')[['Fake', 'Cyber', 'Ética']])
            else:
                st.info("📭 Nenhum dado disponível.")
        else:
            st.info("📭 Nenhuma turma cadastrada.")
    
    # ========== TAB 3: RELATÓRIO COMPLETO ==========
    with tab3:
        st.subheader("📋 Relatório Completo de Pesquisa")
        
        turmas = buscar_todas_turmas()
        
        if turmas:
            if st.button("📊 Gerar Relatório Completo", key="gerar_relatorio_pesquisa"):
                relatorio = f"""
==================================================
   📊 RELATÓRIO DE PESQUISA - CIDADANIA DIGITAL
==================================================
📅 Data: {datetime.now().strftime('%d/%m/%Y %H:%M')}
🏫 EEEF PROFª ODETE MENDES N OLIVEIRA
👨‍🏫 Professores: Irving V. Santos / Luiz Veloso
==================================================

"""
                
                for turma in turmas:
                    alunos = buscar_alunos_por_turma(turma)
                    
                    if alunos:
                        total_alunos = len(alunos)
                        total_pontos = sum([a['pontos'] for a in alunos])
                        media = total_pontos / total_alunos if total_alunos > 0 else 0
                        
                        relatorio += f"\n{'='*50}\n"
                        relatorio += f"🏫 TURMA: {turma}\n"
                        relatorio += f"{'='*50}\n"
                        relatorio += f"👥 Total de Alunos: {total_alunos}\n"
                        relatorio += f"⭐ Total de Pontos: {total_pontos}\n"
                        relatorio += f"📈 Média de Pontos: {media:.1f}\n"
                        relatorio += f"📰 Acertos Fake News: {sum([a['fake_acertos'] for a in alunos])}\n"
                        relatorio += f"🛡️ Acertos Cyber: {sum([a['cyber_acertos'] for a in alunos])}\n"
                        relatorio += f"⚖️ Acertos Ética: {sum([a['etica_acertos'] for a in alunos])}\n\n"
                        
                        relatorio += "📋 RANKING DA TURMA:\n"
                        for i, a in enumerate(alunos[:10], 1):
                            relatorio += f"   {i}º - {a['nome']}: {a['pontos']} pontos\n"
                        
                        relatorio += "\n"
                
                relatorio += f"\n{'='*50}\n"
                relatorio += "   FIM DO RELATÓRIO\n"
                relatorio += f"{'='*50}\n"
                
                st.code(relatorio, language="text")
                
                st.download_button(
                    label="📥 Baixar Relatório TXT",
                    data=relatorio,
                    file_name=f"relatorio_pesquisa_{datetime.now().strftime('%Y%m%d')}.txt",
                    mime="text/plain",
                    key="download_pesquisa"
                )
        else:
            st.info("📭 Nenhuma turma cadastrada.")
    
    # ========== TAB 4: EXPORTAR ==========
    with tab4:
        st.subheader("📥 Exportar Dados")
        
        st.write("**Escolha o formato:**")
        
        formato = st.radio(
            "Formato de exportação:",
            ["📄 TXT", "📊 CSV"],
            key="formato_export"
        )
        
        if st.button("📥 Gerar Arquivo", key="gerar_export"):
            turmas = buscar_todas_turmas()
            
            todos_dados = []
            for turma in turmas:
                alunos = buscar_alunos_por_turma(turma)
                for a in alunos:
                    todos_dados.append({
                        'Nome': a['nome'],
                        'Turma': a['turma'],
                        'Pontos': a['pontos'],
                        'Fake': a['fake_acertos'],
                        'Cyber': a['cyber_acertos'],
                        'Ética': a['etica_acertos'],
                        'Total': a['total_perguntas']
                    })
            
            if todos_dados:
                df_export = pd.DataFrame(todos_dados)
                
                if formato == "📊 CSV":
                    csv = df_export.to_csv(index=False)
                    st.download_button(
                        label="📥 Baixar CSV",
                        data=csv,
                        file_name=f"dados_alunos_{datetime.now().strftime('%Y%m%d')}.csv",
                        mime="text/csv",
                        key="download_csv"
                    )
                    st.dataframe(df_export, use_container_width=True)
                else:
                    txt = df_export.to_string(index=False)
                    st.download_button(
                        label="📥 Baixar TXT",
                        data=txt,
                        file_name=f"dados_alunos_{datetime.now().strftime('%Y%m%d')}.txt",
                        mime="text/plain",
                        key="download_txt"
                    )
                    st.code(txt, language="text")
            else:
                st.info("📭 Nenhum dado disponível.")
    
    st.divider()
    st.info("💡 **Análise de Dados:** Use os relatórios para entender o desempenho das turmas!")

# ========== QUESTIONÁRIO CIDADANIA DIGITAL ==========
elif menu == "📋 Questionário Cidadania Digital":
    st.title("📋 Questionário de Diagnóstico - Cidadania Digital")
    
    st.markdown("""
    <div class="card card-ethic">
        <h4>🎯 SOBRE O QUESTIONÁRIO</h4>
        <p>Olá! Este questionário faz parte do nosso projeto de <strong>Cidadania Digital</strong>.</p>
        <p>Suas respostas são muito importantes para entendermos como nossa escola utiliza a internet e as redes sociais.</p>
        <p>Responda com sinceridade para nos ajudar a construir um ambiente digital mais seguro, ético e saudável para todos! 💙</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.divider()
    
    # ========== TABS ==========
    tab1, tab2, tab3 = st.tabs(["📝 Responder", "📊 Resultados", "🖨️ Cartaz"])
    
    # ========== TAB 1: RESPONDER ==========
    with tab1:
        st.subheader("📝 Preencha o Questionário")
        
                # ========== IDENTIFICAÇÃO ==========
        st.markdown("### 👤 Identificação")
        
        # 🔥 SELECIONAR TURMA PRIMEIRO
        turma = st.selectbox(
            "Turma:",
            ["6º Ano - Anfitrião", "7º Ano - Visitante", "8º Ano - Visitante", "9º Ano - Visitante"],
            key="q_turma"
        )
        
        # 🔥 BUSCAR ALUNOS DA TURMA
        alunos_turma = buscar_alunos_por_turma(turma)
        
        if alunos_turma:
            nomes_alunos = [a['nome'] for a in alunos_turma]
            
            # 🔥 SELECIONAR ALUNO DA LISTA
            nome = st.selectbox(
                "Nome do Aluno(a):",
                nomes_alunos,
                key="q_nome"
            )
        else:
            st.warning("⚠️ Nenhum aluno cadastrado nesta turma!")
            st.info("💡 Cadastre alunos na página **👥 Lista de Alunos**")
            nome = None
        
        data = st.date_input("Data:", key="q_data")
        
        st.divider()
        
        # ========== BLOCO 2: FAKE NEWS ==========
        st.markdown("### 📰 Bloco 2: Fake News")
        st.caption("Cidadania digital também significa saber consumir e compartilhar informações de forma responsável.")
        
        fake = st.radio(
            "2. Você já acreditou ou compartilhou alguma informação na internet que, mais tarde, descobriu ser mentira (Fake News)?",
            [
                "Sim, já aconteceu comigo algumas vezes",
                "Sim, mas foi uma situação muito rara",
                "Não, nunca me aconteceu"
            ],
            key="q_fake"
        )
        
        atitude = st.radio(
            "3. Quando você recebe uma notícia, vídeo ou link curioso, qual é a sua atitude principal antes de repassar?",
            [
                "Compartilho imediatamente se o assunto for interessante",
                "Leio ou assisto com atenção para avaliar se parece verdade",
                "Pesquiso em outros sites confiáveis para checar se é real"
            ],
            key="q_atitude"
        )
        
        st.divider()
        
        # ========== BLOCO 3: CYBERBULLYING ==========
        st.markdown("### 🛡️ Bloco 3: Cyberbullying")
        st.caption("O cyberbullying acontece quando alguém usa a internet para humilhar, ameaçar, excluir ou expor outra pessoa.")
        
        presenciou = st.radio(
            "4. Você já presenciou alguma situação de Cyberbullying envolvendo colegas da escola?",
            [
                "Sim, já vi acontecer com amigos ou colegas",
                "Sim, infelizmente já aconteceu comigo",
                "Não, nunca presenciei nenhuma situação desse tipo"
            ],
            key="q_presenciou"
        )
        
        reacao = st.radio(
            "5. Se você notar que um colega está sendo atacado ou excluído, qual costuma ser a sua reação?",
            [
                "Prefiro não me envolver",
                "Converso em particular com o colega para demonstrar apoio",
                "Procuro ajuda de um adulto de confiança",
                "Acabo interagindo com a postagem (rindo, comentando ou compartilhando)"
            ],
            key="q_reacao"
        )
        
        st.divider()
        
        # ========== BLOCO 4: ÉTICA ==========
        st.markdown("### ⚖️ Bloco 4: Ética nas Redes Digitais")
        
        opiniao = st.radio(
            "6. Você concorda: 'As pessoas são mais agressivas na internet do que pessoalmente'?",
            [
                "Sim, porque acham que estão anônimas ou protegidas",
                "Não, o comportamento reflete como agem no dia a dia",
                "Não tenho certeza ou nunca parei para pensar"
            ],
            key="q_opiniao"
        )
        
        cidadania = st.radio(
            "7. Qual destas é a atitude mais importante para praticarmos a cidadania digital?",
            [
                "Pensar se o comentário pode magoar alguém antes de enviar",
                "Configurar redes sociais como privadas",
                "Não espalhar boatos ou informações duvidosas",
                "Todas as alternativas anteriores são igualmente importantes"
            ],
            key="q_cidadania"
        )
        
        st.divider()
        
                # ========== BOTÃO ENVIAR ==========
        if st.button("✅ Enviar Questionário", key="enviar_questionario"):
            if nome and turma and redes:
                # Juntar redes sociais
                redes_texto = ", ".join(redes)
                if outra_rede:
                    redes_texto += f" ({outra_rede})"
                
                # 🔥 CONVERTER TURMA PARA O FORMATO CURTO
                turma_curta = turma.replace(" - Anfitrião", "").replace(" - Visitante", "")
                
                # Salvar no banco
                from database import salvar_questionario
                salvar_questionario(
                    nome,
                    turma_curta,
                    str(data),
                    redes_texto,
                    fake,
                    atitude,
                    presenciou,
                    reacao,
                    opiniao,
                    cidadania
                )
                
                # 🔥 ATUALIZAR PONTOS DO ALUNO
                if st.session_state.get('nome') == nome:
                    st.session_state.pontos += 5
                    st.session_state.total += 1
                    
                    salvar_aluno(
                        nome,
                        turma,
                        pontos=st.session_state.pontos,
                        fake_acertos=st.session_state.fake_acertos,
                        cyber_acertos=st.session_state.cyber_acertos,
                        etica_acertos=st.session_state.etica_acertos,
                        total_perguntas=st.session_state.total
                    )
                
                st.balloons()
                tocar_som("vitoria")
                st.success(f"✅ Questionário de {nome} enviado com sucesso!")
                st.info("💡 Obrigado por participar! Suas respostas ajudarão a melhorar nossa escola!")
            else:
                st.warning("⚠️ Preencha todos os campos obrigatórios!")
    
    # ========== TAB 2: RESULTADOS ==========
    with tab2:
        st.subheader("📊 Resultados do Questionário")
        
        from database import listar_questionarios
        
        questionarios = listar_questionarios()
        
        if questionarios:
            st.write(f"**Total de respostas: {len(questionarios)}**")
            
            st.divider()
            
            # ========== FILTRO POR TURMA ==========
            turma_filtro = st.selectbox(
                "Filtrar por turma:",
                ["Todas", "6º Ano", "7º Ano", "8º Ano", "9º Ano"],
                key="filtro_resultado"
            )
            
            if turma_filtro != "Todas":
                questionarios = [q for q in questionarios if turma_filtro in q['aluno_turma']]
            
            if questionarios:
                st.write(f"**Mostrando: {len(questionarios)} respostas**")
                
                import pandas as pd
                
                # ========== GRÁFICO 1: REDES SOCIAIS ==========
                st.subheader("📱 Redes Sociais Mais Usadas")
                
                todas_redes = []
                for q in questionarios:
                    todas_redes.extend(q['redes_sociais'].split(", "))
                
                from collections import Counter
                contagem_redes = Counter(todas_redes)
                
                df_redes = pd.DataFrame([
                    {"Rede": k, "Quantidade": v}
                    for k, v in contagem_redes.items()
                ])
                st.bar_chart(df_redes.set_index('Rede'))
                
                st.divider()
                
                # ========== GRÁFICO 2: FAKE NEWS ==========
                st.subheader("📰 Já compartilhou Fake News?")
                
                contagem_fake = Counter([q['fake_news'] for q in questionarios])
                df_fake = pd.DataFrame([
                    {"Resposta": k, "Quantidade": v}
                    for k, v in contagem_fake.items()
                ])
                st.bar_chart(df_fake.set_index('Resposta'))
                
                st.divider()
                
                # ========== GRÁFICO 3: CYBERBULLYING ==========
                st.subheader("🛡️ Já presenciou Cyberbullying?")
                
                contagem_cyber = Counter([q['presenciou_cyber'] for q in questionarios])
                df_cyber = pd.DataFrame([
                    {"Resposta": k, "Quantidade": v}
                    for k, v in contagem_cyber.items()
                ])
                st.bar_chart(df_cyber.set_index('Resposta'))
                
                st.divider()
                
                # ========== TABELA DE RESPOSTAS ==========
                st.subheader("📋 Todas as Respostas")
                
                df = pd.DataFrame([{
                    'Aluno': q['aluno_nome'],
                    'Turma': q['aluno_turma'],
                    'Data': q['data'],
                    'Redes': q['redes_sociais'],
                    'Fake News': q['fake_news'],
                    'Cyber': q['presenciou_cyber'],
                    'Ética': q['atitude_cidadania']
                } for q in questionarios])
                
                st.dataframe(df, use_container_width=True)
            else:
                st.info("📭 Nenhuma resposta para esta turma.")
        else:
            st.info("📭 Nenhum questionário respondido ainda.")
    
    # ========== TAB 3: CARTAZ ==========
    with tab3:
        st.subheader("🖨️ Gerar Cartaz para a Escola")
        
        from database import listar_questionarios
        
        questionarios = listar_questionarios()
        
        if questionarios:
            total = len(questionarios)
            
            # ========== ESTATÍSTICAS ==========
            st.write(f"**Total de respostas: {total}**")
            
            from collections import Counter
            
            # Contagens
            contagem_fake = Counter([q['fake_news'] for q in questionarios])
            contagem_cyber = Counter([q['presenciou_cyber'] for q in questionarios])
            
            # Percentuais
            st.subheader("📊 Resumo dos Resultados")
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.metric("📋 Total de Respostas", total)
            with col2:
                st.metric("📰 Já compartilharam Fake News", f"{sum(contagem_fake.values())}")
            with col3:
                st.metric("🛡️ Já presenciaram Cyberbullying", f"{sum(contagem_cyber.values())}")
            
            st.divider()
            
            # ========== GERAR CARTAZ ==========
            if st.button("🖨️ Gerar Cartaz", key="gerar_cartaz"):
                cartaz = f"""
╔══════════════════════════════════════════════════════════════╗
║                                                              ║
║         📊 PESQUISA DE CIDADANIA DIGITAL - RESULTADOS         ║
║                                                              ║
║         🏫 EEEF PROFª ODETE MENDES N OLIVEIRA                 ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝

📅 Data: {datetime.now().strftime('%d/%m/%Y')}

📋 TOTAL DE RESPOSTAS: {total} alunos

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📰 FAKE NEWS:

"""
                for k, v in contagem_fake.items():
                    pct = (v / total) * 100
                    cartaz += f"   • {k}: {v} alunos ({pct:.1f}%)\n"
                
                cartaz += f"""
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🛡️ CYBERBULLYING:

"""
                for k, v in contagem_cyber.items():
                    pct = (v / total) * 100
                    cartaz += f"   • {k}: {v} alunos ({pct:.1f}%)\n"
                
                cartaz += f"""
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

💡 CONCLUSÃO:

   Com base nas respostas, podemos observar a importância
   de trabalharmos a cidadania digital em nossa escola.

   Juntos, podemos construir um ambiente digital mais
   seguro, ético e saudável para todos!

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

   🌐 PROJETO CIDADANIA DIGITAL
   👨‍🏫 Professores: Irving V. Santos / Luiz Veloso

╔══════════════════════════════════════════════════════════════╗
║                                                              ║
║         "Juntos por uma internet mais segura!" 🌐💙          ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
"""
                st.code(cartaz, language="text")
                
                st.download_button(
                    label="📥 Baixar Cartaz",
                    data=cartaz,
                    file_name=f"cartaz_cidadania_digital_{datetime.now().strftime('%Y%m%d')}.txt",
                    mime="text/plain",
                    key="download_cartaz"
                )
                
                st.success("✅ Cartaz gerado! Imprima e exponha na escola!")
        else:
            st.info("📭 Nenhum questionário respondido ainda.")
    
    st.divider()
    st.info("💡 **Projeto Cidadania Digital:** Juntos por uma internet mais segura!")

# ========== RODAPÉ ==========
st.divider()
st.write("🌐 EEEF PROFª ODETE MENDES N OLIVEIRA - 6º Ano - Professor Irving Vasconcelos dos Santos (CICI)")