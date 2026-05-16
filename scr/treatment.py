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
    Data = pd.DataFrame(resposta.data)
print(carregar_dados())