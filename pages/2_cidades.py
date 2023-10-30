#Libraries
import pandas as pd
import plotly.express as px
import streamlit as st
from haversine import haversine
import plotly.graph_objects as go
import numpy as np
import inflection
import emoji
import matplotlib.pyplot as plt  

st.set_page_config (page_title = 'Cidades', page_icon='🏙️ ', layout='wide')
#=============================================================================
#Import o Dataset:
#=============================================================================


df = pd.read_csv("zomato.csv")


# -----------------------------------------------------------------------------
# Funções
# -----------------------------------------------------------------------------

#Limpeza do DataFrame

def clean_code(df1):
    """ Esta função tem a responsabilidade de limpar o dataframe:
        Tipos de limpeza:
        1. Remoção dos NaN
        2. emovendo a coluna 'Switch to order menu', pois todos os valores eram iguais
        3. Removendo linhas duplicadas
        4. categorizar, inicialmente, todos os restaurantes somente por um tipo de culinária
        
        Input:Dataframe
        Output:Dataframe
    """
    #Removendo linhas NaN.
    df1 = df1.dropna(subset=['cuisines'])
    
    #Removendo a coluna 'Switch to order menu', pois todos os valores eram iguais.
    df1 = df1.drop(columns = ['switch_to_order_menu'], axis = 1)
    
    #Removendo linhas duplicadas
    df1 = df1.drop_duplicates().reset_index() 
    
    #5. categorizar, inicialmente, todos os restaurantes somente por um tipo de culinária.
    df1["cuisines"] = df1.loc[:, "cuisines"].astype(str).apply(lambda x: x.split(",")[0])

    return df1



#1. Fazer uma cópia do dataframe lido e renomear as colunas do DataFrame.

def rename_columns(df):
    df_copy = df.copy()  # Crie uma cópia do DataFrame
    title = lambda x: inflection.titleize(x)
    snakecase = lambda x: inflection.underscore(x)
    spaces = lambda x: x.replace(" ", "")
    cols_old = list(df_copy.columns)
    cols_old = list(map(title, cols_old))
    cols_old = list(map(spaces, cols_old))
    cols_new = list(map(snakecase, cols_old))
    df_copy.columns = cols_new  # Altere as colunas na cópia
    return df_copy  # Retorne a cópia modificada
    
df1 = rename_columns(df)  # Atribua a cópia modificada de volta ao df1


#2. Para colocar o nome dos países com base no código de cada país. (Se você tiver dados em que os países são representados por IDs e desejar mapear esses IDs para nomes de países legíveis. Com essa função e o dicionário, você pode facilmente fazer essa correspondência)

COUNTRIES = {
    1: "India",
    14: "Australia",
    30: "Brazil",
    37: "Canada",
    94: "Indonesia",
    148: "New Zeland",
    162: "Philippines",
    166: "Qatar",
    184: "Singapure",
    189: "South Africa",
    191: "Sri Lanka",
    208: "Turkey",
    214: "United Arab Emirates",
    215: "England",
    216: "United States of America",
}
def country_name(country_id):
    return COUNTRIES[country_id]


#2.1Preenchimento dos nomes dos paises. 
df1['country_code'] =  df1.loc[:, 'country_code'].apply(lambda x: country_name(x))


#3. Criar a categoria do tipo de comida com base no range de valores.

def create_price_tye(price_range):
    if price_range == 1:
        return "cheap"
    elif price_range == 2:
        return "normal"
    elif price_range == 3:
        return "expensive"
    else:
        return "gourmet"

#3.1 Define categorias de preço de acordo com o range.
df1['price_range'] = df1['price_range'].apply(create_price_tye)



#4. Criar o nome das cores com base nos códigos de cores.(Essa função é útil quando você deseja padronizar os nomes das colunas em um DataFrame, especialmente se eles estiverem em diferentes formatos (por exemplo, com espaços ou letras maiúsculas). Ela ajuda a tornar os nomes das colunas mais consistentes e fáceis de trabalhar.)

COLORS = {
    "3F7E00": "darkgreen",
    "5BA829": "green",
    "9ACD32": "lightgreen",
    "CDD614": "orange",
    "FFBA00": "red",
    "CBCBC8": "darkred",
    "FF7800": "darkred",
}
def color_name(color_code):
    return COLORS[color_code]
    
#4.1 Define o padrão de cores das avaliações.
    df1['rating_color'] = df1['rating_color'].apply(color_name)


