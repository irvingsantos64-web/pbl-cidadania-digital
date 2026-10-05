# database.py
import sqlite3
import os
from datetime import datetime

DB_PATH = os.path.join(os.path.dirname(__file__), 'data', 'escola.db')

def get_connection():
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_connection()
    cursor = conn.cursor()
    
    # ========== TABELA ALUNOS ==========
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS alunos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            turma TEXT NOT NULL,
            pontos INTEGER DEFAULT 0,
            fake_acertos INTEGER DEFAULT 0,
            cyber_acertos INTEGER DEFAULT 0,
            etica_acertos INTEGER DEFAULT 0,
            total_perguntas INTEGER DEFAULT 0,
            badges TEXT DEFAULT '',
            data_cadastro DATE DEFAULT CURRENT_DATE
        )
    """)
    # ========== TABELA QUESTOES ==========
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS questoes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            turma TEXT NOT NULL,
            categoria TEXT NOT NULL,
            pergunta TEXT NOT NULL,
            resposta TEXT NOT NULL,
            opcao1 TEXT,
            opcao2 TEXT,
            opcao3 TEXT,
            explicacao TEXT
        )
    """)

       # Tabela de RESPOSTAS PBL
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS respostas_pbl (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            aluno_nome TEXT NOT NULL,
            aluno_turma TEXT NOT NULL,
            caso_titulo TEXT NOT NULL,
            resposta TEXT NOT NULL,
            data TEXT
        )
    """)
    
    # Tabela de ALGORITMOS ANTI-FAKE NEWS
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS algoritmos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            aluno_nome TEXT NOT NULL,
            aluno_turma TEXT NOT NULL,
            passos TEXT NOT NULL,
            data TEXT
        )
    """)

    # Tabela de DESSEÇÕES (Caixa-Preta)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS disseca_algoritmo (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            aluno_nome TEXT NOT NULL,
            aluno_turma TEXT NOT NULL,
            curtidas TEXT NOT NULL,
            conclusao TEXT NOT NULL,
            data TEXT
        )
    """)
    
    # 🔥 Tabela de DEBATES (Discurso de Ódio vs. Liberdade)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS debates (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            aluno_nome TEXT NOT NULL,
            aluno_turma TEXT NOT NULL,
            frase TEXT NOT NULL,
            classificacao TEXT NOT NULL,
            justificativa TEXT NOT NULL,
            data TEXT
        )
    """)

    # Tabela de CANCELAMENTO
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS cancelamento (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            aluno_nome TEXT NOT NULL,
            aluno_turma TEXT NOT NULL,
            caso_titulo TEXT NOT NULL,
            opiniao TEXT NOT NULL,
            data TEXT
        )
    """)
    
    # Tabela de EQUIPES
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS equipes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            turma TEXT NOT NULL,
            pontos INTEGER DEFAULT 0,
            data_criacao TEXT
        )
    """)
    
    # Tabela de ALUNOS_EQUIPES
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS alunos_equipes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            equipe_id INTEGER NOT NULL,
            aluno_nome TEXT NOT NULL,
            aluno_turma TEXT NOT NULL,
            FOREIGN KEY (equipe_id) REFERENCES equipes (id)
        )
    """)
    
    # Tabela de CASOS PBL
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS casos_pbl (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            titulo TEXT NOT NULL,
            descricao TEXT NOT NULL,
            tipo TEXT NOT NULL,
            dados TEXT NOT NULL,
            solucao_esperada TEXT NOT NULL,
            pontos INTEGER DEFAULT 5
        )
    """)

    # Tabela de JÚRI SIMULADO
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS juri_simulado (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            aluno_nome TEXT NOT NULL,
            aluno_turma TEXT NOT NULL,
            caso_titulo TEXT NOT NULL,
            papel TEXT NOT NULL,
            argumento TEXT NOT NULL,
            data TEXT
        )
    """)

    # Tabela de CAMPANHAS
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS campanhas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            aluno_nome TEXT NOT NULL,
            aluno_turma TEXT NOT NULL,
            titulo TEXT NOT NULL,
            tipo TEXT NOT NULL,
            publico TEXT NOT NULL,
            roteiro TEXT NOT NULL,
            divulgacao TEXT NOT NULL,
            data TEXT
        )
    """)
    
    conn.commit()
    conn.close()
    print("✅ Banco de dados criado com sucesso!")

# ============================================================
# 🏆 FUNÇÕES DE EQUIPES
# ============================================================

def criar_equipe_completa(nome, turma):
    """Cria uma nova equipe"""
    from datetime import datetime
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO equipes (nome, turma, pontos, data_criacao)
        VALUES (?, ?, 0, ?)
    """, (nome, turma, datetime.now().strftime("%Y-%m-%d %H:%M")))
    conn.commit()
    equipe_id = cursor.lastrowid
    conn.close()
    return equipe_id


def adicionar_aluno_equipe(equipe_id, aluno_nome, aluno_turma):
    """Adiciona um aluno a uma equipe"""
    conn = get_connection()
    cursor = conn.cursor()
    # Verificar se o aluno já está em alguma equipe
    cursor.execute("""
        SELECT id FROM alunos_equipes 
        WHERE aluno_nome = ? AND aluno_turma = ?
    """, (aluno_nome, aluno_turma))
    if cursor.fetchone() is None:
        cursor.execute("""
            INSERT INTO alunos_equipes (equipe_id, aluno_nome, aluno_turma)
            VALUES (?, ?, ?)
        """, (equipe_id, aluno_nome, aluno_turma))
        conn.commit()
    conn.close()


def listar_equipes_completas():
    """Lista todas as equipes com seus alunos"""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM equipes ORDER BY pontos DESC")
    equipes = [dict(row) for row in cursor.fetchall()]
    
    for equipe in equipes:
        cursor.execute("""
            SELECT aluno_nome FROM alunos_equipes 
            WHERE equipe_id = ?
        """, (equipe['id'],))
        equipe['alunos'] = [row['aluno_nome'] for row in cursor.fetchall()]
    
    conn.close()
    return equipes


def adicionar_pontos_equipe_completa(equipe_id, pontos):
    """Adiciona pontos a uma equipe"""
    from datetime import datetime
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE equipes SET pontos = pontos + ? WHERE id = ?
    """, (pontos, equipe_id))
    cursor.execute("""
        INSERT INTO pontos_equipes (equipe_id, pontos, data)
        VALUES (?, ?, ?)
    """, (equipe_id, pontos, datetime.now().strftime("%Y-%m-%d %H:%M")))
    conn.commit()
    conn.close()


def excluir_equipe_completa(equipe_id):
    """Exclui uma equipe e seus vínculos"""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM alunos_equipes WHERE equipe_id = ?", (equipe_id,))
    cursor.execute("DELETE FROM pontos_equipes WHERE equipe_id = ?", (equipe_id,))
    cursor.execute("DELETE FROM equipes WHERE id = ?", (equipe_id,))
    conn.commit()
    conn.close()


def buscar_equipe_do_aluno(aluno_nome, aluno_turma):
    """Busca a equipe de um aluno"""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT e.* FROM equipes e
        JOIN alunos_equipes ae ON ae.equipe_id = e.id
        WHERE ae.aluno_nome = ? AND ae.aluno_turma = ?
    """, (aluno_nome, aluno_turma))
    equipe = cursor.fetchone()
    conn.close()
    return dict(equipe) if equipe else None


def buscar_questoes_equipe(turma, categoria):
    """Busca questões aleatórias para a equipe"""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT * FROM questoes 
        WHERE turma = ? AND categoria = ?
        ORDER BY RANDOM()
        LIMIT 5
    """, (turma, categoria))
    questoes = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return questoes
    
    # ========== TABELA TURMAS ==========
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS turmas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT UNIQUE NOT NULL,
            descricao TEXT,
            ativa INTEGER DEFAULT 1
        )
    """)

    # 🔥 TABELA DE EQUIPES
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS equipes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            turma TEXT NOT NULL,
            pontos INTEGER DEFAULT 0,
            data_criacao DATE DEFAULT CURRENT_DATE
        )
    """)
    
    # ========== TABELA QUESTÕES ==========
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS questoes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            turma TEXT NOT NULL,
            categoria TEXT NOT NULL,
            pergunta TEXT NOT NULL,
            resposta TEXT,
            opcao1 TEXT,
            opcao2 TEXT,
            opcao3 TEXT,
            opcao4 TEXT,
            explicacao TEXT,
            FOREIGN KEY (turma) REFERENCES turmas(nome)
        )
    """)

    # 🔥 TABELA DE EQUIPES
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS equipes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            turma TEXT NOT NULL,
            pontos INTEGER DEFAULT 0,
            data_criacao DATE DEFAULT CURRENT_DATE
        )
    """)

    # 🔥 TABELA DE ATIVIDADES (CALENDÁRIO)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS atividades (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            titulo TEXT NOT NULL,
            descricao TEXT,
            data DATE NOT NULL,
            horario TEXT,
            turma TEXT,
            tipo TEXT,
            status TEXT DEFAULT 'Agendada',
            data_criacao DATE DEFAULT CURRENT_DATE
        )
    """)

    # 🔥 TABELA DE DESAFIOS SEMANAIS
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS desafios_semanais (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            semana INTEGER,
            ano INTEGER,
            titulo TEXT NOT NULL,
            descricao TEXT,
            categoria TEXT,
            pergunta TEXT,
            resposta TEXT,
            opcao1 TEXT,
            opcao2 TEXT,
            opcao3 TEXT,
            opcao4 TEXT,
            explicacao TEXT,
            pontos INTEGER DEFAULT 5,
            data_inicio DATE,
            data_fim DATE,
            status TEXT DEFAULT 'Ativo'
        )
    """)

    # 🔥 TABELA DE LIVROS
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS livros (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            titulo TEXT NOT NULL,
            autor TEXT,
            categoria TEXT,
            descricao TEXT,
            link TEXT,
            capa TEXT,
            recomendado INTEGER DEFAULT 1,
            data_cadastro DATE DEFAULT CURRENT_DATE
        )
    """)
    
    # 🔥 TABELA DE RESENHAS
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS resenhas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            livro_id INTEGER,
            aluno_nome TEXT,
            aluno_turma TEXT,
            resenha TEXT,
            avaliacao INTEGER,
            data_resenha DATE DEFAULT CURRENT_DATE,
            FOREIGN KEY (livro_id) REFERENCES livros(id)
        )
    """)
    
    # 🔥 INSERIR LIVROS PADRÃO
    cursor.execute("SELECT COUNT(*) FROM livros")
    if cursor.fetchone()[0] == 0:
        livros_padrao = [
            ("Cidadania Digital", "Vários Autores", "Cidadania", "Guia completo sobre cidadania digital para jovens.", None, None),
            ("Fake News e Pós-Verdade", "Vários Autores", "Fake News", "Como identificar e combater notícias falsas.", None, None),
            ("Cyberbullying: O que é e como combater", "Vários Autores", "Cyberbullying", "Guia prático para identificar e combater o cyberbullying.", None, None),
            ("Ética na Internet", "Vários Autores", "Ética", "Reflexões sobre ética e comportamento online.", None, None),
            ("Privacidade na Era Digital", "Vários Autores", "Privacidade", "Como proteger seus dados na internet.", None, None),
            ("O Dilema das Redes", "Documentário", "Redes Sociais", "Documentário sobre o impacto das redes sociais.", None, None),
            ("Você é o que você compartilha", "Vários Autores", "Comportamento", "Reflexões sobre o que compartilhamos online.", None, None),
            ("Cultura Digital e Educação", "Vários Autores", "Educação", "Como a cultura digital transforma a educação.", None, None),
        ]
        
        for livro in livros_padrao:
            cursor.execute("""
                INSERT INTO livros (titulo, autor, categoria, descricao, link, capa)
                VALUES (?, ?, ?, ?, ?, ?)
            """, livro)
    
    # ========== INSERIR TURMAS PADRÃO ==========
    turmas_padrao = [
        ("6º Ano - Anfitrião", "Turma criadora do projeto"),
        ("7º Ano - Visitante", "Turma convidada"),
        ("8º Ano - Visitante", "Turma convidada"),
        ("9º Ano - Visitante", "Turma convidada")
    ]
    
    for turma in turmas_padrao:
        cursor.execute("INSERT OR IGNORE INTO turmas (nome, descricao) VALUES (?, ?)", turma)
    
    conn.commit()
    conn.close()
    print("✅ Banco de dados criado com sucesso!")

def carregar_questoes():
    """Carrega todas as questões do banco"""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM questoes ORDER BY turma, categoria")
    resultado = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return resultado

def buscar_questoes_por_turma(turma):
    """Busca questões por turma"""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM questoes WHERE turma = ?", (turma,))
    resultado = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return resultado

def buscar_questoes_por_turma_e_categoria(turma, categoria):
    """Busca questões por turma e categoria"""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM questoes WHERE turma = ? AND categoria = ?", (turma, categoria))
    resultado = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return resultado

def inserir_questao(turma, categoria, pergunta, resposta, opcao1=None, opcao2=None, opcao3=None, opcao4=None, explicacao=None):
    """Insere uma nova questão no banco"""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO questoes (turma, categoria, pergunta, resposta, opcao1, opcao2, opcao3, opcao4, explicacao)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (turma, categoria, pergunta, resposta, opcao1, opcao2, opcao3, opcao4, explicacao))
    conn.commit()
    conn.close()

def excluir_questao(questao_id):
    """Exclui uma questão do banco"""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM questoes WHERE id = ?", (questao_id,))
    conn.commit()
    conn.close()

def listar_todas_questoes():
    """Lista todas as questões do banco"""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM questoes ORDER BY turma, categoria, id")
    resultado = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return resultado

def listar_questoes_por_turma(turma):
    """Lista questões por turma"""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM questoes WHERE turma = ? ORDER BY categoria, id", (turma,))
    resultado = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return resultado

def listar_questoes_por_categoria(categoria):
    """Lista questões por categoria"""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM questoes WHERE categoria = ? ORDER BY turma, id", (categoria,))
    resultado = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return resultado

def listar_questoes_por_turma_categoria(turma, categoria):
    """Lista questões por turma e categoria"""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM questoes WHERE turma = ? AND categoria = ? ORDER BY id", (turma, categoria))
    resultado = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return resultado

def calcular_impacto_fake(alcance, compartilhamentos, curtidas, revoltados):
    """Calcula o impacto de uma fake news"""
    # Fórmula de impacto
    impacto = (alcance * 1) + (compartilhamentos * 3) + (curtidas * 0.5) + (revoltados * 5)
    
    # Classificação
    if impacto >= 5000:
        classificacao = "🔴 IMPACTO CATASTRÓFICO"
        descricao = "Essa fake news pode causar danos graves à escola e às pessoas!"
    elif impacto >= 2000:
        classificacao = "🟠 IMPACTO ALTO"
        descricao = "Essa fake news está se espalhando rapidamente!"
    elif impacto >= 1000:
        classificacao = "🟡 IMPACTO MODERADO"
        descricao = "Essa fake news está ganhando força!"
    elif impacto >= 500:
        classificacao = "🟢 IMPACTO BAIXO"
        descricao = "Essa fake news ainda pode ser controlada!"
    else:
        classificacao = "⚪ IMPACTO MÍNIMO"
        descricao = "Essa fake news não está se espalhando muito."
    
    return {
        "impacto_total": impacto,
        "classificacao": classificacao,
        "descricao": descricao,
        "alcance": alcance,
        "compartilhamentos": compartilhamentos,
        "curtidas": curtidas,
        "revoltados": revoltados
    }

def salvar_aluno(nome, turma, pontos=0, fake_acertos=0, cyber_acertos=0, etica_acertos=0, total_perguntas=0, badges=""):
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute("SELECT id FROM alunos WHERE nome = ? AND turma = ?", (nome, turma))
    existe = cursor.fetchone()
    
    if existe:
        cursor.execute("""
            UPDATE alunos 
            SET pontos = ?, fake_acertos = ?, cyber_acertos = ?, 
                etica_acertos = ?, total_perguntas = ?, badges = ?
            WHERE nome = ? AND turma = ?
        """, (pontos, fake_acertos, cyber_acertos, etica_acertos, total_perguntas, badges, nome, turma))
    else:
        cursor.execute("""
            INSERT INTO alunos (nome, turma, pontos, fake_acertos, cyber_acertos, 
                               etica_acertos, total_perguntas, badges)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (nome, turma, 0, 0, 0, 0, 0, badges))
    
    conn.commit()
    conn.close()

def buscar_alunos_por_turma(turma):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT * FROM alunos 
        WHERE turma = ? 
        ORDER BY pontos DESC
    """, (turma,))
    resultado = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return resultado

def buscar_todas_turmas():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT nome FROM turmas WHERE ativa = 1 ORDER BY nome")
    resultado = [row[0] for row in cursor.fetchall()]
    conn.close()
    return resultado

def buscar_ranking_geral():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT * FROM alunos 
        ORDER BY pontos DESC 
        LIMIT 10
    """)
    resultado = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return resultado

def buscar_todos_alunos():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT * FROM alunos 
        ORDER BY turma, nome
    """)
    resultado = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return resultado

def excluir_aluno(aluno_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM alunos WHERE id = ?", (aluno_id,))
    conn.commit()
    conn.close()

def buscar_ranking_turmas():
    """Busca o ranking geral das turmas"""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT 
            turma,
            COUNT(*) as total_alunos,
            COALESCE(SUM(pontos), 0) as total_pontos,
            COALESCE(AVG(pontos), 0) as media_pontos,
            COALESCE(SUM(fake_acertos), 0) as total_fake,
            COALESCE(SUM(cyber_acertos), 0) as total_cyber,
            COALESCE(SUM(etica_acertos), 0) as total_etica
        FROM alunos
        GROUP BY turma
        ORDER BY total_pontos DESC
    """)
    resultado = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return resultado

def criar_equipe(nome, turma):
    """Cria uma nova equipe"""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO equipes (nome, turma, pontos)
        VALUES (?, ?, 0)
    """, (nome, turma))
    conn.commit()
    conn.close()

def listar_equipes(turma=None):
    """Lista todas as equipes"""
    conn = get_connection()
    cursor = conn.cursor()
    if turma:
        cursor.execute("SELECT * FROM equipes WHERE turma = ? ORDER BY pontos DESC", (turma,))
    else:
        cursor.execute("SELECT * FROM equipes ORDER BY pontos DESC")
    resultado = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return resultado

def adicionar_pontos_equipe(equipe_id, pontos):
    """Adiciona pontos a uma equipe"""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE equipes SET pontos = pontos + ? WHERE id = ?
    """, (pontos, equipe_id))
    conn.commit()
    conn.close()

def excluir_equipe(equipe_id):
    """Exclui uma equipe"""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM equipes WHERE id = ?", (equipe_id,))
    conn.commit()
    conn.close()

# ========== FUNÇÕES DE EQUIPES ==========

def criar_equipe(nome, turma):
    """Cria uma nova equipe"""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO equipes (nome, turma, pontos)
        VALUES (?, ?, 0)
    """, (nome, turma))
    conn.commit()
    conn.close()

def listar_equipes(turma=None):
    """Lista todas as equipes"""
    conn = get_connection()
    cursor = conn.cursor()
    if turma:
        cursor.execute("SELECT * FROM equipes WHERE turma = ? ORDER BY pontos DESC", (turma,))
    else:
        cursor.execute("SELECT * FROM equipes ORDER BY pontos DESC")
    resultado = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return resultado

def adicionar_pontos_equipe(equipe_id, pontos):
    """Adiciona pontos a uma equipe"""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE equipes SET pontos = pontos + ? WHERE id = ?
    """, (pontos, equipe_id))
    conn.commit()
    conn.close()

def excluir_equipe(equipe_id):
    """Exclui uma equipe"""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM equipes WHERE id = ?", (equipe_id,))
    conn.commit()
    conn.close()

def zerar_pontos_alunos(turma=None, novo_parametro=None):
    """Zera os pontos de todos os alunos (ou de uma turma específica)"""
    conn = get_connection()
    cursor = conn.cursor()
    
    if turma:
        cursor.execute("""
            UPDATE alunos 
            SET pontos = 0, fake_acertos = 0, cyber_acertos = 0, 
                etica_acertos = 0, total_perguntas = 0
            WHERE turma = ?
        """, (turma,))
    else:
        cursor.execute("""
            UPDATE alunos 
            SET pontos = 0, fake_acertos = 0, cyber_acertos = 0, 
                etica_acertos = 0, total_perguntas = 0
        """)

# ========== FUNÇÕES DO CALENDÁRIO ==========

def criar_atividade(titulo, descricao, data, horario, turma, tipo):
    """Cria uma nova atividade no calendário"""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO atividades (titulo, descricao, data, horario, turma, tipo)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (titulo, descricao, data, horario, turma, tipo))
    conn.commit()
    conn.close()

def listar_atividades():
    """Lista todas as atividades"""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM atividades ORDER BY data ASC")
    resultado = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return resultado

def listar_atividades_por_turma(turma):
    """Lista atividades de uma turma"""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM atividades WHERE turma = ? OR turma = 'Todas' ORDER BY data ASC", (turma,))
    resultado = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return resultado

def excluir_atividade(atividade_id):
    """Exclui uma atividade"""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM atividades WHERE id = ?", (atividade_id,))
    conn.commit()
    conn.close()

def buscar_dados_aluno(nome, turma):
    """Busca os dados de um aluno específico"""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM alunos WHERE nome = ? AND turma = ?", (nome, turma))
    resultado = cursor.fetchone()
    conn.close()
    return dict(resultado) if resultado else None
    
    conn.commit()
    conn.close()

import random

def buscar_questoes_embaralhadas(turma, categoria):
    """Busca questões por turma e categoria, embaralhadas"""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM questoes WHERE turma = ? AND categoria = ?", (turma, categoria))
    resultado = [dict(row) for row in cursor.fetchall()]
    conn.close()
    
    # Embaralhar as questões
    random.shuffle(resultado)
    
    return resultado

import datetime

def criar_desafio_semanal(titulo, descricao, categoria, pergunta, resposta, opcao1=None, opcao2=None, opcao3=None, opcao4=None, explicacao=None, pontos=5):
    """Cria um novo desafio semanal"""
    hoje = datetime.datetime.now()
    semana = hoje.isocalendar()[1]
    ano = hoje.year
    data_inicio = hoje.strftime("%Y-%m-%d")
    data_fim = (hoje + datetime.timedelta(days=7)).strftime("%Y-%m-%d")
    
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO desafios_semanais 
        (semana, ano, titulo, descricao, categoria, pergunta, resposta, opcao1, opcao2, opcao3, opcao4, explicacao, pontos, data_inicio, data_fim)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (semana, ano, titulo, descricao, categoria, pergunta, resposta, opcao1, opcao2, opcao3, opcao4, explicacao, pontos, data_inicio, data_fim))
    conn.commit()
    conn.close()

def buscar_desafio_atual():
    """Busca o desafio da semana atual"""
    hoje = datetime.datetime.now()
    semana = hoje.isocalendar()[1]
    ano = hoje.year
    
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT * FROM desafios_semanais 
        WHERE semana = ? AND ano = ? AND status = 'Ativo'
        ORDER BY id DESC LIMIT 1
    """, (semana, ano))
    resultado = cursor.fetchone()
    conn.close()
    return dict(resultado) if resultado else None

def listar_desafios():
    """Lista todos os desafios"""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM desafios_semanais ORDER BY ano DESC, semana DESC")
    resultado = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return resultado

def excluir_desafio(desafio_id):
    """Exclui um desafio"""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM desafios_semanais WHERE id = ?", (desafio_id,))
    conn.commit()
    conn.close()

# ========== FUNÇÕES DA BIBLIOTECA ==========

def listar_livros():
    """Lista todos os livros"""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM livros ORDER BY titulo ASC")
    resultado = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return resultado

def listar_livros_por_categoria(categoria):
    """Lista livros por categoria"""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM livros WHERE categoria = ? ORDER BY titulo ASC", (categoria,))
    resultado = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return resultado

def buscar_livro(termo):
    """Busca livros por título ou autor"""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT * FROM livros 
        WHERE titulo LIKE ? OR autor LIKE ?
        ORDER BY titulo ASC
    """, (f"%{termo}%", f"%{termo}%"))
    resultado = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return resultado

def criar_livro(titulo, autor, categoria, descricao, link=None, capa=None):
    """Cria um novo livro"""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO livros (titulo, autor, categoria, descricao, link, capa)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (titulo, autor, categoria, descricao, link, capa))
    conn.commit()
    conn.close()

def excluir_livro(livro_id):
    """Exclui um livro"""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM livros WHERE id = ?", (livro_id,))
    conn.commit()
    conn.close()

def criar_resenha(livro_id, aluno_nome, aluno_turma, resenha, avaliacao):
    """Cria uma resenha"""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO resenhas (livro_id, aluno_nome, aluno_turma, resenha, avaliacao)
        VALUES (?, ?, ?, ?, ?)
    """, (livro_id, aluno_nome, aluno_turma, resenha, avaliacao))
    conn.commit()
    conn.close()

def listar_resenhas(livro_id):
    """Lista resenhas de um livro"""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM resenhas WHERE livro_id = ? ORDER BY data_resenha DESC", (livro_id,))
    resultado = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return resultado

# ============================================================
# 🏃 PERGUNTAS DE EDUCAÇÃO FÍSICA
# ============================================================

