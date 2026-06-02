import os
import pandas as pd
import streamlit as st
from supabase import create_client, Client
from dotenv import load_dotenv
import scr.treatment as tr

df = tr.carregar_dados()
df = tr.formatar()
refinado=tr.refinamento()
def questao1():
    data=df[df["Category"]=="Office Supplies"]
    return data[data['Sales'] == data['Sales'].max()]
um=questao1()
um=um.iloc[0]


st.set_page_config(page_title='Dashboard - ITAJr',layout='wide')
aba1,aba2,aba3,aba4=st.tabs(['Visão Geral','Análises 1','Análises 2','Conclusões'])

with aba1:
    st.header("Visão Geral")
    st.write("Aqui, mostramos uma tabela portando apenas os dados mais importantes das operações da empresa.")
    st.write(f"Foram ao todo {len(refinado)} operações realizadas ao longo de {((df['Order Date'].max()-df['Order Date'].min()).days)//7} semanas")
    st.write(f'em {refinado["City"].nunique()} cidades.')
    st.dataframe(refinado)

with aba2:
    st.subheader("Análise na categoria \"Office Supplies\":")
    st.write(f"A melhor venda foi realizada em {um['City']} no dia {um['Order Date']}")
    st.write(f"vendendo em {um['Sales']:.2f} reais, o que gerou um lucro de R${um['Profit']:.2f}")
    st.info("Insight: Essa cidade pode ser um polo regional de vendas desse tipo de produto, sugerindo investimento e campanhas.")

    st.divider()

    st.subheader("Total de vendas, em reais, por data: ")
    limite_inferior=df['Order Date'].min().date()
    limite_superior=df['Order Date'].max().date()
    intervalo=st.sidebar.date_input("Faixa de tempo: ",value=(limite_inferior,limite_superior),min_value=limite_inferior,max_value=limite_superior)
    if len(intervalo)==2:
        inicio,fim=intervalo
        df_filtrado=df[(df['Order Date']>=pd.to_datetime(inicio))&(df['Order Date']<=pd.to_datetime(fim))]
    else: df_filtrado=df
    st.bar_chart(df_filtrado.groupby('Order Date')['Sales'].sum())
