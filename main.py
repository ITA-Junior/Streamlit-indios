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

    
    # Criando o sidebar de data e região - 
    limite_inferior=df['Order Date'].min().date()
    limite_superior=df['Order Date'].max().date()
    intervalo=st.sidebar.date_input("Faixa de tempo: ",value=(limite_inferior,limite_superior),min_value=limite_inferior,max_value=limite_superior)
    if len(intervalo)==2:
        inicio,fim=intervalo
        df_filtrado=df[(df['Order Date']>=pd.to_datetime(inicio))&(df['Order Date']<=pd.to_datetime(fim))]
    else: df_filtrado=df
    regioes=df['Region'].unique().tolist()
    regioes.insert(0,'Todas')
    filtro=st.sidebar.selectbox("Região: ",options=regioes)
    if filtro=="Todas":
        df_final=df_filtrado
    else:
        df_final=df_filtrado[df_filtrado['Region']==filtro]

with aba2:
    st.subheader("Análise na categoria \"Office Supplies\":")
    st.write(f"A melhor venda foi realizada em {um['City']} no dia {um['Order Date']}")
    st.write(f"vendendo em {um['Sales']:.2f} reais, o que gerou um lucro de R${um['Profit']:.2f}")
    st.info("Insight: Essa cidade pode ser um polo regional de vendas desse tipo de produto, sugerindo investimento e campanhas.")

    st.divider()

    st.subheader("Total de vendas, em reais, por data e região: ")
    # limite_inferior=df['Order Date'].min().date()
    # limite_superior=df['Order Date'].max().date()
    # intervalo=st.date_input("Faixa de tempo: ",value=(limite_inferior,limite_superior),min_value=limite_inferior,max_value=limite_superior)
    # if len(intervalo)==2:
    #     inicio,fim=intervalo
    #     df_filtrado=df[(df['Order Date']>=pd.to_datetime(inicio))&(df['Order Date']<=pd.to_datetime(fim))]
    # else: df_filtrado=df
    st.bar_chart(df_final.groupby('Order Date')['Sales'].sum())
    st.info("Insight: O gráfico permite identificar picos esporáticos nas vendas que podem estar atrelados a campanhas.")

    st.divider()

    st.subheader("Análise Geográfica de Vendas: ")
    # regioes=df['Region'].unique().tolist()
    # regioes.insert(0,'Todas')
    # filtro=st.selectbox("Região: ",options=regioes)
    # if filtro=="Todas":
    #     df_estado=df
    # else:
    #     df_estado=df[df['Region']==filtro]
    df_estado=df_final.groupby("State")['Sales'].sum()
    st.bar_chart(df_estado)
    st.info("Insight: Concentração de receita indica quais estados são os principais compradores.")

    st.divider()

    st.subheader("As cidades com maiores vendas: ")
    cidades = df_final.groupby("City")['Sales'].sum()
    cidades = cidades.sort_values(ascending=False)
    cidades=cidades[0:10]
    st.bar_chart(cidades)
    st.info("Insight: podemos ver o comportamento das regiões, vendo quais cidades compram mais. Isso nos importa pois, assim,\nsabemos os polos de compra.")

    st.divider()

    st.subheader("Analise de Segmentos: ")
    segmento=df_final.groupby("Segment")['Sales'].sum().reset_index()
    figura=px.pie(segmento,values='Sales',names='Segment',title="Faturamento relativo de cada Segmento: ",hole=0)
    st.plotly_chart(figura,use_container_width=True)
    st.info("Insight: podemos ver aqui qual região precisa de maior investimento e publicidade.")
    
