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

st.set_page_config (page_title = 'Culinárias', page_icon=' 👨‍🍳 ', layout='wide')
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


#Gráfico para os melhores tipos de culinárias.
def top_cuisines_better(df1):
    df_aux = (df1.loc[:,['cuisines', 'aggregate_rating'] ]
                      .groupby('cuisines')
                      .mean()
                      .sort_values('aggregate_rating', ascending=False)
                      .head(qtde_rest)
                      .reset_index())
    
    fig = (px.bar(df_aux, x='cuisines', y='aggregate_rating', title=f'Top {qtde_rest} melhores tipos de culinárias',
                  text_auto=True, labels={'cuisines':'Tipo de Culinária','aggregate_rating':'Avaliação Média'}))
    
    return (fig)

#Gráfico para os piores tipos de culinárias.
def top_cuisines_worse(df1):
    df_aux = (df1.loc[:,['cuisines', 'aggregate_rating'] ]
                      .groupby('cuisines')
                      .mean()
                      .sort_values('aggregate_rating', ascending=True)
                      .head(qtde_rest)
                      .reset_index())
    
    fig = (px.bar(df_aux, x='cuisines', y='aggregate_rating', title=f'Top {qtde_rest} piores tipos de culinárias',
                  text_auto=True, labels={'cuisines':'Tipo de Culinária','aggregate_rating':'Avaliação Média'}))
    
    return (fig)


#Restaurantes mais avaliados.
def restaurants_rating(df1):
    restaurants_rating = (df1.loc[:,['restaurant_name','votes']]
                             .groupby('restaurant_name')
                             .sum()
                             .sort_values('votes', ascending=False)
                             .head(qtde_rest)
                             .reset_index())

    fig = (px.bar(restaurants_rating,x='restaurant_name',y='votes',title=f'Os Top {qtde_rest} restaurantes mais avaliados',
                  text_auto=True, labels={'restaurant_name': 'Nome do Restaurante', 'votes': 'Quantidade de Avaliações'}))
    
    return (fig)

def restaurantes_delivery(df1):
    # Filtrar os restaurantes que aceitam pedidos online e mostrar a nota média
    filtro = df1['has_online_delivery'] == 1
        
    # Listar os restaurantes que aceitam pedidos online
    restaurantes_delivery = (df1.loc[filtro,['restaurant_name', 'aggregate_rating']]
                               .groupby('restaurant_name')
                               .mean()
                               .sort_values(by='aggregate_rating', ascending=False)
                               .head(qtde_rest)
                               .reset_index())
            
    # Plotar o gráfico de barras dos restaurantes que faz pedidos online e as notas médias de cada
    fig = (px.bar(restaurantes_delivery, x='restaurant_name', y='aggregate_rating', title=f'Os TOP {qtde_rest} restaurantes que aceitam pedidos online',
                   text='votes',  labels={'restaurant_name': 'Nome do Restaurante', 'aggregate_rating': 'Nota Média', }))
  
    return (fig)



def data(df1):
    # Filtrar os restaurantes que fazem entrega (sim ou não)
    entrega_sim = df1[df1['has_online_delivery'] == 1]
    entrega_nao = df1[df1['has_online_delivery'] == 0]
    
    # Calcular a quantidade média de avaliações para cada categoria (faz entrega ou não)
    media_avaliacoes_sim = entrega_sim['votes'].mean()
    media_avaliacoes_nao = entrega_nao['votes'].mean()
    
    # Criar um novo DataFrame para os dados do gráfico
    data = (pd.DataFrame({'Entrega': ['Faz Entrega', 'Não Faz Entrega'],'Média de Avaliações': [media_avaliacoes_sim, media_avaliacoes_nao]}))
    
    # Criar um gráfico de pizza (pizza chart)
    fig = px.pie(data, names='Entrega', values='Média de Avaliações', title='Média de Avaliações X Tipo de Entrega')
    
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

#Filtro de seleção de países
linhas_selecionadas = df1['country_code'].isin (country_options)
df1 = df1.loc[linhas_selecionadas, :]  

st.sidebar.markdown( """---""" )


qtde_rest = st.sidebar.slider('Selecione a quantidade de restaurantes que deseja visualizar:', 0, 10, 20)


st.sidebar.markdown( """---""" )

default2_options = ['Italian', 'European']
cuisines_options = st.sidebar.multiselect ('Escolha os Tipos de Culinária:',
                                           df1['cuisines'].unique(), default=default2_options)


#Filtro de seleção de culinárias

linhas_selecionadas = df1['cuisines'].isin (cuisines_options)
df1 = df1.loc[linhas_selecionadas, :] 


st.sidebar.markdown( """---""" )
                               
st.sidebar.markdown( '#### Powered by Elen Carvalho' )


#===================================================================================
#Layout no Stremlit
#===================================================================================

#VISÃO - Culinárias

st.header('🥘Visão Tipos de Culinárias/Restaurantes')

tab1, tab2 = st.tabs( ['Culinárias', 'Restaurantes'])