#Agrupar a quantidade de restaurantes por cidades, contar a quantidade e mostrar os 10 primeiros.
def top_ten_cities_restaurants(df1):
    df_aux = (df1.loc[:, ['city', 'restaurant_id', 'country_code']]
                      .groupby(['city', 'country_code'])
                      .nunique()
                      .sort_values('restaurant_id', ascending=False)
                      .head(10)
                      .reset_index())
    
    #impotar gráfico de barras
    fig = (px.bar(df_aux, x='city', y='restaurant_id', title='Top 10 cidades com mais restaurantes na base de dados',
                  text_auto=True, color='country_code', labels={'city':'Cidades', 'restaurant_id':'Quantidade de restaurantes', 'country_code' : 'País'}))

    return(fig)

# 1. Filtrar o DataFrame para manter apenas restaurantes com nota média acima de 4:
def count_restaurants_above(df1):
    restaurants_above_4 = df1['aggregate_rating'] > 4
    
    #2. Agrupar por cidade, fazer a contagem e mostrar a 7 primeiras:
    df_aux = (df1.loc[restaurants_above_4 , ['city', 'aggregate_rating', 'country_code' ]]
                 .groupby(['city','country_code'])
                 .count().sort_values('aggregate_rating', ascending=False)
                 .head(7)
                 .reset_index())
    
    fig = (px.bar(df_aux,x='city',y='aggregate_rating',title='As top 7 cidades com mais restaurantes com a média de avaliação acima de 4',
                  text_auto=True, color='country_code', labels={'city':'Cidades','aggregate_rating':'Quantidade de restaurantes','country_code':'País'}))
    return(fig)



# 1. Filtrar o DataFrame para manter apenas restaurantes com nota média abaixo de 2,5.
def  count_restaurants_below(df1):
    restaurants_below_4 = df1['aggregate_rating'] < 2.5
    
    #2. Agrupar por cidade, fazer a contagem
    
    df_aux = (df1.loc[restaurants_below_4, ['city', 'aggregate_rating', 'country_code' ]]
                 .groupby(['city', 'country_code'])
                 .count()
                 .sort_values('aggregate_rating', ascending=False)
                 .head(7)
                 .reset_index())
    
    fig = (px.bar(df_aux, x='city', y='aggregate_rating', title='As top 7 cidades com mais restaurantes com a média de avaliação abaixo de 2,5',
                  text_auto=True, color='country_code', labels={'city':'Cidades', 'aggregate_rating':'Quantidade de restaurantes','country_code':'País'}))
    return (fig)


# agrupar as cidades com culinária única, verificar pelo nunique e separar os 10 primeiros:
def cuisines_single(df1):
    df_aux = (df1.loc[:, ['city', 'country_code','cuisines']]
                     .groupby(['city', 'country_code'])
                     .nunique()
                     .sort_values('cuisines', ascending=False).reset_index().head(10))
    
    #importar o grafico de barras:
    fig = (px.bar(df_aux, x='city', y='cuisines', title='Top 10 Cidades com mais Restaurantes com Tipos Culinárias Únicos',
                  text_auto=True, color='country_code',labels={'cuisines':'Quantidade Tipos Culinárias Únicos',
                  'city':'Cidades','country_code' : 'País'}))
    return (fig)

#=============================================================================
#Limpando os dados:
#=============================================================================

df1 = clean_code(df1)

#=============================================================================
#Barra lateral no Stremlit
#=============================================================================
st.sidebar.markdown ('# Filtros')


default_options = ['Brazil', 'England', 'Canada', 'Australia', 'Indonesia']
country_options = st.sidebar.multiselect ('Escolha os países que deseja visualizar as informações:',
                                           df1['country_code'].unique(), default=default_options)


st.sidebar.markdown( """---""" )
                               
st.sidebar.markdown( '#### Powered by Elen Carvalho' )

#Filtro de seleção de países
linhas_selecionadas = df1['country_code'].isin (country_options)
df1 = df1.loc[linhas_selecionadas, :]  

#===================================================================================
#Layout no Stremlit
#===================================================================================

#VISÃO - Cidades

st.header(' 🏙️ Visão Cidades')

st.container()
#Gráfico com as 10 cidadeds com mais restaurantes na base de dados.
fig = top_ten_cities_restaurants(df1)
st.plotly_chart(fig, use_container_width=True,theme='streamlit')


st.container()
col1, col2 = st.columns(2)
with col1:
    #Gráfico com as 7 cidades com mais restaurantes com a média de avaliaçao acima de 4.
    fig = count_restaurants_above(df1)
    st.plotly_chart(fig, use_container_width=True,theme='streamlit')



with col2:
    #Gráfico com as 7 cidades com mais restaurantes com a média de avaliaçao abaixo de 2,5.
    fig = count_restaurants_below(df1)
    st.plotly_chart(fig, use_container_width=True,theme='streamlit')

st.container()
#Gráfico com as 10 cidades com tipos de cuinária único.
fig = cuisines_single(df1)
st.plotly_chart(fig, use_container_width=True,theme='streamlit')





























