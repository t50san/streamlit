#from IPython.display import display
import streamlit as st
import pandas as pd 
import plotly.express as px 

data = pd.read_csv('Imports_Exports_Dataset new.csv')

st.title("Visualização de Dados de Importações e Exportações")

st.sidebar.header("Opções de Filtro")

pais_selecionado = st.sidebar.selectbox(
    "Selecione o País",
    options=data["Country"].unique(),
    index=0
)

tipo_selecionado = st.sidebar.radio(
    "Importação ou Exportação",
    options=data["Import_Export"].unique()
)

categorias_selecionadas = st.sidebar._multiselect(
    "Selecione Categorias",
    options=data['Category'].unique(),
    default=data['Category'].unique()
)

dados_filtrados = data[(data['Country']== pais_selecionado) & (data['Import_Export']== tipo_selecionado) & (data['Category'].isin(categorias_selecionadas))]

st.write(f'### Dados filtrados para - {pais_selecionado}', dados_filtrados)

quantidade_por_categoria = dados_filtrados.groupby('Category')['Quantity'].sum().reset_index() 
fig_quantidade = px.bar(quantidade_por_categoria, x='Category', y='Quantity', title=f'Quantidade Total por Categoria - {pais_selecionado}' )

st.plotly_chart(fig_quantidade)

valor_por_categoria = dados_filtrados.groupby('Category')['Value'].sum().reset_index()
fig_valor = px.pie(valor_por_categoria, names='Category', values='Value', title=f'Valor Total por Categoria - {pais_selecionado}')

st.plotly_chart(fig_valor)

dados_filtrados['Date'] = pd.to_datetime(dados_filtrados['Date'], format='%d-%m-%Y')
peso_ao_longo_tempo = dados_filtrados.groupby('Date')['Weight'].sum().reset_index()
fig_peso = px.line(peso_ao_longo_tempo, x = 'Date', y = 'Weight', title=f'Peso Total ao Longo do Tempo - {pais_selecionado}')
st.plotly_chart(fig_peso)

st.write('Esta aplicação utliza Pandas, Plotly e Streamlit para visualização de dados.')

