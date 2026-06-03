import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.title('Hello streamlit')
st.write('Este é o meu primeiro aplicativo com streamlit')

st.header('Fodasse')
st.subheader('cu')

data = {
    'Nome': ['Paracuru', 'Mosquitao', 'Paje'],
    'Idade': [19, 20, 21],
    'Salario': [1500, 1500, 1500]
}

df = pd.DataFrame(data)

st.dataframe(df)
st.table(df)

fig, ax = plt.subplots()

ax.bar(df['Nome'], df['Salario'])

st.pyplot(fig)

if st.button('Clique aqui'):
    st.write('Botão clicado')

idade = st.slider('Selecione sua idade', 0, 100, 25)
st.write(f'Idade selecionada: {idade}')

opcao = st.selectbox(
    'Escolha um departamento:',
    ['Recursos HUmanos', 'TI','Vendas']
)

st.write(f'Departamento selecionado: {opcao}')

col1, col2 = st.columns(2)

with col1:
    st.header('Coluna 1')
    st.write('Conteudo da coluna 1.')

with col2:
    st.header('Coluna 2')
    st.write('Conteudo da coluna 2.')

st.sidebar.header('Filtros')
preço = st.sidebar.slider('Preço minimo', 0, 100, 19)