import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="Streamlit-Indios📊", layout="wide", page_icon="🚀")

st.markdown(
    """
    <style>
    .stApp {
        background-color: #0A192F !important;
    }
    
    [data-testid="stSidebar"] {
        background-color: #0D203D !important;
    }
    
    h1, h2, h3, h4, h5, h6, p, label, span, .stMarkdown {
        color: #FFD700 !important;
    }
    
    button[data-baseweb="tab"] p {
        color: #FFD700 !important;
    }
    
    button[data-baseweb="tab"][aria-selected="true"] {
        border-bottom-color: #FFD700 !important;
    }
    
    [data-testid="stMetricLabel"] > div {
        color: #FFD700 !important;
    }
    [data-testid="stMetricValue"] > div {
        color: #FFFFFF !important;
    }
    </style>
    """,
    unsafe_allow_html=True
)

plt.rcParams['figure.facecolor'] = '#0A192F'
plt.rcParams['axes.facecolor'] = '#0A192F'
plt.rcParams['text.color'] = '#FFD700'
plt.rcParams['axes.labelcolor'] = '#FFD700'
plt.rcParams['axes.edgecolor'] = '#FFD700'
plt.rcParams['xtick.color'] = '#FFD700'
plt.rcParams['ytick.color'] = '#FFD700'

@st.cache_data(ttl=600)
def load_data():
    try:
        df = pd.read_excel("Sample - Superstore.xls")
        
        df['Order Date'] = pd.to_datetime(df['Order Date'])
        df['Sales'] = pd.to_numeric(df['Sales'], errors='coerce')
        df['Year'] = df['Order Date'].dt.year
        df['Month'] = df['Order Date'].dt.month
        return df
    except Exception as e:
        st.error(f"Erro ao carregar o arquivo de dados local: {e}")
        return pd.DataFrame()

df = load_data()

if df.empty:
    st.warning("Coloque o arquivo da base de dados na mesma pasta do script para visualizar o Dashboard.")
    st.stop()

st.sidebar.header("🔍 Filtros")
anos_disponiveis = df['Year'].unique().tolist()
ano_selecionado = st.sidebar.multiselect("Selecione o(s) Ano(s)", anos_disponiveis, default=anos_disponiveis)

regioes = df['Region'].unique().tolist() if 'Region' in df.columns else df['State'].unique().tolist()
regiao_selecionada = st.sidebar.multiselect("Selecione a Região/Estado", regioes, default=regioes)

df_filtrado = df[df['Year'].isin(ano_selecionado)]
if 'Region' in df.columns:
    df_filtrado = df_filtrado[df_filtrado['Region'].isin(regiao_selecionada)]
else:
    df_filtrado = df_filtrado[df_filtrado['State'].isin(regiao_selecionada)]

st.title("Streamlit-Indios📊")
st.markdown("Navegue pelas abas abaixo para explorar as análises.")

tab1, tab2, tab3, tab4 = st.tabs([
    "🏠 Visão Geral", 
    "📈 Perguntas 1-5", 
    "🚀 Perguntas 6-10", 
    "💡 Conclusões"
])

with tab1:
    st.header("Visão Geral da Base de Dados")
    col1, col2, col3 = st.columns(3)
    col1.metric("Total de Vendas", f"${df_filtrado['Sales'].sum():,.2f}")
    col2.metric("Total de Pedidos", len(df_filtrado))
    col3.metric("Cidades Atendidas", df_filtrado['City'].nunique())
    
    st.dataframe(df_filtrado.head(10), use_container_width=True)
    
    csv = df_filtrado.to_csv(index=False).encode('utf-8')
    st.download_button(label="📥 Baixar Dados Filtrados (CSV)", data=csv, file_name='dados_filtrados.csv', mime='text/csv')

with tab2:
    st.subheader("1. Qual cidade com maior valor de venda para produtos da categoria 'Office Supplies'?")
    df_office = df_filtrado[df_filtrado['Category'] == 'Office Supplies']
    if not df_office.empty:
        cidade_top = df_office.groupby('City')['Sales'].sum().idxmax()
        valor_top = df_office.groupby('City')['Sales'].sum().max()
        st.write(f"**Resultado:** A cidade é **{cidade_top}** com um valor total de **${valor_top:,.2f}**.")
    
    st.divider()

    st.subheader("2. Total de vendas por data do pedido")
    vendas_data = df_filtrado.groupby(df_filtrado['Order Date'].dt.date)['Sales'].sum()
    
    fig2, ax2 = plt.subplots(figsize=(10, 4))
    ax2.plot(vendas_data.index, vendas_data.values, color='cyan')
    ax2.set_title("Vendas Diárias")
    ax2.set_ylabel("Vendas ($)")
    fig2.tight_layout()
    st.pyplot(fig2)

    st.divider()

    st.subheader("3. Total de vendas por estado")
    vendas_estado = df_filtrado.groupby('State')['Sales'].sum().sort_values(ascending=False)
    
    fig3, ax3 = plt.subplots(figsize=(12, 5))
    vendas_estado.plot(kind='bar', ax=ax3, color='gold')
    ax3.set_title("Vendas por Estado")
    ax3.set_ylabel("Vendas ($)")
    plt.xticks(rotation=45, ha='right')
    fig3.tight_layout()
    st.pyplot(fig3)

    st.divider()

    st.subheader("4. Top 10 cidades com maior total de vendas")
    top10_cidades = df_filtrado.groupby('City')['Sales'].sum().nlargest(10)
    
    fig4, ax4 = plt.subplots(figsize=(10, 5))
    top10_cidades.plot(kind='bar', ax=ax4, color='lightgreen')
    ax4.set_title("Top 10 Cidades em Vendas")
    ax4.set_ylabel("Vendas ($)")
    plt.xticks(rotation=45, ha='right')
    fig4.tight_layout()
    st.pyplot(fig4)

    st.divider()

    st.subheader("5. Segmento com maior total de vendas")
    vendas_segmento = df_filtrado.groupby('Segment')['Sales'].sum()
    
    fig5, ax5 = plt.subplots(figsize=(6, 6))
    ax5.pie(vendas_segmento, labels=vendas_segmento.index, autopct='%1.1f%%', startangle=90, colors=['#ff9999','#66b3ff','#99ff99'])
    ax5.set_title("Participação por Segmento")
    fig5.tight_layout()
    st.pyplot(fig5)

