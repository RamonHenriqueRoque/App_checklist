import streamlit as st
from utils import dataframe, visuais
from streamlit_extras.metric_cards import style_metric_cards
import flet as ft

#Conf da pagina
st.set_page_config(
    page_title="Checklist",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={'About': "Mais informação: https://www.linkedin.com/in/ramonhroque/"}
    )

df= dataframe.geral()
df_aba3= df.loc[df["ID"] == df["ID"].max()].copy()

with st.sidebar:
    st.get_option("theme.base")
    st.image("assets/icons/Logo Ramon WHITE.png")
    st.title("Checklist 📊")
    st.divider()
            
    with st.expander('Sobre'):
        st.write('Bem-vindo ao nosso painel de controle interativo! Esta página foi projetada para fornecer uma visão clara e abrangente dos principais indicadores e métricas essenciais para o seu negócio.')
    
    st.divider()
    
    st.markdown('__Filtros__')
    filtro_nome_pessoa = st.multiselect(label = "Nome do usuário", options= df["Nome da Pessoa"].unique(), placeholder= "Selecione o nome abaixo.")        
    filtro_uf = st.multiselect(label = "UF", options= df["UF"].unique(), placeholder= "Selecione o UF abaixo.")
    filtro_estado_civil = st.multiselect(label = "Estado Civil", options= df["Estado Civil"].unique(), placeholder= "Selecione o estado civil abaixo.")
    filtro_genero = st.multiselect(label = "Gênero", options= df["Genero"].unique(), placeholder= "Selecione o gênero abaixo.")
    filtro_alergia = st.radio(label = "Alegia", options= ["Sim ✔️", "Não ❌", "Ambas"], index= 2)
    filtro_vegano = st.radio(label = "Vegano", options= ["Sim ✔️", "Não ❌", "Ambas"], index= 2)
    filtro_personalidade = st.multiselect(label = "Personalidade", options= df["Personalidade"].unique(), placeholder= "Selecione o personalidade abaixo.")

    filtro_data_min = st.date_input(label= "Data de checklist (Inicial)",
                                    value =  df["Data do Checklist"].min(),
                                    min_value= df["Data do Checklist"].min(),
                                    max_value= df["Data do Checklist"].max())
    filtro_data_max = st.date_input(label= "Data de checklist (Final)",
                                    value =  df["Data do Checklist"].max(),
                                    min_value= df["Data do Checklist"].min(),
                                    max_value= df["Data do Checklist"].max())
    
    st.divider()
    st.markdown("""
                LinkedIn → [Ramon Roque](https://www.linkedin.com/in/ramonhroque/)
                ---
                """)

if filtro_nome_pessoa:
    df= df[df["Nome da Pessoa"].isin(filtro_nome_pessoa)]
if filtro_uf:
    df= df[df["UF"].isin(filtro_uf)]
if filtro_estado_civil:
    df= df[df["Estado Civil"].isin(filtro_estado_civil)]
if filtro_genero:
    df= df[df["Genero"].isin(filtro_genero)]
if filtro_alergia:
    if filtro_alergia == "Sim ✔️":
        df= df[df["Alergia"] == 1]
    elif filtro_alergia == "Não ❌":
        df= df[df["Alergia"] == 0]
    else:
        df= df[df["Alergia"].isin([0, 1])]
if filtro_vegano:
    if filtro_vegano == "Sim ✔️":
        df= df[df["Vegano"].isin([1])]
    elif filtro_vegano == "Não ❌":
        df= df[df["Vegano"].isin([0])]
    elif filtro_vegano == "Ambas":
        df= df[df["Vegano"].isin([0, 1])]
if filtro_personalidade:
    df= df[df["Personalidade"].isin(filtro_personalidade)]

if filtro_data_min:
    df= df.loc[(df["Data do Checklist"] >= filtro_data_min) & (df["Data do Checklist"] <= filtro_data_max)]
if filtro_data_max:
    df= df.loc[(df["Data do Checklist"] >= filtro_data_min) & (df["Data do Checklist"] <= filtro_data_max)]

#Titulo
t1, t2 = st.columns((0.1,1)) 

with t1:
    t1.image('assets/icons/icon-Dash.png')
with t2:
    t2.title("Dashboard do Checklist")
    t2.write("Email de contato: hramonroque@gmail.com")

