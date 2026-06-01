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
    resposta = supabase.table("db").select("*").limit(10000).execute()
    Data = pd.DataFrame(resposta.data)
    return Data
df=carregar_dados()

def formatar():
    df['Order Date']=pd.to_datetime(df['Order Date'],format='%Y-%m-%d')
    df['Day']=df["Order Date"].dt.day
    df['Month']=df['Order Date'].dt.month
    df['Year']=df['Order Date'].dt.year
    df['Date']=df['Month'].astype(str)+"//"+df['Year'].astype(str)
    return df