def inserir_perguntas_educacao_fisica():
    """Insere todas as perguntas de Educação Física no banco"""
    
    # 📰 FAKE NEWS
    perguntas_ef_fake = [
        # 6º Ano
        {"turma": "6º Ano - Anfitrião", "categoria": "fake",
         "pergunta": "É verdade que jogar videogame por 10 horas seguidas faz bem à saúde?",
         "resposta": "Fake",
         "explicacao": "O excesso de tela faz mal à saúde! Faça pausas e pratique exercícios."},
        {"turma": "6º Ano - Anfitrião", "categoria": "fake",
         "pergunta": "É verdade que praticar esportes ajuda no crescimento e na saúde?",
         "resposta": "Verdade",
         "explicacao": "Sim! Esportes fortalecem ossos, músculos e melhoram a saúde."},
        {"turma": "6º Ano - Anfitrião", "categoria": "fake",
         "pergunta": "É verdade que comer doces antes do treino dá mais energia?",
         "resposta": "Fake",
         "explicacao": "Doces dão energia rápida, mas não sustentam o treino."},
        {"turma": "6º Ano - Anfitrião", "categoria": "fake",
         "pergunta": "É verdade que beber água durante o exercício faz mal?",
         "resposta": "Fake",
         "explicacao": "Beber água é fundamental! A hidratação evita cãibras."},
        {"turma": "6º Ano - Anfitrião", "categoria": "fake",
         "pergunta": "É verdade que alongar antes do exercício evita lesões?",
         "resposta": "Verdade",
         "explicacao": "Sim! O alongamento prepara o corpo e evita lesões."},
        
        # 7º Ano
        {"turma": "7º Ano - Visitante", "categoria": "fake",
         "pergunta": "É verdade que suar muito significa que o treino foi melhor?",
         "resposta": "Fake",
         "explicacao": "Suar é normal, mas não significa que o treino foi melhor."},
        {"turma": "7º Ano - Visitante", "categoria": "fake",
         "pergunta": "É verdade que fazer exercício melhora a memória e o aprendizado?",
         "resposta": "Verdade",
         "explicacao": "Sim! Exercícios aumentam a oxigenação do cérebro."},
        {"turma": "7º Ano - Visitante", "categoria": "fake",
         "pergunta": "É verdade que só atletas profissionais precisam se aquecer?",
         "resposta": "Fake",
         "explicacao": "Todos precisam se aquecer antes de qualquer atividade física!"},
        {"turma": "7º Ano - Visitante", "categoria": "fake",
         "pergunta": "É verdade que dormir bem ajuda no desempenho esportivo?",
         "resposta": "Verdade",
         "explicacao": "Sim! O sono é fundamental para a recuperação muscular."},
        {"turma": "7º Ano - Visitante", "categoria": "fake",
         "pergunta": "É verdade que pular o café da manhã melhora o rendimento?",
         "resposta": "Fake",
         "explicacao": "O café da manhã é essencial para ter energia durante o dia."},
        
        # 8º Ano
        {"turma": "8º Ano - Visitante", "categoria": "fake",
         "pergunta": "É verdade que musculação atrapalha o crescimento em adolescentes?",
         "resposta": "Fake",
         "explicacao": "Com orientação, musculação é segura e ajuda no crescimento saudável."},
        {"turma": "8º Ano - Visitante", "categoria": "fake",
         "pergunta": "É verdade que o aquecimento deve ser feito antes de qualquer exercício?",
         "resposta": "Verdade",
         "explicacao": "Sim! O aquecimento prepara o corpo e evita lesões."},
        {"turma": "8º Ano - Visitante", "categoria": "fake",
         "pergunta": "É verdade que suplementos alimentares substituem refeições?",
         "resposta": "Fake",
         "explicacao": "Suplementos complementam, mas não substituem uma alimentação equilibrada."},
        {"turma": "8º Ano - Visitante", "categoria": "fake",
         "pergunta": "É verdade que beber refrigerante durante o treino hidrata?",
         "resposta": "Fake",
         "explicacao": "Refrigerantes não hidratam bem. O ideal é água ou isotônicos."},
        {"turma": "8º Ano - Visitante", "categoria": "fake",
         "pergunta": "É verdade que praticar esportes melhora a autoestima?",
         "resposta": "Verdade",
         "explicacao": "Sim! Esportes liberam endorfina, o hormônio da felicidade."},
        
        # 9º Ano
        {"turma": "9º Ano - Visitante", "categoria": "fake",
         "pergunta": "É verdade que anabolizantes são seguros para adolescentes?",
         "resposta": "Fake",
         "explicacao": "Anabolizantes são perigosos e proibidos para adolescentes!"},
        {"turma": "9º Ano - Visitante", "categoria": "fake",
         "pergunta": "É verdade que o exercício físico ajuda no combate à ansiedade?",
         "resposta": "Verdade",
         "explicacao": "Sim! Exercícios liberam endorfina e reduzem a ansiedade."},
        {"turma": "9º Ano - Visitante", "categoria": "fake",
         "pergunta": "É verdade que atletas de e-sports não precisam se exercitar?",
         "resposta": "Fake",
         "explicacao": "Atletas de e-sports também precisam de preparo físico e pausas!"},
        {"turma": "9º Ano - Visitante", "categoria": "fake",
         "pergunta": "É verdade que a atividade física melhora o sono?",
         "resposta": "Verdade",
         "explicacao": "Sim! Quem se exercita dorme melhor."},
        {"turma": "9º Ano - Visitante", "categoria": "fake",
         "pergunta": "É verdade que só quem é magro é saudável?",
         "resposta": "Fake",
         "explicacao": "Saúde não se mede pelo corpo! Cada pessoa tem seu biotipo."},
    ]
    
    # 🛡️ CYBERBULLYING
    perguntas_ef_cyber = [
        # 6º Ano
        {"turma": "6º Ano - Anfitrião", "categoria": "cyber",
         "pergunta": "É correto zombar de um colega nas redes sociais porque ele é menos atlético?",
         "resposta": "Não",
         "explicacao": "Respeitar as diferenças é fundamental! Cyberbullying é crime."},
        {"turma": "6º Ano - Anfitrião", "categoria": "cyber",
         "pergunta": "É correto postar foto de um colega caindo durante o jogo para humilhar?",
         "resposta": "Não",
         "explicacao": "Humilhar é bullying! Respeite sempre."},
        {"turma": "6º Ano - Anfitrião", "categoria": "cyber",
         "pergunta": "É correto excluir um colega do grupo porque ele joga mal?",
         "resposta": "Não",
         "explicacao": "Excluir é uma forma de bullying. Inclua sempre!"},
        {"turma": "6º Ano - Anfitrião", "categoria": "cyber",
         "pergunta": "É correto criar apelidos ofensivos para colegas no esporte?",
         "resposta": "Não",
         "explicacao": "Apelidos ofensivos magoam. Use sempre o nome da pessoa."},
        {"turma": "6º Ano - Anfitrião", "categoria": "cyber",
         "pergunta": "É correto incentivar os colegas durante o jogo?",
         "resposta": "Sim",
         "explicacao": "Incentivar é atitude de um bom cidadão digital!"},
        
        # 7º Ano
        {"turma": "7º Ano - Visitante", "categoria": "cyber",
         "pergunta": "É correto gravar vídeos de colegas sem permissão durante o treino?",
         "resposta": "Não",
         "explicacao": "Gravar sem permissão é invasão de privacidade!"},
        {"turma": "7º Ano - Visitante", "categoria": "cyber",
         "pergunta": "É correto comentar negativamente sobre o corpo de um colega nas redes?",
         "resposta": "Não",
         "explicacao": "Comentários negativos causam danos psicológicos."},
        {"turma": "7º Ano - Visitante", "categoria": "cyber",
         "pergunta": "É correto defender um colega que está sendo zombado online?",
         "resposta": "Sim",
         "explicacao": "Defender é atitude de coragem e cidadania!"},
        {"turma": "7º Ano - Visitante", "categoria": "cyber",
         "pergunta": "É correto espalhar que um colega usa anabolizantes sem provas?",
         "resposta": "Não",
         "explicacao": "Espalhar mentiras é fake news e bullying!"},
        {"turma": "7º Ano - Visitante", "categoria": "cyber",
         "pergunta": "É correto compartilhar meme ofensivo sobre um atleta?",
         "resposta": "Não",
         "explicacao": "Memes ofensivos também são cyberbullying!"},
        
        # 8º Ano
        {"turma": "8º Ano - Visitante", "categoria": "cyber",
         "pergunta": "É correto postar vídeo de um colega errando o gol para ridicularizar?",
         "resposta": "Não",
         "explicacao": "Ridicularizar é bullying! Respeite sempre."},
        {"turma": "8º Ano - Visitante", "categoria": "cyber",
         "pergunta": "É correto fazer comentários racistas sobre atletas nas redes?",
         "resposta": "Não",
         "explicacao": "Racismo é crime! Respeite a diversidade."},
        {"turma": "8º Ano - Visitante", "categoria": "cyber",
         "pergunta": "É correto apoiar um colega que sofreu bullying no esporte?",
         "resposta": "Sim",
         "explicacao": "Apoiar é atitude de cidadão digital!"},
        {"turma": "8º Ano - Visitante", "categoria": "cyber",
         "pergunta": "É correto criar perfil falso para zoar colegas?",
         "resposta": "Não",
         "explicacao": "Perfil falso é crime e cyberbullying!"},
        {"turma": "8º Ano - Visitante", "categoria": "cyber",
         "pergunta": "É correto divulgar o endereço de um colega nas redes?",
         "resposta": "Não",
         "explicacao": "Divulgar dados é perigoso e criminoso!"},
        
        # 9º Ano
        {"turma": "9º Ano - Visitante", "categoria": "cyber",
         "pergunta": "É correto fazer piadas sobre a orientação sexual de atletas?",
         "resposta": "Não",
         "explicacao": "Respeite a diversidade! Piadas ofensivas são bullying."},
        {"turma": "9º Ano - Visitante", "categoria": "cyber",
         "pergunta": "É correto ameaçar um colega por causa de um jogo online?",
         "resposta": "Não",
         "explicacao": "Ameaças são crime! Denuncie."},
        {"turma": "9º Ano - Visitante", "categoria": "cyber",
         "pergunta": "É correto denunciar conteúdo ofensivo nas redes sociais?",
         "resposta": "Sim",
         "explicacao": "Denunciar é atitude de cidadão digital!"},
        {"turma": "9º Ano - Visitante", "categoria": "cyber",
         "pergunta": "É correto xingar um colega no chat durante o jogo?",
         "resposta": "Não",
         "explicacao": "Xingar é falta de respeito! Jogue com educação."},
        {"turma": "9º Ano - Visitante", "categoria": "cyber",
         "pergunta": "É correto apoiar campanhas contra o bullying no esporte?",
         "resposta": "Sim",
         "explicacao": "Apoiar é atitude de cidadão consciente!"},
    ]
    
    # ⚖️ ÉTICA DIGITAL
    perguntas_ef_etica = [
        # 6º Ano
        {"turma": "6º Ano - Anfitrião", "categoria": "etica",
         "pergunta": "Um colega postou foto praticando esporte. O que fazer?",
         "opcao1": "Zombar da foto",
         "opcao2": "Elogiar e incentivar",
         "opcao3": "Compartilhar sem permissão",
         "correta": "Elogiar e incentivar",
         "explicacao": "Incentivar é atitude de cidadão digital!"},
        {"turma": "6º Ano - Anfitrião", "categoria": "etica",
         "pergunta": "Você viu um colega sendo excluído do jogo online. O que fazer?",
         "opcao1": "Ignorar",
         "opcao2": "Convidar o colega para jogar",
         "opcao3": "Zombar também",
         "correta": "Convidar o colega para jogar",
         "explicacao": "Incluir é atitude ética!"},
        {"turma": "6º Ano - Anfitrião", "categoria": "etica",
         "pergunta": "Você perdeu o jogo. O que fazer?",
         "opcao1": "Xingar os colegas",
         "opcao2": "Parabenizar o time adversário",
         "opcao3": "Sair do grupo",
         "correta": "Parabenizar o time adversário",
         "explicacao": "Fair play é fundamental no esporte!"},
        
        # 7º Ano
        {"turma": "7º Ano - Visitante", "categoria": "etica",
         "pergunta": "Você viu fake news sobre um atleta. O que fazer?",
         "opcao1": "Compartilhar",
         "opcao2": "Verificar antes de compartilhar",
         "opcao3": "Ignorar",
         "correta": "Verificar antes de compartilhar",
         "explicacao": "Verificar é atitude de cidadão digital!"},
        {"turma": "7º Ano - Visitante", "categoria": "etica",
         "pergunta": "Um colega está sendo criticado por seu corpo. O que fazer?",
         "opcao1": "Concordar",
         "opcao2": "Defender o colega",
         "opcao3": "Rir",
         "correta": "Defender o colega",
         "explicacao": "Defender é atitude ética!"},
        {"turma": "7º Ano - Visitante", "categoria": "etica",
         "pergunta": "Você quer postar foto do treino. O que fazer?",
         "opcao1": "Postar sem pedir permissão",
         "opcao2": "Pedir permissão aos colegas",
         "opcao3": "Marcar todos sem avisar",
         "correta": "Pedir permissão aos colegas",
         "explicacao": "Respeitar a privacidade é fundamental!"},
        
        # 8º Ano
        {"turma": "8º Ano - Visitante", "categoria": "etica",
         "pergunta": "Você viu um meme ofensivo sobre um atleta. O que fazer?",
         "opcao1": "Compartilhar",
         "opcao2": "Denunciar",
         "opcao3": "Rir",
         "correta": "Denunciar",
         "explicacao": "Denunciar é atitude de cidadão digital!"},
        {"turma": "8º Ano - Visitante", "categoria": "etica",
         "pergunta": "Um colega quer usar anabolizantes. O que fazer?",
         "opcao1": "Incentivar",
         "opcao2": "Alertar sobre os perigos",
         "opcao3": "Ignorar",
         "correta": "Alertar sobre os perigos",
         "explicacao": "Cuidar da saúde é prioridade!"},
        {"turma": "8º Ano - Visitante", "categoria": "etica",
         "pergunta": "Você ganhou um jogo com ajuda de trapaça. O que fazer?",
         "opcao1": "Comemorar",
         "opcao2": "Assumir a trapaça",
         "opcao3": "Esconder",
         "correta": "Assumir a trapaça",
         "explicacao": "Honestidade é fundamental no esporte!"},
        
        # 9º Ano
        {"turma": "9º Ano - Visitante", "categoria": "etica",
         "pergunta": "Você viu um atleta sendo vítima de racismo online. O que fazer?",
         "opcao1": "Ignorar",
         "opcao2": "Denunciar e apoiar",
         "opcao3": "Compartilhar para expor",
         "correta": "Denunciar e apoiar",
         "explicacao": "Denunciar racismo é obrigação de todo cidadão!"},
        {"turma": "9º Ano - Visitante", "categoria": "etica",
         "pergunta": "Você descobriu que um colega usa doping. O que fazer?",
         "opcao1": "Contar para todos",
         "opcao2": "Conversar com um adulto de confiança",
         "opcao3": "Ignorar",
         "correta": "Conversar com um adulto de confiança",
         "explicacao": "Doping é perigoso! Procure ajuda de um adulto."},
        {"turma": "9º Ano - Visitante", "categoria": "etica",
         "pergunta": "Você está perdendo um jogo online. O que fazer?",
         "opcao1": "Xingar os colegas",
         "opcao2": "Manter o respeito e continuar",
         "opcao3": "Sair do jogo",
         "correta": "Manter o respeito e continuar",
         "explicacao": "Respeito é fundamental, mesmo perdendo!"},
    ]
    
    # 🔥 Juntar todas
    todas_perguntas = perguntas_ef_fake + perguntas_ef_cyber + perguntas_ef_etica
    
    # 🔥 Inserir no banco
    conn = get_connection()
    cursor = conn.cursor()
    
    inseridas = 0
    for p in todas_perguntas:
        # Verificar se já existe (evitar duplicatas)
        cursor.execute("""
            SELECT id FROM questoes 
            WHERE pergunta = ? AND turma = ? AND categoria = ?
        """, (p['pergunta'], p['turma'], p['categoria']))
        
        if cursor.fetchone() is None:
            cursor.execute("""
                INSERT INTO questoes 
                (turma, categoria, pergunta, resposta, opcao1, opcao2, opcao3, explicacao)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                p['turma'],
                p['categoria'],
                p['pergunta'],
                p.get('resposta', p.get('correta', '')),
                p.get('opcao1'),
                p.get('opcao2'),
                p.get('opcao3'),
                p.get('explicacao', '')
            ))
            inseridas += 1
    
    conn.commit()
    conn.close()
    
    print(f"✅ {inseridas} perguntas de Educação Física inseridas!")
    return inseridas

def inserir_perguntas_interdisciplinares():
    """Insere perguntas de Matemática, Ed. Física e Desafios"""
    
    todas_perguntas = (
        perguntas_mat_fake_6ano + perguntas_mat_fake_7ano + 
        perguntas_mat_fake_8ano + perguntas_mat_fake_9ano +
        perguntas_ef_mat_6ano + perguntas_ef_mat_7ano + 
        perguntas_ef_mat_8ano + perguntas_ef_mat_9ano +
        perguntas_desafio_6ano + perguntas_desafio_7ano + 
        perguntas_desafio_8ano + perguntas_desafio_9ano
    )
    
    conn = get_connection()
    cursor = conn.cursor()
    inseridas = 0
    
    for p in todas_perguntas:
        cursor.execute("""
            SELECT id FROM questoes 
            WHERE pergunta = ? AND turma = ?
        """, (p['pergunta'], p['turma']))
        
        if cursor.fetchone() is None:
            cursor.execute("""
                INSERT INTO questoes 
                (turma, categoria, pergunta, resposta, opcao1, opcao2, opcao3, explicacao)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                p['turma'],
                p['categoria'],
                p['pergunta'],
                p.get('resposta', p.get('correta', '')),
                p.get('opcao1'),
                p.get('opcao2'),
                p.get('opcao3'),
                p.get('explicacao', '')
            ))
            inseridas += 1
    
    conn.commit()
    conn.close()
    print(f"✅ {inseridas} perguntas interdisciplinares inseridas!")
    return inseridas

# ============================================================
# 🧠 PERGUNTAS INTERDISCIPLINARES
# ============================================================

def inserir_perguntas_interdisciplinares():
    """Insere perguntas que misturam Cidadania + Matemática + Ed. Física"""
    
    perguntas = [
        # 6º Ano
        {"turma": "6º Ano - Anfitrião", "categoria": "etica",
         "pergunta": "Um atleta postou um treino de 45 min. Se treina 4x/semana, quantos minutos em 1 mês? E se postar fake news, o que fazer?",
         "opcao1": "720 min / Compartilhar",
         "opcao2": "720 min / Verificar e denunciar",
         "opcao3": "180 min / Ignorar",
         "correta": "720 min / Verificar e denunciar",
         "explicacao": "45 × 4 × 4 = 720 min. Sempre verifique antes de compartilhar!"},
        
        {"turma": "6º Ano - Anfitrião", "categoria": "exatas",
         "pergunta": "Se 5 alunos correm 100m cada, quantos metros no total?",
         "resposta": "500",
         "explicacao": "5 × 100 = 500 metros."},
        
        {"turma": "6º Ano - Anfitrião", "categoria": "fake",
         "pergunta": "Uma fake news foi compartilhada 100 vezes. Se cada pessoa compartilhar para 10 amigos, quantas verão? E o que fazer?",
         "opcao1": "1000 / Compartilhar",
         "opcao2": "1000 / Verificar antes",
         "opcao3": "500 / Ignorar",
         "correta": "1000 / Verificar antes",
         "explicacao": "100 × 10 = 1000 pessoas. Sempre verifique!"},
        
        {"turma": "7º Ano - Visitante", "categoria": "etica",
         "pergunta": "Um atleta treina 2h/dia, 5 dias/semana. Quantas horas em 4 semanas? Se postar fake news sobre rival, o que fazer?",
         "opcao1": "40h / Compartilhar",
         "opcao2": "40h / Denunciar",
         "opcao3": "20h / Ignorar",
         "correta": "40h / Denunciar",
         "explicacao": "2 × 5 × 4 = 40h. Denunciar fake news é cidadania!"},
        
        {"turma": "7º Ano - Visitante", "categoria": "fake",
         "pergunta": "Um jogador acertou 18 de 24 arremessos. Qual a %? Se sofrer cyberbullying, o que fazer?",
         "opcao1": "60% / Ignorar",
         "opcao2": "75% / Denunciar e apoiar",
         "opcao3": "80% / Rir",
         "correta": "75% / Denunciar e apoiar",
         "explicacao": "18 ÷ 24 = 75%. Cyberbullying deve ser denunciado!"},
        
        {"turma": "7º Ano - Visitante", "categoria": "fake",
         "pergunta": "Se 3 em cada 10 notícias são fake, quantas em 50? E o que fazer ao encontrar?",
         "opcao1": "10 / Compartilhar",
         "opcao2": "15 / Denunciar",
         "opcao3": "20 / Ignorar",
         "correta": "15 / Denunciar",
         "explicacao": "3/10 de 50 = 15 fake news. Denunciar é cidadania!"},
        
        # 8º Ano
        {"turma": "8º Ano - Visitante", "categoria": "etica",
         "pergunta": "Se 60% dos alunos praticam esporte e há 40 alunos, quantos praticam? Se um colega sofrer bullying, o que fazer?",
         "opcao1": "24 / Rir",
         "opcao2": "24 / Defender e denunciar",
         "opcao3": "30 / Ignorar",
         "correta": "24 / Defender e denunciar",
         "explicacao": "60% de 40 = 24 alunos. Defender é cidadania!"},
        
        {"turma": "8º Ano - Visitante", "categoria": "fake",
         "pergunta": "Um atleta corre 10 km em 50 min. Qual a velocidade média em km/h? Se postar foto sem permissão, o que fazer?",
         "opcao1": "10 km/h / Ignorar",
         "opcao2": "12 km/h / Alertar sobre privacidade",
         "opcao3": "15 km/h / Compartilhar",
         "correta": "12 km/h / Alertar sobre privacidade",
         "explicacao": "10/(50/60) = 12 km/h. Respeitar a privacidade é fundamental!"},
        
        {"turma": "8º Ano - Visitante", "categoria": "fake",
         "pergunta": "Uma fake news foi compartilhada 2.500 vezes. Se cada compartilhamento atinge 8 pessoas, quantas foram atingidas?",
         "opcao1": "10000",
         "opcao2": "20000",
         "opcao3": "25000",
         "correta": "20000",
         "explicacao": "2500 × 8 = 20.000 pessoas atingidas!"},
        
        # 9º Ano
        {"turma": "9º Ano - Visitante", "categoria": "etica",
         "pergunta": "Um atleta melhorou 15% em 60s. Qual o novo tempo? Se sofrer racismo online, o que fazer?",
         "opcao1": "51s / Ignorar",
         "opcao2": "51s / Denunciar e apoiar",
         "opcao3": "45s / Compartilhar",
         "correta": "51s / Denunciar e apoiar",
         "explicacao": "60 × 0,85 = 51s. Racismo é crime! Denuncie."},
        
        {"turma": "9º Ano - Visitante", "categoria": "fake",
         "pergunta": "Se 1 fake news gera 5 novas a cada hora, quantas em 6 horas? E o que fazer?",
         "opcao1": "15625 / Compartilhar",
         "opcao2": "15625 / Denunciar",
         "opcao3": "1000 / Ignorar",
         "correta": "15625 / Denunciar",
         "explicacao": "5^6 = 15.625. Denunciar é cidadania!"},
        
        {"turma": "9º Ano - Visitante", "categoria": "fake",
         "pergunta": "Um atleta treina 4h/dia, 6 dias/semana. Quantas horas em 1 ano (52 semanas)?",
         "opcao1": "1000h",
         "opcao2": "1248h",
         "opcao3": "1500h",
         "correta": "1248h",
         "explicacao": "4 × 6 × 52 = 1.248 horas."},
    ]
    
    conn = get_connection()
    cursor = conn.cursor()
    inseridas = 0
    
    for p in perguntas:
        cursor.execute("""
            SELECT id FROM questoes 
            WHERE pergunta = ? AND turma = ?
        """, (p['pergunta'], p['turma']))
        
        if cursor.fetchone() is None:
            cursor.execute("""
                INSERT INTO questoes 
                (turma, categoria, pergunta, resposta, opcao1, opcao2, opcao3, explicacao)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                p['turma'], p['categoria'], p['pergunta'],
                p.get('resposta', p.get('correta', '')),
                p.get('opcao1'), p.get('opcao2'), p.get('opcao3'),
                p.get('explicacao', '')
            ))
            inseridas += 1
    
    conn.commit()
    conn.close()
    print(f"✅ {inseridas} perguntas interdisciplinares inseridas!")
    return inseridas

# ============================================================
# 🧠 PERGUNTAS INTERDISCIPLINARES (Matemática + Ed. Física)
# ============================================================

def inserir_perguntas_interdisciplinares():
    """Insere todas as perguntas de Matemática, Ed. Física e Desafios"""
    
    # ========== MATEMÁTICA + CIDADANIA - FAKE NEWS ==========
    perguntas_mat_fake = [
        # 6º Ano
        {"turma": "6º Ano - Anfitrião", "categoria": "fake",
         "pergunta": "Uma fake news foi compartilhada 100 vezes. Se cada pessoa compartilhar para 10 amigos, quantas pessoas verão?",
         "resposta": "1000",
         "explicacao": "100 × 10 = 1000 pessoas. Fake news se espalham como epidemia!"},
        {"turma": "6º Ano - Anfitrião", "categoria": "fake",
         "pergunta": "Se 3 em cada 10 notícias são fake, quantas fake news existem em 50 notícias?",
         "resposta": "15",
         "explicacao": "3/10 de 50 = 15 fake news. Sempre verifique!"},
        {"turma": "6º Ano - Anfitrião", "categoria": "fake",
         "pergunta": "Um vídeo fake tem 200 curtidas. Se 1/4 são de robôs, quantas curtidas são reais?",
         "resposta": "150",
         "explicacao": "1/4 de 200 = 50. 200 - 50 = 150 curtidas reais."},
        # 7º Ano
        {"turma": "7º Ano - Visitante", "categoria": "fake",
         "pergunta": "Uma notícia falsa foi vista por 1.200 pessoas. Se 40% acreditaram, quantas acreditaram?",
         "resposta": "480",
         "explicacao": "40% de 1200 = 480 pessoas acreditaram na fake news."},
        {"turma": "7º Ano - Visitante", "categoria": "fake",
         "pergunta": "Um post fake tem 3.500 compartilhamentos por dia. Quantos em 7 dias?",
         "resposta": "24500",
         "explicacao": "3500 × 7 = 24.500 compartilhamentos em uma semana!"},
        # 8º Ano
        {"turma": "8º Ano - Visitante", "categoria": "fake",
         "pergunta": "Um vídeo fake teve 15.000 visualizações. Se 60% foram de pessoas diferentes, quantas pessoas viram?",
         "resposta": "9000",
         "explicacao": "60% de 15000 = 9.000 pessoas diferentes."},
        {"turma": "8º Ano - Visitante", "categoria": "fake",
         "pergunta": "Se 12% das notícias sobre política são fake, quantas fake news há em 5.000 notícias?",
         "resposta": "600",
         "explicacao": "12% de 5000 = 600 fake news."},
        # 9º Ano
        {"turma": "9º Ano - Visitante", "categoria": "fake",
         "pergunta": "Uma fake news atingiu 50.000 pessoas. Se 35% acreditaram, quantas foram enganadas?",
         "resposta": "17500",
         "explicacao": "35% de 50000 = 17.500 pessoas enganadas!"},
        {"turma": "9º Ano - Visitante", "categoria": "fake",
         "pergunta": "Se 1 fake news gera 5 novas a cada hora, quantas existirão em 6 horas?",
         "resposta": "15625",
         "explicacao": "5^6 = 15.625 fake news. É uma progressão geométrica!"},
    ]
    
    # ========== EDUCAÇÃO FÍSICA + MATEMÁTICA ==========
    perguntas_ef_mat = [
        # 6º Ano
        {"turma": "6º Ano - Anfitrião", "categoria": "fake",
         "pergunta": "Um aluno corre 400 metros em 2 minutos. Quantos metros corre em 5 minutos?",
         "resposta": "1000",
         "explicacao": "400 ÷ 2 = 200 m/min. 200 × 5 = 1000 metros."},
        {"turma": "6º Ano - Anfitrião", "categoria": "fake",
         "pergunta": "Se você faz 20 flexões por dia, quantas faz em 1 semana?",
         "resposta": "140",
         "explicacao": "20 × 7 = 140 flexões por semana."},
        {"turma": "6º Ano - Anfitrião", "categoria": "fake",
         "pergunta": "Um jogo de futebol tem 90 minutos. Quantos segundos tem?",
         "resposta": "5400",
         "explicacao": "90 × 60 = 5.400 segundos."},
        # 7º Ano
        {"turma": "7º Ano - Visitante", "categoria": "fake",
         "pergunta": "Um atleta treina 2 horas por dia, 5 dias por semana. Quantas horas treina em 4 semanas?",
         "resposta": "40",
         "explicacao": "2 × 5 = 10h/semana. 10 × 4 = 40 horas."},
        {"turma": "7º Ano - Visitante", "categoria": "fake",
         "pergunta": "Se uma corrida tem 5 km e você já correu 3.200 m, quantos metros faltam?",
         "resposta": "1800",
         "explicacao": "5 km = 5000 m. 5000 - 3200 = 1.800 metros."},
        {"turma": "7º Ano - Visitante", "categoria": "fake",
         "pergunta": "Um jogador acertou 18 de 24 arremessos. Qual a porcentagem de acerto?",
         "resposta": "75%",
         "explicacao": "18 ÷ 24 = 0,75 = 75% de acerto."},
        # 8º Ano
        {"turma": "8º Ano - Visitante", "categoria": "fake",
         "pergunta": "Um atleta corre 10 km em 50 minutos. Qual sua velocidade média em km/h?",
         "resposta": "12",
         "explicacao": "10 km em 50 min = 10/(50/60) = 12 km/h."},
        {"turma": "8º Ano - Visitante", "categoria": "fake",
         "pergunta": "Se 3/5 dos alunos praticam esporte, quantos de 40 alunos praticam?",
         "resposta": "24",
         "explicacao": "3/5 de 40 = 24 alunos praticam esporte."},
        {"turma": "8º Ano - Visitante", "categoria": "fake",
         "pergunta": "Um time fez 85 pontos em 5 jogos. Qual a média por jogo?",
         "resposta": "17",
         "explicacao": "85 ÷ 5 = 17 pontos por jogo."},
        # 9º Ano
        {"turma": "9º Ano - Visitante", "categoria": "fake",
         "pergunta": "Um atleta melhorou seu tempo de 60s para 54s. Qual a melhoria percentual?",
         "resposta": "10%",
         "explicacao": "(60-54)/60 = 6/60 = 0,1 = 10% de melhoria."},
        {"turma": "9º Ano - Visitante", "categoria": "fake",
         "pergunta": "Se você queima 500 cal/hora, quantas horas para queimar 2.000 cal?",
         "resposta": "4",
         "explicacao": "2000 ÷ 500 = 4 horas."},
        {"turma": "9º Ano - Visitante", "categoria": "fake",
         "pergunta": "Um atleta treina 4h/dia, 6 dias/semana. Quantas horas em 1 ano (52 semanas)?",
         "resposta": "1248",
         "explicacao": "4 × 6 × 52 = 1.248 horas por ano."},
    ]
    
    # ========== DESAFIO INTERDISCIPLINAR ==========
    perguntas_desafio = [
        {"turma": "6º Ano - Anfitrião", "categoria": "etica",
         "pergunta": "Um colega postou um treino de 30 min. Se ele treina 4x/semana, quantos minutos em 1 mês? E se ele postar fake news, o que fazer?",
         "opcao1": "480 min / Compartilhar",
         "opcao2": "480 min / Verificar e denunciar",
         "opcao3": "120 min / Ignorar",
         "correta": "480 min / Verificar e denunciar",
         "explicacao": "30 × 4 × 4 = 480 min. Sempre verifique antes de compartilhar!"},
        {"turma": "7º Ano - Visitante", "categoria": "etica",
         "pergunta": "Um atleta treina 2h/dia, 5 dias/semana. Quantas horas em 4 semanas? Se ele postar fake news sobre um rival, o que fazer?",
         "opcao1": "40h / Compartilhar",
         "opcao2": "40h / Denunciar",
         "opcao3": "20h / Ignorar",
         "correta": "40h / Denunciar",
         "explicacao": "2 × 5 × 4 = 40h. Denunciar fake news é cidadania!"},
        {"turma": "8º Ano - Visitante", "categoria": "etica",
         "pergunta": "Se 60% dos alunos praticam esporte e há 40 alunos, quantos praticam? Se um colega sofrer bullying, o que fazer?",
         "opcao1": "24 / Rir",
         "opcao2": "24 / Defender e denunciar",
         "opcao3": "30 / Ignorar",
         "correta": "24 / Defender e denunciar",
         "explicacao": "60% de 40 = 24 alunos. Defender é cidadania!"},
        {"turma": "9º Ano - Visitante", "categoria": "etica",
         "pergunta": "Um atleta melhorou 15% em 60s. Qual o novo tempo? Se sofrer racismo online, o que fazer?",
         "opcao1": "51s / Ignorar",
         "opcao2": "51s / Denunciar e apoiar",
         "opcao3": "45s / Compartilhar",
         "correta": "51s / Denunciar e apoiar",
         "explicacao": "60 × 0,85 = 51s. Racismo é crime! Denuncie."},
    ]
    
    # ========== JUNTAR TUDO ==========
    todas = perguntas_mat_fake + perguntas_ef_mat + perguntas_desafio
    
    # ========== INSERIR NO BANCO ==========
    conn = get_connection()
    cursor = conn.cursor()
    inseridas = 0
    
    for p in todas:
        cursor.execute("""
            SELECT id FROM questoes 
            WHERE pergunta = ? AND turma = ?
        """, (p['pergunta'], p['turma']))
        
        if cursor.fetchone() is None:
            cursor.execute("""
                INSERT INTO questoes 
                (turma, categoria, pergunta, resposta, opcao1, opcao2, opcao3, explicacao)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                p['turma'],
                p['categoria'],
                p['pergunta'],
                p.get('resposta', p.get('correta', '')),
                p.get('opcao1'),
                p.get('opcao2'),
                p.get('opcao3'),
                p.get('explicacao', '')
            ))
            inseridas += 1
    
    conn.commit()
    conn.close()
    print(f"✅ {inseridas} perguntas interdisciplinares inseridas!")
    return inseridas