#Cards
card_1, card_2, card_3, card_4 = st.columns(4)
card_1.metric(label= "Quantidade Checklist", value= df["ID"].nunique())
card_2.metric(label= "% Checklist", value= df["ID"].nunique() / dataframe.geral()["ID"].nunique() * 100)
card_3.metric(label= "Top 1 - Linguagem", value= dataframe.card_linguagem(df))
card_4.metric(label= "Top 1 - Software", value= dataframe.card_software(df))
style_metric_cards(background_color = "#282a36", border_color = "#ffffff", border_left_color = "#ffffff")

#Estrutura
aba1, aba2, aba3 = st.tabs(["Tabela", "Analise", "Ultimo Checklist"])

with aba1:
    st.dataframe(df)
    st.caption('Tabela completa com todas as informações inseridas.')

    @st.cache_data
    def convert_df(df):
        # IMPORTANT: Cache the conversion to prevent computation on every rerun
        return df.to_csv().encode("utf-8")

    st.download_button(label="Download dos dados em CSV",
                       data=convert_df(dataframe.geral()),
                       file_name="Dados_checklist.csv",
                       mime="text/csv")

with aba2:
    col, col0 = st.columns(2)
    with col:
        st.plotly_chart(visuais.barra_prog(df), use_container_width= True)
    with col0:
        st.plotly_chart(visuais.barra_software(df), use_container_width= True)
        
    st.divider()
    col1, col2, col3 = st.columns(3)
    with col1:
        st.plotly_chart(visuais.sunburst_comida(df), use_container_width= True)
        st.caption('Clicar nos circulos centrais para ter um cenário mais específico.')
    with col2:
        st.plotly_chart(visuais.bar_ano_nascimento(df), use_container_width= True)
    with col3:
        st.plotly_chart(visuais.barra_personalidade(df), use_container_width= True)

    st.divider()
    col4, col5 = st.columns(2)
    with col4:
        st.plotly_chart(visuais.histograma_quant_N_Residência(df), use_container_width= True)
    with col5:
        st.plotly_chart(visuais.barra_EstadoCivil_Genero(df), use_container_width= True)

    st.divider()
    st.subheader("Mapa das localizações com base no CEP inserido.")
    visuais.mapa(df)
    
with aba3:
    st.markdown("<h1 style='text-align: center; color: white;'>Ultimo Checklist Realizado.</h1>", unsafe_allow_html=True)
    st.container(height= 1, border= False)

    col6, col7 = st.columns(2)
    with col6:
        st.markdown(f"<h6 style='text-align: center; color: white;'>Nome do analista: {df_aba3['Nome do Analista'].unique()[0]}</h6>", unsafe_allow_html=True)
    with col7:
        st.markdown(f"<h6 style='text-align: center; color: white;'>Data do checklist: {df_aba3['Data do Checklist'].unique()[0]}</h6>", unsafe_allow_html=True)

    col8, col9, col10, col11 = st.columns(4)
    col8.metric(label= "Nome do usuário", value= df_aba3['Nome da Pessoa'].unique()[0])
    col9.metric(label= "Número de Residência", value= df_aba3['N_Residencia'].unique()[0])
    col10.metric(label= "Estado Civil", value= df_aba3['Estado Civil'].unique()[0])
    col11.metric(label= "Gênero", value= df_aba3['Genero'].unique()[0])

    
    st.divider()
    col12, col13 = st.columns(2)
    with col12:
        linguagem = ", ".join(df_aba3['Linguagem_Programacao'].unique())
        software = ", ".join(df_aba3['Software'].unique())
        
        st.write(f"Linguagem de Programação: {linguagem[::-1].replace(',', ' e ', 1)[::-1]}")
        st.write(f"Software: {software[::-1].replace(',', ' e ', 1)[::-1]}")
    with col13:
        personalidade = df_aba3['Personalidade'].unique()[0]
        st.write(f"Personalidade: {personalidade[::-1].replace(',', ' e ', 1)[::-1]}")
    st.divider()

    col14, col15 = st.columns(2)
    with col14:
        st.plotly_chart(visuais.sunburst_comida(df_aba3), use_container_width= True)
        st.caption('Clicar nos circulos centrais para ter um cenário mais específico.')
    with col15:
        st.markdown(f"<h6 style='text-align: center; color: white'>Mapa de localização com base no CEP inserido.</h6>", unsafe_allow_html=True)
        visuais.mapa(df_aba3)

    st.divider()
    st.markdown(f"<h6 style='text-align: center; color: white'>Tabela completa</h6>", unsafe_allow_html=True)
    st.dataframe(df_aba3)