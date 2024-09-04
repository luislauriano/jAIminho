import streamlit as st
import pandas as pd
import pickle
import gzip

# Carregar o modelo
with gzip.open('model_teste.pkl.gz', 'rb') as f:
    model = pickle.load(f)

# Função para gerar dados de entrada
def prepare_input(tipo_demanda, horario, local, nota_avaliacao_ai, tempo_medio_atendimento, estado, regiao, cidade, numero_funcionarios, mes, dia_semana, ano):
    # Criar um DataFrame com os dados de entrada
    input_data = pd.DataFrame({
        'tipo_demanda': [tipo_demanda],
        'horario': [horario],
        'local': [local],
        'nota_avaliacao_ai': [nota_avaliacao_ai],
        'tempo_medio_atendimento': [tempo_medio_atendimento],
        'estado': [estado],
        'regiao': [regiao],
        'cidade': [cidade],
        'numero_funcionarios': [numero_funcionarios],
        'mes': [mes],
        'dia_semana': [dia_semana],
        'ano': [ano]
    })
    
   
    # Convertendo variáveis categóricas para variáveis dummy
    input_data = pd.get_dummies(input_data)
    
    # Ajustar o dataframe para ter as mesmas colunas que o modelo
    model_columns = model.feature_names_in_
    input_data = input_data.reindex(columns=model_columns, fill_value=0)
    
    
    return input_data

# Título do aplicativo
st.title("Previsão de Picos de Atendimento - jAIminho")

df = pd.read_csv('Dados_tratados.csv')

with st.container():
    st.dataframe(df.head(10),1000,400)

with st.container():
    st.header('Insira as informações solicitadas abaixo para a previsão do modelo:')
    col1, col2, col3 = st.columns(3)
    with col1:
        # Inputs do usuário
        tipo_demanda = st.selectbox('Selecione o Tipo de Demanda', ['Pacotes', 'Cartas', 'Expressa', 'Outro'])
    with col2:
        horario = st.number_input('Selecione o Horário (horas)', 0, 23, 12)
    with col3:
        local = st.selectbox('Selecione o Local', ['Agência Central', 'Agência Bairro', 'Centro de Distribuição'])
    col4, col5 = st.columns(2)
    with col4:
        nota_avaliacao_ai = st.number_input('Nota de Avaliação AI', 0, 5, 3)
    with col5:
        tempo_medio_atendimento = st.number_input('Tempo Médio de Atendimento (min)', 0, 60, 15)
    
    col7, col8, col9 = st.columns(3)
    with col7:
        regiao = st.selectbox('Selecione a Região', ['Sudeste', 'Nordeste'])
    with col8:
        cidade = st.selectbox('Selecione a Cidade', ['Salvador', 'Belo Horizonte', 'São Paulo', 'Rio de Janeiro'])
    with col9:
        estado = st.selectbox('Selecione o Estado', ['SP', 'MG', 'RJ', 'BA'])
    numero_funcionarios = st.slider('Número de Funcionários', 1, 100, 10)
    col10, col11, col12 = st.columns(3)
    with col10:
        mes = st.slider('Mês', 1, 12, 6)
    with col11:
        dia_semana = st.selectbox('Dia da Semana', ['Segunda', 'Terça', 'Quarta', 'Quinta', 'Sexta', 'Sábado', 'Domingo'])
    with col12:
        ano = st.slider('Ano', 2010, 2024, 2014)

# Preparar dados de entrada
input_data = prepare_input(tipo_demanda, horario, local, nota_avaliacao_ai, tempo_medio_atendimento, estado, regiao, cidade, numero_funcionarios, mes, dia_semana, ano)

# Fazer a previsão
try:
    if not input_data.empty:
        predicao = model.predict(input_data)
        st.write(f"Previsão de Volume de Atendimentos: {int(predicao[0])}")
    else:
        st.write("Não foi possível fazer a previsão devido a problemas com os dados de entrada.")
except Exception as e:
    st.write(f"Erro ao fazer a previsão: {e}")


media_volume_atendimentos = df['volume_atendimentos'].mean()
maior_volume_atendimentos = df['volume_atendimentos'].max()

with st.container():
    st.header('Dashboard para tomada de decisão')

    col4, col5 = st.columns(2)

    with col4:
        st.metric("Média do volume de atendimentos atual","{:,.2f}".format(media_volume_atendimentos))
    
    with col5:
        st.metric("Maior volume de atendimentos atual","{:,.2f}".format(maior_volume_atendimentos))
    
    col1, col2 = st.columns(2)
    
    with col1:
        
        st.subheader("Volume de atendimentos por dia da semana")
        grouped_data = df.groupby('dia_semana')['volume_atendimentos'].sum().sort_values(ascending = False)
        st.line_chart(grouped_data)
    with col2:
        st.subheader("Volume de atendimentos por mes")
        grouped_data_dois = df.groupby('mes')['volume_atendimentos'].sum().sort_values(ascending = False)
        st.area_chart(grouped_data_dois)
    