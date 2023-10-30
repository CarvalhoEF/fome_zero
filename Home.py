import streamlit as st
from PIL import Image
import pandas as pd
import plotly.express as px
import streamlit as st
from haversine import haversine
import plotly.graph_objects as go
import numpy as np
import inflection
import emoji
import matplotlib.pyplot as plt  
import folium as folium
from folium.plugins import MarkerCluster
from streamlit_folium import folium_static
import locale
st.set_page_config (page_title = 'Home page', page_icon='⚙️', layout='wide')


                    
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
    
# ============================================
# REALIZANDO A LIMPEZA DO DATAFRAME
# ============================================

df1 = clean_code (df1)

# ============================================
# Barra Lateral
# ============================================
st.sidebar.markdown ('# Fome Zero')

image_path = 'logo1.png'
image = Image.open ( image_path )
st.sidebar.image( image, width=100)


st.sidebar.markdown ('# Filtros')

default_options = ['Brazil', 'England', 'Canada', 'Australia']
country_options = st.sidebar.multiselect ('Escolha os Paises que Deseja visualizar as Informações:',
                                           df1['country_code'].unique(), default=default_options)


st.sidebar.write ('### Dados Tratados')


@st.cache_data
def convert_df(df1):
    # Função para converter o dataframe em um arquivo CSV
    return df1.to_csv().encode('utf-8')

csv = convert_df(df1)


st.sidebar.download_button(
    label="Download",
    data=csv,
    file_name='dados.csv',
    mime='text/csv')



st.sidebar.markdown( """---""" )
st.sidebar.markdown( '#### Powered by Elen Carvalho' )
                                           
#Filtro de seleção de Paises
linhas_selecionadas = df1['country_code'].isin (country_options)
df1 = df1.loc[linhas_selecionadas, :]                                       
                                           

# =======================================
# Layout no Streamlit
# =======================================


st.title( 'Fome Zero Growth Dashboard' )

st.container()

st.markdown ('### I. Problema de Negócio:')

st.markdown (" A empresa Fome Zero é uma marktplace de restaurantes. Ou seja, seu core business é facilitar o encontro e negociações de clientes e restaurantes. Os restaurantes fazem o cadastros dentro da plataforma da Fome Zero, que disponibiliza informações como endereço, tipo de culinária servida, se possui reservas, se faz entregas e também uma nota de avalição  dos serviços e produtos do restaurante, dentre outras informações. O conjunto de dados que representa o contexto está disponível na plataforma do Kaggle e disponível para download em Dados na barra lateral.  " )

st.markdown ('### II. Objetivo:')
st.markdown (""" 
                Fome Zero Dashboard foi construido para ajudar o time de négocio a tomar melhores decisões baseados nos dados mais relevantes encontrados na análise exploratória dos dados, fazendo uma pesquisa interativa com os filtros e as três principais visões do empreemdimento: 
                - Visão Países:
                - Visão Cidades: 
                - Visão Cozinhas e Restaurantes 
                """)

st.markdown (' ## O Melhor lugar para encontrar seu mais novo restaurante favorito!')

st.markdown ('### Temos as seguintes marcas dentro da nossa plataforma:')
st.container()
        
col1, col2, col3, col4, col5 = st.columns (5, gap='small')

with st.container():
    with col1:
        #Quantidade de restaurantes cadastrados
        df_aux = df1.loc[:, ['restaurant_id']].count()
        col1.metric ( label='Restaurantes Cadastrados', value=df_aux, help='Quantidade Restaurantes conforme filtro')
    
    with col2:
        #Quantidade de países 
        df_aux = df1.loc[:,'country_code'].nunique()
        col2.metric ( label='Países Selecionados', value=df_aux, help='Quantidade de Países conforme filtro')
    
    with col3:
        #Quantidade de cidades
        df_aux = df1.loc[:, 'city'].nunique()
        col3.metric ( label='Cidades Cadastradas', value=df_aux, help='Quantidade de Cidades conforme filtro')
    
    with col4:
        #Quantidade de Avaliações feitas na plataforma
        df_aux = df1.loc[:,'votes'].sum()
        locale.setlocale(locale.LC_ALL, '')
        df_aux = locale.format_string('%d', df_aux, grouping=True)
        col4.metric ( label='Avaliações na Plataforma', value=df_aux, help='Qtde Avaliações conforme filtro')
        
    with col5:
        #Quantidade de tipos de culinárias feitas na plataforma
        df_aux = df1.loc[:,'cuisines'].nunique()
        col5.metric ( label='Tipos de Culinárias Oferecidas', value=df_aux, help='Qtde Avaliações conforme filtro')
        

