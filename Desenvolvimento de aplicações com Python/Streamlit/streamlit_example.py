import streamlit as st
import folium
from streamlit_folium import folium_static as st_folium
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

def plota_pivot_table(df, value, index, func, ylabel, xlabel, opcao='nada'):
  if opcao == 'nada':
    pd.pivot_table(df, values=value, index=index,aggfunc=func).plot(figsize=[15, 5])
  elif opcao == 'unstack':
    pd.pivot_table(df, values=value, index=index,aggfunc=func).unstack().plot(figsize=[15, 5])
  elif opcao == 'sort':
    pd.pivot_table(df, values=value, index=index,aggfunc=func).sort_values(value).plot(figsize=[15, 5])
  plt.ylabel(ylabel)
  plt.xlabel(xlabel)
  return None


sinasc = pd.read_csv('C:\DEV\Datasets\input_M15_SINASC_RO_2019.csv')


# STREAMLIT

# STREAMLIT CONFIGURATION
st.set_page_config(page_title='Análise SINASC RO 2019', page_icon=':baby:', initial_sidebar_state='auto', layout='wide')

# Custom CSS for gradient background and container styling
st.markdown("""
    <style>
        .stApp {
            background: linear-gradient(to right, #c9d6ff, #e2e2e2);
            color: white;
            margin: 0 auto;
            
            
        }
        .main-title, .subheader, .stMarkdown, .stPlotlyChart, .stPyplot {
            color: black !important;
        }
        .main-title {
            font-size: 36px;
            font-weight: bold;
            text-align: center;
            margin-top: 20px;
        }
        .subheader {
            font-size: 24px;
            font-weight: bold;
            margin-bottom: 20px;
        }
        .container {
            padding: 20px;
            margin-bottom: 20px;
            border-radius: 10px;
            background-color: #c9d6ff
            border: 2px solid #e2e2e2;
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
            color: white;  /* Text color inside container */
        }
        .dataframe thead {
            color: white; /* Table header text color */
        }
        .dataframe tbody {
            color: white; /* Table body text color */
        }
    </style>
""", unsafe_allow_html=True)

# Main Title
st.markdown('<div class="main-title">Análise SINASC RO 2019</div>', unsafe_allow_html=True)
st.markdown('---')

# Subheader
st.markdown('<div class="subheader">Data Set</div>', unsafe_allow_html=True)
st.table(sinasc.head())
st.markdown('---')

# layout de duas colunas
col1, col2 = st.columns(2)

with col1:
  with st.container():
    # ajustando tamanho do container
    st.markdown('<style>div.Widget.row-widget.stRadio > div{flex-direction:row;}</style>', unsafe_allow_html=True)

    # SELECTBOX

    # titulo
    st.subheader('Quantidade de nascimentos por variável')

    # Capturando a variavel mes
    sinasc['MES'] = sinasc['DTNASC'].str[5:7]

    # criando um selectbox para escolher a variavel
    variavel = st.selectbox('Escolha uma variável para análise', ['IDADEMAE', 'ESCMAE', 'MES'])

    # Criando a figura e o eixo
    fig, ax = plt.subplots(figsize=(10, 5))

    # plotando o value counts da variavel escolhida sorted
    sinasc[variavel].value_counts().sort_index().plot(kind='bar', ax=ax)
    st.pyplot(fig)

with col2:
  # MAPA STREAMLIT

  # criando um mapa de value counts nascimento dos bebês por cada municipio em um mapa
  # latitude e longitude dos municipios já estão no dataframe sinasc nas colunas lat e long
  # então vamos usar essas colunas para plotar o mapa

  # titulo
  st.subheader('Mapa de nascimentos por município')

  sinasc_not_null = sinasc.dropna(subset=['munResLat', 'munResLon', 'munResNome'])

  # Calculando o número de nascimentos por município
  birth_counts = sinasc_not_null['munResNome'].value_counts().reset_index()
  birth_counts.columns = ['munResNome', 'nascimentos']

  # Mesclando as contagens de nascimentos com os dados de localização
  sinasc_not_null = sinasc_not_null.merge(birth_counts, on='munResNome')

  # Criando o mapa
  m = folium.Map(location=[-10.0, -62.0], zoom_start=7)

  # Adicionando pontos ao mapa
  for index, row in sinasc_not_null.iterrows():
    folium.CircleMarker(
      location=[row['munResLat'], row['munResLon']],
      radius=(row['nascimentos']**0.5)/5,  # Usando a raiz quadrada para suavizar o tamanho dos círculos
      popup=f"{row['munResNome']}: {row['nascimentos']} nascimentos",
      color='#3186cc',
      fill=True,
      fill_color='#3186cc'
    ).add_to(m)

  # Exibindo o mapa no Streamlit
  st_folium(m, width=700, height=500)

import time

'Starting a long computation...'

# Add a placeholder
latest_iteration = st.empty()
bar = st.progress(0)

for i in range(100):
  # Update the progress bar with each iteration.
  latest_iteration.text(f'Iteration {i+1}')
  bar.progress(i + 1)
  time.sleep(0.1)

st.write('...and now we\'re done!')

#%%