def buscar_questoes_exatas(turma):
    """Busca perguntas de Matemática e Ed. Física"""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT * FROM questoes 
        WHERE turma = ? AND categoria = 'exatas'
        ORDER BY RANDOM()
    """, (turma,))
    questoes = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return questoes

# ============================================================
# 📚 BANCO DE PERGUNTAS — CATEGORIAS SEPARADAS
# ============================================================
#
# fake      → Cidadania Digital (Verdade/Fake)
# mat_fake  → Matemática + Cidadania (Verdade/Fake)
# cyber     → Cyberbullying (Sim/Não)
# etica     → Ética Digital (Múltipla escolha)
# inter     → Desafio Interdisciplinar (Múltipla escolha)
#
# ============================================================


def inserir_perguntas_categorias_separadas():
    """Insere todas as perguntas nas categorias corretas"""
    
    # ========== 📰 FAKE NEWS - CIDADANIA DIGITAL ==========
    perguntas_fake_cidadania = [
        {"turma": "6º Ano - Anfitrião", "categoria": "fake",
         "pergunta": "É verdade que devemos compartilhar tudo o que vemos na internet?",
         "resposta": "Fake",
         "explicacao": "Não! Sempre verifique antes de compartilhar."},
        {"turma": "6º Ano - Anfitrião", "categoria": "fake",
         "pergunta": "É verdade que fake news podem causar danos reais?",
         "resposta": "Verdade",
         "explicacao": "Sim! Fake news podem prejudicar pessoas e instituições."},
        {"turma": "6º Ano - Anfitrião", "categoria": "fake",
         "pergunta": "É verdade que tudo que está na internet é verdade?",
         "resposta": "Fake",
         "explicacao": "Não! Qualquer pessoa pode publicar qualquer coisa."},
        {"turma": "6º Ano - Anfitrião", "categoria": "fake",
         "pergunta": "É verdade que devemos verificar a fonte antes de compartilhar?",
         "resposta": "Verdade",
         "explicacao": "Sim! Verificar a fonte é o primeiro passo."},
        {"turma": "6º Ano - Anfitrião", "categoria": "fake",
         "pergunta": "É verdade que fotos e vídeos nunca são editados?",
         "resposta": "Fake",
         "explicacao": "Muitas fotos e vídeos são editados para enganar."},
    ]
    
    # ========== 🧮 MATEMÁTICA + CIDADANIA - FAKE NEWS ==========
    perguntas_mat_fake = [
        {"turma": "6º Ano - Anfitrião", "categoria": "mat_fake",
         "pergunta": "É verdade que 1 em cada 3 notícias na internet é falsa?",
         "resposta": "Fake",
         "explicacao": "Não há um número exato. O importante é sempre verificar!"},
        {"turma": "6º Ano - Anfitrião", "categoria": "mat_fake",
         "pergunta": "Uma fake news foi compartilhada 100 vezes. Se cada pessoa compartilhar para 10 amigos, 1000 pessoas verão. É verdade?",
         "resposta": "Verdade",
         "explicacao": "100 × 10 = 1000 pessoas. Fake news se espalham rápido!"},
        {"turma": "6º Ano - Anfitrião", "categoria": "mat_fake",
         "pergunta": "Se 3 em cada 10 notícias são fake, em 50 notícias teremos 15 fake news. É verdade?",
         "resposta": "Verdade",
         "explicacao": "3/10 de 50 = 15 fake news. Sempre verifique!"}, 
        {"turma": "6º Ano - Anfitrião", "categoria": "mat_fake",
         "pergunta": "É verdade que 1 em cada 3 notícias na internet é falsa?",
         "resposta": "Fake",
         "explicacao": "Não há um número exato. O importante é sempre verificar!"},
        {"turma": "6º Ano - Anfitrião", "categoria": "mat_fake",
         "pergunta": "Uma fake news foi compartilhada 100 vezes. Se cada pessoa compartilhar para 10 amigos, 1000 pessoas verão. É verdade?",
         "resposta": "Verdade",
         "explicacao": "100 × 10 = 1000 pessoas. Fake news se espalham rápido!"},
        {"turma": "6º Ano - Anfitrião", "categoria": "mat_fake",
         "pergunta": "Se 3 em cada 10 notícias são fake, em 50 notícias teremos 15 fake news. É verdade?",
         "resposta": "Verdade",
         "explicacao": "3/10 de 50 = 15 fake news. Sempre verifique!"},
        {"turma": "6º Ano - Anfitrião", "categoria": "mat_fake",
         "pergunta": "Um vídeo fake tem 200 curtidas. Se 1/4 são de robôs, 50 curtidas são de robôs. É verdade?",
         "resposta": "Verdade",
         "explicacao": "1/4 de 200 = 50. Sempre desconfie de números redondos!"},
        {"turma": "6º Ano - Anfitrião", "categoria": "mat_fake",
         "pergunta": "Se uma fake news atinge 500 pessoas e cada uma compartilha para 4, atinge 2000 pessoas. É verdade?",
         "resposta": "Verdade",
         "explicacao": "500 × 4 = 2000 pessoas. Fake news são perigosas!"},
        
        # ========== 7º ANO ==========
        {"turma": "7º Ano - Visitante", "categoria": "mat_fake",
         "pergunta": "Uma notícia falsa foi vista por 1.200 pessoas. Se 40% acreditaram, 480 acreditaram. É verdade?",
         "resposta": "Verdade",
         "explicacao": "40% de 1200 = 480 pessoas acreditaram na fake news."},
        {"turma": "7º Ano - Visitante", "categoria": "mat_fake",
         "pergunta": "Um post fake tem 3.500 compartilhamentos por dia. Em 7 dias, terá 24.500. É verdade?",
         "resposta": "Verdade",
         "explicacao": "3500 × 7 = 24.500 compartilhamentos em uma semana!"},
        {"turma": "7º Ano - Visitante", "categoria": "mat_fake",
         "pergunta": "Se 5% das notícias são fake, em 2.000 notícias teremos 100 fake news. É verdade?",
         "resposta": "Verdade",
         "explicacao": "5% de 2000 = 100 fake news. Sempre verifique!"},
        {"turma": "7º Ano - Visitante", "categoria": "mat_fake",
         "pergunta": "Uma fake news foi desmentida após 48 horas. Se passaram 2.880 minutos. É verdade?",
         "resposta": "Verdade",
         "explicacao": "48 × 60 = 2.880 minutos. Muito tempo para uma mentira!"},
        {"turma": "7º Ano - Visitante", "categoria": "mat_fake",
         "pergunta": "Se uma pessoa compartilha 3 fake news por dia, em 30 dias serão 90. É verdade?",
         "resposta": "Verdade",
         "explicacao": "3 × 30 = 90 fake news em um mês. Isso é muito!"},
        {"turma": "7º Ano - Visitante", "categoria": "mat_fake",
         "pergunta": "Uma notícia falsa foi vista por 1.200 pessoas. Se 40% acreditaram, 480 acreditaram. É verdade?",
         "resposta": "Verdade",
         "explicacao": "40% de 1200 = 480 pessoas acreditaram na fake news."},
        
        # ========== 8º ANO ==========
        {"turma": "8º Ano - Visitante", "categoria": "mat_fake",
         "pergunta": "Um vídeo fake teve 15.000 visualizações. Se 60% foram de pessoas diferentes, 9.000 pessoas viram. É verdade?",
         "resposta": "Verdade",
         "explicacao": "60% de 15000 = 9.000 pessoas diferentes."},
        {"turma": "8º Ano - Visitante", "categoria": "mat_fake",
         "pergunta": "Uma fake news foi compartilhada 2.500 vezes. Se cada compartilhamento atinge 8 pessoas, 20.000 foram atingidas. É verdade?",
         "resposta": "Verdade",
         "explicacao": "2500 × 8 = 20.000 pessoas atingidas!"},
        {"turma": "8º Ano - Visitante", "categoria": "mat_fake",
         "pergunta": "Se 12% das notícias sobre política são fake, em 5.000 notícias teremos 600 fake news. É verdade?",
         "resposta": "Verdade",
         "explicacao": "12% de 5000 = 600 fake news. Isso é alarmante!"},
        {"turma": "8º Ano - Visitante", "categoria": "mat_fake",
         "pergunta": "Um site fake publicou 25 notícias falsas em 5 dias. A média é de 5 por dia. É verdade?",
         "resposta": "Verdade",
         "explicacao": "25 ÷ 5 = 5 notícias falsas por dia."},
        {"turma": "8º Ano - Visitante", "categoria": "mat_fake",
         "pergunta": "Se uma fake news foi vista 1.000 vezes e 0,5% denunciaram, 5 denúncias foram feitas. É verdade?",
         "resposta": "Verdade",
         "explicacao": "0,5% de 1000 = 5 denúncias. Poucas pessoas denunciam!"},
        {"turma": "8º Ano - Visitante", "categoria": "mat_fake",
         "pergunta": "Se 12% das notícias sobre política são fake, em 5.000 notícias teremos 600 fake news. É verdade?",
         "resposta": "Verdade",
         "explicacao": "12% de 5000 = 600 fake news. Isso é alarmante!"},
        
        # ========== 9º ANO ==========
        {"turma": "9º Ano - Visitante", "categoria": "mat_fake",
         "pergunta": "Uma fake news atingiu 50.000 pessoas. Se 35% acreditaram, 17.500 foram enganadas. É verdade?",
         "resposta": "Verdade",
         "explicacao": "35% de 50000 = 17.500 pessoas enganadas!"},
        {"turma": "9º Ano - Visitante", "categoria": "mat_fake",
         "pergunta": "Se uma fake news cresce 20% ao dia, a partir de 100 pessoas, em 3 dias serão 172 pessoas. É verdade?",
         "resposta": "Verdade",
         "explicacao": "100 × 1,2 = 120 (dia 1); 120 × 1,2 = 144 (dia 2); 144 × 1,2 = 172,8 (dia 3)."},
        {"turma": "9º Ano - Visitante", "categoria": "mat_fake",
         "pergunta": "Um estudo mostrou que 68% das fake news são compartilhadas por 10% das pessoas. Se 1.000 pessoas compartilham fake news, 100 são responsáveis por 68%. É verdade?",
         "resposta": "Verdade",
         "explicacao": "10% de 1000 = 100 pessoas são responsáveis pela maioria!"},
        {"turma": "9º Ano - Visitante", "categoria": "mat_fake",
         "pergunta": "Se 1 fake news gera 5 novas a cada hora, em 6 horas existirão 15.625. É verdade?",
         "resposta": "Verdade",
         "explicacao": "5^6 = 15.625 fake news. É uma progressão geométrica!"},
        {"turma": "9º Ano - Visitante", "categoria": "mat_fake",
         "pergunta": "Uma fake news foi vista 200.000 vezes. Se 0,1% denunciaram, 200 denúncias foram feitas. É verdade?",
         "resposta": "Verdade",
         "explicacao": "0,1% de 200.000 = 200 denúncias. Ainda é pouco!"},
        {"turma": "9º Ano - Visitante", "categoria": "mat_fake",
         "pergunta": "Uma fake news atingiu 50.000 pessoas. Se 35% acreditaram, 17.500 foram enganadas. É verdade?",
         "resposta": "Verdade",
         "explicacao": "35% de 50000 = 17.500 pessoas enganadas!"},    
    ]
    
    # ========== 🧠 DESAFIO INTERDISCIPLINAR ==========
    perguntas_inter = [
        {"turma": "6º Ano - Anfitrião", "categoria": "inter",
         "pergunta": "Um atleta postou um treino de 45 minutos. Se ele treina 4 vezes por semana, quantos minutos em 1 mês?",
         "opcao1": "720 min",
         "opcao2": "180 min",
         "opcao3": "500 min",
         "resposta": "720 min",
         "explicacao": "45 × 4 × 4 = 720 minutos."},
        {"turma": "6º Ano - Anfitrião", "categoria": "inter",
         "pergunta": "Se 5 alunos correm 100m cada, quantos metros no total?",
         "opcao1": "400m",
         "opcao2": "500m",
         "opcao3": "600m",
         "resposta": "500m",
         "explicacao": "5 × 100 = 500 metros."},
        {"turma": "6º Ano - Anfitrião", "categoria": "inter",
         "pergunta": "Um atleta postou um treino de 45 minutos. Se ele treina 4 vezes por semana, quantos minutos em 1 mês?",
         "opcao1": "720 min",
         "opcao2": "180 min",
         "opcao3": "500 min",
         "resposta": "720 min",
         "explicacao": "45 × 4 × 4 = 720 minutos."},
        {"turma": "6º Ano - Anfitrião", "categoria": "inter",
         "pergunta": "Se 5 alunos correm 100m cada, quantos metros no total?",
         "opcao1": "400m",
         "opcao2": "500m",
         "opcao3": "600m",
         "resposta": "500m",
         "explicacao": "5 × 100 = 500 metros."},
        {"turma": "6º Ano - Anfitrião", "categoria": "inter",
         "pergunta": "Se você faz 20 flexões por dia, quantas faz em 1 semana?",
         "opcao1": "100",
         "opcao2": "140",
         "opcao3": "180",
         "resposta": "140",
         "explicacao": "20 × 7 = 140 flexões por semana."},
        {"turma": "6º Ano - Anfitrião", "categoria": "inter",
         "pergunta": "Um jogo de futebol tem 90 minutos. Quantos segundos tem?",
         "opcao1": "5400",
         "opcao2": "3600",
         "opcao3": "7200",
         "resposta": "5400",
         "explicacao": "90 × 60 = 5.400 segundos."},
        {"turma": "6º Ano - Anfitrião", "categoria": "inter",
         "pergunta": "Se uma pessoa bebe 2 litros de água por dia, quantos litros bebe em 30 dias?",
         "opcao1": "30",
         "opcao2": "60",
         "opcao3": "90",
         "resposta": "60",
         "explicacao": "2 × 30 = 60 litros por mês."},
        {"turma": "7º Ano - Visitante", "categoria": "inter",
         "pergunta": "Um jogador acertou 18 de 24 arremessos. Qual a porcentagem?",
         "opcao1": "60%",
         "opcao2": "75%",
         "opcao3": "80%",
         "resposta": "75%",
         "explicacao": "18 ÷ 24 = 75%."},
        {"turma": "7º Ano - Visitante", "categoria": "inter",
         "pergunta": "Um atleta treina 2 horas por dia, 5 dias por semana. Quantas horas treina em 4 semanas?",
         "opcao1": "20h",
         "opcao2": "40h",
         "opcao3": "60h",
         "resposta": "40h",
         "explicacao": "2 × 5 = 10h/semana. 10 × 4 = 40 horas."},
        {"turma": "7º Ano - Visitante", "categoria": "inter",
         "pergunta": "Se uma corrida tem 5 km e você já correu 3.200 m, quantos metros faltam?",
         "opcao1": "1800",
         "opcao2": "2200",
         "opcao3": "1500",
         "resposta": "1800",
         "explicacao": "5 km = 5000 m. 5000 - 3200 = 1.800 metros."},
        {"turma": "7º Ano - Visitante", "categoria": "inter",
         "pergunta": "Um jogador acertou 18 de 24 arremessos. Qual a porcentagem de acerto?",
         "opcao1": "60%",
         "opcao2": "75%",
         "opcao3": "80%",
         "resposta": "75%",
         "explicacao": "18 ÷ 24 = 0,75 = 75% de acerto."},
        {"turma": "7º Ano - Visitante", "categoria": "inter",
         "pergunta": "Se você queima 300 calorias por hora de exercício, quantas queima em 45 minutos?",
         "opcao1": "150",
         "opcao2": "225",
         "opcao3": "300",
         "resposta": "225",
         "explicacao": "300 ÷ 60 = 5 cal/min. 5 × 45 = 225 calorias."},
        {"turma": "7º Ano - Visitante", "categoria": "inter",
         "pergunta": "Um time ganhou 12 de 20 jogos. Qual a porcentagem de vitórias?",
         "opcao1": "50%",
         "opcao2": "60%",
         "opcao3": "70%",
         "resposta": "60%",
         "explicacao": "12 ÷ 20 = 0,6 = 60% de vitórias."},
        {"turma": "8º Ano - Visitante", "categoria": "inter",
         "pergunta": "Se 3/5 dos alunos praticam esporte, quantos de 40 alunos praticam?",
         "opcao1": "20",
         "opcao2": "24",
         "opcao3": "30",
         "resposta": "24",
         "explicacao": "3/5 de 40 = 24 alunos."},
        {"turma": "8º Ano - Visitante", "categoria": "inter",
         "pergunta": "Um atleta corre 10 km em 50 minutos. Qual sua velocidade média em km/h?",
         "opcao1": "10 km/h",
         "opcao2": "12 km/h",
         "opcao3": "15 km/h",
         "resposta": "12 km/h",
         "explicacao": "10 km em 50 min = 10/(50/60) = 12 km/h."},
        {"turma": "8º Ano - Visitante", "categoria": "inter",
         "pergunta": "Se 3/5 dos alunos praticam esporte, quantos de 40 alunos praticam?",
         "opcao1": "20",
         "opcao2": "24",
         "opcao3": "30",
         "resposta": "24",
         "explicacao": "3/5 de 40 = 24 alunos praticam esporte."},
        {"turma": "8º Ano - Visitante", "categoria": "inter",
         "pergunta": "Um time fez 85 pontos em 5 jogos. Qual a média por jogo?",
         "opcao1": "15",
         "opcao2": "17",
         "opcao3": "20",
         "resposta": "17",
         "explicacao": "85 ÷ 5 = 17 pontos por jogo."},
        {"turma": "8º Ano - Visitante", "categoria": "inter",
         "pergunta": "Se você faz 3 séries de 12 repetições, quantas repetições no total?",
         "opcao1": "30",
         "opcao2": "36",
         "opcao3": "40",
         "resposta": "36",
         "explicacao": "3 × 12 = 36 repetições."},
        {"turma": "8º Ano - Visitante", "categoria": "inter",
         "pergunta": "Uma piscina olímpica tem 50 m. Quantas voltas para nadar 1.500 m?",
         "opcao1": "20",
         "opcao2": "30",
         "opcao3": "40",
         "resposta": "30",
         "explicacao": "1500 ÷ 50 = 30 voltas."},
        {"turma": "9º Ano - Visitante", "categoria": "inter",
         "pergunta": "Um atleta melhorou seu tempo de 60s para 54s. Qual a melhoria percentual?",
         "opcao1": "5%",
         "opcao2": "10%",
         "opcao3": "15%",
         "resposta": "10%",
         "explicacao": "(60-54)/60 = 10%."},
{"turma": "9º Ano - Visitante", "categoria": "inter",
         "pergunta": "Um atleta melhorou seu tempo de 60s para 54s. Qual a melhoria percentual?",
         "opcao1": "5%",
         "opcao2": "10%",
         "opcao3": "15%",
         "resposta": "10%",
         "explicacao": "(60-54)/60 = 6/60 = 0,1 = 10% de melhoria."},
        {"turma": "9º Ano - Visitante", "categoria": "inter",
         "pergunta": "Se você queima 500 cal/hora, quantas horas para queimar 2.000 cal?",
         "opcao1": "2",
         "opcao2": "4",
         "opcao3": "6",
         "resposta": "4",
         "explicacao": "2000 ÷ 500 = 4 horas."},
        {"turma": "9º Ano - Visitante", "categoria": "inter",
         "pergunta": "Um time fez 120 pontos em 8 jogos. Qual a média? Se melhorar 25%, qual será?",
         "opcao1": "15 e 18,75",
         "opcao2": "18 e 22,5",
         "opcao3": "20 e 25",
         "resposta": "15 e 18,75",
         "explicacao": "120 ÷ 8 = 15. 15 × 1,25 = 18,75 pontos."},
        {"turma": "9º Ano - Visitante", "categoria": "inter",
         "pergunta": "Se um corredor faz 5 km em 25 min, quanto tempo leva para 8 km?",
         "opcao1": "35 min",
         "opcao2": "40 min",
         "opcao3": "45 min",
         "resposta": "40 min",
         "explicacao": "5 km → 25 min. 1 km → 5 min. 8 km → 40 min."},
        {"turma": "9º Ano - Visitante", "categoria": "inter",
         "pergunta": "Um atleta treina 4h/dia, 6 dias/semana. Quantas horas em 1 ano (52 semanas)?",
         "opcao1": "1000h",
         "opcao2": "1248h",
         "opcao3": "1500h",
         "resposta": "1248h",
         "explicacao": "4 × 6 × 52 = 1.248 horas por ano."},
    ]

    # ========== 🌐 CULTURA DIGITAL ==========
    perguntas_cultura_digital = [
        # ========== 6º ANO ==========
        {"turma": "6º Ano - Anfitrião", "categoria": "fake",
         "pergunta": "É verdade que tudo o que você posta na internet fica para sempre?",
         "resposta": "Verdade",
         "explicacao": "Sim! A internet nunca esquece. Pense antes de postar!"},
        {"turma": "6º Ano - Anfitrião", "categoria": "fake",
         "pergunta": "É verdade que podemos apagar tudo o que postamos na internet?",
         "resposta": "Fake",
         "explicacao": "Não! Prints e cópias podem guardar para sempre."},
        {"turma": "6º Ano - Anfitrião", "categoria": "fake",
         "pergunta": "É verdade que a 'pegada digital' é tudo o que deixamos na internet?",
         "resposta": "Verdade",
         "explicacao": "Sim! Cada clique, curtida e post deixa rastros."},
        {"turma": "6º Ano - Anfitrião", "categoria": "fake",
         "pergunta": "É verdade que podemos usar a internet sem nos preocupar com segurança?",
         "resposta": "Fake",
         "explicacao": "Não! Segurança digital é fundamental!"},
        {"turma": "6º Ano - Anfitrião", "categoria": "fake",
         "pergunta": "É verdade que a tecnologia pode ser usada para o bem e para o mal?",
         "resposta": "Verdade",
         "explicacao": "Sim! Depende de como usamos."},
        
        # ========== 7º ANO ==========
        {"turma": "7º Ano - Visitante", "categoria": "fake",
         "pergunta": "É verdade que os algoritmos decidem o que vemos nas redes sociais?",
         "resposta": "Verdade",
         "explicacao": "Sim! Eles mostram o que acham que você vai gostar."},
        {"turma": "7º Ano - Visitante", "categoria": "fake",
         "pergunta": "É verdade que a internet é um espaço livre sem regras?",
         "resposta": "Fake",
         "explicacao": "Não! Existem leis e regras de convivência."},
        {"turma": "7º Ano - Visitante", "categoria": "fake",
         "pergunta": "É verdade que a cultura digital inclui saber usar a tecnologia com ética?",
         "resposta": "Verdade",
         "explicacao": "Sim! Ética digital é parte da cultura digital."},
        {"turma": "7º Ano - Visitante", "categoria": "fake",
         "pergunta": "É verdade que podemos confiar em todas as informações que os algoritmos mostram?",
         "resposta": "Fake",
         "explicacao": "Não! Algoritmos podem reforçar fake news."},
        {"turma": "7º Ano - Visitante", "categoria": "fake",
         "pergunta": "É verdade que a cultura digital envolve colaboração e compartilhamento?",
         "resposta": "Verdade",
         "explicacao": "Sim! A internet é feita de trocas."},
        
        # ========== 8º ANO ==========
        {"turma": "8º Ano - Visitante", "categoria": "fake",
         "pergunta": "É verdade que a cultura digital inclui a 'cultura maker'?",
         "resposta": "Verdade",
         "explicacao": "Sim! Criar, consertar e inovar fazem parte."},
        {"turma": "8º Ano - Visitante", "categoria": "fake",
         "pergunta": "É verdade que a tecnologia é neutra e não influencia a sociedade?",
         "resposta": "Fake",
         "explicacao": "Não! A tecnologia transforma a sociedade."},
        {"turma": "8º Ano - Visitante", "categoria": "fake",
         "pergunta": "É verdade que a cultura digital envolve respeitar direitos autorais?",
         "resposta": "Verdade",
         "explicacao": "Sim! Baixar e copiar sem permissão é crime."},
        {"turma": "8º Ano - Visitante", "categoria": "fake",
         "pergunta": "É verdade que a inteligência artificial pode criar preconceitos?",
         "resposta": "Verdade",
         "explicacao": "Sim! Se os dados forem preconceituosos, a IA também será."},
        {"turma": "8º Ano - Visitante", "categoria": "fake",
         "pergunta": "É verdade que a cultura digital é só sobre usar redes sociais?",
         "resposta": "Fake",
         "explicacao": "Não! É sobre criar, programar, colaborar e se expressar."},
        
        # ========== 9º ANO ==========
        {"turma": "9º Ano - Visitante", "categoria": "fake",
         "pergunta": "É verdade que a cultura digital inclui a programação e o pensamento computacional?",
         "resposta": "Verdade",
         "explicacao": "Sim! Programar é uma forma de se expressar."},
        {"turma": "9º Ano - Visitante", "categoria": "fake",
         "pergunta": "É verdade que a tecnologia sempre melhora a vida das pessoas?",
         "resposta": "Fake",
         "explicacao": "Não! Depende de como é usada."},
        {"turma": "9º Ano - Visitante", "categoria": "fake",
         "pergunta": "É verdade que a cultura digital envolve a inclusão de todos?",
         "resposta": "Verdade",
         "explicacao": "Sim! A internet deve ser um espaço para todos."},
        {"turma": "9º Ano - Visitante", "categoria": "fake",
         "pergunta": "É verdade que a cultura digital é igual em todos os países?",
         "resposta": "Fake",
         "explicacao": "Não! Cada lugar tem sua cultura e suas regras."},
        {"turma": "9º Ano - Visitante", "categoria": "fake",
         "pergunta": "É verdade que a cultura digital pode ajudar a resolver problemas sociais?",
         "resposta": "Verdade",
         "explicacao": "Sim! Tecnologia pode transformar realidades."},
    ]

    # ========== 🤝 RESPONSABILIDADE E CIDADANIA ==========
    perguntas_responsabilidade = [
        # ========== 6º ANO ==========
        {"turma": "6º Ano - Anfitrião", "categoria": "cyber",
         "pergunta": "É correto defender um colega que está sendo vítima de cyberbullying?",
         "resposta": "Sim",
         "explicacao": "Defender é atitude de cidadão responsável!"},
        {"turma": "6º Ano - Anfitrião", "categoria": "cyber",
         "pergunta": "É correto denunciar conteúdo ofensivo nas redes sociais?",
         "resposta": "Sim",
         "explicacao": "Denunciar é responsabilidade de todos!"},
        {"turma": "6º Ano - Anfitrião", "categoria": "etica",
         "pergunta": "Você viu uma fake news sobre a escola. O que fazer?",
         "opcao1": "Compartilhar",
         "opcao2": "Verificar e avisar a direção",
         "opcao3": "Ignorar",
         "correta": "Verificar e avisar a direção",
         "explicacao": "Responsabilidade é agir com cuidado!"},
        {"turma": "6º Ano - Anfitrião", "categoria": "cyber",
         "pergunta": "É correto avisar um adulto se você sofrer cyberbullying?",
         "resposta": "Sim",
         "explicacao": "Procurar ajuda é atitude sábia e responsável!"},
        {"turma": "6º Ano - Anfitrião", "categoria": "etica",
         "pergunta": "Você viu um colega postando fotos de outro sem permissão. O que fazer?",
         "opcao1": "Rir",
         "opcao2": "Avisar o colega sobre o perigo",
         "opcao3": "Compartilhar",
         "correta": "Avisar o colega sobre o perigo",
         "explicacao": "Respeitar a privacidade é fundamental!"},
        
        # ========== 7º ANO ==========
        {"turma": "7º Ano - Visitante", "categoria": "cyber",
         "pergunta": "É correto apoiar campanhas contra o cyberbullying?",
         "resposta": "Sim",
         "explicacao": "Apoiar é atitude de cidadão consciente!"},
        {"turma": "7º Ano - Visitante", "categoria": "cyber",
         "pergunta": "É correto criar grupos para excluir alguém?",
         "resposta": "Não",
         "explicacao": "Excluir é uma forma de bullying!"},
        {"turma": "7º Ano - Visitante", "categoria": "etica",
         "pergunta": "Você descobriu que um colega está sofrendo cyberbullying. O que fazer?",
         "opcao1": "Ignorar",
         "opcao2": "Apoiar, denunciar e conversar com um adulto",
         "opcao3": "Rir",
         "correta": "Apoiar, denunciar e conversar com um adulto",
         "explicacao": "Responsabilidade é agir para proteger!"},
        {"turma": "7º Ano - Visitante", "categoria": "cyber",
         "pergunta": "É correto fazer comentários racistas online?",
         "resposta": "Não",
         "explicacao": "Racismo é crime! Respeite a diversidade."},
        {"turma": "7º Ano - Visitante", "categoria": "etica",
         "pergunta": "Você viu um amigo compartilhando fake news. O que fazer?",
         "opcao1": "Compartilhar também",
         "opcao2": "Conversar e mostrar que é fake",
         "opcao3": "Ignorar",
         "correta": "Conversar e mostrar que é fake",
         "explicacao": "Responsabilidade é ajudar os outros a entender!"},
        
        # ========== 8º ANO ==========
        {"turma": "8º Ano - Visitante", "categoria": "cyber",
         "pergunta": "É correto denunciar discurso de ódio nas redes sociais?",
         "resposta": "Sim",
         "explicacao": "Denunciar é responsabilidade de todo cidadão!"},
        {"turma": "8º Ano - Visitante", "categoria": "cyber",
         "pergunta": "É correto compartilhar fake news sem verificar?",
         "resposta": "Não",
         "explicacao": "Compartilhar sem verificar é irresponsável!"},
        {"turma": "8º Ano - Visitante", "categoria": "etica",
         "pergunta": "Você descobriu que um colega está sendo vítima de racismo online. O que fazer?",
         "opcao1": "Ignorar",
         "opcao2": "Apoiar, denunciar e conversar com um adulto",
         "opcao3": "Rir",
         "correta": "Apoiar, denunciar e conversar com um adulto",
         "explicacao": "Racismo é crime! Denuncie e apoie!"},
        {"turma": "8º Ano - Visitante", "categoria": "cyber",
         "pergunta": "É correto criar perfil falso para enganar pessoas?",
         "resposta": "Não",
         "explicacao": "Perfil falso é crime e falta de responsabilidade!"},
        {"turma": "8º Ano - Visitante", "categoria": "etica",
         "pergunta": "Você viu um colega postando conteúdo ofensivo. O que fazer?",
         "opcao1": "Compartilhar",
         "opcao2": "Denunciar e conversar com o colega",
         "opcao3": "Rir",
         "correta": "Denunciar e conversar com o colega",
         "explicacao": "Responsabilidade é agir com ética!"},
        
        # ========== 9º ANO ==========
        {"turma": "9º Ano - Visitante", "categoria": "cyber",
         "pergunta": "É correto ajudar a combater fake news nas redes sociais?",
         "resposta": "Sim",
         "explicacao": "Combater fake news é responsabilidade de todos!"},
        {"turma": "9º Ano - Visitante", "categoria": "cyber",
         "pergunta": "É correto compartilhar conteúdo de ódio?",
         "resposta": "Não",
         "explicacao": "Conteúdo de ódio é crime! Denuncie."},
        {"turma": "9º Ano - Visitante", "categoria": "etica",
         "pergunta": "Você viu um atleta sendo vítima de racismo online. O que fazer?",
         "opcao1": "Ignorar",
         "opcao2": "Denunciar, apoiar e criar campanha de conscientização",
         "opcao3": "Compartilhar",
         "correta": "Denunciar, apoiar e criar campanha de conscientização",
         "explicacao": "Responsabilidade é agir para transformar!"},
        {"turma": "9º Ano - Visitante", "categoria": "cyber",
         "pergunta": "É correto denunciar conteúdo racista nas redes sociais?",
         "resposta": "Sim",
         "explicacao": "Denunciar racismo é obrigação de todo cidadão!"},
        {"turma": "9º Ano - Visitante", "categoria": "etica",
         "pergunta": "Você viu uma fake news que pode causar pânico. O que fazer?",
         "opcao1": "Compartilhar",
         "opcao2": "Verificar, denunciar e avisar as autoridades",
         "opcao3": "Ignorar",
         "correta": "Verificar, denunciar e avisar as autoridades",
         "explicacao": "Responsabilidade é proteger a comunidade!"},
    ]

    # ========== 🤖 DEEPFAKE ==========
    perguntas_deepfake = [
        # ========== 6º ANO ==========
        {"turma": "6º Ano - Anfitrião", "categoria": "fake",
         "pergunta": "É verdade que deepfake é um vídeo ou áudio falso criado por inteligência artificial?",
         "resposta": "Verdade",
         "explicacao": "Sim! Deepfake usa IA para criar vídeos e áudios falsos muito realistas."},
        {"turma": "6º Ano - Anfitrião", "categoria": "fake",
         "pergunta": "É verdade que deepfakes são sempre fáceis de identificar?",
         "resposta": "Fake",
         "explicacao": "Não! Deepfakes podem ser muito realistas e difíceis de detectar."},
        {"turma": "6º Ano - Anfitrião", "categoria": "fake",
         "pergunta": "É verdade que podemos confiar em tudo que vemos em vídeo?",
         "resposta": "Fake",
         "explicacao": "Não! Vídeos podem ser editados ou criados por IA (deepfake)."},
        {"turma": "6º Ano - Anfitrião", "categoria": "fake",
         "pergunta": "É verdade que deepfakes podem ser usados para enganar pessoas?",
         "resposta": "Verdade",
         "explicacao": "Sim! Deepfakes são usados para espalhar mentiras e manipular."},
        {"turma": "6º Ano - Anfitrião", "categoria": "fake",
         "pergunta": "É verdade que devemos desconfiar de vídeos muito estranhos ou exagerados?",
         "resposta": "Verdade",
         "explicacao": "Sim! Vídeos estranhos podem ser deepfakes."},
        
        # ========== 7º ANO ==========
        {"turma": "7º Ano - Visitante", "categoria": "fake",
         "pergunta": "É verdade que deepfakes podem imitar a voz de uma pessoa real?",
         "resposta": "Verdade",
         "explicacao": "Sim! A IA pode clonar vozes e enganar pessoas por telefone."},
        {"turma": "7º Ano - Visitante", "categoria": "fake",
         "pergunta": "É verdade que deepfakes são sempre criados para o bem?",
         "resposta": "Fake",
         "explicacao": "Não! Deepfakes podem ser usados para crimes e manipulação."},
        {"turma": "7º Ano - Visitante", "categoria": "fake",
         "pergunta": "É verdade que devemos verificar a fonte antes de compartilhar um vídeo?",
         "resposta": "Verdade",
         "explicacao": "Sim! Sempre verifique a fonte antes de compartilhar!"},
        {"turma": "7º Ano - Visitante", "categoria": "fake",
         "pergunta": "É verdade que deepfakes podem ser usados para criar fake news políticas?",
         "resposta": "Verdade",
         "explicacao": "Sim! Deepfakes políticos são uma grande ameaça à democracia."},
        {"turma": "7º Ano - Visitante", "categoria": "fake",
         "pergunta": "É verdade que toda pessoa famosa que aparece em vídeo é real?",
         "resposta": "Fake",
         "explicacao": "Não! Pode ser um deepfake feito por IA."},
        
        # ========== 8º ANO ==========
        {"turma": "8º Ano - Visitante", "categoria": "fake",
         "pergunta": "É verdade que deepfakes podem ser detectados por softwares especiais?",
         "resposta": "Verdade",
         "explicacao": "Sim! Existem ferramentas que ajudam a detectar deepfakes."},
        {"turma": "8º Ano - Visitante", "categoria": "fake",
         "pergunta": "É verdade que deepfakes são 100% perfeitos e impossíveis de detectar?",
         "resposta": "Fake",
         "explicacao": "Não! Deepfakes podem ter falhas, como olhos estranhos ou movimentos estranhos."},
        {"turma": "8º Ano - Visitante", "categoria": "fake",
         "pergunta": "É verdade que deepfakes podem ser usados para extorsão e chantagem?",
         "resposta": "Verdade",
         "explicacao": "Sim! Criminosos usam deepfakes para chantagear pessoas."},
        {"turma": "8º Ano - Visitante", "categoria": "fake",
         "pergunta": "É verdade que devemos denunciar deepfakes falsos que encontramos?",
         "resposta": "Verdade",
         "explicacao": "Sim! Denunciar é uma forma de combater a desinformação."},
        {"turma": "8º Ano - Visitante", "categoria": "fake",
         "pergunta": "É verdade que toda IA é deepfake?",
         "resposta": "Fake",
         "explicacao": "Não! IA é uma tecnologia, deepfake é um uso específico dela."},
        
        # ========== 9º ANO ==========
        {"turma": "9º Ano - Visitante", "categoria": "fake",
         "pergunta": "É verdade que deepfakes podem ser usados em golpes financeiros?",
         "resposta": "Verdade",
         "explicacao": "Sim! Criminosos usam deepfakes para se passar por parentes e pedir dinheiro."},
        {"turma": "9º Ano - Visitante", "categoria": "fake",
         "pergunta": "É verdade que a lei brasileira já pune quem cria deepfakes para prejudicar outros?",
         "resposta": "Verdade",
         "explicacao": "Sim! Criar deepfakes para prejudicar é crime."},
        {"turma": "9º Ano - Visitante", "categoria": "fake",
         "pergunta": "É verdade que deepfakes podem influenciar eleições?",
         "resposta": "Verdade",
         "explicacao": "Sim! Deepfakes políticos são uma ameaça à democracia."},
        {"turma": "9º Ano - Visitante", "categoria": "fake",
         "pergunta": "É verdade que podemos acreditar em qualquer áudio que recebemos?",
         "resposta": "Fake",
         "explicacao": "Não! Áudios podem ser clonados por IA."},
        {"turma": "9º Ano - Visitante", "categoria": "fake",
         "pergunta": "É verdade que a educação midiática ajuda a combater deepfakes?",
         "resposta": "Verdade",
         "explicacao": "Sim! Aprender a analisar mídias é essencial."},
    ]

    # ========== 🧠 INTELIGÊNCIA ARTIFICIAL ==========
    perguntas_ia = [
        # ========== 6º ANO ==========
        {"turma": "6º Ano - Anfitrião", "categoria": "fake",
         "pergunta": "É verdade que Inteligência Artificial (IA) é uma tecnologia que faz máquinas aprenderem?",
         "resposta": "Verdade",
         "explicacao": "Sim! IA é a capacidade de máquinas aprenderem e tomarem decisões."},
        {"turma": "6º Ano - Anfitrião", "categoria": "fake",
         "pergunta": "É verdade que a IA é um robô que pensa como um humano?",
         "resposta": "Fake",
         "explicacao": "Não! IA é um software, não um robô físico."},
        {"turma": "6º Ano - Anfitrião", "categoria": "fake",
         "pergunta": "É verdade que a IA está presente em celulares e assistentes virtuais?",
         "resposta": "Verdade",
         "explicacao": "Sim! Alexa, Siri e Google Assistente usam IA."},
        {"turma": "6º Ano - Anfitrião", "categoria": "fake",
         "pergunta": "É verdade que a IA sempre dá respostas corretas?",
         "resposta": "Fake",
         "explicacao": "Não! IA pode errar e dar informações falsas."},
        {"turma": "6º Ano - Anfitrião", "categoria": "fake",
         "pergunta": "É verdade que devemos verificar as informações que a IA nos dá?",
         "resposta": "Verdade",
         "explicacao": "Sim! Sempre verifique as informações!"},
        
        # ========== 7º ANO ==========
        {"turma": "7º Ano - Visitante", "categoria": "fake",
         "pergunta": "É verdade que a IA pode aprender com os dados que recebe?",
         "resposta": "Verdade",
         "explicacao": "Sim! IA aprende com dados e melhora com o tempo."},
        {"turma": "7º Ano - Visitante", "categoria": "fake",
         "pergunta": "É verdade que a IA é sempre neutra e sem preconceitos?",
         "resposta": "Fake",
         "explicacao": "Não! Se os dados forem preconceituosos, a IA também será."},
        {"turma": "7º Ano - Visitante", "categoria": "fake",
         "pergunta": "É verdade que a IA pode ajudar a resolver problemas sociais?",
         "resposta": "Verdade",
         "explicacao": "Sim! IA pode ajudar na saúde, educação e meio ambiente."},
        {"turma": "7º Ano - Visitante", "categoria": "fake",
         "pergunta": "É verdade que a IA pode substituir totalmente os humanos?",
         "resposta": "Fake",
         "explicacao": "Não! IA complementa, mas não substitui os humanos."},
        {"turma": "7º Ano - Visitante", "categoria": "fake",
         "pergunta": "É verdade que devemos usar a IA com responsabilidade?",
         "resposta": "Verdade",
         "explicacao": "Sim! Ética e responsabilidade são fundamentais."},
        
        # ========== 8º ANO ==========
        {"turma": "8º Ano - Visitante", "categoria": "fake",
         "pergunta": "É verdade que a IA pode criar textos, imagens e vídeos?",
         "resposta": "Verdade",
         "explicacao": "Sim! ChatGPT, DALL-E e outras IAs criam conteúdo."},
        {"turma": "8º Ano - Visitante", "categoria": "fake",
         "pergunta": "É verdade que a IA pode ser usada para espalhar fake news?",
         "resposta": "Verdade",
         "explicacao": "Sim! IAs podem criar textos e imagens falsas em massa."},
        {"turma": "8º Ano - Visitante", "categoria": "fake",
         "pergunta": "É verdade que toda IA é confiável?",
         "resposta": "Fake",
         "explicacao": "Não! É preciso verificar as informações geradas por IA."},
        {"turma": "8º Ano - Visitante", "categoria": "fake",
         "pergunta": "É verdade que devemos citar quando usamos IA para criar algo?",
         "resposta": "Verdade",
         "explicacao": "Sim! Transparência é fundamental."},
        {"turma": "8º Ano - Visitante", "categoria": "fake",
         "pergunta": "É verdade que a IA pode ser usada para o bem e para o mal?",
         "resposta": "Verdade",
         "explicacao": "Sim! Depende de como usamos."},
        
        # ========== 9º ANO ==========
        {"turma": "9º Ano - Visitante", "categoria": "fake",
         "pergunta": "É verdade que a IA pode tomar decisões sem intervenção humana?",
         "resposta": "Verdade",
         "explicacao": "Sim! Mas é preciso ter ética e supervisão."},
        {"turma": "9º Ano - Visitante", "categoria": "fake",
         "pergunta": "É verdade que a IA pode ser usada em armas autônomas?",
         "resposta": "Verdade",
         "explicacao": "Sim! E isso é um tema ético muito debatido."},
        {"turma": "9º Ano - Visitante", "categoria": "fake",
         "pergunta": "É verdade que a IA pode substituir empregos?",
         "resposta": "Verdade",
         "explicacao": "Sim! Mas também cria novas profissões."},
        {"turma": "9º Ano - Visitante", "categoria": "fake",
         "pergunta": "É verdade que a IA é sempre segura e sem riscos?",
         "resposta": "Fake",
         "explicacao": "Não! IA pode ter vieses, erros e ser usada para o mal."},
        {"turma": "9º Ano - Visitante", "categoria": "fake",
         "pergunta": "É verdade que precisamos de leis para regular a IA?",
         "resposta": "Verdade",
         "explicacao": "Sim! A regulação da IA é essencial para proteger as pessoas."},
    ]

    # ========== JUNTAR TUDO ==========
    todas = (
        perguntas_fake_cidadania + 
        perguntas_mat_fake + 
        perguntas_inter +
        perguntas_cultura_digital +
        perguntas_responsabilidade +
        perguntas_deepfake +
        perguntas_ia
    )
    
    # ========== INSERIR NO BANCO ==========
    conn = get_connection()
    cursor = conn.cursor()
    inseridas = 0
    
    for p in todas:
        cursor.execute("""
            SELECT id FROM questoes 
            WHERE pergunta = ? AND turma = ?
        """, (p['pergunta'], p['turma']))
        
        if cursor.fetchone() is None:
            cursor.execute("""
                INSERT INTO questoes 
                (turma, categoria, pergunta, resposta, opcao1, opcao2, opcao3, explicacao)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                p['turma'],
                p['categoria'],
                p['pergunta'],
                p.get('resposta', ''),
                p.get('opcao1'),
                p.get('opcao2'),
                p.get('opcao3'),
                p.get('explicacao', '')
            ))
            inseridas += 1
    
    conn.commit()
    conn.close()
    print(f"✅ {inseridas} perguntas inseridas nas categorias separadas!")
    return inseridas


