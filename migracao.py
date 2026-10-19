import pandas
import sqlite3

ARQUIVO_CSV = "Tabela_Escola_2025_V2.csv"
BANCO_DADOS = "censo_escolar.db"
TAMANHO_BLOCO = 50000

ESTADOS_ALVO = [
    "AL", "BA", "CE", "MA", "PB", "PE", "PI", "RN", "SE",
    "ES", "MG", "RJ", "SP"
]

# Ordem EXATA do enunciado e do CSV (no_entidade primeiro, co_entidade em segundo)
COLUNAS_EXATAS = [
    "no_entidade", "co_entidade", "no_uf", "sg_uf", "co_uf",
    "no_municipio", "co_municipio", "nu_ano_censo", "qt_mat_bas",
    "qt_mat_inf", "qt_mat_fund", "qt_mat_med", "qt_mat_prof",
    "qt_mat_eja", "qt_mat_esp"
]

def executar_migracao():
    conn = sqlite3.connect(BANCO_DADOS)
    cursor = conn.cursor()

    # Criação da tabela seguindo a ordem exata do professor
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS instituicoes (
            no_entidade TEXT,
            co_entidade INTEGER PRIMARY KEY,
            no_uf TEXT,
            sg_uf TEXT,
            co_uf INTEGER,
            no_municipio TEXT,
            co_municipio INTEGER,
            nu_ano_censo INTEGER,
            qt_mat_bas INTEGER,
            qt_mat_inf INTEGER,
            qt_mat_fund INTEGER,
            qt_mat_med INTEGER,
            qt_mat_prof INTEGER,
            qt_mat_eja INTEGER,
            qt_mat_esp INTEGER
        )
    """)
    conn.commit()

    leitor = pandas.read_csv(
        ARQUIVO_CSV,
        sep=";",
        encoding="latin1",
        chunksize=TAMANHO_BLOCO,
        low_memory=False
    )

    for bloco in leitor:
        bloco.columns = bloco.columns.str.lower().str.replace('ï»¿', '')
        
        # Garante a filtragem e a ordem exata das colunas
        colunas_filtradas = [c for c in COLUNAS_EXATAS if c in bloco.columns]
        bloco = bloco[colunas_filtradas]
        bloco_filtrado = bloco[bloco['sg_uf'].isin(ESTADOS_ALVO)]

        if not bloco_filtrado.empty:
            bloco_filtrado.to_sql('instituicoes', conn, if_exists='append', index=False)

    conn.close()
    print("Migração concluída com sucesso na ordem exata solicitada!")

if __name__ == "__main__":
    executar_migracao()