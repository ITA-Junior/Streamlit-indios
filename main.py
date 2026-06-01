import os
import pandas as pd
import streamlit as st
from supabase import create_client, Client
from dotenv import load_dotenv
import scr.treatment as tr

df = tr.carregar_dados()
df = tr.formatar(df)

def questao1():
    data=df[df["Category"]=="Office Supplies"]
    return data[data['Sales'] == data['Sales'].max()]


st.set_page_config(page_title='Dashboard - ITAJr',layout='wide')
aba1,aba2,aba3,aba4=st.tabs(['Visão Geral','Análises 1','Análises 2','Conclusões'])

with aba1:
    st.header("Visão Geral")
    