with tab1:
    st.markdown ('## Melhores Restaurantes dos Principais tipos Culinários')
    with st.container():
        col1, col2 = st.columns(2)
       
        with col1:
            #Qual a melhor culinária e a nota média agregada:
            # Calcular a contagem de votos por culinária
            df_counts = df1.loc[:, ['cuisines', 'votes', 'aggregate_rating','country_code', 'city']].groupby(['cuisines', 'country_code', 'city']).count().head(qtde_rest)
            df_counts = df_counts.rename(columns={'votes': 'count_votes'})
            
            # Calcular a média da avaliação agregada (average rating) por culinária
            df_avg_rating = df1.loc[:, ['cuisines', 'aggregate_rating']].groupby('cuisines').mean().head(qtde_rest)
            df_avg_rating = df_avg_rating.rename(columns={'aggregate_rating': 'average_rating'})
                   
            # Combinar os resultados em um único DataFrame
            result = df_counts.join(df_avg_rating, on='cuisines').reset_index()
            
            # Ordenar os resultados pelo número de votos e, em caso de empate, pela média da avaliação agregada
            result = result.sort_values(['count_votes', 'average_rating'], ascending=[False, False])
            
            # Escolha a métrica e o valor para exibir 
            metric_label = "Culinária com a maior contagem de votos"
            metric_value = f"{result.iloc[0, 0]}, {result.iloc[0, 3]} votos"
            metric_help = f"Média da avaliação,{result.iloc[0, 5]:.2} - Cidade:{result.iloc[0, 2]} - País:{result.iloc[0, 1]}"
            
            st.metric(metric_label, metric_value, metric_help )
                    
        with col2:
            # Calcular a contagem de votos por culinária
            df_counts = df1.loc[:, ['cuisines', 'votes', 'aggregate_rating', 'country_code', 'city']].groupby(['cuisines', 'country_code', 'city']).count().head(qtde_rest)
            df_counts = df_counts.rename(columns={'votes': 'count_votes'})
            
            # Calcular a média da avaliação agregada (average rating) por culinária
            df_avg_rating = df1.loc[:, ['cuisines', 'aggregate_rating']].groupby('cuisines').mean().head(qtde_rest)
            df_avg_rating = df_avg_rating.rename(columns={'aggregate_rating': 'average_rating'})
                   
            # Combinar os resultados em um único DataFrame
            result = df_counts.join(df_avg_rating, on='cuisines').reset_index()
            
            # Ordenar os resultados pelo número de votos e, em caso de empate, pela média da avaliação agregada
            result = result.sort_values(['count_votes', 'average_rating'], ascending=[True, True])
            
            # Escolha a métrica e o valor para exibir 
            metric_label = "Culinária com a menor contagem de votos"
            metric_value = f"{result.iloc[0, 0]}, {result.iloc[0, 3]} votos"
            metric_help = f"Média da avaliação,{result.iloc[0, 5]:.2} - Cidade:{result.iloc[0, 2]} - País:{result.iloc[0, 1]}"
            
            st.metric(metric_label, metric_value,  metric_help )
    


    with st.container():
        
        st.write(f'## Top {qtde_rest} Restaurantes \n')
        #Tabela com os Restaurantes com maior pontuação
        df_aux = (df1.loc[:,['restaurant_id', 'restaurant_name', 'country_code', 'city', 'cuisines', 'average_cost_for_two', 'aggregate_rating','votes']]
                     .sort_values(['aggregate_rating','restaurant_id'], ascending=[False, True])
                     .head(qtde_rest)
                     .reset_index(drop=True))
        
        st.dataframe(df_aux)
        
                                  
                    
    with st.container():
            #Gráfico de barras com o melhor tipo de culinára.
            fig = top_cuisines_better(df1)
            st.plotly_chart (fig, use_container_width=True, theme='streamlit')
        
        
    with st.container():
            #Gráfico de barras com o pior tipo de culinária.
            fig = top_cuisines_worse(df1)
            st.plotly_chart (fig, use_container_width=True, theme='streamlit')


with tab2:
    with st.container():
        st.markdown ('Restaurantes que fazem reservas e tem nota média acima de 4')
        # Filtrar os restaurantes que fazem reservas com nota média acima de 4
        filtro = (df1['has_table_booking'] == 1) & (df1['aggregate_rating'] > 4)
        
        # Filtrar o DataFrame com base no filtro
        restaurantes_filtrados = df1[filtro]
        
        # Listar os melhores restaurantes com base na nota média
        restaurantes = restaurantes_filtrados[['restaurant_name', 'cuisines', 'aggregate_rating', 'votes', 'city', 'country_code']].sort_values('aggregate_rating', ascending=False)
        st.dataframe(restaurantes)

    with st.container():
        
        #Os (quantidade definida pelo filtro) Restaurantes mais avaliados.
        fig = restaurants_rating(df1)
        st.plotly_chart(fig, use_container_width=True,theme='streamlit')
    

    with st.container():
        
        #Os (quantidade definida pelo filtro) restaurantes que aceitam pedidos on-line.
        fig = restaurantes_delivery(df1)
        st.plotly_chart(fig, use_container_width=True,theme='streamlit')

    
    with st.container():
        #Restaurantes (quantidade definida pelo filtro) que fazm entrega X Quatidade média de avaliações
        fig = data(df1)
        st.plotly_chart(fig, use_container_width=True,theme='streamlit')


