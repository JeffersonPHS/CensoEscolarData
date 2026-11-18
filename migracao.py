import pandas
import os
from sqlalchemy import create_engine
from dotenv import load_dotenv

load_dotenv()


ARQUIVO_CSV = "Tabela_Escola_2025_V2.csv"
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



    BancoDados_url = f"postgresql+psycopg2://{os.getenv('DB_USER')}:{os.getenv('DB_PASS')}@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}"





    engine = create_engine(BancoDados_url)

    leitorCaractere = pandas.read_csv(
        ARQUIVO_CSV,
        sep=";",
        encoding="latin1",
        chunksize=TAMANHO_BLOCO,
        low_memory=False
    )

    blocos_inseridos = 0






    for bloco in leitorCaractere:
        
        bloco.columns = bloco.columns.str.lower().str.replace('ï»¿', '')
        
        for coluna in COLUNAS_EXATAS:
            if coluna not in bloco.columns:
                bloco[coluna] = 0

        bloco = bloco[COLUNAS_EXATAS]

        bloco = bloco.fillna(0)

        blocoFiltrado = bloco[bloco['sg_uf'].isin(ESTADOS_ALVO)]





        if not blocoFiltrado.empty:
            blocoFiltrado.to_sql('instituicoes', engine, if_exists='append', index=False)
            
            blocos_inseridos += 1
            




if __name__ == "__main__":
    executar_migracao()