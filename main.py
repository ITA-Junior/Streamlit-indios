import os
import pandas as pd
import streamlit as st
from supabase import create_client, Client
from dotenv import load_dotenv
import scr.treatment as tr
import plotly.express as px

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
    intervalo=st.date_input("Faixa de tempo: ",value=(limite_inferior,limite_superior),min_value=limite_inferior,max_value=limite_superior)
    if len(intervalo)==2:
        inicio,fim=intervalo
        df_filtrado=df[(df['Order Date']>=pd.to_datetime(inicio))&(df['Order Date']<=pd.to_datetime(fim))]
    else: df_filtrado=df
    st.bar_chart(df_filtrado.groupby('Order Date')['Sales'].sum())
    st.info("Insight: O gráfico permite identificar picos sazonais nas vendas que podem estar atrelados a campanhas ou períodos do ano.")

    st.divider()

    st.subheader("Análise Geográfica de Vendas: ")
    regioes=df['Region'].unique().tolist()
    regioes.insert(0,'Todas')
    filtro=st.selectbox("Região: ",options=regioes)
    if filtro=="Todas":
        df_estado=df
    else:
        df_estado=df[df['Region']==filtro]
    df_estado=df_estado.groupby("State")['Sales'].sum()
    st.bar_chart(df_estado)
    st.info("Insight: Concentração de receita indica quais estados são os principais motores financeiros da operação.")

    st.divider()

    st.subheader("As cidades com maiores vendas: ")
    cidades = df.groupby("City")['Sales'].sum()
    cidades = cidades.sort_values(ascending=False)
    cidades=cidades[0:10]
    st.bar_chart(cidades)
    st.info("Insight: O esforço logístico deve ser priorizado nessas 10 cidades para garantir satisfação e maior retorno financeiro.")

    st.divider()

    st.subheader("Analise de Segmentos: ")
    segmento=df.groupby("Segment")['Sales'].sum().reset_index()
    figura=px.pie(segmento,values='Sales',names='Segment',title="Faturamento relativo de cada Segmento: ",hole=0)
    st.plotly_chart(figura,use_container_width=True)
    st.info("Insight: podemos ver aqui qual região precisa de maior investimento e publicidade.")
    
with aba3:
    st.subheader("Análise anual de cada Segmento: ")
    anos=df['Year'].unique().tolist()
    anos.insert(0,'Todos')
    opcao=st.selectbox("Ano Selecionado: ",options=anos)
    if opcao=='Todos':
        planilha=df
    else: planilha=df[df['Year']==opcao]
    grafico=planilha.groupby(['Segment'])['Sales'].sum()
    st.bar_chart(grafico)
    st.info("Insight: Aqui vemos de que forma o retorno financeiro por segmento se comporta anualmente")

    st.divider()

    st.subheader('Simulação de Desconto: ')
    st.write(f"Note que, nas vendas, um total de {len(df[df['Sales']>=1000])} de casos tiveram um valor de venda maior do que R$1000,00.")
    st.write("Vamos, agora, simular se esses 2 casos tivessem algum desconto em suas compras: ")
    desconto=st.number_input('Escolha a porcentagem de desconto:',min_value=0,max_value=100)
    desconto=float(desconto/100)
    coisa=df
    dineiro=(coisa.loc[coisa['Sales']>1000,'Sales']*desconto).sum()
    st.write(f"Para comparação, se dessemos tal desconto nos produtos, um total de {dineiro:.2f} reais seria dado em desconto.")
    st.write(f"")
    st.info("Insight: Uma pequena quantidade de compras de alto valor atinge o teto do desconto, o que não prejudicaria gravemente a margem geral.")

    st.divider()

    st.subheader('Comparação entre as médias com e sem Desconto')
    coisa=df
    st.write(f"O Valor médio de venda, supondo sem aplicação de desconto, é de {df['Sales'].mean():.2f} reais.")
    st.write(f"Já para o caso de aplicação de desconto, a média do retorno é de R${(coisa['Sales'].where(coisa['Sales']>=1000,coisa['Sales']*(1-desconto))).mean():.2f}")
    st.info("Insight: O impacto absoluto por venda de alto valor mostra o custo direto dessa política de fidelização.")

    st.divider()

    st.subheader("Vendas de cada segmento em relação ao tempo: ")