with tab3:
    st.subheader("6. Total de vendas por segmento e por ano")
    vendas_seg_ano = df_filtrado.groupby(['Year', 'Segment'])['Sales'].sum().unstack()
    
    fig6, ax6 = plt.subplots(figsize=(10, 5))
    vendas_seg_ano.plot(kind='bar', ax=ax6)
    ax6.set_title("Vendas por Segmento e Ano")
    ax6.set_ylabel("Vendas ($)")
    plt.xticks(rotation=0)
    fig6.tight_layout()
    st.pyplot(fig6)

    st.divider()

    st.subheader("7 & 8. Simulador de Desconto")
    col_sim1, col_sim2, col_sim3 = st.columns(3)
    limite_valor = col_sim1.number_input("Valor limite da venda ($)", value=1000)
    desc_maior = col_sim2.slider("Desconto para valores altos (%)", 0, 50, 15) / 100
    desc_menor = col_sim3.slider("Desconto padrão (%)", 0, 50, 10) / 100

    df_simulacao = df_filtrado.copy()
    df_simulacao['Desconto_Simulado'] = df_simulacao['Sales'].apply(lambda x: desc_maior if x > limite_valor else desc_menor)
    df_simulacao['Sales_Apos_Desconto'] = df_simulacao['Sales'] * (1 - df_simulacao['Desconto_Simulado'])
    
    qtd_desc_maior = len(df_simulacao[df_simulacao['Desconto_Simulado'] == desc_maior])
    
    st.write(f"**Quantas vendas receberam {desc_maior*100}% de desconto?** {qtd_desc_maior} vendas.")
    st.write(f"**Média de venda ANTES:** ${df_simulacao['Sales'].mean():,.2f}")
    st.write(f"**Média de venda DEPOIS:** ${df_simulacao['Sales_Apos_Desconto'].mean():,.2f}")

    st.divider()

    st.subheader("9. Média de vendas por segmento, ano e mês")
    df_filtrado['Ano-Mês'] = df_filtrado['Order Date'].dt.to_period('M')
    media_mensal_seg = df_filtrado.groupby(['Ano-Mês', 'Segment'])['Sales'].mean().unstack()
    media_mensal_seg.index = media_mensal_seg.index.to_timestamp()
    
    fig9, ax9 = plt.subplots(figsize=(10, 5))
    media_mensal_seg.plot(kind='line', ax=ax9, marker='o', alpha=0.7)
    ax9.set_title("Evolução da Média de Vendas")
    ax9.set_ylabel("Média de Vendas ($)")
    fig9.tight_layout()
    st.pyplot(fig9)

    st.divider()

    st.subheader("10. Total de vendas por categoria e subcategoria (Top 12)")
    top12_subcats = df_filtrado.groupby('Sub-Category')['Sales'].sum().nlargest(12).index
    df_top12 = df_filtrado[df_filtrado['Sub-Category'].isin(top12_subcats)]
    vendas_cat_sub = df_top12.groupby(['Sub-Category', 'Category'])['Sales'].sum().unstack()
    
    fig10, ax10 = plt.subplots(figsize=(12, 6))
    vendas_cat_sub.plot(kind='bar', stacked=True, ax=ax10)
    ax10.set_title("Vendas das Top 12 Subcategorias")
    ax10.set_ylabel("Vendas ($)")
    plt.xticks(rotation=45, ha='right')
    fig10.tight_layout()
    st.pyplot(fig10)

with tab4:
    st.header("Conclusões & Recomendações")
    st.markdown("""
    - As visualizações facilitam a rápida identificação de estados e cidades chave para o faturamento.
    - O simulador mostra como a margem reage às faixas de descontos personalizadas.
    - O uso do Matplotlib permitiu simplificar a infraestrutura do app, tornando a renderização local direta.
    """)