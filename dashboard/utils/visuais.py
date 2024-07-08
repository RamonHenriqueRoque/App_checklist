import plotly.graph_objects as go
import plotly.express as px
import streamlit as st
import pandas as pd

def histograma_quant_N_Residência(dataframe):
    df= dataframe[["ID", "N_Residencia"]].drop_duplicates()[["N_Residencia"]].value_counts().reset_index()
    fig = px.bar(data_frame= df,
                        y= "count",
                        x= "N_Residencia", 
                        text= "N_Residencia",
                        text_auto = True)
    
    fig.update_xaxes(type='category')
    fig.update_yaxes(showticklabels=False)
    fig.update_traces(marker=dict(color='#ffc107'), textfont_size=12, textangle=0, textposition="outside", cliponaxis=False) 

    fig.update_layout(bargap=0.2,
                      title = {'text': "Barra das quantidades de número de residência",
                               'y':0.9, # new
                               'x':0.5,
                               'xanchor': 'center',
                               'yanchor': 'top',
                               'font_family': "Times New Roman",
                               'font_color': "#ffffff",},
                      xaxis={'title': 'Nº de Residência'},
                      yaxis={'title': ''},
                      margin=dict(l=0, r=0, b=0, t=80, pad=0))

    return fig

def barra_prog(df):
    fig = px.bar(data_frame= df[["ID", "Linguagem_Programacao"]].drop_duplicates()[["Linguagem_Programacao"]].value_counts().reset_index(),
                 y= "count",
                 x= "Linguagem_Programacao",
                 text= "count",
                 text_auto = True,
                )
    fig.update_traces(marker=dict(color='#ffc107'), textfont_size=12, textangle=0, textposition="outside", cliponaxis=False) 
    fig.update_yaxes(showticklabels=False)
    fig.update_layout(bargap=0.2,
                      title = {'text': "Grafico barra de Linguegem de programação",
                               'y':0.9, # new
                               'x':0.5,
                               'xanchor': 'center',
                               'yanchor': 'top',
                               'font_family': "Times New Roman",
                               'font_color': "#ffffff",},
                      yaxis={'title':''},
                      xaxis={'title': 'Linguagem de Programação'},
                      margin=dict(l=0, r=0, b=0, t=80, pad=0))
    return fig

def barra_software(df):
    fig = px.bar(data_frame= df[["ID", "Software"]].drop_duplicates()[["Software"]].value_counts().reset_index(),
                 y= "count",
                 x= "Software",
                 text= "count",
                 text_auto = True)
    fig.update_traces(marker=dict(color='#ffc107'), textfont_size=12, textangle=0, textposition="outside", cliponaxis=False) 
    fig.update_yaxes(showticklabels=False)
    fig.update_layout(bargap=0.2,
                      title = {'text': "Grafico barra de Software",
                               'y':0.9, # new
                               'x':0.5,
                               'xanchor': 'center',
                               'yanchor': 'top',
                               'font_family': "Times New Roman",
                               'font_color': "#ffffff",},
                      yaxis={'title':''},
                      xaxis={'title': 'Software'},
                      margin=dict(l=0, r=0, b=0, t=80, pad=0))
    return fig

def barra_EstadoCivil_Genero(df):
    fig = px.bar(data_frame= df[["ID", "Estado Civil", "Genero"]].drop_duplicates()[["Estado Civil", "Genero"]].value_counts().reset_index(),
                 y= "count",
                 x= "Estado Civil",
                 color= "Genero",
                 text= "count",
                 text_auto = True,
                 color_discrete_map={'Feminino': '#ffe107',
                                     'Masculino': '#B39E05',
                                     'Outros': "#7F7104"},
                 barmode="group")
    fig.update_traces(textfont_size=12, textangle=0, textposition="outside", cliponaxis=False)
    fig.update_yaxes(showticklabels=False)
    fig.update_layout(bargap=0.2,
                      title = {'text': "Barra de Estado Civil por Gênero",
                               'y':0.9, # new
                               'x':0.5,
                               'xanchor': 'center',
                               'yanchor': 'top',
                               'font_family': "Times New Roman",
                               'font_color': "#ffffff",},
                      yaxis={'title':''},
                      xaxis={'title': 'Estado Civil'},
                      margin=dict(l=0, r=0, b=0, t=80, pad=0),
                      legend=dict(title= "Gênero"))
    return fig