with aba3:
    st.subheader("Análise anual de cada Segmento: ")
    regioes=df['Region'].unique().tolist()
    regioes.insert(0,'Todas')
    filtro=st.selectbox("Região: ",options=regioes)
    if filtro=="Todas":
        planilha=df
    else:
        planilha=df[df['Region']==filtro]
    anos=planilha['Year'].unique().tolist()
    anos.insert(0,'Todos')
    opcao=st.selectbox("Ano Selecionado: ",options=anos)
    if opcao=='Todos':
        planilha=planilha
    else: planilha=planilha[planilha['Year']==opcao]
    grafico=planilha.groupby(['Segment'])['Sales'].sum()
    st.bar_chart(grafico)
    st.info("Insight: Aqui vemos de que forma o retorno financeiro por segmento se comporta anualmente.")

    st.divider()

    st.subheader('Simulação de Desconto: ')
    st.write(f"Note que, nas vendas, um total de {len(df_final[df_final['Sales']>=1000])} de casos tiveram um valor de venda maior do que R$1000,00")
    st.write("na região e faixa de tempo selecionadas.")
    st.write("Vamos, agora, simular se esses casos tivessem algum desconto em suas compras: ")
    desconto=st.number_input('Escolha a porcentagem de desconto:',min_value=0,max_value=100)
    desconto=float(desconto/100)
    coisa=df_final
    dineiro=(coisa.loc[coisa['Sales']>1000,'Sales']*desconto).sum()
    st.write(f"Se dessemos tal desconto nos produtos, um total de {dineiro:.2f} reais seria dado em desconto.")
    coisa = df_final
    dineiro=coisa['Sales'].where(coisa['Sales']<=1000,coisa['Sales']*(1-desconto)).sum()
    st.write(f"Isso faria com que o retorno total caisse de {df_final['Sales'].sum():.2f} reais para {dineiro:.2f}.")
    st.info("Insight: Uma pequena quantidade de compras de alto valor atinge o teto do desconto, o que não prejudicaria gravemente a margem geral.")

    st.subheader('Comparação entre as médias com e sem Desconto')
    coisa=df_final
    st.write(f"O Valor médio de venda, supondo sem aplicação de desconto, é de {df_final['Sales'].mean():.2f} reais.")
    st.write(f"Já para o caso de aplicação de desconto, a média do retorno é de R${(coisa['Sales'].where(coisa['Sales']>=1000,coisa['Sales']*(1-desconto))).mean():.2f}.")
    st.info("Insight: O impacto absoluto deste tipo de desconto não tem grandes impactos sobre a média das vendas.")

    st.divider()

    st.subheader("Vendas de cada segmento em relação ao tempo: ")
    df_final['Mes_Ano'] = df_final['Order Date'].dt.to_period('M').dt.to_timestamp()
    vendas_linha = df_final.groupby(['Mes_Ano', 'Segment'])['Sales'].sum().reset_index()
    fig_linhas = px.line(
        vendas_linha, 
        x='Mes_Ano', 
        y='Sales', 
        color='Segment', # Separa uma linha de cor diferente para cada Segmento
        labels={'Mes_Ano': 'Data', 'Sales': 'Vendas (R$)', 'Segment': 'Segmento'}
    )
    st.plotly_chart(fig_linhas, use_container_width=True)
    st.info("Insight: Podemos ver as preferências temporais de cada região. Esse tipo de informação é importante para organizar campanhas e anúncios.")

    st.divider()

    st.subheader('As Vendas das melhores Categorias e Subcategorias: ')
    vendas = df_final.groupby(['Category', 'Sub-Category'])['Sales'].sum().reset_index()
    top12=vendas.sort_values(by='Sales', ascending=False).head(12)
    fig_top12 = px.bar(
        top12, 
        x='Sales', 
        y='Sub-Category',    
        color='Category',   
        orientation='h',    
        title='Total de Vendas nas Top 12 Subcategorias',
        labels={'Sales': 'Total de Vendas (R$)', 'Sub-Category': 'Subcategoria', 'Category': 'Categoria'}
    )
    fig_top12.update_layout(yaxis={'categoryorder': 'total ascending'})
    st.plotly_chart(fig_top12, use_container_width=True)
    st.info("Insight: Podemos ver os produtos com maiores vendas com a região e faixa de tempo. A partir desses dados,\npodemos saber qual tipo de estoque reforçar.")

with aba4:
    st.subheader("Conclusões e Resultados: ")
    