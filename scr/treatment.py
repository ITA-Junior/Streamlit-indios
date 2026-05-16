import os 
import pandas as pd
import streamlit as st
from supabase import create_client, Client
from dotenv import load_dotenv
load_dotenv()
url: str = os.environ.get("SUPABASE_URL")
key: str = os.environ.get("SUPABASE_KEY")
supabase: Client = create_client(url, key)
@st.cache_data(ttl=600)
def carregar_dados():

    resposta = supabase.table("db").select("*").limit(100000).execute()
    Data = pd.DataFrame(resposta.data)
    return Data
df=carregar_dados()
categoria='Office Supplies'
categorias ='Category'
cidades = 'City'
parametro='Sales'
df_util=df[df[categorias]==categoria]

#AQUI TEMOS A FILA QUE INDICA TODOS OS DADOS DA CIDADE QUE RESPONDE À PERGUNTA 1
venda_max = df_util[df_util[parametro]==df_util[parametro].max()]
# AQUI TEMOS A CIDADE EM QUESTÃO JUNTAMENTE COM O SEU ÍNDICE (POSIÇAO NA TABELA GIGANTESCA)
venda_max[cidades]

datas = df.groupby('Order Date')
contagem_data=datas.count()
estados=df.groupby('State')
contagem_estados=estados.count()
cidades=df.groupby('City')
contagem_cidades=cidades.count()
contagem_cidades=contagem_cidades[0:10]
st.bar_chart(contagem_cidades)