def sunburst_comida(df):
    df = df[["ID", "Alergia", "Vegano", "Comidas"]].drop_duplicates()[["Alergia", "Vegano", "Comidas"]].value_counts().reset_index()
    df["Alergia"]= df["Alergia"].map({0 : "Não Alergico", 1 : "Alergico"})
    df["Vegano"]= df["Vegano"].map({0 : "Não Vegano/Vegetariano", 1 : "Vegano/Vegetariano"})

    fig = px.sunburst(df,
                      path= ["Alergia", "Vegano", "Comidas"],
                      values='count',
                      color= "Vegano",
                      color_discrete_map={'(?)':'#9e7609', 'Não Vegano/Vegetariano':'gold', 'Vegano/Vegetariano':'#F0B635'})
    
    fig.update_layout(title = {'text': "Alergia X Vegano/Vegetariano X Comida",
                            'y':0.9, # new
                            'x':0.5,
                            'xanchor': 'center',
                            'yanchor': 'top',
                            'font_family': "Times New Roman",
                            'font_color': "#ffffff",},
                    margin=dict(l=0, r=0, b=0, t=80, pad=0))

    return fig

def barra_personalidade(df):
    df = df[["ID", "Personalidade"]].drop_duplicates()["Personalidade"].value_counts().reset_index()
    df["Personalidade"] = df["Personalidade"].apply(lambda x: "".join(x[:4]))

    fig = px.bar(data_frame= df, y= "count", x= "Personalidade", text= "count")
    fig.update_traces(marker=dict(color='#ffc107'), textfont_size=12, textangle=0, textposition="outside", cliponaxis=False) 
    fig.update_yaxes(showticklabels=False)
    fig.update_layout(title = {'text': "Personalidade",
                            'y':0.9, # new
                            'x':0.5,
                            'xanchor': 'center',
                            'yanchor': 'top',
                            'font_family': "Times New Roman",
                            'font_color': "#ffffff",},
                    yaxis={'title':''},
                    xaxis={'title':'Personalidade'},
                    margin=dict(l=0, r=0, b=0, t=80, pad=0))
    return fig

def bar_ano_nascimento(df):
    df = df[["ID", "Data de Nascimento"]].drop_duplicates()
    df["Data de Nascimento"] = pd.to_datetime(df["Data de Nascimento"], dayfirst=True).dt.year.astype('str')
    df= df["Data de Nascimento"].value_counts().reset_index()
    
    fig = px.bar(data_frame= df,
                 y= "Data de Nascimento",
                 x= "count",
                 text= "count")
    
    fig.update_yaxes(type='category', categoryorder = 'total ascending')
    fig.update_traces(marker=dict(color='#ffc107'), textfont_size=12, textangle=0, textposition="outside", cliponaxis=False) 
    fig.update_layout(title = {'text': "Ano de Nascimento",
                            'y':0.9, # new
                            'x':0.5,
                            'xanchor': 'center',
                            'yanchor': 'top',
                            'font_family': "Times New Roman",
                            'font_color': "#ffffff",},
                    yaxis={'title':''},
                    xaxis={'title': ''},
                    margin=dict(l=0, r=0, b=0, t=80, pad=0))
    fig.update_xaxes(showticklabels=False)
    
    return fig

def mapa(df):
    df= df[["ID", "lat", "lon"]].drop_duplicates()
        
    fig = st.map(df, size=20, color='#ffc107', use_container_width = True)
    return fig