# ========== BUSCAR PERGUNTAS POR CATEGORIA ==========
def buscar_questoes_por_categoria(turma, categoria):
    """Busca questões embaralhadas de uma categoria específica"""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT * FROM questoes 
        WHERE turma = ? AND categoria = ?
        ORDER BY RANDOM()
    """, (turma, categoria))
    questoes = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return questoes

# ============================================================
# 🧠 PENSAMENTO CRÍTICO
# ============================================================
perguntas_critico = [
    # ========== 6º ANO ==========
    {"turma": "6º Ano - Anfitrião", "categoria": "fake",
     "pergunta": "Você viu uma notícia que diz: 'Cientistas descobrem que chocolate cura câncer'. O que fazer?",
     "resposta": "Fake",
     "explicacao": "Pensamento crítico é questionar antes de acreditar. Verifique a fonte!"},
    {"turma": "6º Ano - Anfitrião", "categoria": "fake",
     "pergunta": "É verdade que devemos acreditar em tudo que nossos amigos enviam?",
     "resposta": "Fake",
     "explicacao": "Não! Amigos podem repassar fake news sem saber."},
    {"turma": "6º Ano - Anfitrião", "categoria": "fake",
     "pergunta": "É verdade que precisamos questionar as informações que recebemos?",
     "resposta": "Verdade",
     "explicacao": "Sim! Questionar é o primeiro passo do pensamento crítico."},
    {"turma": "6º Ano - Anfitrião", "categoria": "fake",
     "pergunta": "É verdade que manchetes exageradas sempre são verdadeiras?",
     "resposta": "Fake",
     "explicacao": "Não! Manchetes exageradas são táticas de clickbait."},
    {"turma": "6º Ano - Anfitrião", "categoria": "fake",
     "pergunta": "É verdade que devemos comparar notícias de fontes diferentes?",
     "resposta": "Verdade",
     "explicacao": "Sim! Comparar fontes ajuda a confirmar a verdade."},
    
    # ========== 7º ANO ==========
    {"turma": "7º Ano - Visitante", "categoria": "fake",
     "pergunta": "É verdade que toda notícia que viraliza é verdadeira?",
     "resposta": "Fake",
     "explicacao": "Não! Viralizar não significa que é verdade."},
    {"turma": "7º Ano - Visitante", "categoria": "fake",
     "pergunta": "É verdade que devemos analisar quem escreveu a notícia antes de acreditar?",
     "resposta": "Verdade",
     "explicacao": "Sim! Analisar o autor é fundamental."},
    {"turma": "7º Ano - Visitante", "categoria": "fake",
     "pergunta": "É verdade que toda notícia com muitas curtidas é confiável?",
     "resposta": "Fake",
     "explicacao": "Não! Curtidas não são prova de verdade."},
    {"turma": "7º Ano - Visitante", "categoria": "fake",
     "pergunta": "É verdade que precisamos desconfiar de notícias que nos deixam com raiva?",
     "resposta": "Verdade",
     "explicacao": "Sim! Fake news exploram emoções fortes."},
    {"turma": "7º Ano - Visitante", "categoria": "fake",
     "pergunta": "É verdade que podemos confiar em tudo que está na internet?",
     "resposta": "Fake",
     "explicacao": "Não! Qualquer pessoa pode publicar qualquer coisa."},
    
    # ========== 8º ANO ==========
    {"turma": "8º Ano - Visitante", "categoria": "fake",
     "pergunta": "É verdade que devemos buscar a fonte original de uma notícia?",
     "resposta": "Verdade",
     "explicacao": "Sim! A fonte original é a mais confiável."},
    {"turma": "8º Ano - Visitante", "categoria": "fake",
     "pergunta": "É verdade que toda notícia que concorda com nossa opinião é verdadeira?",
     "resposta": "Fake",
     "explicacao": "Não! Isso é o viés de confirmação."},
    {"turma": "8º Ano - Visitante", "categoria": "fake",
     "pergunta": "É verdade que devemos verificar a data da notícia?",
     "resposta": "Verdade",
     "explicacao": "Sim! Notícias antigas podem ser recicladas."},
    {"turma": "8º Ano - Visitante", "categoria": "fake",
     "pergunta": "É verdade que toda notícia com foto é verdadeira?",
     "resposta": "Fake",
     "explicacao": "Não! Fotos podem ser editadas ou tiradas de contexto."},
    {"turma": "8º Ano - Visitante", "categoria": "fake",
     "pergunta": "É verdade que devemos questionar nossos próprios preconceitos?",
     "resposta": "Verdade",
     "explicacao": "Sim! Questionar preconceitos é pensamento crítico."},
    
    # ========== 9º ANO ==========
    {"turma": "9º Ano - Visitante", "categoria": "fake",
     "pergunta": "É verdade que devemos analisar múltiplas perspectivas antes de formar opinião?",
     "resposta": "Verdade",
     "explicacao": "Sim! Múltiplas perspectivas enriquecem o pensamento crítico."},
    {"turma": "9º Ano - Visitante", "categoria": "fake",
     "pergunta": "É verdade que toda notícia de site desconhecido é fake?",
     "resposta": "Fake",
     "explicacao": "Não! Mas é preciso verificar a credibilidade do site."},
    {"turma": "9º Ano - Visitante", "categoria": "fake",
     "pergunta": "É verdade que devemos identificar nossos vieses ao analisar notícias?",
     "resposta": "Verdade",
     "explicacao": "Sim! Reconhecer vieses é fundamental."},
    {"turma": "9º Ano - Visitante", "categoria": "fake",
     "pergunta": "É verdade que toda notícia que nos deixa com raiva é fake?",
     "resposta": "Fake",
     "explicacao": "Não! Mas fake news exploram emoções fortes."},
    {"turma": "9º Ano - Visitante", "categoria": "fake",
     "pergunta": "É verdade que o pensamento crítico ajuda a combater a desinformação?",
     "resposta": "Verdade",
     "explicacao": "Sim! Pensar criticamente é a melhor defesa."},
]

# ============================================================
# 🔬 PENSAMENTO CIENTÍFICO
# ============================================================
perguntas_cientifico = [
    # ========== 6º ANO ==========
    {"turma": "6º Ano - Anfitrião", "categoria": "fake",
     "pergunta": "Como você pode COMPROVAR se uma notícia é verdadeira?",
     "resposta": "Verdade",
     "explicacao": "Investigando, testando e comprovando em fontes confiáveis."},
    {"turma": "6º Ano - Anfitrião", "categoria": "fake",
     "pergunta": "É verdade que devemos testar nossas hipóteses antes de acreditar?",
     "resposta": "Verdade",
     "explicacao": "Sim! O método científico começa com hipóteses."},
    {"turma": "6º Ano - Anfitrião", "categoria": "fake",
     "pergunta": "É verdade que toda opinião é científica?",
     "resposta": "Fake",
     "explicacao": "Não! Opinião não é ciência. Ciência precisa de evidências."},
    {"turma": "6º Ano - Anfitrião", "categoria": "fake",
     "pergunta": "É verdade que devemos buscar evidências antes de acreditar?",
     "resposta": "Verdade",
     "explicacao": "Sim! Evidências são a base do pensamento científico."},
    {"turma": "6º Ano - Anfitrião", "categoria": "fake",
     "pergunta": "É verdade que podemos acreditar em tudo que um cientista diz?",
     "resposta": "Fake",
     "explicacao": "Não! A ciência é feita de testes e comprovações."},
    
    # ========== 7º ANO ==========
    {"turma": "7º Ano - Visitante", "categoria": "fake",
     "pergunta": "É verdade que o método científico começa com uma pergunta?",
     "resposta": "Verdade",
     "explicacao": "Sim! Toda pesquisa começa com uma pergunta."},
    {"turma": "7º Ano - Visitante", "categoria": "fake",
     "pergunta": "É verdade que toda pesquisa científica é definitiva?",
     "resposta": "Fake",
     "explicacao": "Não! A ciência está sempre em evolução."},
    {"turma": "7º Ano - Visitante", "categoria": "fake",
     "pergunta": "É verdade que devemos verificar a metodologia de uma pesquisa?",
     "resposta": "Verdade",
     "explicacao": "Sim! A metodologia mostra como a pesquisa foi feita."},
    {"turma": "7º Ano - Visitante", "categoria": "fake",
     "pergunta": "É verdade que toda pesquisa com muitos participantes é confiável?",
     "resposta": "Fake",
     "explicacao": "Não! A qualidade da metodologia importa mais que a quantidade."},
    {"turma": "7º Ano - Visitante", "categoria": "fake",
     "pergunta": "É verdade que devemos replicar experimentos para confirmar resultados?",
     "resposta": "Verdade",
     "explicacao": "Sim! A replicação é fundamental na ciência."},
    
    # ========== 8º ANO ==========
    {"turma": "8º Ano - Visitante", "categoria": "fake",
     "pergunta": "É verdade que a ciência busca explicações naturais para fenômenos?",
     "resposta": "Verdade",
     "explicacao": "Sim! A ciência busca explicações baseadas em evidências."},
    {"turma": "8º Ano - Visitante", "categoria": "fake",
     "pergunta": "É verdade que toda teoria científica é uma opinião?",
     "resposta": "Fake",
     "explicacao": "Não! Teoria científica é baseada em evidências."},
    {"turma": "8º Ano - Visitante", "categoria": "fake",
     "pergunta": "É verdade que devemos avaliar a credibilidade das fontes científicas?",
     "resposta": "Verdade",
     "explicacao": "Sim! Fontes confiáveis são essenciais."},
    {"turma": "8º Ano - Visitante", "categoria": "fake",
     "pergunta": "É verdade que toda descoberta científica é imutável?",
     "resposta": "Fake",
     "explicacao": "Não! A ciência evolui com novas descobertas."},
    {"turma": "8º Ano - Visitante", "categoria": "fake",
     "pergunta": "É verdade que devemos questionar resultados sem evidências?",
     "resposta": "Verdade",
     "explicacao": "Sim! Questionar é parte do método científico."},
    
    # ========== 9º ANO ==========
    {"turma": "9º Ano - Visitante", "categoria": "fake",
     "pergunta": "É verdade que a ciência é um processo de construção coletiva?",
     "resposta": "Verdade",
     "explicacao": "Sim! A ciência é feita por muitas pessoas."},
    {"turma": "9º Ano - Visitante", "categoria": "fake",
     "pergunta": "É verdade que toda pesquisa científica é neutra?",
     "resposta": "Fake",
     "explicacao": "Não! Pesquisas podem ter interesses por trás."},
    {"turma": "9º Ano - Visitante", "categoria": "fake",
     "pergunta": "É verdade que devemos avaliar conflitos de interesse em pesquisas?",
     "resposta": "Verdade",
     "explicacao": "Sim! Conflitos de interesse podem influenciar resultados."},
    {"turma": "9º Ano - Visitante", "categoria": "fake",
     "pergunta": "É verdade que toda notícia científica é confiável?",
     "resposta": "Fake",
     "explicacao": "Não! Notícias podem distorcer pesquisas científicas."},
    {"turma": "9º Ano - Visitante", "categoria": "fake",
     "pergunta": "É verdade que o ceticismo científico ajuda a combater fake news?",
     "resposta": "Verdade",
     "explicacao": "Sim! Ceticismo é a base do pensamento científico."},
]

# ============================================================
# 🎨 PENSAMENTO CRIATIVO
# ============================================================
perguntas_criativo = [
    # ========== 6º ANO ==========
    {"turma": "6º Ano - Anfitrião", "categoria": "etica",
     "pergunta": "Como você pode combater fake news na sua escola?",
     "opcao1": "Reclamar com o professor",
     "opcao2": "Criar uma campanha com cartazes, vídeos e memes",
     "opcao3": "Ignorar",
     "correta": "Criar uma campanha com cartazes, vídeos e memes",
     "explicacao": "Pensamento criativo é buscar soluções inovadoras!"},
    {"turma": "6º Ano - Anfitrião", "categoria": "etica",
     "pergunta": "Como você pode ajudar um colega que sofre cyberbullying?",
     "opcao1": "Rir também",
     "opcao2": "Criar um grupo de apoio e denunciar",
     "opcao3": "Ignorar",
     "correta": "Criar um grupo de apoio e denunciar",
     "explicacao": "Criatividade também é ajudar o próximo!"},
    {"turma": "6º Ano - Anfitrião", "categoria": "etica",
     "pergunta": "Como você pode ensinar seus pais sobre fake news?",
     "opcao1": "Não fazer nada",
     "opcao2": "Criar um jogo ou apresentação divertida",
     "opcao3": "Reclamar",
     "correta": "Criar um jogo ou apresentação divertida",
     "explicacao": "Pensamento criativo é ensinar de forma inovadora!"},
    {"turma": "6º Ano - Anfitrião", "categoria": "etica",
     "pergunta": "Como você pode usar a tecnologia para o bem?",
     "opcao1": "Só jogar",
     "opcao2": "Criar conteúdo educativo e ajudar pessoas",
     "opcao3": "Não usar",
     "correta": "Criar conteúdo educativo e ajudar pessoas",
     "explicacao": "Criatividade é usar a tecnologia para transformar!"},
    {"turma": "6º Ano - Anfitrião", "categoria": "etica",
     "pergunta": "Como você pode deixar a internet um lugar melhor?",
     "opcao1": "Só reclamar",
     "opcao2": "Compartilhar conteúdo positivo e denunciar o ruim",
     "opcao3": "Sair das redes",
     "correta": "Compartilhar conteúdo positivo e denunciar o ruim",
     "explicacao": "Criatividade é agir para melhorar!"},
    
    # ========== 7º ANO ==========
    {"turma": "7º Ano - Visitante", "categoria": "etica",
     "pergunta": "Como você pode criar uma campanha contra cyberbullying?",
     "opcao1": "Fazer um cartaz simples",
     "opcao2": "Criar vídeos, memes e hashtags",
     "opcao3": "Não fazer nada",
     "correta": "Criar vídeos, memes e hashtags",
     "explicacao": "Criatividade é usar várias ferramentas!"},
    {"turma": "7º Ano - Visitante", "categoria": "etica",
     "pergunta": "Como você pode ajudar a combater fake news na sua comunidade?",
     "opcao1": "Ignorar",
     "opcao2": "Criar um grupo de verificação de fatos",
     "opcao3": "Só reclamar",
     "correta": "Criar um grupo de verificação de fatos",
     "explicacao": "Criatividade é organizar soluções!"},
    {"turma": "7º Ano - Visitante", "categoria": "etica",
     "pergunta": "Como você pode ensinar cidadania digital para crianças menores?",
     "opcao1": "Dar uma palestra chata",
     "opcao2": "Criar histórias, jogos e quadrinhos",
     "opcao3": "Não ensinar",
     "correta": "Criar histórias, jogos e quadrinhos",
     "explicacao": "Criatividade é adaptar a linguagem!"},
    {"turma": "7º Ano - Visitante", "categoria": "etica",
     "pergunta": "Como você pode usar as redes sociais para o bem?",
     "opcao1": "Só postar fotos",
     "opcao2": "Criar conteúdo educativo e inspirador",
     "opcao3": "Não usar",
     "correta": "Criar conteúdo educativo e inspirador",
     "explicacao": "Criatividade é inspirar pessoas!"},
    {"turma": "7º Ano - Visitante", "categoria": "etica",
     "pergunta": "Como você pode resolver um conflito online de forma criativa?",
     "opcao1": "Xingar de volta",
     "opcao2": "Conversar com respeito e buscar ajuda",
     "opcao3": "Sair do grupo",
     "correta": "Conversar com respeito e buscar ajuda",
     "explicacao": "Criatividade é resolver conflitos com diálogo!"},
    
    # ========== 8º ANO ==========
    {"turma": "8º Ano - Visitante", "categoria": "etica",
     "pergunta": "Como você pode criar uma campanha de conscientização digital?",
     "opcao1": "Fazer um cartaz",
     "opcao2": "Criar uma campanha multiplataforma com vídeos, podcasts e posts",
     "opcao3": "Não fazer nada",
     "correta": "Criar uma campanha multiplataforma com vídeos, podcasts e posts",
     "explicacao": "Criatividade é usar várias mídias!"},
    {"turma": "8º Ano - Visitante", "categoria": "etica",
     "pergunta": "Como você pode ajudar a tornar a internet mais segura?",
     "opcao1": "Reclamar",
     "opcao2": "Criar conteúdo sobre segurança digital e denunciar crimes",
     "opcao3": "Não usar",
     "correta": "Criar conteúdo sobre segurança digital e denunciar crimes",
     "explicacao": "Criatividade é proteger os outros!"},
    {"turma": "8º Ano - Visitante", "categoria": "etica",
     "pergunta": "Como você pode usar a tecnologia para ajudar pessoas?",
     "opcao1": "Só jogar",
     "opcao2": "Criar aplicativos ou projetos sociais",
     "opcao3": "Não usar",
     "correta": "Criar aplicativos ou projetos sociais",
     "explicacao": "Criatividade é transformar vidas!"},
    {"turma": "8º Ano - Visitante", "categoria": "etica",
     "pergunta": "Como você pode combater o discurso de ódio online?",
     "opcao1": "Responder com ódio",
     "opcao2": "Criar campanhas de amor e denunciar",
     "opcao3": "Ignorar",
     "correta": "Criar campanhas de amor e denunciar",
     "explicacao": "Criatividade é espalhar o bem!"},
    {"turma": "8º Ano - Visitante", "categoria": "etica",
     "pergunta": "Como você pode ensinar cidadania digital de forma criativa?",
     "opcao1": "Dar uma palestra",
     "opcao2": "Criar um jogo educativo ou uma peça de teatro",
     "opcao3": "Não ensinar",
     "correta": "Criar um jogo educativo ou uma peça de teatro",
     "explicacao": "Criatividade é ensinar brincando!"},
    
    # ========== 9º ANO ==========
    {"turma": "9º Ano - Visitante", "categoria": "etica",
     "pergunta": "Como você pode criar um projeto de cidadania digital?",
     "opcao1": "Fazer um cartaz",
     "opcao2": "Criar um projeto completo com pesquisa, campanha e avaliação",
     "opcao3": "Não fazer nada",
     "correta": "Criar um projeto completo com pesquisa, campanha e avaliação",
     "explicacao": "Criatividade é planejar e executar!"},
    {"turma": "9º Ano - Visitante", "categoria": "etica",
     "pergunta": "Como você pode usar a inteligência artificial para o bem?",
     "opcao1": "Só brincar",
     "opcao2": "Criar soluções para problemas sociais",
     "opcao3": "Não usar",
     "correta": "Criar soluções para problemas sociais",
     "explicacao": "Criatividade é usar a IA para transformar!"},
    {"turma": "9º Ano - Visitante", "categoria": "etica",
     "pergunta": "Como você pode combater fake news de forma inovadora?",
     "opcao1": "Reclamar",
     "opcao2": "Criar ferramentas ou campanhas de verificação",
     "opcao3": "Ignorar",
     "correta": "Criar ferramentas ou campanhas de verificação",
     "explicacao": "Criatividade é inovar na solução!"},
    {"turma": "9º Ano - Visitante", "categoria": "etica",
     "pergunta": "Como você pode inspirar outras pessoas a serem cidadãos digitais?",
     "opcao1": "Dar lição de moral",
     "opcao2": "Ser exemplo e criar conteúdo inspirador",
     "opcao3": "Não fazer nada",
     "correta": "Ser exemplo e criar conteúdo inspirador",
     "explicacao": "Criatividade é inspirar pelo exemplo!"},
    {"turma": "9º Ano - Visitante", "categoria": "etica",
     "pergunta": "Como você pode deixar um legado positivo na internet?",
     "opcao1": "Postar qualquer coisa",
     "opcao2": "Criar conteúdo que ajude e inspire pessoas",
     "opcao3": "Não se importar",
     "correta": "Criar conteúdo que ajude e inspire pessoas",
     "explicacao": "Criatividade é deixar o mundo melhor!"},
]

# ============================================================
# 📋 FUNÇÕES DE CASOS PBL
# ============================================================

def inserir_casos_pbl():
    """Insere os casos PBL no banco"""
    conn = get_connection()
    cursor = conn.cursor()
    
    casos = [
        # ========== CASO 1: FAKE NEWS ==========
        {
            "titulo": "Fake News sobre a Merenda Escolar",
            "descricao": "Uma mensagem no WhatsApp diz que a merenda da escola está vencida. Em 2 dias, a mensagem foi compartilhada 120 vezes. Cada compartilhamento atinge 8 pessoas. 300 pessoas curtiram a mensagem.",
            "tipo": "fake_news",
            "dados": "compartilhamentos=120;alcance_por_compartilhamento=8;curtidas=300",
            "solucao_esperada": "Verificar a fonte, avisar a direção, criar comunicado oficial",
            "pontos": 5
        },
        
        # ========== CASO 2: CYBERBULLYING ==========
        {
            "titulo": "Cyberbullying no Grupo da Turma",
            "descricao": "Um aluno criou um grupo para zombar de um colega. 15 alunos participaram. Cada um enviou 10 mensagens ofensivas. O colega ficou triste e parou de vir à escola.",
            "tipo": "cyberbullying",
            "dados": "alunos_participantes=15;mensagens_por_aluno=10",
            "solucao_esperada": "Denunciar, apoiar o colega, conversar com adultos, denunciar o grupo",
            "pontos": 5
        },
        
        # ========== CASO 3: DISCURSO DE ÓDIO ==========
        {
            "titulo": "Discurso de Ódio nas Redes Sociais",
            "descricao": "Um comentário racista foi postado em uma rede social. 500 pessoas viram, 200 compartilharam e 50 denunciaram. A vítima ficou abalada.",
            "tipo": "discurso_odio",
            "dados": "visualizacoes=500;compartilhamentos=200;denuncias=50",
            "solucao_esperada": "Denunciar, apoiar a vítima, criar campanha de conscientização",
            "pontos": 5
        },
        
        # ========== CASO 4: CULTURA DO CANCELAMENTO ==========
        {
            "titulo": "Cultura do Cancelamento",
            "descricao": "Uma aluna postou uma opinião polêmica. Em 1 dia, 200 pessoas comentaram, 100 xingaram e 50 defenderam. A aluna apagou a conta.",
            "tipo": "cancelamento",
            "dados": "comentarios=200;xingamentos=100;defesas=50",
            "solucao_esperada": "Debater com respeito, não cancelar, buscar diálogo",
            "pontos": 5
        },
        
        # ========== CASO 5: DEEPFAKE ==========
        {
            "titulo": "Deepfake de um Colega",
            "descricao": "Um aluno criou um vídeo deepfake de um colega dizendo algo que ele nunca disse. O vídeo teve 1.000 visualizações em 3 horas. 300 pessoas compartilharam.",
            "tipo": "deepfake",
            "dados": "visualizacoes=1000;compartilhamentos=300;tempo_horas=3",
            "solucao_esperada": "Denunciar, avisar a vítima, procurar a direção, denunciar à polícia",
            "pontos": 5
        },
        
        # ========== CASO 6: EFEITO BOLHA ==========
        {
            "titulo": "Efeito Bolha nas Redes",
            "descricao": "Um aluno só vê conteúdo sobre futebol. O algoritmo mostra 90% de conteúdo sobre futebol e 10% de outros assuntos. Ele acha que todos gostam de futebol.",
            "tipo": "efeito_bolha",
            "dados": "conteudo_futebol=90;conteudo_outros=10",
            "solucao_esperada": "Seguir pessoas diferentes, buscar outras fontes, sair da bolha",
            "pontos": 5
        },
    ]
    
    inseridos = 0
    for caso in casos:
        cursor.execute("""
            SELECT id FROM casos_pbl WHERE titulo = ?
        """, (caso['titulo'],))
        
        if cursor.fetchone() is None:
            cursor.execute("""
                INSERT INTO casos_pbl (titulo, descricao, tipo, dados, solucao_esperada, pontos)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (
                caso['titulo'],
                caso['descricao'],
                caso['tipo'],
                caso['dados'],
                caso['solucao_esperada'],
                caso['pontos']
            ))
            inseridos += 1
    
    conn.commit()
    conn.close()
    print(f"✅ {inseridos} casos PBL inseridos!")
    return inseridos


