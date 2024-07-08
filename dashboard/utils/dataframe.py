import sys
import os
import pandas as pd


# Adiciona o diretório 'checklist' ao sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
from services import sqlLite

def geral():
    sql = '''SELECT 
                ch.id_checklist AS ch_id_checklist,
                ch.id_aparelho AS ch_id_aparelho,
                ch.id_pessoal AS ch_id_pessoal,
                ch.id_conhecimento AS ch_id_conhecimento,
                ch.id_comida AS ch_id_comida,
                ch.id_personalidade AS ch_id_personalidade,
                ch.data_checklist AS ch_data_checklist,
                
                pe.id_pessoal AS pe_id_pessoal,
                pe.cep AS CEP,
                pe.nome AS pe_nome,
                pe.n_residencia AS pe_n_residencia,
                pe.data_nascimento AS pe_data_nascimento,
                pe.uf AS pe_uf,
                pe.cidade AS Cidade,
                pe.bairro AS pe_bairro,
                pe.endereco AS pe_endereco,
                pe.estado_civil AS pe_estado_civil,
                pe.genero AS pe_genero,
                pe.lon AS lon,
                pe.lat AS lat,
                
                ap.id_aparelho AS ap_id_aparelho,
                ap.nome_computador AS ap_nome_computador,
                ap.id_login AS ap_id_login,

                co.id_comida AS co_id_comida,
                co.alergia AS co_alergia,
                co.vegano_vegetariano AS co_vegano_vegetariano,

                per.id_personalidade AS per_id_personalidade,
                per.nome AS per_nome,

                cu.id_login AS cu_id_login,
                cu.nome_completo AS cu_nome_completo,

                lp.id_conhecimento AS lp_id_conhecimento,
                lp.nome AS Linguagem_Programacao,

                so.id_conhecimento AS so_id_conhecimento,
                so.nome AS Software,

                ca.id_comida AS co_id_comida,
                ca.nome AS Comidas


             FROM checklist AS ch
             FULL OUTER JOIN pessoal AS pe 
             ON ch.id_pessoal = pe.id_pessoal
             FULL OUTER JOIN aparelho AS ap
             ON ch.id_aparelho = ap.id_aparelho
             FULL OUTER JOIN comida AS co
             ON ch.id_comida = co.id_comida
             FULL OUTER JOIN personalidade AS per
             ON ch.id_personalidade = per.id_personalidade
             FULL OUTER JOIN cadastro_usuario AS cu
             on ap.id_login = cu.id_login
             FULL OUTER JOIN linguagem_programacao AS lp
             on ch.id_conhecimento = lp.id_conhecimento
             FULL OUTER JOIN software AS so
             on ch.id_conhecimento = so.id_conhecimento
             FULL OUTER JOIN cardapio AS ca
             on co.id_comida = ca.id_comida
             
            '''
    colunas, resultados = sqlLite.SQLite().db_execute(query= sql)

    colunas = [coluna[0] for coluna in colunas]
    
    df = pd.DataFrame(data= resultados,columns= colunas)

    df = df[['ch_id_checklist', 'ch_data_checklist', 
             'pe_nome', 'pe_n_residencia', 'pe_data_nascimento', "CEP", 'pe_uf', "Cidade",  'pe_bairro', 'pe_endereco', "lon", "lat", 'pe_estado_civil', 'pe_genero', 
             'ap_nome_computador', 
             'co_alergia', 'co_vegano_vegetariano', 
             'per_nome', 
             "cu_nome_completo", 
             "Linguagem_Programacao",
             "Software",
             "Comidas"]]
    df["ch_data_checklist"]= pd.to_datetime(df["ch_data_checklist"]).dt.date

    df.rename(columns={'ch_id_checklist' : "ID", 'ch_data_checklist' : "Data do Checklist", 'pe_nome' : "Nome da Pessoa", 'pe_n_residencia' : "N_Residencia", 
                       'pe_data_nascimento' : "Data de Nascimento", 'pe_uf' : "UF", 'pe_bairro' : "Bairro", 'pe_endereco' : "Endereço", 'pe_estado_civil' : "Estado Civil", 
                       'per_nome' : "Personalidade", 'pe_genero' : "Genero", "cu_nome_completo" : "Nome do Analista", 'co_alergia' : "Alergia", 'co_vegano_vegetariano' : "Vegano",
                       "ap_nome_computador": "Nome do Aparelho"}, inplace= True)
    df.dropna(inplace= True, subset = "Nome da Pessoa")
    return df

def card_linguagem(df = geral()):
    df = df[["ID", "Linguagem_Programacao"]].drop_duplicates()[["Linguagem_Programacao"]].value_counts().reset_index()
    try:
        return df["Linguagem_Programacao"].loc[0] + " - " + str(df["count"].loc[0])
    except:
        return "0"
    
def card_software(df = geral()):
    df = df[["ID", "Software"]].drop_duplicates()[["Software"]].value_counts().reset_index()

    try:
        return df["Software"].loc[0] + " - " + str(df["count"].loc[0])
    except:
        return "0"