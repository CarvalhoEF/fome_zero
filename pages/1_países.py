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
import folium as folium
from folium.plugins import MarkerCluster
from streamlit_folium import folium_static

st.set_page_config (page_title = 'Países', page_icon='🌎', layout='wide')
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
    

#agrupar a quantidade de restaurante por país e contar.
def number_restaurants_country(df1):
    df_aux= (df1.loc[:,['restaurant_id','country_code']]
                     .groupby('country_code')
                     .nunique()
                     .sort_values('restaurant_id', ascending=False)
                     .reset_index())
    
    #importar o gráfico de barras:
    fig = (px.bar(df_aux, x='country_code', y='restaurant_id', title='Quantidade de Restaurantes Registrados por País',
                 text_auto=True, labels={'restaurant_id':'Quantidade de restaurantes','country_code' : 'Países'}))
    return(fig)
    
#agrupar a quantidade de cidades por país e contar:
def city_country(df1):
    df_aux= (df1.loc[:,['city','country_code']]
                     .groupby('country_code')
                     .nunique().sort_values('city', ascending=False)
                     .reset_index())
    
    #importar o gráfico de barras:
    fig = (px.bar(df_aux, x='country_code', y='city', title='Quantidade de Cidades Registrados por País',
                  text_auto=True, labels={'city':'Cidades','country_code' : 'Países'}))
    return (fig)

# Agrupar as avaliações por pais e calcular a média:
def avg_country(df1):
    df_aux = (df1.loc[:, ['votes','country_code']]
                     .groupby('country_code')
                     .mean().sort_values('votes', ascending=False)
                     .reset_index())
    
    #importar o gráfico de barras:
    fig = px.bar(df_aux, x='country_code', y='votes', title='Média de avaliações feita por país',
                 text_auto=True, labels={'votes':'Quantidade de Avaliações','country_code' : 'Países'})
    return (fig)

#Agrupar o preço de prato para dois por país e calcular a média:
def avg_coubtry_cost(df1):
    df_aux = (df1.loc[:,['country_code', 'average_cost_for_two', 'currency']]
                      .groupby(['country_code', 'currency'])
                      .mean().sort_values('average_cost_for_two', ascending=False)
                      .reset_index())
    
    #importar o gráfico de barras:
    fig = (px.bar(df_aux, x='country_code', y='average_cost_for_two', title='Média do preço de prato para duas pessoas por país',
                  text_auto=True,text= 'currency', labels={'average_cost_for_two':'Preço de prato para duas pessoas','country_code':'Países','currency': 'Moeda'}))
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

#VISÃO - PAÍS

st.header(' 🌎 Visão Países')

tab1, tab2 = st.tabs( ['Visão Gerencial', 'Visão Geográfica'])


with tab1:
    with st.container():

        #Gráfico de barras com o número de restaurantes por país
        fig = number_restaurants_country(df1)
        st.plotly_chart(fig, use_container_width=True,theme='streamlit')
        
        
        st.container()
        
        #Gráfico de barras com o número de cidades registradas por país
        fig = city_country(df1)
        st.plotly_chart(fig, use_container_width=True,theme='streamlit')
        
        
        
        st.container()
        col1, col2 = st.columns(2)
        with col1:
            #Gráfico de barras com a média de avaliações registradas por país
            fig = avg_country(df1)
            st.plotly_chart(fig, use_container_width=True,theme='streamlit')
        
        
        
        with col2:
            #Gráfico de barras na 2ª coluna com a média de Preço de Prato para Duas Pessoas registradas por país
            fig = avg_coubtry_cost(df1)
            st.plotly_chart(fig, use_container_width=True,theme='streamlit')


with tab2:
    with st.container():
        st.write ('## Mapa com a Localização dos restaurantes')

        df_aux = (df1.loc[:, ['city', 'aggregate_rating', 'currency', 'cuisines', 'rating_color', 'restaurant_id','latitude', 'longitude', 'average_cost_for_two', 'restaurant_name']]
             .groupby(['city', 'cuisines','rating_color', 'currency', 'restaurant_id', 'restaurant_name'])
             .median().reset_index())


        map1 = folium.Map()
        marker_cluster = folium.plugins.MarkerCluster().add_to(map1)
        
                            
        for i in range ( len(df_aux) ):
            popup_html = f'<div style="width: 250px;">' \
                         f"<b>{df_aux.loc[i, 'restaurant_name']}</b><br><br>" \
                         \
                         f"Preço para dois: {df_aux.loc[i, 'average_cost_for_two']:.2f} ( {df_aux.loc[i, 'currency']})<br> " \
                         f"Type: {df_aux.loc[i, 'cuisines']}<br>" \
                         f"Nota: {df_aux.loc[i, 'aggregate_rating']}/5.0" \
                         f'</div>'
            folium.Marker ([df_aux.loc[i, 'latitude'], df_aux.loc[i, 'longitude']],
                           popup=popup_html, width=500, height=500, tooltip='clique aqui', parse_html=True,  
                           zoom_start=30, tiles= 'Stamen Toner', 
                           icon=folium.Icon(color=df_aux.loc[i, 'rating_color'] , icon='home')).add_to(marker_cluster)
            
        folium_static(map1)


