def listar_casos_pbl():
    """Lista todos os casos PBL"""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM casos_pbl ORDER BY id")
    casos = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return casos


def buscar_caso_pbl(caso_id):
    """Busca um caso PBL específico"""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM casos_pbl WHERE id = ?", (caso_id,))
    caso = cursor.fetchone()
    conn.close()
    return dict(caso) if caso else None

def salvar_resposta_pbl(aluno_nome, aluno_turma, caso_titulo, resposta):
    """Salva a resposta do aluno no banco"""
    from datetime import datetime
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO respostas_pbl (aluno_nome, aluno_turma, caso_titulo, resposta, data)
        VALUES (?, ?, ?, ?, ?)
    """, (
        aluno_nome,
        aluno_turma,
        caso_titulo,
        resposta,
        datetime.now().strftime("%Y-%m-%d %H:%M")
    ))
    conn.commit()
    conn.close()


def listar_respostas_pbl():
    """Lista todas as respostas PBL"""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM respostas_pbl ORDER BY data DESC")
    respostas = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return respostas


def listar_respostas_pbl_aluno(aluno_nome, aluno_turma):
    """Lista as respostas de um aluno específico"""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT * FROM respostas_pbl 
        WHERE aluno_nome = ? AND aluno_turma = ?
        ORDER BY data DESC
    """, (aluno_nome, aluno_turma))
    respostas = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return respostas

def excluir_resposta_pbl(resposta_id):
    """Exclui uma resposta PBL específica"""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM respostas_pbl WHERE id = ?", (resposta_id,))
    conn.commit()
    conn.close()


def excluir_respostas_pbl_por_turma(turma):
    """Exclui todas as respostas PBL de uma turma"""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM respostas_pbl WHERE aluno_turma = ?", (turma,))
    linhas = cursor.rowcount
    conn.commit()
    conn.close()
    return linhas


def excluir_todas_respostas_pbl():
    """Exclui TODAS as respostas PBL"""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM respostas_pbl")
    linhas = cursor.rowcount
    conn.commit()
    conn.close()
    return linhas

# ============================================================
# 📝 FUNÇÕES DE ALGORITMOS
# ============================================================

def salvar_algoritmo(aluno_nome, aluno_turma, passos):
    """Salva o algoritmo do aluno no banco"""
    from datetime import datetime
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO algoritmos (aluno_nome, aluno_turma, passos, data)
        VALUES (?, ?, ?, ?)
    """, (
        aluno_nome,
        aluno_turma,
        passos,
        datetime.now().strftime("%Y-%m-%d %H:%M")
    ))
    conn.commit()
    conn.close()


def listar_algoritmos():
    """Lista todos os algoritmos"""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM algoritmos ORDER BY data DESC")
    algoritmos = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return algoritmos


def listar_algoritmos_aluno(aluno_nome, aluno_turma):
    """Lista os algoritmos de um aluno"""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT * FROM algoritmos 
        WHERE aluno_nome = ? AND aluno_turma = ?
        ORDER BY data DESC
    """, (aluno_nome, aluno_turma))
    algoritmos = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return algoritmos


def excluir_algoritmo(algoritmo_id):
    """Exclui um algoritmo"""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM algoritmos WHERE id = ?", (algoritmo_id,))
    conn.commit()
    conn.close()


def excluir_todos_algoritmos():
    """Exclui TODOS os algoritmos"""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM algoritmos")
    linhas = cursor.rowcount
    conn.commit()
    conn.close()
    return linhas

# ============================================================
# 🧠 FUNÇÕES DE DISSECAR ALGORITMO (CAIXA-PRETA)
# ============================================================

def salvar_dissecacao(aluno_nome, aluno_turma, curtidas, conclusao):
    """Salva a dissecação do algoritmo"""
    from datetime import datetime
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO disseca_algoritmo (aluno_nome, aluno_turma, curtidas, conclusao, data)
        VALUES (?, ?, ?, ?, ?)
    """, (
        aluno_nome,
        aluno_turma,
        str(curtidas),
        conclusao,
        datetime.now().strftime("%Y-%m-%d %H:%M")
    ))
    conn.commit()
    conn.close()

def listar_dissecacoes():
    """Lista todas as dissecações"""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM disseca_algoritmo ORDER BY data DESC")
    disseca = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return disseca


def listar_dissecacoes_aluno(aluno_nome, aluno_turma):
    """Lista as dissecações de um aluno"""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT * FROM disseca_algoritmo 
        WHERE aluno_nome = ? AND aluno_turma = ?
        ORDER BY data DESC
    """, (aluno_nome, aluno_turma))
    disseca = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return disseca


def excluir_dissecacao(dissecacao_id):
    """Exclui uma dissecação"""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM disseca_algoritmo WHERE id = ?", (dissecacao_id,))
    conn.commit()
    conn.close()

# ============================================================
# ⚖️ FUNÇÕES DE DEBATE (Discurso de Ódio vs. Liberdade)
# ============================================================

def salvar_debate(aluno_nome, aluno_turma, frase, classificacao, justificativa):
    """Salva a classificação do aluno no banco"""
    from datetime import datetime
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO debates (aluno_nome, aluno_turma, frase, classificacao, justificativa, data)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (
        aluno_nome,
        aluno_turma,
        frase,
        classificacao,
        justificativa,
        datetime.now().strftime("%Y-%m-%d %H:%M")
    ))
    conn.commit()
    conn.close()


def listar_debates():
    """Lista todos os debates"""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM debates ORDER BY data DESC")
    debates = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return debates


def listar_debates_aluno(aluno_nome, aluno_turma):
    """Lista os debates de um aluno"""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT * FROM debates 
        WHERE aluno_nome = ? AND aluno_turma = ?
        ORDER BY data DESC
    """, (aluno_nome, aluno_turma))
    debates = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return debates


def contar_debates_por_frase(frase):
    """Conta quantos alunos classificaram cada frase"""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT classificacao, COUNT(*) as total 
        FROM debates 
        WHERE frase = ?
        GROUP BY classificacao
    """, (frase,))
    resultado = {row['classificacao']: row['total'] for row in cursor.fetchall()}
    conn.close()
    return resultado


def excluir_debate(debate_id):
    """Exclui um debate"""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM debates WHERE id = ?", (debate_id,))
    conn.commit()
    conn.close()

# ============================================================
# 🅴 FUNÇÕES DE CULTURA DO CANCELAMENTO
# ============================================================

def salvar_cancelamento(aluno_nome, aluno_turma, caso_titulo, opiniao):
    """Salva a opinião do aluno sobre o caso"""
    from datetime import datetime
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO cancelamento (aluno_nome, aluno_turma, caso_titulo, opiniao, data)
        VALUES (?, ?, ?, ?, ?)
    """, (
        aluno_nome,
        aluno_turma,
        caso_titulo,
        opiniao,
        datetime.now().strftime("%Y-%m-%d %H:%M")
    ))
    conn.commit()
    conn.close()


def listar_cancelamentos():
    """Lista todos os cancelamentos"""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM cancelamento ORDER BY data DESC")
    cancelamentos = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return cancelamentos


def listar_cancelamentos_aluno(aluno_nome, aluno_turma):
    """Lista os cancelamentos de um aluno"""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT * FROM cancelamento 
        WHERE aluno_nome = ? AND aluno_turma = ?
        ORDER BY data DESC
    """, (aluno_nome, aluno_turma))
    cancelamentos = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return cancelamentos


def excluir_cancelamento(cancelamento_id):
    """Exclui um cancelamento"""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM cancelamento WHERE id = ?", (cancelamento_id,))
    conn.commit()
    conn.close()

# ============================================================
# 🅸 FUNÇÕES DE JÚRI SIMULADO
# ============================================================

def salvar_juri(aluno_nome, aluno_turma, caso_titulo, papel, argumento):
    """Salva o argumento do aluno no júri"""
    from datetime import datetime
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO juri_simulado (aluno_nome, aluno_turma, caso_titulo, papel, argumento, data)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (
        aluno_nome,
        aluno_turma,
        caso_titulo,
        papel,
        argumento,
        datetime.now().strftime("%Y-%m-%d %H:%M")
    ))
    conn.commit()
    conn.close()


def listar_juri():
    """Lista todos os argumentos do júri"""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM juri_simulado ORDER BY data DESC")
    juri = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return juri


def listar_juri_aluno(aluno_nome, aluno_turma):
    """Lista os argumentos de um aluno"""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT * FROM juri_simulado 
        WHERE aluno_nome = ? AND aluno_turma = ?
        ORDER BY data DESC
    """, (aluno_nome, aluno_turma))
    juri = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return juri


def listar_juri_por_caso(caso_titulo):
    """Lista todos os argumentos de um caso"""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT * FROM juri_simulado 
        WHERE caso_titulo = ?
        ORDER BY papel, data DESC
    """, (caso_titulo,))
    juri = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return juri


def excluir_juri(juri_id):
    """Exclui um argumento do júri"""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM juri_simulado WHERE id = ?", (juri_id,))
    conn.commit()
    conn.close()

# ============================================================
# 🔄 FUNÇÃO DE ATUALIZAÇÃO DO BANCO
# ============================================================

def atualizar_banco():
    """Verifica e cria tabelas que faltam no banco"""
    conn = get_connection()
    cursor = conn.cursor()
    
    # Verificar tabelas existentes
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
    tabelas = [row[0] for row in cursor.fetchall()]
    
    # ========== TABELA JURI_SIMULADO ==========
    if 'juri_simulado' not in tabelas:
        cursor.execute("""
            CREATE TABLE juri_simulado (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                aluno_nome TEXT NOT NULL,
                aluno_turma TEXT NOT NULL,
                caso_titulo TEXT NOT NULL,
                papel TEXT NOT NULL,
                argumento TEXT NOT NULL,
                data TEXT
            )
        """)
        print("✅ Tabela juri_simulado criada!")

    # ========== TABELA DADOS_DESINFORMACAO ==========
    if 'dados_desinformacao' not in tabelas:
        cursor.execute("""
            CREATE TABLE dados_desinformacao (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                aluno_nome TEXT NOT NULL,
                aluno_turma TEXT NOT NULL,
                analise TEXT NOT NULL,
                conclusao TEXT NOT NULL,
                data TEXT
            )
        """)
        print("✅ Tabela dados_desinformacao criada!")
    
    # ========== TABELA CANCELAMENTO ==========
    if 'cancelamento' not in tabelas:
        cursor.execute("""
            CREATE TABLE cancelamento (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                aluno_nome TEXT NOT NULL,
                aluno_turma TEXT NOT NULL,
                caso_titulo TEXT NOT NULL,
                opiniao TEXT NOT NULL,
                data TEXT
            )
        """)
        print("✅ Tabela cancelamento criada!")
    
    # ========== TABELA DEBATES ==========
    if 'debates' not in tabelas:
        cursor.execute("""
            CREATE TABLE debates (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                aluno_nome TEXT NOT NULL,
                aluno_turma TEXT NOT NULL,
                frase TEXT NOT NULL,
                classificacao TEXT NOT NULL,
                justificativa TEXT NOT NULL,
                data TEXT
            )
        """)
        print("✅ Tabela debates criada!")
    
    # ========== TABELA DISSECA_ALGORITMO ==========
    if 'disseca_algoritmo' not in tabelas:
        cursor.execute("""
            CREATE TABLE disseca_algoritmo (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                aluno_nome TEXT NOT NULL,
                aluno_turma TEXT NOT NULL,
                curtidas TEXT NOT NULL,
                conclusao TEXT NOT NULL,
                data TEXT
            )
        """)
        print("✅ Tabela disseca_algoritmo criada!")
    
    # ========== TABELA ALGORITMOS ==========
    if 'algoritmos' not in tabelas:
        cursor.execute("""
            CREATE TABLE algoritmos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                aluno_nome TEXT NOT NULL,
                aluno_turma TEXT NOT NULL,
                passos TEXT NOT NULL,
                data TEXT
            )
        """)
        print("✅ Tabela algoritmos criada!")
    
    # ========== TABELA RESPOSTAS_PBL ==========
    if 'respostas_pbl' not in tabelas:
        cursor.execute("""
            CREATE TABLE respostas_pbl (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                aluno_nome TEXT NOT NULL,
                aluno_turma TEXT NOT NULL,
                caso_titulo TEXT NOT NULL,
                resposta TEXT NOT NULL,
                data TEXT
            )
        """)
        print("✅ Tabela respostas_pbl criada!")
    
    # ========== TABELA CASOS_PBL ==========
    if 'casos_pbl' not in tabelas:
        cursor.execute("""
            CREATE TABLE casos_pbl (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                titulo TEXT NOT NULL,
                descricao TEXT NOT NULL,
                tipo TEXT NOT NULL,
                dados TEXT NOT NULL,
                solucao_esperada TEXT NOT NULL,
                pontos INTEGER DEFAULT 5
            )
        """)
        print("✅ Tabela casos_pbl criada!")
    
    # ========== TABELA EQUIPES ==========
    if 'equipes' not in tabelas:
        cursor.execute("""
            CREATE TABLE equipes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT NOT NULL,
                turma TEXT NOT NULL,
                pontos INTEGER DEFAULT 0,
                data_criacao TEXT
            )
        """)
        print("✅ Tabela equipes criada!")
    
    # ========== TABELA ALUNOS_EQUIPES ==========
    if 'alunos_equipes' not in tabelas:
        cursor.execute("""
            CREATE TABLE alunos_equipes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                equipe_id INTEGER NOT NULL,
                aluno_nome TEXT NOT NULL,
                aluno_turma TEXT NOT NULL,
                FOREIGN KEY (equipe_id) REFERENCES equipes (id)
            )
        """)
        print("✅ Tabela alunos_equipes criada!")
    
    # ========== TABELA QUESTOES ==========
    if 'questoes' not in tabelas:
        cursor.execute("""
            CREATE TABLE questoes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                turma TEXT NOT NULL,
                categoria TEXT NOT NULL,
                pergunta TEXT NOT NULL,
                resposta TEXT NOT NULL,
                opcao1 TEXT,
                opcao2 TEXT,
                opcao3 TEXT,
                explicacao TEXT
            )
        """)
        print("✅ Tabela questoes criada!")
    
    # ========== TABELA ALUNOS ==========
    if 'alunos' not in tabelas:
        cursor.execute("""
            CREATE TABLE alunos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT NOT NULL,
                turma TEXT NOT NULL,
                pontos INTEGER DEFAULT 0,
                fake_acertos INTEGER DEFAULT 0,
                cyber_acertos INTEGER DEFAULT 0,
                etica_acertos INTEGER DEFAULT 0,
                total_perguntas INTEGER DEFAULT 0,
                badges TEXT DEFAULT '',
                data_cadastro DATE DEFAULT CURRENT_DATE
            )
        """)
        print("✅ Tabela alunos criada!")

    # Tabela de DADOS DA DESINFORMAÇÃO
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS dados_desinformacao (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            aluno_nome TEXT NOT NULL,
            aluno_turma TEXT NOT NULL,
            analise TEXT NOT NULL,
            conclusao TEXT NOT NULL,
            data TEXT
        )
    """)

    # ========== TABELA CAMPANHAS ==========
    if 'campanhas' not in tabelas:
        cursor.execute("""
            CREATE TABLE campanhas (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                aluno_nome TEXT NOT NULL,
                aluno_turma TEXT NOT NULL,
                titulo TEXT NOT NULL,
                tipo TEXT NOT NULL,
                publico TEXT NOT NULL,
                roteiro TEXT NOT NULL,
                divulgacao TEXT NOT NULL,
                data TEXT
            )
        """)
        print("✅ Tabela campanhas criada!")

    # Tabela de INFOGRÁFICOS
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS infograficos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            aluno_nome TEXT NOT NULL,
            aluno_turma TEXT NOT NULL,
            titulo TEXT NOT NULL,
            tema TEXT NOT NULL,
            dados TEXT NOT NULL,
            cores TEXT NOT NULL,
            icones TEXT NOT NULL,
            data TEXT
        )
    """)

    # ========== TABELA INFOGRAFICOS ==========
    if 'infograficos' not in tabelas:
        cursor.execute("""
            CREATE TABLE infograficos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                aluno_nome TEXT NOT NULL,
                aluno_turma TEXT NOT NULL,
                titulo TEXT NOT NULL,
                tema TEXT NOT NULL,
                dados TEXT NOT NULL,
                cores TEXT NOT NULL,
                icones TEXT NOT NULL,
                data TEXT
            )
        """)
        print("✅ Tabela infograficos criada!")

    # Tabela de PODCASTS
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS podcasts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            aluno_nome TEXT NOT NULL,
            aluno_turma TEXT NOT NULL,
            titulo TEXT NOT NULL,
            tema TEXT NOT NULL,
            duracao TEXT NOT NULL,
            convidado TEXT,
            roteiro TEXT NOT NULL,
            data TEXT
        )
    """)

    # ========== TABELA PODCASTS ==========
    if 'podcasts' not in tabelas:
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS podcasts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                aluno_nome TEXT NOT NULL,
                aluno_turma TEXT NOT NULL,
                titulo TEXT NOT NULL,
                tema TEXT NOT NULL,
                duracao TEXT NOT NULL,
                convidado TEXT,
                roteiro TEXT NOT NULL,
                data TEXT
            )
        """)
        print("✅ Tabela podcasts criada!")

    # ========== TABELA TURMAS ==========
    if 'turmas' not in tabelas:
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS turmas (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT NOT NULL UNIQUE
            )
        """)
        print("✅ Tabela turmas criada!")
    
    # ========== TABELA ATIVIDADES ==========
    if 'atividades' not in tabelas:
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS atividades (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                titulo TEXT NOT NULL,
                descricao TEXT,
                data TEXT NOT NULL,
                horario TEXT,
                turma TEXT,
                tipo TEXT
            )
        """)
        print("✅ Tabela atividades criada!")
    
    # ========== TABELA DESAFIOS_SEMANAIS ==========
    if 'desafios_semanais' not in tabelas:
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS desafios_semanais (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                titulo TEXT NOT NULL,
                descricao TEXT,
                categoria TEXT,
                pergunta TEXT NOT NULL,
                resposta TEXT NOT NULL,
                opcao1 TEXT,
                opcao2 TEXT,
                opcao3 TEXT,
                explicacao TEXT,
                pontos INTEGER DEFAULT 5,
                semana INTEGER,
                ano INTEGER,
                data_inicio TEXT,
                data_fim TEXT
            )
        """)
        print("✅ Tabela desafios_semanais criada!")
    
    # ========== TABELA LIVROS ==========
    if 'livros' not in tabelas:
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS livros (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                titulo TEXT NOT NULL,
                autor TEXT NOT NULL,
                categoria TEXT,
                descricao TEXT,
                link TEXT
            )
        """)
        print("✅ Tabela livros criada!")
    
    # ========== TABELA RESENHAS ==========
    if 'resenhas' not in tabelas:
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS resenhas (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                livro_id INTEGER NOT NULL,
                aluno_nome TEXT NOT NULL,
                aluno_turma TEXT NOT NULL,
                resenha TEXT NOT NULL,
                avaliacao INTEGER,
                data_resenha TEXT,
                FOREIGN KEY (livro_id) REFERENCES livros (id)
            )
        """)
        print("✅ Tabela resenhas criada!")
    
    # ========== TABELA PONTOS_EQUIPES ==========
    if 'pontos_equipes' not in tabelas:
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS pontos_equipes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                equipe_id INTEGER NOT NULL,
                pontos INTEGER NOT NULL,
                data TEXT,
                FOREIGN KEY (equipe_id) REFERENCES equipes (id)
            )
        """)
        print("✅ Tabela pontos_equipes criada!")

    # ========== TABELA QUESTIONARIO ==========
    if 'questionario' not in tabelas:
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS questionario (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                aluno_nome TEXT NOT NULL,
                aluno_turma TEXT NOT NULL,
                data TEXT NOT NULL,
                redes_sociais TEXT NOT NULL,
                fake_news TEXT NOT NULL,
                atitude_noticia TEXT NOT NULL,
                presenciou_cyber TEXT NOT NULL,
                reacao_cyber TEXT NOT NULL,
                opiniao_agressividade TEXT NOT NULL,
                atitude_cidadania TEXT NOT NULL
            )
        """)
        print("✅ Tabela questionario criada!")

    conn.commit()      
    conn.close()
    print("✅ Banco de dados atualizado!")
    
# ============================================================
# 🅷 FUNÇÕES DE DADOS DA DESINFORMAÇÃO
# ============================================================

def salvar_analise_dados(aluno_nome, aluno_turma, analise, conclusao):
    """Salva a análise do aluno"""
    from datetime import datetime
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO dados_desinformacao (aluno_nome, aluno_turma, analise, conclusao, data)
        VALUES (?, ?, ?, ?, ?)
    """, (
        aluno_nome,
        aluno_turma,
        analise,
        conclusao,
        datetime.now().strftime("%Y-%m-%d %H:%M")
    ))
    conn.commit()
    conn.close()


def listar_analises():
    """Lista todas as análises"""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM dados_desinformacao ORDER BY data DESC")
    analises = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return analises


def listar_analises_aluno(aluno_nome, aluno_turma):
    """Lista as análises de um aluno"""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT * FROM dados_desinformacao 
        WHERE aluno_nome = ? AND aluno_turma = ?
        ORDER BY data DESC
    """, (aluno_nome, aluno_turma))
    analises = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return analises


def excluir_analise(analise_id):
    """Exclui uma análise"""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM dados_desinformacao WHERE id = ?", (analise_id,))
    conn.commit()
    conn.close()
    conn.commit()
    conn.close()
    print("✅ Banco de dados atualizado!")

# ============================================================
# 🅹 FUNÇÕES DE CAMPANHAS
# ============================================================

def salvar_campanha(aluno_nome, aluno_turma, titulo, tipo, publico, roteiro, divulgacao):
    """Salva a campanha do aluno"""
    from datetime import datetime
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO campanhas (aluno_nome, aluno_turma, titulo, tipo, publico, roteiro, divulgacao, data)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        aluno_nome,
        aluno_turma,
        titulo,
        tipo,
        publico,
        roteiro,
        divulgacao,
        datetime.now().strftime("%Y-%m-%d %H:%M")
    ))
    conn.commit()
    conn.close()


def listar_campanhas():
    """Lista todas as campanhas"""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM campanhas ORDER BY data DESC")
    campanhas = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return campanhas


def listar_campanhas_aluno(aluno_nome, aluno_turma):
    """Lista as campanhas de um aluno"""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT * FROM campanhas 
        WHERE aluno_nome = ? AND aluno_turma = ?
        ORDER BY data DESC
    """, (aluno_nome, aluno_turma))
    campanhas = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return campanhas


def excluir_campanha(campanha_id):
    """Exclui uma campanha"""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM campanhas WHERE id = ?", (campanha_id,))
    conn.commit()
    conn.close()

# ============================================================
# 🅵 FUNÇÕES DE INFOGRÁFICOS
# ============================================================

def salvar_infografico(aluno_nome, aluno_turma, titulo, tema, dados, cores, icones):
    """Salva o infográfico do aluno"""
    from datetime import datetime
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO infograficos (aluno_nome, aluno_turma, titulo, tema, dados, cores, icones, data)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        aluno_nome,
        aluno_turma,
        titulo,
        tema,
        dados,
        cores,
        icones,
        datetime.now().strftime("%Y-%m-%d %H:%M")
    ))
    conn.commit()
    conn.close()


def listar_infograficos():
    """Lista todos os infográficos"""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM infograficos ORDER BY data DESC")
    infograficos = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return infograficos


def listar_infograficos_aluno(aluno_nome, aluno_turma):
    """Lista os infográficos de um aluno"""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT * FROM infograficos 
        WHERE aluno_nome = ? AND aluno_turma = ?
        ORDER BY data DESC
    """, (aluno_nome, aluno_turma))
    infograficos = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return infograficos


def excluir_infografico(infografico_id):
    """Exclui um infográfico"""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM infograficos WHERE id = ?", (infografico_id,))
    conn.commit()
    conn.close()

# ============================================================
# 🅶 FUNÇÕES DE PODCASTS
# ============================================================

def salvar_podcast(aluno_nome, aluno_turma, titulo, tema, duracao, convidado, roteiro):
    """Salva o podcast do aluno"""
    from datetime import datetime
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO podcasts (aluno_nome, aluno_turma, titulo, tema, duracao, convidado, roteiro, data)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        aluno_nome,
        aluno_turma,
        titulo,
        tema,
        duracao,
        convidado,
        roteiro,
        datetime.now().strftime("%Y-%m-%d %H:%M")
    ))
    conn.commit()
    conn.close()


def listar_podcasts():
    """Lista todos os podcasts"""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM podcasts ORDER BY data DESC")
    podcasts = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return podcasts


def listar_podcasts_aluno(aluno_nome, aluno_turma):
    """Lista os podcasts de um aluno"""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT * FROM podcasts 
        WHERE aluno_nome = ? AND aluno_turma = ?
        ORDER BY data DESC
    """, (aluno_nome, aluno_turma))
    podcasts = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return podcasts


def excluir_podcast(podcast_id):
    """Exclui um podcast"""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM podcasts WHERE id = ?", (podcast_id,))
    conn.commit()
    conn.close()

# ============================================================
# 🔥 INSERIR PERGUNTAS EXTRAS (Deepfake, IA, Cultura Digital, etc.)
# ============================================================

