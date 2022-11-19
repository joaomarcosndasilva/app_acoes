import streamlit as st
import yfinance as yf
import datetime
from time import sleep

icone_info = "ℹ️"
icone_warning = "⚠️"
icone_erro = "🚨"
icone_sucess = "✅"

def graficos_analises():
    inicio = st.sidebar.date_input('Data Inicial', datetime.date(2015, 1, 1))
    fim = st.sidebar.date_input('Data Final', datetime.datetime.now().date())
    ticket = yf.Ticker(acao)
    df = ticket.history(period='1d', start=inicio, end=fim)

    st.line_chart(df.Close)

    st.sidebar.info('GRÁFICOS', icon=icone_sucess)
    cb_volume = st.sidebar.checkbox('Gráfico de Volume')
    if cb_volume:
        with st.spinner('Aguarde...'):
            sleep(0.5)
        st.info('Gráfico de Volume', icon=icone_sucess)
        st.line_chart(df.Volume)
    cb_dividendos = st.sidebar.checkbox('Gráfico de dividendos')
    if cb_dividendos:
        with st.spinner('Aguarde...'):
            sleep(0.5)
        st.info('Gráfico de dividendos!', icon=icone_sucess)
        st.line_chart(df.Dividends)
    st.sidebar.warning('PREVER PREÇOS FUTUROS', icon=icone_warning)
    cb_kbest = st.sidebar.checkbox('KBEST')
    if cb_kbest:
        with st.spinner('Aguarde...'):
            sleep(0.5)
        st.error('O KBEST ainda não estão funcionando, por favor, aguarde + alguns dias', icon=icone_erro)
    cb_fbprophet = st.sidebar.checkbox('FBPROPHET')
    if cb_fbprophet:
        with st.spinner('Aguarde...'):
            sleep(0.5)
        st.error('O FBPROPHET ainda não estão funcionando, por favor, aguarde + alguns dias', icon=icone_erro)
    cb_neural = st.sidebar.checkbox('REDES NEURAIS')
    if cb_neural:
        with st.spinner('Aguarde...'):
            sleep(0.5)
        st.error('Nenhuma Rede Neural para previsão ainda, por favor, alguns + alguns dias', icon=icone_erro)

st.title('Análise de ativos da B3')
st.write('by J. Brutus')
st.subheader('Essa aplicação faz uma análise dos principais papeis que compõe o índice do IBOVESPA')

st.sidebar.success('ANÁLISES COM O  YAHOO FINANCE', icon=icone_info)

select_modo = st.sidebar.radio("Selecione como você quer ver a análise", ("Lista de ativos", "Digitar o código"))

if select_modo == "Digitar o código":
    acao = st.sidebar.text_input('Digite o código do Ativo e selecione as datas!', 'VALE3', help='Digite o código do ativo sem o ".SA" e pressione ENTER. ')
    acao = f'{acao}.SA'
    if acao:
        try:
            graficos_analises()
        except:
            st.warning(f'Você digitou o ativo {acao}. e selecionou os períodos ')
            st.error("Alguma coisa não está certa. Tente alterar o período de datas")

elif select_modo == "Lista de ativos":
    papeis = ['ABEV3', 'BBAS3', 'BBDC4', 'PETR4', 'VALE3', 'BEEF3', 'CMIG4', 'CPLE3']
    acao = st.sidebar.selectbox('Selecione o ativo e as datas que preferir', papeis, help="Está Lista contém apenas os ativos de ações mais líquidas do índice Ibovespa.")
    acao = f'{acao}.SA'
    graficos_analises()

else:
    st.info('Marque como você vai querer a análise')