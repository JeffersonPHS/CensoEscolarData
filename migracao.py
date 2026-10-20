import pandas
import sqlite3

ARQUIVO_CSV = "Tabela_Escola_2025_V2.csv"
BANCO_DADOS = "censo_escolar.db"
TAMANHO_BLOCO = 50000

ESTADOS_ALVO = [
    "AL", "BA", "CE", "MA", "PB", "PE", "PI", "RN", "SE",
    "ES", "MG", "RJ", "SP"
]


COLUNAS_EXATAS = [
    "no_entidade", "co_entidade", "no_uf", "sg_uf", "co_uf",
    "no_municipio", "co_municipio", "nu_ano_censo", "qt_mat_bas",
    "qt_mat_inf", "qt_mat_fund", "qt_mat_med", "qt_mat_prof",
    "qt_mat_eja", "qt_mat_esp"
]

def executar_migracao():
    conn = sqlite3.connect(BANCO_DADOS)
    cursor = conn.cursor()
    
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

    leitorCaractere = pandas.read_csv(
        ARQUIVO_CSV,
        sep=";",
        encoding="latin1",
        chunksize=TAMANHO_BLOCO,
        low_memory=False
    )

    for bloco in leitorCaractere:

        bloco.columns = bloco.columns.str.lower().str.replace('ï»¿', '')
        
        
        colunasFiltradas = [coluna for coluna in COLUNAS_EXATAS if coluna in bloco.columns]


        bloco = bloco[colunasFiltradas]


        blocoFiltrado = bloco[bloco['sg_uf'].isin(ESTADOS_ALVO)]


        if not blocoFiltrado.empty:


            blocoFiltrado.to_sql('instituicoes', conn, if_exists='append', index=False)


    conn.close()


if __name__ == "__main__":
    executar_migracao()