def inserir_perguntas_extras():
    """Insere as perguntas que faltam: deepfake, IA, cultura digital, etc."""
    
    perguntas_extras = [
        # ========== 🤖 DEEPFAKE ==========
        {"turma": "6º Ano - Anfitrião", "categoria": "fake",
         "pergunta": "É verdade que deepfake é um vídeo ou áudio falso criado por inteligência artificial?",
         "resposta": "Verdade",
         "explicacao": "Sim! Deepfake usa IA para criar vídeos e áudios falsos muito realistas."},
        {"turma": "6º Ano - Anfitrião", "categoria": "fake",
         "pergunta": "É verdade que deepfakes são sempre fáceis de identificar?",
         "resposta": "Fake",
         "explicacao": "Não! Deepfakes podem ser muito realistas e difíceis de detectar."},
        {"turma": "7º Ano - Visitante", "categoria": "fake",
         "pergunta": "É verdade que deepfakes podem imitar a voz de uma pessoa real?",
         "resposta": "Verdade",
         "explicacao": "Sim! A IA pode clonar vozes e enganar pessoas por telefone."},
        {"turma": "8º Ano - Visitante", "categoria": "fake",
         "pergunta": "É verdade que deepfakes podem ser detectados por softwares especiais?",
         "resposta": "Verdade",
         "explicacao": "Sim! Existem ferramentas que ajudam a detectar deepfakes."},
        {"turma": "9º Ano - Visitante", "categoria": "fake",
         "pergunta": "É verdade que a lei brasileira já pune quem cria deepfakes para prejudicar outros?",
         "resposta": "Verdade",
         "explicacao": "Sim! Criar deepfakes para prejudicar é crime."},
        
        # ========== 🧠 INTELIGÊNCIA ARTIFICIAL ==========
        {"turma": "6º Ano - Anfitrião", "categoria": "fake",
         "pergunta": "É verdade que Inteligência Artificial (IA) é uma tecnologia que faz máquinas aprenderem?",
         "resposta": "Verdade",
         "explicacao": "Sim! IA é a capacidade de máquinas aprenderem e tomarem decisões."},
        {"turma": "6º Ano - Anfitrião", "categoria": "fake",
         "pergunta": "É verdade que a IA sempre dá respostas corretas?",
         "resposta": "Fake",
         "explicacao": "Não! IA pode errar e dar informações falsas."},
        {"turma": "7º Ano - Visitante", "categoria": "fake",
         "pergunta": "É verdade que a IA pode aprender com os dados que recebe?",
         "resposta": "Verdade",
         "explicacao": "Sim! IA aprende com dados e melhora com o tempo."},
        {"turma": "8º Ano - Visitante", "categoria": "fake",
         "pergunta": "É verdade que a IA pode criar textos, imagens e vídeos?",
         "resposta": "Verdade",
         "explicacao": "Sim! ChatGPT, DALL-E e outras IAs criam conteúdo."},
        {"turma": "9º Ano - Visitante", "categoria": "fake",
         "pergunta": "É verdade que precisamos de leis para regular a IA?",
         "resposta": "Verdade",
         "explicacao": "Sim! A regulação da IA é essencial para proteger as pessoas."},
        
        # ========== 🌐 CULTURA DIGITAL ==========
        {"turma": "6º Ano - Anfitrião", "categoria": "fake",
         "pergunta": "É verdade que tudo o que você posta na internet fica para sempre?",
         "resposta": "Verdade",
         "explicacao": "Sim! A internet nunca esquece. Pense antes de postar!"},
        {"turma": "6º Ano - Anfitrião", "categoria": "fake",
         "pergunta": "É verdade que podemos apagar tudo o que postamos na internet?",
         "resposta": "Fake",
         "explicacao": "Não! Prints e cópias podem guardar para sempre."},
        {"turma": "7º Ano - Visitante", "categoria": "fake",
         "pergunta": "É verdade que os algoritmos decidem o que vemos nas redes sociais?",
         "resposta": "Verdade",
         "explicacao": "Sim! Eles mostram o que acham que você vai gostar."},
        {"turma": "8º Ano - Visitante", "categoria": "fake",
         "pergunta": "É verdade que a cultura digital inclui a 'cultura maker'?",
         "resposta": "Verdade",
         "explicacao": "Sim! Criar, consertar e inovar fazem parte."},
        {"turma": "9º Ano - Visitante", "categoria": "fake",
         "pergunta": "É verdade que a cultura digital inclui a programação e o pensamento computacional?",
         "resposta": "Verdade",
         "explicacao": "Sim! Programar é uma forma de se expressar."},
        
        # ========== 🤝 RESPONSABILIDADE E CIDADANIA ==========
        {"turma": "6º Ano - Anfitrião", "categoria": "cyber",
         "pergunta": "É correto defender um colega que está sendo vítima de cyberbullying?",
         "resposta": "Sim",
         "explicacao": "Defender é atitude de cidadão responsável!"},
        {"turma": "7º Ano - Visitante", "categoria": "cyber",
         "pergunta": "É correto apoiar campanhas contra o cyberbullying?",
         "resposta": "Sim",
         "explicacao": "Apoiar é atitude de cidadão consciente!"},
        {"turma": "8º Ano - Visitante", "categoria": "cyber",
         "pergunta": "É correto denunciar discurso de ódio nas redes sociais?",
         "resposta": "Sim",
         "explicacao": "Denunciar é responsabilidade de todo cidadão!"},
        {"turma": "9º Ano - Visitante", "categoria": "cyber",
         "pergunta": "É correto ajudar a combater fake news nas redes sociais?",
         "resposta": "Sim",
         "explicacao": "Combater fake news é responsabilidade de todos!"},
    ]
    
    conn = get_connection()
    cursor = conn.cursor()
    inseridas = 0
    
    for p in perguntas_extras:
        cursor.execute("""
            SELECT id FROM questoes 
            WHERE pergunta = ? AND turma = ?
        """, (p['pergunta'], p['turma']))
        
        if cursor.fetchone() is None:
            cursor.execute("""
                INSERT INTO questoes 
                (turma, categoria, pergunta, resposta, opcao1, opcao2, opcao3, explicacao)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                p['turma'],
                p['categoria'],
                p['pergunta'],
                p.get('resposta', p.get('correta', '')),
                p.get('opcao1'),
                p.get('opcao2'),
                p.get('opcao3'),
                p.get('explicacao', '')
            ))
            inseridas += 1
    
    conn.commit()
    conn.close()
    print(f"✅ {inseridas} perguntas extras inseridas!")
    return inseridas

def inserir_todas_perguntas_recuperacao():
    """Insere TODAS as perguntas no banco (recuperação completa)"""
    
    todas_perguntas = [
        # ========== 📰 FAKE NEWS - 6º ANO ==========
        {"turma": "6º Ano - Anfitrião", "categoria": "fake",
         "pergunta": "É verdade que devemos compartilhar tudo o que vemos na internet?",
         "resposta": "Fake", "explicacao": "Não! Sempre verifique antes de compartilhar."},
        {"turma": "6º Ano - Anfitrião", "categoria": "fake",
         "pergunta": "É verdade que fake news podem causar danos reais?",
         "resposta": "Verdade", "explicacao": "Sim! Fake news podem prejudicar pessoas."},
        {"turma": "6º Ano - Anfitrião", "categoria": "fake",
         "pergunta": "É verdade que tudo que está na internet é verdade?",
         "resposta": "Fake", "explicacao": "Não! Qualquer pessoa pode publicar."},
        {"turma": "6º Ano - Anfitrião", "categoria": "fake",
         "pergunta": "É verdade que devemos verificar a fonte antes de compartilhar?",
         "resposta": "Verdade", "explicacao": "Sim! Verificar a fonte é o primeiro passo."},
        {"turma": "6º Ano - Anfitrião", "categoria": "fake",
         "pergunta": "É verdade que fotos e vídeos nunca são editados?",
         "resposta": "Fake", "explicacao": "Muitas fotos e vídeos são editados."},
        {"turma": "6º Ano - Anfitrião", "categoria": "fake",
         "pergunta": "Você viu uma notícia que diz: 'Cientistas descobrem que chocolate cura câncer'. O que fazer?",
         "resposta": "Fake", "explicacao": "Pensamento crítico é questionar antes de acreditar."},
        {"turma": "6º Ano - Anfitrião", "categoria": "fake",
         "pergunta": "É verdade que devemos acreditar em tudo que nossos amigos enviam?",
         "resposta": "Fake", "explicacao": "Não! Amigos podem repassar fake news."},
        {"turma": "6º Ano - Anfitrião", "categoria": "fake",
         "pergunta": "É verdade que precisamos questionar as informações que recebemos?",
         "resposta": "Verdade", "explicacao": "Sim! Questionar é o primeiro passo."},
        {"turma": "6º Ano - Anfitrião", "categoria": "fake",
         "pergunta": "É verdade que manchetes exageradas sempre são verdadeiras?",
         "resposta": "Fake", "explicacao": "Não! São táticas de clickbait."},
        {"turma": "6º Ano - Anfitrião", "categoria": "fake",
         "pergunta": "É verdade que devemos comparar notícias de fontes diferentes?",
         "resposta": "Verdade", "explicacao": "Sim! Comparar fontes ajuda a confirmar."},
        
        # ========== 📰 FAKE NEWS - 7º ANO ==========
        {"turma": "7º Ano - Visitante", "categoria": "fake",
         "pergunta": "É verdade que toda notícia que viraliza é verdadeira?",
         "resposta": "Fake", "explicacao": "Não! Viralizar não significa que é verdade."},
        {"turma": "7º Ano - Visitante", "categoria": "fake",
         "pergunta": "É verdade que devemos analisar quem escreveu a notícia?",
         "resposta": "Verdade", "explicacao": "Sim! Analisar o autor é fundamental."},
        {"turma": "7º Ano - Visitante", "categoria": "fake",
         "pergunta": "É verdade que toda notícia com muitas curtidas é confiável?",
         "resposta": "Fake", "explicacao": "Não! Curtidas não são prova de verdade."},
        {"turma": "7º Ano - Visitante", "categoria": "fake",
         "pergunta": "É verdade que precisamos desconfiar de notícias que nos deixam com raiva?",
         "resposta": "Verdade", "explicacao": "Sim! Fake news exploram emoções fortes."},
        {"turma": "7º Ano - Visitante", "categoria": "fake",
         "pergunta": "É verdade que podemos confiar em tudo que está na internet?",
         "resposta": "Fake", "explicacao": "Não! Qualquer pessoa pode publicar."},
        {"turma": "7º Ano - Visitante", "categoria": "fake",
         "pergunta": "É verdade que fake news se espalham mais rápido que notícias verdadeiras?",
         "resposta": "Verdade", "explicacao": "Sim! Estudos mostram que se espalham 6x mais rápido."},
        {"turma": "7º Ano - Visitante", "categoria": "fake",
         "pergunta": "É verdade que checar em 3 fontes diferentes ajuda a confirmar uma notícia?",
         "resposta": "Verdade", "explicacao": "Sim! Sempre verifique em várias fontes."},
        {"turma": "7º Ano - Visitante", "categoria": "fake",
         "pergunta": "É verdade que robôs podem criar notícias falsas automaticamente?",
         "resposta": "Verdade", "explicacao": "Sim! Bots espalham fake news em massa."},
        {"turma": "7º Ano - Visitante", "categoria": "fake",
         "pergunta": "É verdade que toda corrente de WhatsApp é verdadeira?",
         "resposta": "Fake", "explicacao": "Não! Correntes são um dos maiores veículos de fake news."},
        {"turma": "7º Ano - Visitante", "categoria": "fake",
         "pergunta": "É verdade que vídeos deepfake podem enganar as pessoas?",
         "resposta": "Verdade", "explicacao": "Sim! Deepfakes são vídeos falsos criados por IA."},
        
        # ========== 📰 FAKE NEWS - 8º ANO ==========
        {"turma": "8º Ano - Visitante", "categoria": "fake",
         "pergunta": "É verdade que IA pode criar notícias falsas realistas?",
         "resposta": "Verdade", "explicacao": "Sim! IA pode gerar textos, fotos e vídeos falsos."},
        {"turma": "8º Ano - Visitante", "categoria": "fake",
         "pergunta": "É verdade que sites com muitos anúncios são sempre confiáveis?",
         "resposta": "Fake", "explicacao": "Não! Muitos anúncios podem indicar site sensacionalista."},
        {"turma": "8º Ano - Visitante", "categoria": "fake",
         "pergunta": "É verdade que fake news podem influenciar eleições?",
         "resposta": "Verdade", "explicacao": "Sim! Fake news políticas são um grande problema."},
        {"turma": "8º Ano - Visitante", "categoria": "fake",
         "pergunta": "É verdade que toda notícia com muitos compartilhamentos é verdadeira?",
         "resposta": "Fake", "explicacao": "Não! Fake news se espalham mais rápido que a verdade."},
        {"turma": "8º Ano - Visitante", "categoria": "fake",
         "pergunta": "É verdade que checar agências de fact-checking ajuda a identificar fake news?",
         "resposta": "Verdade", "explicacao": "Sim! Agências como Aos Fatos e Lupa ajudam a verificar."},
        {"turma": "8º Ano - Visitante", "categoria": "fake",
         "pergunta": "É verdade que fake news podem causar danos à saúde pública?",
         "resposta": "Verdade", "explicacao": "Sim! Fake news sobre saúde podem levar a mortes."},
        {"turma": "8º Ano - Visitante", "categoria": "fake",
         "pergunta": "É verdade que podemos identificar fake news pelo URL do site?",
         "resposta": "Verdade", "explicacao": "Sim! URLs estranhos podem indicar sites falsos."},
        {"turma": "8º Ano - Visitante", "categoria": "fake",
         "pergunta": "É verdade que toda notícia que concorda com nossa opinião é verdadeira?",
         "resposta": "Fake", "explicacao": "Não! Isso é o viés de confirmação."},
        {"turma": "8º Ano - Visitante", "categoria": "fake",
         "pergunta": "É verdade que a educação midiática ajuda a combater fake news?",
         "resposta": "Verdade", "explicacao": "Sim! Aprender a analisar notícias é fundamental."},
        {"turma": "8º Ano - Visitante", "categoria": "fake",
         "pergunta": "É verdade que deepfakes podem ser usados para extorsão e chantagem?",
         "resposta": "Verdade", "explicacao": "Sim! Criminosos usam deepfakes para chantagear."},
        
        # ========== 📰 FAKE NEWS - 9º ANO ==========
        {"turma": "9º Ano - Visitante", "categoria": "fake",
         "pergunta": "É verdade que deepfakes podem ser usados para manipular opinião pública?",
         "resposta": "Verdade", "explicacao": "Sim! Deepfakes são uma ameaça à democracia."},
        {"turma": "9º Ano - Visitante", "categoria": "fake",
         "pergunta": "É verdade que toda notícia de site desconhecido é fake?",
         "resposta": "Fake", "explicacao": "Não! Mas é preciso verificar a credibilidade."},
        {"turma": "9º Ano - Visitante", "categoria": "fake",
         "pergunta": "É verdade que fake news podem ser usadas como arma de guerra?",
         "resposta": "Verdade", "explicacao": "Sim! A desinformação é usada em conflitos."},
        {"turma": "9º Ano - Visitante", "categoria": "fake",
         "pergunta": "É verdade que algoritmos podem amplificar fake news?",
         "resposta": "Verdade", "explicacao": "Sim! Algoritmos priorizam conteúdo sensacionalista."},
        {"turma": "9º Ano - Visitante", "categoria": "fake",
         "pergunta": "É verdade que podemos usar ferramentas de IA para detectar fake news?",
         "resposta": "Verdade", "explicacao": "Sim! IA pode ajudar a identificar padrões."},
        {"turma": "9º Ano - Visitante", "categoria": "fake",
         "pergunta": "É verdade que fake news só afetam pessoas com pouca educação?",
         "resposta": "Fake", "explicacao": "Não! Qualquer pessoa pode ser enganada."},
        {"turma": "9º Ano - Visitante", "categoria": "fake",
         "pergunta": "É verdade que checar a data da notícia ajuda a identificar fake news?",
         "resposta": "Verdade", "explicacao": "Sim! Notícias antigas podem ser recicladas."},
        {"turma": "9º Ano - Visitante", "categoria": "fake",
         "pergunta": "É verdade que a verificação de fatos é uma habilidade essencial no século XXI?",
         "resposta": "Verdade", "explicacao": "Sim! Saber verificar informações é fundamental."},
        {"turma": "9º Ano - Visitante", "categoria": "fake",
         "pergunta": "É verdade que deepfakes podem influenciar eleições?",
         "resposta": "Verdade", "explicacao": "Sim! Deepfakes políticos são uma ameaça."},
        {"turma": "9º Ano - Visitante", "categoria": "fake",
         "pergunta": "É verdade que podemos acreditar em qualquer áudio que recebemos?",
         "resposta": "Fake", "explicacao": "Não! Áudios podem ser clonados por IA."},
        
        # ========== 🛡️ CYBERBULLYING - 6º ANO ==========
        {"turma": "6º Ano - Anfitrião", "categoria": "cyber",
         "pergunta": "É correto zombar de um colega nas redes sociais?",
         "resposta": "Não", "explicacao": "Respeitar as diferenças é fundamental!"},
        {"turma": "6º Ano - Anfitrião", "categoria": "cyber",
         "pergunta": "É correto postar foto de um colega para humilhar?",
         "resposta": "Não", "explicacao": "Humilhar é bullying!"},
        {"turma": "6º Ano - Anfitrião", "categoria": "cyber",
         "pergunta": "É correto excluir um colega do grupo online?",
         "resposta": "Não", "explicacao": "Excluir é uma forma de bullying."},
        {"turma": "6º Ano - Anfitrião", "categoria": "cyber",
         "pergunta": "É correto criar apelidos ofensivos?",
         "resposta": "Não", "explicacao": "Apelidos ofensivos magoam."},
        {"turma": "6º Ano - Anfitrião", "categoria": "cyber",
         "pergunta": "É correto defender um colega que está sendo zombado?",
         "resposta": "Sim", "explicacao": "Defender é atitude de coragem!"},
        {"turma": "6º Ano - Anfitrião", "categoria": "cyber",
         "pergunta": "É correto espalhar mentiras sobre um colega?",
         "resposta": "Não", "explicacao": "Espalhar mentiras é fake news e bullying!"},
        {"turma": "6º Ano - Anfitrião", "categoria": "cyber",
         "pergunta": "É correto compartilhar meme ofensivo sobre alguém?",
         "resposta": "Não", "explicacao": "Memes ofensivos são cyberbullying!"},
        {"turma": "6º Ano - Anfitrião", "categoria": "cyber",
         "pergunta": "É correto avisar um adulto se sofrer cyberbullying?",
         "resposta": "Sim", "explicacao": "Procurar ajuda é atitude sábia!"},
        {"turma": "6º Ano - Anfitrião", "categoria": "cyber",
         "pergunta": "É correto bloquear quem te ofende online?",
         "resposta": "Sim", "explicacao": "Bloquear é uma forma de se proteger!"},
        {"turma": "6º Ano - Anfitrião", "categoria": "cyber",
         "pergunta": "É correto gravar vídeos de colegas sem permissão?",
         "resposta": "Não", "explicacao": "Gravar sem permissão é invasão de privacidade!"},
        
        # ========== 🛡️ CYBERBULLYING - 7º ANO ==========
        {"turma": "7º Ano - Visitante", "categoria": "cyber",
         "pergunta": "É correto comentar negativamente sobre o corpo de alguém?",
         "resposta": "Não", "explicacao": "Comentários negativos causam danos psicológicos."},
        {"turma": "7º Ano - Visitante", "categoria": "cyber",
         "pergunta": "É correto criar perfil falso para zoar colegas?",
         "resposta": "Não", "explicacao": "Perfil falso é crime e cyberbullying!"},
        {"turma": "7º Ano - Visitante", "categoria": "cyber",
         "pergunta": "É correto divulgar o endereço de alguém nas redes?",
         "resposta": "Não", "explicacao": "Divulgar dados é perigoso e criminoso!"},
        {"turma": "7º Ano - Visitante", "categoria": "cyber",
         "pergunta": "É correto fazer piadas racistas online?",
         "resposta": "Não", "explicacao": "Racismo é crime! Respeite a diversidade."},
        {"turma": "7º Ano - Visitante", "categoria": "cyber",
         "pergunta": "É correto apoiar um colega que sofreu bullying?",
         "resposta": "Sim", "explicacao": "Apoiar é atitude de cidadão digital!"},
        {"turma": "7º Ano - Visitante", "categoria": "cyber",
         "pergunta": "É correto fazer piadas homofóbicas online?",
         "resposta": "Não", "explicacao": "Homofobia é crime! Respeite a diversidade."},
        {"turma": "7º Ano - Visitante", "categoria": "cyber",
         "pergunta": "É correto ameaçar alguém por causa de um jogo online?",
         "resposta": "Não", "explicacao": "Ameaças são crime! Denuncie."},
        {"turma": "7º Ano - Visitante", "categoria": "cyber",
         "pergunta": "É correto denunciar conteúdo ofensivo?",
         "resposta": "Sim", "explicacao": "Denunciar é atitude de cidadão digital!"},
        {"turma": "7º Ano - Visitante", "categoria": "cyber",
         "pergunta": "É correto xingar um colega no chat durante o jogo?",
         "resposta": "Não", "explicacao": "Xingar é falta de respeito!"},
        {"turma": "7º Ano - Visitante", "categoria": "cyber",
         "pergunta": "É correto apoiar campanhas contra o bullying?",
         "resposta": "Sim", "explicacao": "Apoiar é atitude de cidadão consciente!"},
        
        # ========== 🛡️ CYBERBULLYING - 8º ANO ==========
        {"turma": "8º Ano - Visitante", "categoria": "cyber",
         "pergunta": "É correto postar vídeo de um colega errando para ridicularizar?",
         "resposta": "Não", "explicacao": "Ridicularizar é bullying!"},
        {"turma": "8º Ano - Visitante", "categoria": "cyber",
         "pergunta": "É correto fazer comentários capacitistas online?",
         "resposta": "Não", "explicacao": "Capacitismo é crime! Respeite a diversidade."},
        {"turma": "8º Ano - Visitante", "categoria": "cyber",
         "pergunta": "É correto criar grupos para excluir alguém?",
         "resposta": "Não", "explicacao": "Excluir é uma forma de bullying!"},
        {"turma": "8º Ano - Visitante", "categoria": "cyber",
         "pergunta": "É correto fazer comentários sobre a religião de alguém?",
         "resposta": "Não", "explicacao": "Respeitar a religião do próximo é fundamental!"},
        {"turma": "8º Ano - Visitante", "categoria": "cyber",
         "pergunta": "É correto apoiar vítimas de cyberbullying?",
         "resposta": "Sim", "explicacao": "Apoiar é atitude de cidadão digital!"},
        {"turma": "8º Ano - Visitante", "categoria": "cyber",
         "pergunta": "É correto fazer comentários gordofóbicos online?",
         "resposta": "Não", "explicacao": "Gordofobia é crime! Respeite todos os corpos."},
        {"turma": "8º Ano - Visitante", "categoria": "cyber",
         "pergunta": "É correto fazer comentários sobre a aparência de alguém?",
         "resposta": "Não", "explicacao": "Comentários sobre aparência podem magoar."},
        {"turma": "8º Ano - Visitante", "categoria": "cyber",
         "pergunta": "É correto denunciar conteúdo de ódio?",
         "resposta": "Sim", "explicacao": "Denunciar é atitude de cidadão digital!"},
        {"turma": "8º Ano - Visitante", "categoria": "cyber",
         "pergunta": "É correto fazer comentários xenofóbicos online?",
         "resposta": "Não", "explicacao": "Xenofobia é crime! Respeite todas as origens."},
        {"turma": "8º Ano - Visitante", "categoria": "cyber",
         "pergunta": "É correto ajudar alguém que está sofrendo bullying?",
         "resposta": "Sim", "explicacao": "Ajudar é atitude de cidadão consciente!"},
        
        # ========== 🛡️ CYBERBULLYING - 9º ANO ==========
        {"turma": "9º Ano - Visitante", "categoria": "cyber",
         "pergunta": "É correto fazer comentários sobre a orientação sexual de alguém?",
         "resposta": "Não", "explicacao": "Respeite a diversidade!"},
        {"turma": "9º Ano - Visitante", "categoria": "cyber",
         "pergunta": "É correto ameaçar alguém por causa de política?",
         "resposta": "Não", "explicacao": "Ameaças são crime! Denuncie."},
        {"turma": "9º Ano - Visitante", "categoria": "cyber",
         "pergunta": "É correto denunciar conteúdo de ódio?",
         "resposta": "Sim", "explicacao": "Denunciar é atitude de cidadão digital!"},
        {"turma": "9º Ano - Visitante", "categoria": "cyber",
         "pergunta": "É correto fazer comentários sobre a classe social de alguém?",
         "resposta": "Não", "explicacao": "Respeite todas as pessoas."},
        {"turma": "9º Ano - Visitante", "categoria": "cyber",
         "pergunta": "É correto apoiar campanhas contra o bullying?",
         "resposta": "Sim", "explicacao": "Apoiar é atitude de cidadão consciente!"},
        {"turma": "9º Ano - Visitante", "categoria": "cyber",
         "pergunta": "É correto fazer comentários etaristas online?",
         "resposta": "Não", "explicacao": "Etarismo é crime! Respeite todas as idades."},
        {"turma": "9º Ano - Visitante", "categoria": "cyber",
         "pergunta": "É correto fazer comentários sobre a deficiência de alguém?",
         "resposta": "Não", "explicacao": "Capacitismo é crime! Respeite a diversidade."},
        {"turma": "9º Ano - Visitante", "categoria": "cyber",
         "pergunta": "É correto denunciar conteúdo racista?",
         "resposta": "Sim", "explicacao": "Denunciar racismo é obrigação de todo cidadão!"},
        {"turma": "9º Ano - Visitante", "categoria": "cyber",
         "pergunta": "É correto fazer comentários sobre a origem regional de alguém?",
         "resposta": "Não", "explicacao": "Xenofobia é crime! Respeite todas as origens."},
        {"turma": "9º Ano - Visitante", "categoria": "cyber",
         "pergunta": "É correto apoiar vítimas de cyberbullying?",
         "resposta": "Sim", "explicacao": "Apoiar é atitude de cidadão digital!"},
        # ========== ⚖️ ÉTICA DIGITAL - 6º ANO ==========
        {"turma": "6º Ano - Anfitrião", "categoria": "etica",
         "pergunta": "Um colega postou foto praticando esporte. O que fazer?",
         "opcao1": "Zombar da foto", "opcao2": "Elogiar e incentivar", "opcao3": "Compartilhar sem permissão",
         "correta": "Elogiar e incentivar", "explicacao": "Incentivar é atitude de cidadão digital!"},
        {"turma": "6º Ano - Anfitrião", "categoria": "etica",
         "pergunta": "Você viu um colega sendo excluído do jogo online. O que fazer?",
         "opcao1": "Ignorar", "opcao2": "Convidar o colega para jogar", "opcao3": "Zombar também",
         "correta": "Convidar o colega para jogar", "explicacao": "Incluir é atitude ética!"},
        {"turma": "6º Ano - Anfitrião", "categoria": "etica",
         "pergunta": "Você perdeu o jogo. O que fazer?",
         "opcao1": "Xingar os colegas", "opcao2": "Parabenizar o time adversário", "opcao3": "Sair do grupo",
         "correta": "Parabenizar o time adversário", "explicacao": "Fair play é fundamental no esporte!"},
        {"turma": "6º Ano - Anfitrião", "categoria": "etica",
         "pergunta": "Você viu fake news sobre um atleta. O que fazer?",
         "opcao1": "Compartilhar", "opcao2": "Verificar antes de compartilhar", "opcao3": "Ignorar",
         "correta": "Verificar antes de compartilhar", "explicacao": "Verificar é atitude de cidadão digital!"},
        {"turma": "6º Ano - Anfitrião", "categoria": "etica",
         "pergunta": "Um colega está sendo criticado por seu corpo. O que fazer?",
         "opcao1": "Concordar", "opcao2": "Defender o colega", "opcao3": "Rir",
         "correta": "Defender o colega", "explicacao": "Defender é atitude ética!"},
        {"turma": "6º Ano - Anfitrião", "categoria": "etica",
         "pergunta": "Você quer postar foto do treino. O que fazer?",
         "opcao1": "Postar sem pedir permissão", "opcao2": "Pedir permissão aos colegas", "opcao3": "Marcar todos sem avisar",
         "correta": "Pedir permissão aos colegas", "explicacao": "Respeitar a privacidade é fundamental!"},
        {"turma": "6º Ano - Anfitrião", "categoria": "etica",
         "pergunta": "Você viu um meme ofensivo sobre um atleta. O que fazer?",
         "opcao1": "Compartilhar", "opcao2": "Denunciar", "opcao3": "Rir",
         "correta": "Denunciar", "explicacao": "Denunciar é atitude de cidadão digital!"},
        {"turma": "6º Ano - Anfitrião", "categoria": "etica",
         "pergunta": "Um colega quer usar anabolizantes. O que fazer?",
         "opcao1": "Incentivar", "opcao2": "Alertar sobre os perigos", "opcao3": "Ignorar",
         "correta": "Alertar sobre os perigos", "explicacao": "Cuidar da saúde é prioridade!"},
        {"turma": "6º Ano - Anfitrião", "categoria": "etica",
         "pergunta": "Você ganhou um jogo com ajuda de trapaça. O que fazer?",
         "opcao1": "Comemorar", "opcao2": "Assumir a trapaça", "opcao3": "Esconder",
         "correta": "Assumir a trapaça", "explicacao": "Honestidade é fundamental no esporte!"},
        {"turma": "6º Ano - Anfitrião", "categoria": "etica",
         "pergunta": "Você viu alguém sendo racista online. O que fazer?",
         "opcao1": "Ignorar", "opcao2": "Denunciar e apoiar a vítima", "opcao3": "Compartilhar",
         "correta": "Denunciar e apoiar a vítima", "explicacao": "Denunciar racismo é obrigação de todo cidadão!"},
        
        # ========== ⚖️ ÉTICA DIGITAL - 7º ANO ==========
        {"turma": "7º Ano - Visitante", "categoria": "etica",
         "pergunta": "Você viu fake news sobre um time. O que fazer?",
         "opcao1": "Compartilhar", "opcao2": "Verificar antes de compartilhar", "opcao3": "Ignorar",
         "correta": "Verificar antes de compartilhar", "explicacao": "Verificar é atitude de cidadão digital!"},
        {"turma": "7º Ano - Visitante", "categoria": "etica",
         "pergunta": "Um colega está sendo criticado por sua altura. O que fazer?",
         "opcao1": "Concordar", "opcao2": "Defender o colega", "opcao3": "Rir",
         "correta": "Defender o colega", "explicacao": "Defender é atitude ética!"},
        {"turma": "7º Ano - Visitante", "categoria": "etica",
         "pergunta": "Você quer postar foto do treino. O que fazer?",
         "opcao1": "Postar sem pedir permissão", "opcao2": "Pedir permissão aos colegas", "opcao3": "Marcar todos sem avisar",
         "correta": "Pedir permissão aos colegas", "explicacao": "Respeitar a privacidade é fundamental!"},
        {"turma": "7º Ano - Visitante", "categoria": "etica",
         "pergunta": "Você viu um meme ofensivo sobre um atleta. O que fazer?",
         "opcao1": "Compartilhar", "opcao2": "Denunciar", "opcao3": "Rir",
         "correta": "Denunciar", "explicacao": "Denunciar é atitude de cidadão digital!"},
        {"turma": "7º Ano - Visitante", "categoria": "etica",
         "pergunta": "Um colega quer usar anabolizantes. O que fazer?",
         "opcao1": "Incentivar", "opcao2": "Alertar sobre os perigos", "opcao3": "Ignorar",
         "correta": "Alertar sobre os perigos", "explicacao": "Cuidar da saúde é prioridade!"},
        {"turma": "7º Ano - Visitante", "categoria": "etica",
         "pergunta": "Você viu um colega postando conteúdo ofensivo. O que fazer?",
         "opcao1": "Compartilhar", "opcao2": "Denunciar e conversar com o colega", "opcao3": "Rir",
         "correta": "Denunciar e conversar com o colega", "explicacao": "Responsabilidade é agir com ética!"},
        {"turma": "7º Ano - Visitante", "categoria": "etica",
         "pergunta": "Você descobriu que um colega está sofrendo cyberbullying. O que fazer?",
         "opcao1": "Ignorar", "opcao2": "Apoiar, denunciar e conversar com um adulto", "opcao3": "Rir",
         "correta": "Apoiar, denunciar e conversar com um adulto", "explicacao": "Responsabilidade é agir para proteger!"},
        
        # ========== ⚖️ ÉTICA DIGITAL - 8º ANO ==========
        {"turma": "8º Ano - Visitante", "categoria": "etica",
         "pergunta": "Você viu um meme ofensivo sobre um atleta. O que fazer?",
         "opcao1": "Compartilhar", "opcao2": "Denunciar", "opcao3": "Rir",
         "correta": "Denunciar", "explicacao": "Denunciar é atitude de cidadão digital!"},
        {"turma": "8º Ano - Visitante", "categoria": "etica",
         "pergunta": "Um colega quer usar anabolizantes. O que fazer?",
         "opcao1": "Incentivar", "opcao2": "Alertar sobre os perigos", "opcao3": "Ignorar",
         "correta": "Alertar sobre os perigos", "explicacao": "Cuidar da saúde é prioridade!"},
        {"turma": "8º Ano - Visitante", "categoria": "etica",
         "pergunta": "Você ganhou um jogo com ajuda de trapaça. O que fazer?",
         "opcao1": "Comemorar", "opcao2": "Assumir a trapaça", "opcao3": "Esconder",
         "correta": "Assumir a trapaça", "explicacao": "Honestidade é fundamental no esporte!"},
        {"turma": "8º Ano - Visitante", "categoria": "etica",
         "pergunta": "Você viu um atleta sendo vítima de racismo online. O que fazer?",
         "opcao1": "Ignorar", "opcao2": "Denunciar e apoiar", "opcao3": "Compartilhar para expor",
         "correta": "Denunciar e apoiar", "explicacao": "Denunciar racismo é obrigação de todo cidadão!"},
        {"turma": "8º Ano - Visitante", "categoria": "etica",
         "pergunta": "Você descobriu que um colega está sendo vítima de racismo online. O que fazer?",
         "opcao1": "Ignorar", "opcao2": "Apoiar, denunciar e conversar com um adulto", "opcao3": "Rir",
         "correta": "Apoiar, denunciar e conversar com um adulto", "explicacao": "Racismo é crime! Denuncie e apoie!"},
        {"turma": "8º Ano - Visitante", "categoria": "etica",
         "pergunta": "Você viu um colega postando conteúdo ofensivo. O que fazer?",
         "opcao1": "Compartilhar", "opcao2": "Denunciar e conversar com o colega", "opcao3": "Rir",
         "correta": "Denunciar e conversar com o colega", "explicacao": "Responsabilidade é agir com ética!"},
        {"turma": "8º Ano - Visitante", "categoria": "etica",
         "pergunta": "Você quer postar foto do treino. O que fazer?",
         "opcao1": "Postar sem pedir permissão", "opcao2": "Pedir permissão aos colegas", "opcao3": "Marcar todos sem avisar",
         "correta": "Pedir permissão aos colegas", "explicacao": "Respeitar a privacidade é fundamental!"},
        
        # ========== ⚖️ ÉTICA DIGITAL - 9º ANO ==========
        {"turma": "9º Ano - Visitante", "categoria": "etica",
         "pergunta": "Você viu um atleta sendo vítima de racismo online. O que fazer?",
         "opcao1": "Ignorar", "opcao2": "Denunciar e apoiar", "opcao3": "Compartilhar para expor",
         "correta": "Denunciar e apoiar", "explicacao": "Denunciar racismo é obrigação de todo cidadão!"},
        {"turma": "9º Ano - Visitante", "categoria": "etica",
         "pergunta": "Você descobriu que um colega usa doping. O que fazer?",
         "opcao1": "Contar para todos", "opcao2": "Conversar com um adulto de confiança", "opcao3": "Ignorar",
         "correta": "Conversar com um adulto de confiança", "explicacao": "Doping é perigoso! Procure ajuda de um adulto."},
        {"turma": "9º Ano - Visitante", "categoria": "etica",
         "pergunta": "Você está perdendo um jogo online. O que fazer?",
         "opcao1": "Xingar os colegas", "opcao2": "Manter o respeito e continuar", "opcao3": "Sair do jogo",
         "correta": "Manter o respeito e continuar", "explicacao": "Respeito é fundamental, mesmo perdendo!"},
        {"turma": "9º Ano - Visitante", "categoria": "etica",
         "pergunta": "Você viu uma fake news que pode causar pânico. O que fazer?",
         "opcao1": "Compartilhar", "opcao2": "Verificar, denunciar e avisar as autoridades", "opcao3": "Ignorar",
         "correta": "Verificar, denunciar e avisar as autoridades", "explicacao": "Responsabilidade é proteger a comunidade!"},
        {"turma": "9º Ano - Visitante", "categoria": "etica",
         "pergunta": "Você viu um meme ofensivo sobre um atleta. O que fazer?",
         "opcao1": "Compartilhar", "opcao2": "Denunciar", "opcao3": "Rir",
         "correta": "Denunciar", "explicacao": "Denunciar é atitude de cidadão digital!"},
        {"turma": "9º Ano - Visitante", "categoria": "etica",
         "pergunta": "Você viu um amigo compartilhando fake news. O que fazer?",
         "opcao1": "Compartilhar também", "opcao2": "Conversar e mostrar que é fake", "opcao3": "Ignorar",
         "correta": "Conversar e mostrar que é fake", "explicacao": "Responsabilidade é ajudar os outros a entender!"},
    ]
    
    conn = get_connection()
    cursor = conn.cursor()
    inseridas = 0
    
    for p in todas_perguntas:
        cursor.execute("""
            SELECT id FROM questoes 
            WHERE pergunta = ? AND turma = ?
        """, (p['pergunta'], p['turma']))
        
        if cursor.fetchone() is None:
            cursor.execute("""
                INSERT INTO questoes 
                (turma, categoria, pergunta, resposta, opcao1, opcao2, opcao3, explicacao)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                p['turma'],
                p['categoria'],
                p['pergunta'],
                p.get('resposta', ''),
                p.get('opcao1'),
                p.get('opcao2'),
                p.get('opcao3'),
                p.get('explicacao', '')
            ))
            inseridas += 1
    
    conn.commit()
    conn.close()
    print(f"✅ {inseridas} perguntas inseridas!")
    return inseridas

