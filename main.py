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

    resposta = supabase.table("db").select("*").execute()
    df = pd.DataFrame(resposta.data)


# --- CONSTRUÇÃO DA TELA DO STREAMLIT ---
st.set_page_config(page_title="Projeto ITA Jr", layout="wide")

st.title("Dashboard de Vendas - ITA Jr 🚀")

st.write("Conectando ao Supabase e carregando a planilha...")

# Chama a função para criar o DataFrame
df_vendas = carregar_dados()

# Verifica se deu certo e mostra na tela
if df_vendas is not None:
    if not df_vendas.empty:
        st.success("Conexão bem-sucedida! Veja a sua base de dados no formato Pandas:")
        # Mostra as primeiras linhas para não pesar a tela
        st.dataframe(df_vendas.head(10)) 
    else:
        st.warning("Conectou com sucesso, mas a tabela 'db' está vazia no Supabase.")