# ============================================================
# 🏃 PERGUNTAS DO QUIZ DE EDUCAÇÃO FÍSICA (55)
# ============================================================

def inserir_quiz_educacao_fisica():
    """Insere as 55 perguntas do Quiz de Educação Física"""
    
    perguntas_quiz_ef = [
        # ========== 1 a 10 ==========
        {"turma": "6º Ano - Anfitrião", "categoria": "exatas",
         "pergunta": "Qual é um dos principais objetivos da Educação Física?",
         "opcao1": "Promover atividades relacionadas ao movimento e à saúde",
         "opcao2": "Ensinar somente matemática",
         "opcao3": "Ensinar apenas música",
         "resposta": "Promover atividades relacionadas ao movimento e à saúde",
         "explicacao": "A Educação Física promove movimento e saúde."},
        {"turma": "6º Ano - Anfitrião", "categoria": "exatas",
         "pergunta": "Qual destes é um esporte?",
         "opcao1": "Leitura",
         "opcao2": "Futebol",
         "opcao3": "Desenho",
         "resposta": "Futebol",
         "explicacao": "Futebol é um esporte coletivo."},
        {"turma": "6º Ano - Anfitrião", "categoria": "exatas",
         "pergunta": "Para que serve o alongamento?",
         "opcao1": "Para impedir os movimentos",
         "opcao2": "Para aumentar o cansaço",
         "opcao3": "Para preparar e alongar os músculos",
         "resposta": "Para preparar e alongar os músculos",
         "explicacao": "O alongamento prepara os músculos."},
        {"turma": "6º Ano - Anfitrião", "categoria": "exatas",
         "pergunta": "No handebol, qual é o principal objetivo dos jogadores?",
         "opcao1": "Marcar gols na equipe adversária",
         "opcao2": "Colocar a bola em uma cesta",
         "opcao3": "Derrubar os jogadores adversários",
         "resposta": "Marcar gols na equipe adversária",
         "explicacao": "No handebol, o objetivo é marcar gols."},
        {"turma": "6º Ano - Anfitrião", "categoria": "exatas",
         "pergunta": "Quais são as três modalidades de ginástica que fazem parte dos Jogos Olímpicos?",
         "opcao1": "Ginástica artística, ginástica de trampolim e ginástica acrobática",
         "opcao2": "Ginástica artística, ginástica rítmica e ginástica de trampolim",
         "opcao3": "Ginástica rítmica, ginástica acrobática e ginástica laboral",
         "resposta": "Ginástica artística, ginástica rítmica e ginástica de trampolim",
         "explicacao": "Essas são as três modalidades olímpicas."},
        {"turma": "6º Ano - Anfitrião", "categoria": "exatas",
         "pergunta": "No futebol, a bola é conduzida principalmente:",
         "opcao1": "Com as mãos",
         "opcao2": "Com a cabeça",
         "opcao3": "Com os pés",
         "resposta": "Com os pés",
         "explicacao": "No futebol, a bola é conduzida com os pés."},
        {"turma": "6º Ano - Anfitrião", "categoria": "exatas",
         "pergunta": "Qual destes é um esporte de combate?",
         "opcao1": "Vôlei",
         "opcao2": "Judô",
         "opcao3": "Atletismo",
         "resposta": "Judô",
         "explicacao": "Judô é uma arte marcial e esporte de combate."},
        {"turma": "6º Ano - Anfitrião", "categoria": "exatas",
         "pergunta": "Qual objeto é utilizado para jogar tênis de mesa?",
         "opcao1": "Raquete",
         "opcao2": "Cesta",
         "opcao3": "Bastão",
         "resposta": "Raquete",
         "explicacao": "O tênis de mesa usa raquete."},
        {"turma": "6º Ano - Anfitrião", "categoria": "exatas",
         "pergunta": "Qual atitude é importante durante a prática esportiva?",
         "opcao1": "Brigar com os colegas",
         "opcao2": "Desrespeitar as regras",
         "opcao3": "Respeitar os colegas",
         "resposta": "Respeitar os colegas",
         "explicacao": "Respeitar é fundamental no esporte."},
        {"turma": "6º Ano - Anfitrião", "categoria": "exatas",
         "pergunta": "O que significa trabalhar em equipe?",
         "opcao1": "Não participar da atividade",
         "opcao2": "Ajudar e colaborar com os colegas",
         "opcao3": "Fazer tudo sozinho",
         "resposta": "Ajudar e colaborar com os colegas",
         "explicacao": "Trabalhar em equipe é colaborar."},
        
        # ========== 11 a 20 ==========
        {"turma": "7º Ano - Visitante", "categoria": "exatas",
         "pergunta": "Qual destes é um exercício físico?",
         "opcao1": "Caminhada",
         "opcao2": "Dormir",
         "opcao3": "Assistir televisão",
         "resposta": "Caminhada",
         "explicacao": "Caminhada é um exercício físico."},
        {"turma": "7º Ano - Visitante", "categoria": "exatas",
         "pergunta": "A corrida faz parte de qual modalidade esportiva?",
         "opcao1": "Xadrez",
         "opcao2": "Tênis de mesa",
         "opcao3": "Atletismo",
         "resposta": "Atletismo",
         "explicacao": "A corrida faz parte do atletismo."},
        {"turma": "7º Ano - Visitante", "categoria": "exatas",
         "pergunta": "Qual esporte utiliza uma rede para separar os jogadores?",
         "opcao1": "Futebol",
         "opcao2": "Vôlei",
         "opcao3": "Atletismo",
         "resposta": "Vôlei",
         "explicacao": "O vôlei usa uma rede central."},
        {"turma": "7º Ano - Visitante", "categoria": "exatas",
         "pergunta": "A prática regular de exercícios físicos pode:",
         "opcao1": "Contribuir para a saúde",
         "opcao2": "Impedir qualquer movimento",
         "opcao3": "Aumentar o sedentarismo",
         "resposta": "Contribuir para a saúde",
         "explicacao": "Exercícios físicos contribuem para a saúde."},
        {"turma": "7º Ano - Visitante", "categoria": "exatas",
         "pergunta": "Qual destas é uma brincadeira?",
         "opcao1": "Prova escrita",
         "opcao2": "Leitura",
         "opcao3": "Pega-pega",
         "resposta": "Pega-pega",
         "explicacao": "Pega-pega é uma brincadeira popular."},
        {"turma": "7º Ano - Visitante", "categoria": "exatas",
         "pergunta": "O que é equilíbrio?",
         "opcao1": "Capacidade de permanecer estável",
         "opcao2": "Capacidade de correr muito rápido",
         "opcao3": "Capacidade de levantar muito peso",
         "resposta": "Capacidade de permanecer estável",
         "explicacao": "Equilíbrio é a capacidade de permanecer estável."},
        {"turma": "7º Ano - Visitante", "categoria": "exatas",
         "pergunta": "No jogo de queimado, qual é o objetivo principal?",
         "opcao1": "Fazer uma cesta",
         "opcao2": "Acertar os jogadores da equipe adversária com a bola",
         "opcao3": "Fazer gols em uma trave",
         "resposta": "Acertar os jogadores da equipe adversária com a bola",
         "explicacao": "No queimado, o objetivo é acertar os adversários."},
        {"turma": "7º Ano - Visitante", "categoria": "exatas",
         "pergunta": "Por que a alimentação saudável é importante?",
         "opcao1": "Porque substitui todos os exercícios",
         "opcao2": "Porque impede a prática esportiva",
         "opcao3": "Porque ajuda no funcionamento do organismo",
         "resposta": "Porque ajuda no funcionamento do organismo",
         "explicacao": "Alimentação saudável ajuda o organismo."},
        {"turma": "7º Ano - Visitante", "categoria": "exatas",
         "pergunta": "Qual destas alternativas apresenta um jogo de tabuleiro?",
         "opcao1": "Dama",
         "opcao2": "Futebol",
         "opcao3": "Natação",
         "resposta": "Dama",
         "explicacao": "Dama é um jogo de tabuleiro."},
        {"turma": "7º Ano - Visitante", "categoria": "exatas",
         "pergunta": "Antes de uma atividade física, é importante:",
         "opcao1": "Começar imediatamente sem preparação",
         "opcao2": "Fazer uma preparação adequada",
         "opcao3": "Evitar qualquer movimento",
         "resposta": "Fazer uma preparação adequada",
         "explicacao": "A preparação evita lesões."},
        
        # ========== 21 a 30 ==========
        {"turma": "8º Ano - Visitante", "categoria": "exatas",
         "pergunta": "Qual esporte é praticado com as mãos e uma bola, buscando marcar gols?",
         "opcao1": "Tênis",
         "opcao2": "Atletismo",
         "opcao3": "Handebol",
         "resposta": "Handebol",
         "explicacao": "Handebol é jogado com as mãos."},
        {"turma": "8º Ano - Visitante", "categoria": "exatas",
         "pergunta": "Qual destes esportes é praticado em uma piscina?",
         "opcao1": "Natação",
         "opcao2": "Futsal",
         "opcao3": "Handebol",
         "resposta": "Natação",
         "explicacao": "Natação é praticada na piscina."},
        {"turma": "8º Ano - Visitante", "categoria": "exatas",
         "pergunta": "No futebol, quem pode usar as mãos dentro da sua área?",
         "opcao1": "O atacante",
         "opcao2": "O goleiro",
         "opcao3": "O zagueiro",
         "resposta": "O goleiro",
         "explicacao": "Só o goleiro pode usar as mãos na área."},
        {"turma": "8º Ano - Visitante", "categoria": "exatas",
         "pergunta": "Qual atividade ajuda a desenvolver a coordenação motora?",
         "opcao1": "Dormir",
         "opcao2": "Assistir televisão",
         "opcao3": "Pular corda",
         "resposta": "Pular corda",
         "explicacao": "Pular corda desenvolve coordenação motora."},
        {"turma": "8º Ano - Visitante", "categoria": "exatas",
         "pergunta": "O que é flexibilidade?",
         "opcao1": "Capacidade de movimentar o corpo com amplitude",
         "opcao2": "Capacidade de correr mais rápido",
         "opcao3": "Capacidade de levantar mais peso",
         "resposta": "Capacidade de movimentar o corpo com amplitude",
         "explicacao": "Flexibilidade é a amplitude de movimento."},
        {"turma": "8º Ano - Visitante", "categoria": "exatas",
         "pergunta": "Qual esporte utiliza uma raquete e uma bola?",
         "opcao1": "Futebol",
         "opcao2": "Tênis",
         "opcao3": "Natação",
         "resposta": "Tênis",
         "explicacao": "Tênis usa raquete e bola."},
        {"turma": "8º Ano - Visitante", "categoria": "exatas",
         "pergunta": "Qual destes é um esporte individual?",
         "opcao1": "Futebol",
         "opcao2": "Vôlei",
         "opcao3": "Atletismo",
         "resposta": "Atletismo",
         "explicacao": "Atletismo pode ser individual."},
        {"turma": "8º Ano - Visitante", "categoria": "exatas",
         "pergunta": "O que devemos fazer quando um colega vence uma competição?",
         "opcao1": "Parabenizar e respeitar o colega",
         "opcao2": "Brigar com o colega",
         "opcao3": "Desistir da atividade",
         "resposta": "Parabenizar e respeitar o colega",
         "explicacao": "Respeitar e parabenizar é fair play."},
        {"turma": "8º Ano - Visitante", "categoria": "exatas",
         "pergunta": "Na brincadeira barra-bandeira, qual é um dos principais objetivos?",
         "opcao1": "Fazer uma cesta",
         "opcao2": "Capturar a bandeira da equipe adversária",
         "opcao3": "Fazer um gol",
         "resposta": "Capturar a bandeira da equipe adversária",
         "explicacao": "O objetivo é capturar a bandeira."},
        {"turma": "8º Ano - Visitante", "categoria": "exatas",
         "pergunta": "O dominó é um jogo que utiliza:",
         "opcao1": "Uma bola e uma rede",
         "opcao2": "Raquetes e uma mesa",
         "opcao3": "Peças com números ou símbolos",
         "resposta": "Peças com números ou símbolos",
         "explicacao": "Dominó usa peças numeradas."},
        
        # ========== 31 a 40 ==========
        {"turma": "9º Ano - Visitante", "categoria": "exatas",
         "pergunta": "O que é resistência física?",
         "opcao1": "Capacidade de realizar uma atividade durante determinado tempo",
         "opcao2": "Capacidade de ficar parado",
         "opcao3": "Capacidade de dormir por muito tempo",
         "resposta": "Capacidade de realizar uma atividade durante determinado tempo",
         "explicacao": "Resistência é a capacidade de durar."},
        {"turma": "9º Ano - Visitante", "categoria": "exatas",
         "pergunta": "Qual esporte utiliza uma raquete e uma rede?",
         "opcao1": "Futebol",
         "opcao2": "Tênis",
         "opcao3": "Atletismo",
         "resposta": "Tênis",
         "explicacao": "Tênis usa raquete e rede."},
        {"turma": "9º Ano - Visitante", "categoria": "exatas",
         "pergunta": "O que significa cooperação?",
         "opcao1": "Trabalhar sempre sozinho",
         "opcao2": "Impedir os colegas de participar",
         "opcao3": "Trabalhar junto para alcançar um objetivo",
         "resposta": "Trabalhar junto para alcançar um objetivo",
         "explicacao": "Cooperação é trabalhar junto."},
        {"turma": "9º Ano - Visitante", "categoria": "exatas",
         "pergunta": "Qual atitude demonstra respeito durante um jogo?",
         "opcao1": "Cumprir as regras",
         "opcao2": "Ofender o adversário",
         "opcao3": "Trapacear",
         "resposta": "Cumprir as regras",
         "explicacao": "Cumprir as regras é respeitar."},
        {"turma": "9º Ano - Visitante", "categoria": "exatas",
         "pergunta": "Qual é uma das funções do árbitro?",
         "opcao1": "Torcer por uma equipe",
         "opcao2": "Fiscalizar e aplicar as regras",
         "opcao3": "Participar como jogador",
         "resposta": "Fiscalizar e aplicar as regras",
         "explicacao": "O árbitro fiscaliza as regras."},
        {"turma": "9º Ano - Visitante", "categoria": "exatas",
         "pergunta": "Qual esporte é conhecido por utilizar uma bola oval?",
         "opcao1": "Natação",
         "opcao2": "Tênis de mesa",
         "opcao3": "Futebol americano",
         "resposta": "Futebol americano",
         "explicacao": "Futebol americano usa bola oval."},
        {"turma": "9º Ano - Visitante", "categoria": "exatas",
         "pergunta": "O que caracteriza o sedentarismo?",
         "opcao1": "Pouca ou nenhuma prática de atividades físicas",
         "opcao2": "Prática diária de esportes",
         "opcao3": "Participação em competições",
         "resposta": "Pouca ou nenhuma prática de atividades físicas",
         "explicacao": "Sedentarismo é falta de atividade física."},
        {"turma": "9º Ano - Visitante", "categoria": "exatas",
         "pergunta": "Beber água durante atividades físicas ajuda:",
         "opcao1": "A aumentar o cansaço",
         "opcao2": "Na hidratação do corpo",
         "opcao3": "A impedir os movimentos",
         "resposta": "Na hidratação do corpo",
         "explicacao": "Água hidrata o corpo."},
        {"turma": "9º Ano - Visitante", "categoria": "exatas",
         "pergunta": "O xadrez é um jogo que utiliza:",
         "opcao1": "Uma bola e uma rede",
         "opcao2": "Raquetes e uma mesa",
         "opcao3": "Um tabuleiro e peças",
         "resposta": "Um tabuleiro e peças",
         "explicacao": "Xadrez usa tabuleiro e peças."},
        {"turma": "9º Ano - Visitante", "categoria": "exatas",
         "pergunta": "O que significa fair play no esporte?",
         "opcao1": "Respeitar as regras, os adversários e o espírito esportivo",
         "opcao2": "Fazer qualquer coisa para vencer",
         "opcao3": "Desrespeitar o árbitro",
         "resposta": "Respeitar as regras, os adversários e o espírito esportivo",
         "explicacao": "Fair play é jogar com respeito."},
        
        # ========== 41 a 50 (Copa do Mundo 2026) ==========
        {"turma": "9º Ano - Visitante", "categoria": "exatas",
         "pergunta": "Qual seleção foi campeã da Copa do Mundo de 2026?",
         "opcao1": "Argentina",
         "opcao2": "Brasil",
         "opcao3": "Espanha",
         "resposta": "Espanha",
         "explicacao": "Espanha foi campeã em 2026."},
        {"turma": "9º Ano - Visitante", "categoria": "exatas",
         "pergunta": "Quais países sediaram juntos a Copa do Mundo de 2026?",
         "opcao1": "Brasil, Argentina e Chile",
         "opcao2": "Canadá, México e Estados Unidos",
         "opcao3": "Espanha, Portugal e Marrocos",
         "resposta": "Canadá, México e Estados Unidos",
         "explicacao": "Foram 3 países sede."},
        {"turma": "9º Ano - Visitante", "categoria": "exatas",
         "pergunta": "Quantas seleções participaram da Copa do Mundo de 2026?",
         "opcao1": "32 seleções",
         "opcao2": "40 seleções",
         "opcao3": "48 seleções",
         "resposta": "48 seleções",
         "explicacao": "2026 teve 48 seleções."},
        {"turma": "9º Ano - Visitante", "categoria": "exatas",
         "pergunta": "Quais são os nomes dos três mascotes oficiais da Copa do Mundo de 2026?",
         "opcao1": "Maple, Zayu e Clutch",
         "opcao2": "Willie, Juanito e Fuleco",
         "opcao3": "Goleo, Zakumi e La'eeb",
         "resposta": "Maple, Zayu e Clutch",
         "explicacao": "Esses são os mascotes."},
        {"turma": "9º Ano - Visitante", "categoria": "exatas",
         "pergunta": "Em que ano o Brasil conquistou sua última Copa do Mundo?",
         "opcao1": "1994",
         "opcao2": "2002",
         "opcao3": "2010",
         "resposta": "2002",
         "explicacao": "Brasil foi campeão em 2002."},
        {"turma": "9º Ano - Visitante", "categoria": "exatas",
         "pergunta": "Qual é o nome da bola oficial da Copa do Mundo de 2026?",
         "opcao1": "Brazuca",
         "opcao2": "Jabulani",
         "opcao3": "Trionda",
         "resposta": "Trionda",
         "explicacao": "A bola oficial de 2026 é a Trionda."},
        {"turma": "9º Ano - Visitante", "categoria": "exatas",
         "pergunta": "Quem é conhecido mundialmente como o 'Rei do Futebol'?",
         "opcao1": "Pelé",
         "opcao2": "Messi",
         "opcao3": "Cristiano Ronaldo",
         "resposta": "Pelé",
         "explicacao": "Pelé é o Rei do Futebol."},
        {"turma": "9º Ano - Visitante", "categoria": "exatas",
         "pergunta": "Quantas vezes Lionel Messi ganhou o prêmio Bola de Ouro?",
         "opcao1": "5 vezes",
         "opcao2": "8 vezes",
         "opcao3": "10 vezes",
         "resposta": "8 vezes",
         "explicacao": "Messi ganhou 8 Bolas de Ouro."},
        {"turma": "9º Ano - Visitante", "categoria": "exatas",
         "pergunta": "Quantas vezes Cristiano Ronaldo ganhou o prêmio Bola de Ouro?",
         "opcao1": "3 vezes",
         "opcao2": "4 vezes",
         "opcao3": "5 vezes",
         "resposta": "5 vezes",
         "explicacao": "Cristiano Ronaldo ganhou 5 Bolas de Ouro."},
        {"turma": "9º Ano - Visitante", "categoria": "exatas",
         "pergunta": "Qual seleção perdeu para a Espanha na final da Copa do Mundo de 2026?",
         "opcao1": "Argentina",
         "opcao2": "França",
         "opcao3": "Brasil",
         "resposta": "Argentina",
         "explicacao": "Argentina perdeu para a Espanha."},
        
        # ========== 51 a 55 ==========
        {"turma": "9º Ano - Visitante", "categoria": "exatas",
         "pergunta": "O que é ginástica de condicionamento físico?",
         "opcao1": "Uma atividade que busca melhorar a condição física e a saúde",
         "opcao2": "Uma atividade realizada somente para competir",
         "opcao3": "Uma brincadeira feita apenas com bola",
         "resposta": "Uma atividade que busca melhorar a condição física e a saúde",
         "explicacao": "Ginástica de condicionamento melhora a saúde."},
        {"turma": "9º Ano - Visitante", "categoria": "exatas",
         "pergunta": "O que são jogos eletrônicos?",
         "opcao1": "Jogos praticados somente em quadras",
         "opcao2": "Jogos realizados por meio de aparelhos eletrônicos",
         "opcao3": "Jogos praticados somente com peças de madeira",
         "resposta": "Jogos realizados por meio de aparelhos eletrônicos",
         "explicacao": "Jogos eletrônicos usam aparelhos eletrônicos."},
        {"turma": "9º Ano - Visitante", "categoria": "exatas",
         "pergunta": "Como é realizada a brincadeira amarelinha?",
         "opcao1": "Pulando sobre os espaços desenhados no chão",
         "opcao2": "Correndo atrás de uma bola para fazer gols",
         "opcao3": "Arremessando uma bola em uma cesta",
         "resposta": "Pulando sobre os espaços desenhados no chão",
         "explicacao": "Amarelinha é pulada no chão."},
        {"turma": "9º Ano - Visitante", "categoria": "exatas",
         "pergunta": "O que significa inclusão nas atividades de Educação Física?",
         "opcao1": "Permitir que somente os alunos com maior habilidade participem",
         "opcao2": "Separar os alunos durante as atividades",
         "opcao3": "Permitir a participação de todos, respeitando suas diferenças",
         "resposta": "Permitir a participação de todos, respeitando suas diferenças",
         "explicacao": "Inclusão é respeitar todos."},
        {"turma": "9º Ano - Visitante", "categoria": "exatas",
         "pergunta": "Quem criou o judô?",
         "opcao1": "Pelé",
         "opcao2": "Jigoro Kano",
         "opcao3": "Ayrton Senna",
         "resposta": "Jigoro Kano",
         "explicacao": "Jigoro Kano criou o judô."},
    ]
    
    conn = get_connection()
    cursor = conn.cursor()
    inseridas = 0
    
    for p in perguntas_quiz_ef:
        cursor.execute("""
            SELECT id FROM questoes 
            WHERE pergunta = ? AND turma = ?
        """, (p['pergunta'], p['turma']))
        
        if cursor.fetchone() is None:
            cursor.execute("""
                INSERT INTO questoes 
                (turma, categoria, pergunta, resposta, opcao1, opcao2, opcao3, explicacao)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                p['turma'],
                p['categoria'],
                p['pergunta'],
                p.get('resposta', ''),
                p.get('opcao1'),
                p.get('opcao2'),
                p.get('opcao3'),
                p.get('explicacao', '')
            ))
            inseridas += 1
    
    conn.commit()
    conn.close()
    print(f"✅ {inseridas} perguntas do Quiz de EF inseridas!")
    return inseridas

# ============================================================
# 🤖 MAIS 50 PERGUNTAS DE DEEPFAKE E IA
# ============================================================

def inserir_mais_deepfake_ia():
    """Insere mais 50 perguntas sobre Deepfake e IA"""
    
    perguntas_extras = [
        # ========== 🤖 DEEPFAKE (25) ==========
        {"turma": "6º Ano - Anfitrião", "categoria": "fake",
         "pergunta": "É verdade que deepfake pode ser usado para criar vídeos de pessoas famosas dizendo coisas que elas nunca disseram?",
         "resposta": "Verdade", "explicacao": "Sim! Deepfakes podem imitar qualquer pessoa."},
        {"turma": "6º Ano - Anfitrião", "categoria": "fake",
         "pergunta": "É verdade que todo deepfake é fácil de identificar a olho nu?",
         "resposta": "Fake", "explicacao": "Não! Muitos deepfakes são muito realistas."},
        {"turma": "6º Ano - Anfitrião", "categoria": "fake",
         "pergunta": "É verdade que devemos desconfiar de vídeos com movimentos estranhos nos olhos?",
         "resposta": "Verdade", "explicacao": "Sim! Olhos estranhos podem indicar deepfake."},
        {"turma": "6º Ano - Anfitrião", "categoria": "fake",
         "pergunta": "É verdade que deepfakes podem ser usados para criar boatos sobre a escola?",
         "resposta": "Verdade", "explicacao": "Sim! Deepfakes podem espalhar mentiras."},
        {"turma": "6º Ano - Anfitrião", "categoria": "fake",
         "pergunta": "É verdade que podemos confiar em qualquer vídeo que recebemos no celular?",
         "resposta": "Fake", "explicacao": "Não! Vídeos podem ser deepfakes."},
        {"turma": "7º Ano - Visitante", "categoria": "fake",
         "pergunta": "É verdade que deepfakes podem ser usados para criar notícias falsas com âncoras famosos?",
         "resposta": "Verdade", "explicacao": "Sim! Deepfakes podem imitar jornalistas."},
        {"turma": "7º Ano - Visitante", "categoria": "fake",
         "pergunta": "É verdade que toda deepfake é criada por criminosos?",
         "resposta": "Fake", "explicacao": "Não! Deepfakes também são usados em filmes e educação."},
        {"turma": "7º Ano - Visitante", "categoria": "fake",
         "pergunta": "É verdade que devemos verificar a fonte antes de compartilhar um vídeo?",
         "resposta": "Verdade", "explicacao": "Sim! Sempre verifique a fonte."},
        {"turma": "7º Ano - Visitante", "categoria": "fake",
         "pergunta": "É verdade que deepfakes podem ser usados para enganar pessoas por telefone?",
         "resposta": "Verdade", "explicacao": "Sim! Vozes podem ser clonadas por IA."},
        {"turma": "7º Ano - Visitante", "categoria": "fake",
         "pergunta": "É verdade que toda pessoa que aparece em vídeo é real?",
         "resposta": "Fake", "explicacao": "Não! Pode ser um deepfake."},
        {"turma": "8º Ano - Visitante", "categoria": "fake",
         "pergunta": "É verdade que existem softwares para detectar deepfakes?",
         "resposta": "Verdade", "explicacao": "Sim! Ferramentas ajudam a detectar deepfakes."},
        {"turma": "8º Ano - Visitante", "categoria": "fake",
         "pergunta": "É verdade que deepfakes podem ser usados em golpes financeiros?",
         "resposta": "Verdade", "explicacao": "Sim! Criminosos usam deepfakes para enganar."},
        {"turma": "8º Ano - Visitante", "categoria": "fake",
         "pergunta": "É verdade que toda deepfake é perfeita e impossível de detectar?",
         "resposta": "Fake", "explicacao": "Não! Deepfakes podem ter falhas."},
        {"turma": "8º Ano - Visitante", "categoria": "fake",
         "pergunta": "É verdade que deepfakes podem ser usados para manipular eleições?",
         "resposta": "Verdade", "explicacao": "Sim! Deepfakes políticos são uma ameaça."},
        {"turma": "8º Ano - Visitante", "categoria": "fake",
         "pergunta": "É verdade que podemos acreditar em qualquer áudio que recebemos?",
         "resposta": "Fake", "explicacao": "Não! Áudios podem ser clonados."},
        {"turma": "9º Ano - Visitante", "categoria": "fake",
         "pergunta": "É verdade que a lei brasileira pune quem cria deepfakes para prejudicar outros?",
         "resposta": "Verdade", "explicacao": "Sim! Criar deepfakes para prejudicar é crime."},
        {"turma": "9º Ano - Visitante", "categoria": "fake",
         "pergunta": "É verdade que deepfakes podem ser usados para extorsão?",
         "resposta": "Verdade", "explicacao": "Sim! Criminosos usam deepfakes para chantagear."},
        {"turma": "9º Ano - Visitante", "categoria": "fake",
         "pergunta": "É verdade que a educação midiática ajuda a combater deepfakes?",
         "resposta": "Verdade", "explicacao": "Sim! Aprender a analisar mídias é essencial."},
        {"turma": "9º Ano - Visitante", "categoria": "fake",
         "pergunta": "É verdade que deepfakes podem influenciar a opinião pública?",
         "resposta": "Verdade", "explicacao": "Sim! Deepfakes são uma ameaça à democracia."},
        {"turma": "9º Ano - Visitante", "categoria": "fake",
         "pergunta": "É verdade que toda IA é deepfake?",
         "resposta": "Fake", "explicacao": "Não! IA é uma tecnologia, deepfake é um uso."},
        {"turma": "9º Ano - Visitante", "categoria": "fake",
         "pergunta": "É verdade que devemos denunciar deepfakes falsos que encontramos?",
         "resposta": "Verdade", "explicacao": "Sim! Denunciar é uma forma de combater."},
        {"turma": "9º Ano - Visitante", "categoria": "fake",
         "pergunta": "É verdade que deepfakes podem ser usados para criar provas falsas?",
         "resposta": "Verdade", "explicacao": "Sim! Deepfakes podem ser usados em crimes."},
        {"turma": "9º Ano - Visitante", "categoria": "fake",
         "pergunta": "É verdade que podemos confiar em tudo que vemos na internet?",
         "resposta": "Fake", "explicacao": "Não! Sempre verifique."},
        {"turma": "9º Ano - Visitante", "categoria": "fake",
         "pergunta": "É verdade que deepfakes podem ser usados para criar conteúdo educativo?",
         "resposta": "Verdade", "explicacao": "Sim! Deepfakes podem ser usados para o bem."},
        {"turma": "9º Ano - Visitante", "categoria": "fake",
         "pergunta": "É verdade que precisamos de leis para regular deepfakes?",
         "resposta": "Verdade", "explicacao": "Sim! A regulação é essencial para proteger as pessoas."},
        
        # ========== 🧠 INTELIGÊNCIA ARTIFICIAL (25) ==========
        {"turma": "6º Ano - Anfitrião", "categoria": "fake",
         "pergunta": "É verdade que IA é uma tecnologia que faz máquinas aprenderem?",
         "resposta": "Verdade", "explicacao": "Sim! IA faz máquinas aprenderem."},
        {"turma": "6º Ano - Anfitrião", "categoria": "fake",
         "pergunta": "É verdade que a IA é um robô que pensa como um humano?",
         "resposta": "Fake", "explicacao": "Não! IA é um software, não um robô físico."},
        {"turma": "6º Ano - Anfitrião", "categoria": "fake",
         "pergunta": "É verdade que a IA está presente em celulares e assistentes virtuais?",
         "resposta": "Verdade", "explicacao": "Sim! Alexa, Siri e Google Assistente usam IA."},
        {"turma": "6º Ano - Anfitrião", "categoria": "fake",
         "pergunta": "É verdade que a IA sempre dá respostas corretas?",
         "resposta": "Fake", "explicacao": "Não! IA pode errar e dar informações falsas."},
        {"turma": "6º Ano - Anfitrião", "categoria": "fake",
         "pergunta": "É verdade que devemos verificar as informações que a IA nos dá?",
         "resposta": "Verdade", "explicacao": "Sim! Sempre verifique as informações!"},
        {"turma": "7º Ano - Visitante", "categoria": "fake",
         "pergunta": "É verdade que a IA pode aprender com os dados que recebe?",
         "resposta": "Verdade", "explicacao": "Sim! IA aprende com dados e melhora."},
        {"turma": "7º Ano - Visitante", "categoria": "fake",
         "pergunta": "É verdade que a IA é sempre neutra e sem preconceitos?",
         "resposta": "Fake", "explicacao": "Não! Se os dados forem preconceituosos, a IA também será."},
        {"turma": "7º Ano - Visitante", "categoria": "fake",
         "pergunta": "É verdade que a IA pode ajudar a resolver problemas sociais?",
         "resposta": "Verdade", "explicacao": "Sim! IA pode ajudar na saúde e educação."},
        {"turma": "7º Ano - Visitante", "categoria": "fake",
         "pergunta": "É verdade que a IA pode substituir totalmente os humanos?",
         "resposta": "Fake", "explicacao": "Não! IA complementa, mas não substitui."},
        {"turma": "7º Ano - Visitante", "categoria": "fake",
         "pergunta": "É verdade que devemos usar a IA com responsabilidade?",
         "resposta": "Verdade", "explicacao": "Sim! Ética e responsabilidade são fundamentais."},
        {"turma": "8º Ano - Visitante", "categoria": "fake",
         "pergunta": "É verdade que a IA pode criar textos, imagens e vídeos?",
         "resposta": "Verdade", "explicacao": "Sim! ChatGPT, DALL-E e outras IAs criam conteúdo."},
        {"turma": "8º Ano - Visitante", "categoria": "fake",
         "pergunta": "É verdade que a IA pode ser usada para espalhar fake news?",
         "resposta": "Verdade", "explicacao": "Sim! IAs podem criar textos e imagens falsas."},
        {"turma": "8º Ano - Visitante", "categoria": "fake",
         "pergunta": "É verdade que toda IA é confiável?",
         "resposta": "Fake", "explicacao": "Não! É preciso verificar as informações."},
        {"turma": "8º Ano - Visitante", "categoria": "fake",
         "pergunta": "É verdade que devemos citar quando usamos IA para criar algo?",
         "resposta": "Verdade", "explicacao": "Sim! Transparência é fundamental."},
        {"turma": "8º Ano - Visitante", "categoria": "fake",
         "pergunta": "É verdade que a IA pode ser usada para o bem e para o mal?",
         "resposta": "Verdade", "explicacao": "Sim! Depende de como usamos."},
        {"turma": "8º Ano - Visitante", "categoria": "fake",
         "pergunta": "É verdade que a IA pode aprender sozinha sem supervisão?",
         "resposta": "Verdade", "explicacao": "Sim! IA pode aprender sozinha, mas precisa de supervisão."},
        {"turma": "8º Ano - Visitante", "categoria": "fake",
         "pergunta": "É verdade que a IA pode ser usada para diagnósticos médicos?",
         "resposta": "Verdade", "explicacao": "Sim! IA ajuda em diagnósticos médicos."},
        {"turma": "8º Ano - Visitante", "categoria": "fake",
         "pergunta": "É verdade que a IA é sempre ética?",
         "resposta": "Fake", "explicacao": "Não! A ética da IA depende de quem a programa."},
        {"turma": "9º Ano - Visitante", "categoria": "fake",
         "pergunta": "É verdade que a IA pode tomar decisões sem intervenção humana?",
         "resposta": "Verdade", "explicacao": "Sim! Mas é preciso ter ética e supervisão."},
        {"turma": "9º Ano - Visitante", "categoria": "fake",
         "pergunta": "É verdade que a IA pode ser usada em armas autônomas?",
         "resposta": "Verdade", "explicacao": "Sim! E isso é um tema ético muito debatido."},
        {"turma": "9º Ano - Visitante", "categoria": "fake",
         "pergunta": "É verdade que a IA pode substituir empregos?",
         "resposta": "Verdade", "explicacao": "Sim! Mas também cria novas profissões."},
        {"turma": "9º Ano - Visitante", "categoria": "fake",
         "pergunta": "É verdade que a IA é sempre segura e sem riscos?",
         "resposta": "Fake", "explicacao": "Não! IA pode ter vieses, erros e ser usada para o mal."},
        {"turma": "9º Ano - Visitante", "categoria": "fake",
         "pergunta": "É verdade que precisamos de leis para regular a IA?",
         "resposta": "Verdade", "explicacao": "Sim! A regulação da IA é essencial."},
        {"turma": "9º Ano - Visitante", "categoria": "fake",
         "pergunta": "É verdade que a IA pode ajudar a combater fake news?",
         "resposta": "Verdade", "explicacao": "Sim! IA pode ajudar a identificar fake news."},
        {"turma": "9º Ano - Visitante", "categoria": "fake",
         "pergunta": "É verdade que a IA pode ser usada para criar arte e música?",
         "resposta": "Verdade", "explicacao": "Sim! IA pode criar arte e música."},
        {"turma": "9º Ano - Visitante", "categoria": "fake",
         "pergunta": "É verdade que a IA pode aprender com os erros?",
         "resposta": "Verdade", "explicacao": "Sim! IA aprende com erros e melhora."},
    ]
    
    conn = get_connection()
    cursor = conn.cursor()
    inseridas = 0
    
    for p in perguntas_extras:
        cursor.execute("""
            SELECT id FROM questoes 
            WHERE pergunta = ? AND turma = ?
        """, (p['pergunta'], p['turma']))
        
        if cursor.fetchone() is None:
            cursor.execute("""
                INSERT INTO questoes 
                (turma, categoria, pergunta, resposta, opcao1, opcao2, opcao3, explicacao)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                p['turma'],
                p['categoria'],
                p['pergunta'],
                p.get('resposta', ''),
                p.get('opcao1'),
                p.get('opcao2'),
                p.get('opcao3'),
                p.get('explicacao', '')
            ))
            inseridas += 1
    
    conn.commit()
    conn.close()
    print(f"✅ {inseridas} perguntas de Deepfake/IA inseridas!")
    return inseridas

# ============================================================
# 📋 FUNÇÕES DO QUESTIONÁRIO DE DIAGNÓSTICO
# ============================================================

def salvar_questionario(aluno_nome, aluno_turma, data, redes, fake, atitude, presenciou, reacao, opiniao, cidadania):
    """Salva as respostas do questionário"""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO questionario 
        (aluno_nome, aluno_turma, data, redes_sociais, fake_news, atitude_noticia, 
         presenciou_cyber, reacao_cyber, opiniao_agressividade, atitude_cidadania)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (aluno_nome, aluno_turma, data, redes, fake, atitude, presenciou, reacao, opiniao, cidadania))
    conn.commit()
    conn.close()


def listar_questionarios():
    """Lista todos os questionários"""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM questionario ORDER BY data DESC")
    questionarios = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return questionarios


def listar_questionarios_por_turma(turma):
    """Lista questionários de uma turma"""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM questionario WHERE aluno_turma = ? ORDER BY data DESC", (turma,))
    questionarios = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return questionarios


def contar_respostas(campo, valor=None):
    """Conta quantas respostas tem para um campo"""
    conn = get_connection()
    cursor = conn.cursor()
    
    if valor:
        cursor.execute(f"SELECT COUNT(*) FROM questionario WHERE {campo} = ?", (valor,))
    else:
        cursor.execute(f"SELECT {campo}, COUNT(*) FROM questionario GROUP BY {campo}")
    
    resultado = cursor.fetchall()
    conn.close()
    return resultado


def excluir_questionario(questionario_id):
    """Exclui um questionário"""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM questionario WHERE id = ?", (questionario_id,))
    conn.commit()
    conn.close()

# ============================================================
# 🔧 FUNÇÕES QUE FALTAVAM
# ============================================================

def listar_turmas():
    """Lista todas as turmas"""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM turmas ORDER BY nome")
    turmas = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return turmas


def listar_equipes_completas():
    """Lista todas as equipes com seus alunos"""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM equipes ORDER BY pontos DESC")
    equipes = [dict(row) for row in cursor.fetchall()]
    
    for equipe in equipes:
        cursor.execute("""
            SELECT aluno_nome FROM alunos_equipes 
            WHERE equipe_id = ?
        """, (equipe['id'],))
        equipe['alunos'] = [row['aluno_nome'] for row in cursor.fetchall()]
    
    conn.close()
    return equipes


def listar_juri():
    """Lista todos os argumentos do júri"""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM juri_simulado ORDER BY data DESC")
    juri = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return juri


def listar_cancelamentos():
    """Lista todos os cancelamentos"""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM cancelamento ORDER BY data DESC")
    cancelamentos = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return cancelamentos


def listar_analises():
    """Lista todas as análises de dados"""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM dados_desinformacao ORDER BY data DESC")
    analises = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return analises


def listar_campanhas():
    """Lista todas as campanhas"""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM campanhas ORDER BY data DESC")
    campanhas = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return campanhas


def listar_infograficos():
    """Lista todos os infográficos"""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM infograficos ORDER BY data DESC")
    infograficos = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return infograficos


def listar_podcasts():
    """Lista todos os podcasts"""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM podcasts ORDER BY data DESC")
    podcasts = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return podcasts


def listar_livros():
    """Lista todos os livros"""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM livros ORDER BY titulo ASC")
    livros = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return livros


def listar_atividades():
    """Lista todas as atividades"""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM atividades ORDER BY data ASC")
    atividades = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return atividades


def listar_dissecacoes():
    """Lista todas as dissecações"""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM disseca_algoritmo ORDER BY data DESC")
    disseca = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return disseca


def listar_debates():
    """Lista todos os debates"""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM debates ORDER BY data DESC")
    debates = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return debates


def listar_respostas_pbl():
    """Lista todas as respostas PBL"""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM respostas_pbl ORDER BY data DESC")
    respostas = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return respostas


def listar_respostas_pbl_aluno(aluno_nome, aluno_turma):
    """Lista as respostas PBL de um aluno"""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT * FROM respostas_pbl 
        WHERE aluno_nome = ? AND aluno_turma = ?
        ORDER BY data DESC
    """, (aluno_nome, aluno_turma))
    respostas = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return respostas

# ============================================================
# 🤖 GERADOR DE PERGUNTAS (IA SIMPLES)
# ============================================================

def gerar_pergunta_ia(categoria, turma):
    """Gera uma pergunta nova baseada nas existentes"""
    
    import random
    
    # ========== BANCO DE TEMPLATES ==========
    templates = {
        "fake": [
            "É verdade que {assunto}?",
            "Você acredita que {assunto}?",
            "É correto afirmar que {assunto}?",
            "Uma notícia diz que {assunto}. Isso é verdade?",
            "É fake ou verdade: {assunto}?"
        ],
        "cyber": [
            "É correto {assunto}?",
            "Você acha certo {assunto}?",
            "É ético {assunto}?",
            "Devemos {assunto}?",
            "É bullying {assunto}?"
        ],
        "etica": [
            "O que fazer quando {assunto}?",
            "Qual a atitude correta quando {assunto}?",
            "Como agir se {assunto}?",
            "Qual a melhor decisão quando {assunto}?",
            "O que é certo fazer se {assunto}?"
        ]
    }
    
    # ========== BANCO DE ASSUNTOS ==========
    assuntos = {
        "fake": [
            "um vídeo deepfake mostra uma pessoa famosa dizendo algo",
            "uma notícia diz que a escola vai fechar",
            "um áudio clonado por IA pede dinheiro",
            "uma imagem editada mostra um evento que não aconteceu",
            "um site desconhecido publica uma notícia bombástica",
            "uma corrente de WhatsApp fala de um perigo iminente",
            "uma IA cria uma notícia falsa sobre política",
            "um perfil falso espalha mentiras sobre um colega",
            "uma notícia antiga é republicada como nova",
            "um vídeo editado mostra uma briga que não existiu"
        ],
        "cyber": [
            "zombar de um colega nas redes sociais",
            "criar um perfil falso para enganar alguém",
            "compartilhar uma foto sem permissão",
            "excluir um colega do grupo da turma",
            "espalhar mentiras sobre um colega",
            "criar figurinhas humilhantes de alguém",
            "fazer comentários ofensivos sobre a aparência",
            "ameaçar alguém por mensagem",
            "divulgar o endereço de um colega",
            "gravar vídeos sem permissão"
        ],
        "etica": [
            "um colega posta uma fake news",
            "você vê alguém sofrendo cyberbullying",
            "um amigo compartilha um meme ofensivo",
            "você recebe um áudio clonado por IA",
            "um colega está sendo excluído do grupo",
            "você vê uma notícia suspeita",
            "um amigo pede para você compartilhar uma mentira",
            "você descobre que um colega usa IA para enganar",
            "um colega posta foto sua sem permissão",
            "você vê um comentário racista online"
        ]
    }
    
    # ========== GERAR PERGUNTA ==========
    if categoria in templates and categoria in assuntos:
        template = random.choice(templates[categoria])
        assunto = random.choice(assuntos[categoria])
        pergunta = template.format(assunto=assunto)
        
        # ========== GERAR OPÇÕES ==========
        if categoria == "fake":
            opcoes = ["Verdade", "Fake"]
            resposta = random.choice(opcoes)
        elif categoria == "cyber":
            opcoes = ["Sim", "Não"]
            resposta = random.choice(opcoes)
        else:
            opcoes = ["Opção A", "Opção B", "Opção C"]
            resposta = random.choice(opcoes)
        
        return {
            "turma": turma,
            "categoria": categoria,
            "pergunta": pergunta,
            "opcao1": opcoes[0] if len(opcoes) > 0 else "",
            "opcao2": opcoes[1] if len(opcoes) > 1 else "",
            "opcao3": opcoes[2] if len(opcoes) > 2 else "",
            "resposta": resposta,
            "explicacao": f"Pergunta gerada automaticamente pela IA. Sempre verifique a fonte!"
        }
    
    return None


def gerar_multiplas_perguntas(categoria, turma, quantidade=5):
    """Gera várias perguntas de uma vez"""
    perguntas = []
    for _ in range(quantidade):
        p = gerar_pergunta_ia(categoria, turma)
        if p:
            perguntas.append(p)
    return perguntas


def salvar_pergunta_gerada(pergunta):
    """Salva uma pergunta gerada no banco"""
    conn = get_connection()
    cursor = conn.cursor()
    
    # Verificar se já existe
    cursor.execute("""
        SELECT id FROM questoes 
        WHERE pergunta = ? AND turma = ?
    """, (pergunta['pergunta'], pergunta['turma']))
    
    if cursor.fetchone() is None:
        cursor.execute("""
            INSERT INTO questoes 
            (turma, categoria, pergunta, resposta, opcao1, opcao2, opcao3, explicacao)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            pergunta['turma'],
            pergunta['categoria'],
            pergunta['pergunta'],
            pergunta['resposta'],
            pergunta.get('opcao1'),
            pergunta.get('opcao2'),
            pergunta.get('opcao3'),
            pergunta.get('explicacao', '')
        ))
        conn.commit()
        conn.close()
        return True
    
    conn.close()
    return False

# ============================================================
# 🤖 INSERIR PERGUNTAS DE DEEPFAKE E IA
# ============================================================

def inserir_perguntas_deepfake_ia():
    """Insere as perguntas sobre Deepfake e IA"""
    
    perguntas = [
        # ========== 6º ANO ==========
        {"turma": "6º Ano - Anfitrião", "categoria": "fake",
         "pergunta": "É verdade que deepfake é um vídeo ou áudio falso criado por inteligência artificial?",
         "resposta": "Verdade",
         "explicacao": "Sim! Deepfake usa IA para criar vídeos e áudios falsos muito realistas."},
        
        {"turma": "6º Ano - Anfitrião", "categoria": "fake",
         "pergunta": "É verdade que a Inteligência Artificial pode aprender com os dados que recebe?",
         "resposta": "Verdade",
         "explicacao": "Sim! A IA aprende com dados e melhora com o tempo."},
        
        # ========== 7º ANO ==========
        {"turma": "7º Ano - Visitante", "categoria": "fake",
         "pergunta": "É verdade que deepfakes podem imitar a voz de uma pessoa real?",
         "resposta": "Verdade",
         "explicacao": "Sim! A IA pode clonar vozes e enganar pessoas por telefone."},
        
        {"turma": "7º Ano - Visitante", "categoria": "fake",
         "pergunta": "É verdade que a IA sempre dá respostas corretas?",
         "resposta": "Fake",
         "explicacao": "Não! A IA pode errar e dar informações falsas. Sempre verifique!"},
        
        # ========== 8º ANO ==========
        {"turma": "8º Ano - Visitante", "categoria": "fake",
         "pergunta": "É verdade que deepfakes podem ser usados para criar fake news políticas?",
         "resposta": "Verdade",
         "explicacao": "Sim! Deepfakes políticos são uma grande ameaça à democracia."},
        
        {"turma": "8º Ano - Visitante", "categoria": "fake",
         "pergunta": "É verdade que a IA pode criar textos, imagens e vídeos sozinha?",
         "resposta": "Verdade",
         "explicacao": "Sim! ChatGPT, DALL-E e outras IAs criam conteúdo automaticamente."},
        
        # ========== 9º ANO ==========
        {"turma": "9º Ano - Visitante", "categoria": "fake",
         "pergunta": "É verdade que deepfakes podem ser usados em golpes financeiros?",
         "resposta": "Verdade",
         "explicacao": "Sim! Criminosos usam deepfakes para se passar por parentes e pedir dinheiro."},
        
        {"turma": "9º Ano - Visitante", "categoria": "fake",
         "pergunta": "É verdade que a lei brasileira já pune quem cria deepfakes para prejudicar outros?",
         "resposta": "Verdade",
         "explicacao": "Sim! Criar deepfakes para prejudicar é crime no Brasil."},
        
        {"turma": "9º Ano - Visitante", "categoria": "fake",
         "pergunta": "É verdade que a IA pode ser usada para o bem e para o mal?",
         "resposta": "Verdade",
         "explicacao": "Sim! Depende de como usamos. A ética é fundamental!"},
        
        {"turma": "9º Ano - Visitante", "categoria": "fake",
         "pergunta": "É verdade que devemos verificar as informações que a IA nos dá?",
         "resposta": "Verdade",
         "explicacao": "Sim! Sempre verifique as informações, mesmo as geradas por IA!"},
    ]
    
    conn = get_connection()
    cursor = conn.cursor()
    inseridas = 0
    
    for p in perguntas:
        cursor.execute("""
            SELECT id FROM questoes 
            WHERE pergunta = ? AND turma = ?
        """, (p['pergunta'], p['turma']))
        
        if cursor.fetchone() is None:
            cursor.execute("""
                INSERT INTO questoes 
                (turma, categoria, pergunta, resposta, opcao1, opcao2, opcao3, explicacao)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                p['turma'],
                p['categoria'],
                p['pergunta'],
                p.get('resposta', ''),
                p.get('opcao1'),
                p.get('opcao2'),
                p.get('opcao3'),
                p.get('explicacao', '')
            ))
            inseridas += 1
    
    conn.commit()
    conn.close()
    print(f"✅ {inseridas} perguntas de Deepfake/IA inseridas!")
    return inseridas

# ============================================================
# 🧠 MAIS 20 PERGUNTAS DE INTER (Desafio Interdisciplinar)
# ============================================================

def inserir_mais_inter():
    """Insere mais 20 perguntas de Desafio Interdisciplinar"""
    
    perguntas = [
        # ========== 6º ANO ==========
        {"turma": "6º Ano - Anfitrião", "categoria": "inter",
         "pergunta": "Um aluno corre 300 metros em 1 minuto. Quantos metros corre em 4 minutos?",
         "opcao1": "900m", "opcao2": "1200m", "opcao3": "1500m",
         "resposta": "1200m", "explicacao": "300 × 4 = 1200 metros."},
        
        {"turma": "6º Ano - Anfitrião", "categoria": "inter",
         "pergunta": "Se 6 amigos compartilham 4 fake news cada, quantas fake news são compartilhadas?",
         "opcao1": "20", "opcao2": "24", "opcao3": "28",
         "resposta": "24", "explicacao": "6 × 4 = 24 fake news. Sempre verifique!"},
        
        {"turma": "6º Ano - Anfitrião", "categoria": "inter",
         "pergunta": "Um jogo de basquete tem 4 quartos de 12 minutos. Quantos minutos tem o jogo?",
         "opcao1": "36 min", "opcao2": "48 min", "opcao3": "60 min",
         "resposta": "48 min", "explicacao": "4 × 12 = 48 minutos."},
        
        {"turma": "6º Ano - Anfitrião", "categoria": "inter",
         "pergunta": "Se uma pessoa faz 40 minutos de exercício por dia, quantos minutos faz em 5 dias?",
         "opcao1": "160 min", "opcao2": "200 min", "opcao3": "240 min",
         "resposta": "200 min", "explicacao": "40 × 5 = 200 minutos."},
        
        {"turma": "6º Ano - Anfitrião", "categoria": "inter",
         "pergunta": "Uma fake news foi vista por 400 pessoas. Se 1/4 acreditou, quantas acreditaram?",
         "opcao1": "50", "opcao2": "100", "opcao3": "150",
         "resposta": "100", "explicacao": "1/4 de 400 = 100 pessoas."},
        
        # ========== 7º ANO ==========
        {"turma": "7º Ano - Visitante", "categoria": "inter",
         "pergunta": "Um atleta treina 4 horas por dia, 5 dias por semana. Quantas horas em 4 semanas?",
         "opcao1": "60h", "opcao2": "80h", "opcao3": "100h",
         "resposta": "80h", "explicacao": "4 × 5 = 20h/semana. 20 × 4 = 80 horas."},
        
        {"turma": "7º Ano - Visitante", "categoria": "inter",
         "pergunta": "Se uma corrida tem 12 km e você já correu 7.500 m, quantos metros faltam?",
         "opcao1": "3500m", "opcao2": "4500m", "opcao3": "5500m",
         "resposta": "4500m", "explicacao": "12 km = 12000 m. 12000 - 7500 = 4500 metros."},
        
        {"turma": "7º Ano - Visitante", "categoria": "inter",
         "pergunta": "Um jogador acertou 24 de 32 arremessos. Qual a porcentagem de acerto?",
         "opcao1": "65%", "opcao2": "70%", "opcao3": "75%",
         "resposta": "75%", "explicacao": "24 ÷ 32 = 0,75 = 75% de acerto."},
        
        {"turma": "7º Ano - Visitante", "categoria": "inter",
         "pergunta": "Se você queima 450 calorias por hora, quantas queima em 40 minutos?",
         "opcao1": "200", "opcao2": "300", "opcao3": "400",
         "resposta": "300", "explicacao": "450 ÷ 60 = 7,5 cal/min. 7,5 × 40 = 300 calorias."},
        
        {"turma": "7º Ano - Visitante", "categoria": "inter",
         "pergunta": "Um time ganhou 18 de 30 jogos. Qual a porcentagem de vitórias?",
         "opcao1": "50%", "opcao2": "60%", "opcao3": "70%",
         "resposta": "60%", "explicacao": "18 ÷ 30 = 0,6 = 60% de vitórias."},
        
        # ========== 8º ANO ==========
        {"turma": "8º Ano - Visitante", "categoria": "inter",
         "pergunta": "Um atleta corre 18 km em 1 hora e 30 minutos. Qual sua velocidade média em km/h?",
         "opcao1": "10 km/h", "opcao2": "12 km/h", "opcao3": "15 km/h",
         "resposta": "12 km/h", "explicacao": "18 km em 90 min = 18/(90/60) = 12 km/h."},
        
        {"turma": "8º Ano - Visitante", "categoria": "inter",
         "pergunta": "Se 5/6 dos alunos praticam esporte, quantos de 60 alunos praticam?",
         "opcao1": "40", "opcao2": "50", "opcao3": "60",
         "resposta": "50", "explicacao": "5/6 de 60 = 50 alunos praticam esporte."},
        
        {"turma": "8º Ano - Visitante", "categoria": "inter",
         "pergunta": "Um time fez 135 pontos em 9 jogos. Qual a média por jogo?",
         "opcao1": "12", "opcao2": "15", "opcao3": "18",
         "resposta": "15", "explicacao": "135 ÷ 9 = 15 pontos por jogo."},
        
        {"turma": "8º Ano - Visitante", "categoria": "inter",
         "pergunta": "Se você faz 5 séries de 12 repetições, quantas repetições no total?",
         "opcao1": "50", "opcao2": "60", "opcao3": "70",
         "resposta": "60", "explicacao": "5 × 12 = 60 repetições."},
        
        {"turma": "8º Ano - Visitante", "categoria": "inter",
         "pergunta": "Uma piscina olímpica tem 50 m. Quantas voltas para nadar 2.500 m?",
         "opcao1": "40", "opcao2": "50", "opcao3": "60",
         "resposta": "50", "explicacao": "2500 ÷ 50 = 50 voltas."},
        
        # ========== 9º ANO ==========
        {"turma": "9º Ano - Visitante", "categoria": "inter",
         "pergunta": "Um atleta melhorou seu tempo de 90s para 72s. Qual a melhoria percentual?",
         "opcao1": "10%", "opcao2": "15%", "opcao3": "20%",
         "resposta": "20%", "explicacao": "(90-72)/90 = 18/90 = 0,2 = 20% de melhoria."},
        
        {"turma": "9º Ano - Visitante", "categoria": "inter",
         "pergunta": "Se você queima 700 cal/hora, quantas horas para queimar 3.500 cal?",
         "opcao1": "4", "opcao2": "5", "opcao3": "6",
         "resposta": "5", "explicacao": "3500 ÷ 700 = 5 horas."},
        
        {"turma": "9º Ano - Visitante", "categoria": "inter",
         "pergunta": "Um time fez 180 pontos em 12 jogos. Qual a média? Se melhorar 25%, qual será?",
         "opcao1": "15 e 18,75", "opcao2": "15 e 20", "opcao3": "20 e 25",
         "resposta": "15 e 18,75", "explicacao": "180 ÷ 12 = 15. 15 × 1,25 = 18,75."},
        
        {"turma": "9º Ano - Visitante", "categoria": "inter",
         "pergunta": "Se um corredor faz 10 km em 45 min, quanto tempo leva para 15 km?",
         "opcao1": "60 min", "opcao2": "67,5 min", "opcao3": "75 min",
         "resposta": "67,5 min", "explicacao": "10 km → 45 min. 15 km → 67,5 min."},
        
        {"turma": "9º Ano - Visitante", "categoria": "inter",
         "pergunta": "Um atleta treina 6h/dia, 5 dias/semana. Quantas horas em 1 ano (52 semanas)?",
         "opcao1": "1200h", "opcao2": "1560h", "opcao3": "2000h",
         "resposta": "1560h", "explicacao": "6 × 5 × 52 = 1.560 horas por ano."},
    ]
    
    conn = get_connection()
    cursor = conn.cursor()
    inseridas = 0
    
    for p in perguntas:
        cursor.execute("""
            SELECT id FROM questoes 
            WHERE pergunta = ? AND turma = ?
        """, (p['pergunta'], p['turma']))
        
        if cursor.fetchone() is None:
            cursor.execute("""
                INSERT INTO questoes 
                (turma, categoria, pergunta, resposta, opcao1, opcao2, opcao3, explicacao)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                p['turma'],
                p['categoria'],
                p['pergunta'],
                p.get('resposta', ''),
                p.get('opcao1'),
                p.get('opcao2'),
                p.get('opcao3'),
                p.get('explicacao', '')
            ))
            inseridas += 1
    
    conn.commit()
    conn.close()
    print(f"✅ {inseridas} perguntas de inter inseridas!")
    return inseridas

# ============================================================
# 🧮 MAIS 10 PERGUNTAS DE MAT_FAKE
# ============================================================

def inserir_mais_mat_fake():
    """Insere mais 10 perguntas de Matemática + Cidadania"""
    
    perguntas = [
        {"turma": "6º Ano - Anfitrião", "categoria": "mat_fake",
         "pergunta": "Uma fake news foi compartilhada 150 vezes. Se cada pessoa compartilhar para 12 amigos, quantas verão?",
         "resposta": "1800", "explicacao": "150 × 12 = 1800 pessoas."},
        
        {"turma": "6º Ano - Anfitrião", "categoria": "mat_fake",
         "pergunta": "Se 4 em cada 10 notícias são fake, quantas fake news existem em 80 notícias?",
         "resposta": "32", "explicacao": "4/10 de 80 = 32 fake news."},
        
        {"turma": "7º Ano - Visitante", "categoria": "mat_fake",
         "pergunta": "Uma notícia falsa foi vista por 2.500 pessoas. Se 30% acreditaram, quantas acreditaram?",
         "resposta": "750", "explicacao": "30% de 2500 = 750 pessoas."},
        
        {"turma": "7º Ano - Visitante", "categoria": "mat_fake",
         "pergunta": "Um post fake tem 4.200 compartilhamentos por dia. Quantos em 10 dias?",
         "resposta": "42000", "explicacao": "4200 × 10 = 42.000 compartilhamentos."},
        
        {"turma": "8º Ano - Visitante", "categoria": "mat_fake",
         "pergunta": "Um vídeo fake teve 25.000 visualizações. Se 70% foram de pessoas diferentes, quantas viram?",
         "resposta": "17500", "explicacao": "70% de 25000 = 17.500 pessoas."},
        
        {"turma": "8º Ano - Visitante", "categoria": "mat_fake",
         "pergunta": "Se 15% das notícias são fake, quantas fake news há em 8.000 notícias?",
         "resposta": "1200", "explicacao": "15% de 8000 = 1.200 fake news."},
        
        {"turma": "8º Ano - Visitante", "categoria": "mat_fake",
         "pergunta": "Um site fake publicou 40 notícias falsas em 8 dias. Qual a média por dia?",
         "resposta": "5", "explicacao": "40 ÷ 8 = 5 notícias por dia."},
        
        {"turma": "9º Ano - Visitante", "categoria": "mat_fake",
         "pergunta": "Uma fake news atingiu 80.000 pessoas. Se 45% acreditaram, quantas foram enganadas?",
         "resposta": "36000", "explicacao": "45% de 80000 = 36.000 pessoas."},
        
        {"turma": "9º Ano - Visitante", "categoria": "mat_fake",
         "pergunta": "Se uma fake news cresce 30% ao dia, quantas pessoas verão em 3 dias a partir de 100?",
         "resposta": "219", "explicacao": "100 × 1,3 = 130 (dia 1); 130 × 1,3 = 169 (dia 2); 169 × 1,3 = 219,7 (dia 3)."},
        
        {"turma": "9º Ano - Visitante", "categoria": "mat_fake",
         "pergunta": "Se 1 fake news gera 6 novas a cada hora, quantas existirão em 5 horas?",
         "resposta": "7776", "explicacao": "6^5 = 7.776 fake news."},
    ]
    
    conn = get_connection()
    cursor = conn.cursor()
    inseridas = 0
    
    for p in perguntas:
        cursor.execute("""
            SELECT id FROM questoes 
            WHERE pergunta = ? AND turma = ?
        """, (p['pergunta'], p['turma']))
        
        if cursor.fetchone() is None:
            cursor.execute("""
                INSERT INTO questoes 
                (turma, categoria, pergunta, resposta, opcao1, opcao2, opcao3, explicacao)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                p['turma'],
                p['categoria'],
                p['pergunta'],
                p.get('resposta', ''),
                p.get('opcao1'),
                p.get('opcao2'),
                p.get('opcao3'),
                p.get('explicacao', '')
            ))
            inseridas += 1
    
    conn.commit()
    conn.close()
    print(f"✅ {inseridas} perguntas de mat_fake inseridas!")
    return inseridas