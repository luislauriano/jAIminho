import streamlit as st
import pandas as pd
import pickle
import gzip
import plotly.express as px

with gzip.open('model.pkl.gz', 'rb') as f:
    model = pickle.load(f)


def prepare_input(tipo_demanda, horario, local, nota_avaliacao_ai, tempo_medio_atendimento, estado, numero_funcionarios, mes, dia_semana, ano):
    input_data = pd.DataFrame({
        'tipo_demanda': [tipo_demanda],
        'horario': [horario],
        'local': [local],
        'nota_avaliacao_ai': [nota_avaliacao_ai],
        'tempo_medio_atendimento': [tempo_medio_atendimento],
        'estado': [estado],
        'numero_funcionarios': [numero_funcionarios],
        'mes': [mes],
        'dia_semana': [dia_semana],
        'ano': [ano]
    })
    
    input_data = pd.get_dummies(input_data)
    
    model_columns = model.feature_names_in_
    input_data = input_data.reindex(columns=model_columns, fill_value=0)
    
    
    return input_data

df = pd.read_csv('Dados_tratados.csv')
media_volume_atendimentos = df['volume_atendimentos'].mean()
maior_volume_atendimentos = df['volume_atendimentos'].max()

with st.container():
   
    col4, col5 = st.columns(2)

    with col4:
        st.markdown(
            f"""
            <style>
            .metric-container {{
                display: flex;
                align-items: center;
                font-size: 13px;
                color: #034381
            }}
            .metric-label {{
                margin-right: 10px;
                
            }}
            .metric-value {{
                font-size: 20px; /* Ajuste o tamanho conforme necessário */
                font-weight: medium;
                padding: 5px 10px; /* Adiciona algum preenchimento ao redor do número */
             
                border-radius: 10px; /* Adiciona bordas arredondadas */
                background-color: #034381; /* Define a cor do fundo (opcional) */
                color: #FFDC02; /* Define a cor do texto como amarela */
                font-family: 'Poppins', sans-serif; /* Define a fonte como Poppins */
            }}
            </style>
            <div class="metric-container">
                <div class="metric-label">Média do volume de <br> atendimentos atual:</div>
                <div class="metric-value">{media_volume_atendimentos:,.2f}</div>
            </div>
            """,
            unsafe_allow_html=True
        )
    
    with col5:
       
        st.markdown(
            f"""
            <style>
            .metric-container-dois {{
                display: flex;
                align-items: center;
                font-size: 13px;
                color: #034381
            }}
            .metric-label-dois {{
                margin-right: 10px;
                
            }}
            .metric-value-dois {{
                font-size: 20px; /* Ajuste o tamanho conforme necessário */
                font-weight: medium;
                padding: 5px 10px; /* Adiciona algum preenchimento ao redor do número */
                border-radius: 10px; /* Adiciona bordas arredondadas */
                background-color: #FFDC02; /* Define a cor do fundo (opcional) */
                color: #034381; /* Define a cor do texto como amarela */
                font-family: 'Poppins', sans-serif; /* Define a fonte como Poppins */
            }}
            </style>
            <div class="metric-container-dois">
                <div class="metric-label-dois">Maior volume de <br> atendimentos atual:</div>
                <div class="metric-value-dois">{maior_volume_atendimentos:,.2f}</div>
            </div>
            """,
            unsafe_allow_html=True
        )
    
    col1, col2 = st.columns(2)
    
    with col1:
        
        
        grouped_data = df.groupby('dia_semana')['volume_atendimentos'].sum().sort_values(ascending = False)
        st.markdown(
            """
            <style>
            .custom-subheader {
                margin-top: 20px;
                color: #034381; /* Cor do texto */
                font-size: 18px; /* Tamanho da fonte */
                font-weight: medium; /*
                font-family: 'Poppins', sans-serif; /* 
            }
            </style>
            <div class="custom-subheader">
                Volume de atendimentos por dia da semana
            </div>
            """,
            unsafe_allow_html=True
        )
        st.line_chart(grouped_data)

    with col2:
        
        grouped_data_dois = df.groupby('mes')['volume_atendimentos'].sum().sort_values(ascending = False)
        st.markdown(
            """
            <style>
            .custom-subheader-dois {
                margin-top: 20px;
                color: #034381; /* Cor do texto */
                font-size: 18px; /* Tamanho da fonte */
                font-weight: medium; /*
                font-family: 'Poppins', sans-serif; /* 
            }
            </style>
            <div class="custom-subheader-dois">
                Volume de atendimentos por mês
            </div>
            """,
            unsafe_allow_html=True
        )
        st.area_chart(grouped_data_dois)


    col6, col7 = st.columns(2)
    
    with col6:
        
        
        grouped_data_seis = df.groupby('local')['volume_atendimentos_nao_finalizados'].sum().sort_values(ascending = False)

        st.markdown(
            """
            <style>
            .custom-subheader-seis {
                margin-top: 20px;
                color: #034381; /* Cor do texto */
                font-size: 18px; /* Tamanho da fonte */
                font-weight: medium; /*
                font-family: 'Poppins', sans-serif; /* 
            }
            </style>
            <div class="custom-subheader-seis">
                Volume de atendimentos não finalizados por local
            </div>
            """,
            unsafe_allow_html=True
        )
        fig = px.bar(
        grouped_data_seis,
        x=grouped_data_seis.index,
        y=grouped_data_seis.values,
        color=grouped_data_seis.index,  
        color_discrete_sequence=['#034381', '#FFDC02', '#5C5C5C']  
        )
        fig.update_layout(
        width=300,  
        height=380,  
        showlegend=False,
        yaxis_title='volume',
        plot_bgcolor='rgba(0, 0, 0, 0)', 
        )
        st.plotly_chart(fig)

    with col7:
        
        grouped_data_sete = df.groupby('local')['volume_atendimentos_finalizados'].sum().sort_values(ascending = False)
        st.markdown(
            """
            <style>
            .custom-subheader-sete {
                margin-top: 20px;
                color: #034381; /* Cor do texto */
                font-size: 18px; /* Tamanho da fonte */
                font-weight: medium; /*
                font-family: 'Poppins', sans-serif; /* 
            }
            </style>
            <div class="custom-subheader-sete">
                Volume de atendimentos finalizados por local
            </div>
            """,
            unsafe_allow_html=True
        )
        fig = px.bar(
        grouped_data_sete,
        x=grouped_data_sete.index,
        y=grouped_data_sete.values,
        color=grouped_data_sete.index,  
        color_discrete_sequence=['#034381', '#FFDC02', '#5C5C5C'] 
        )
         
        fig.update_layout(
        width=400,  
        height=410,  
      
        yaxis_title='volume',
        plot_bgcolor='rgba(0, 0, 0, 0)',  
        
        )
        st.plotly_chart(fig)

st.markdown(
    """
    <style>
    .custom-subheader-tres {
        font-size: 18px; /* Ajuste o tamanho da fonte conforme necessário */
        font-weight: bold; /* Define o peso da fonte */
        text-align: center; /* Centraliza o texto */
        margin-bottom: 10px; /* Espaço abaixo do título */
        font-family: 'Poppins', sans-serif; /* Define a fonte como Poppins */
        color: #034381;
    }
    .custom-text-tres {
        font-size: 14px; /* Ajuste o tamanho da fonte conforme necessário */
        text-align: center; /* Centraliza o texto */
        line-height: 1.5; /* Ajusta o espaçamento entre linhas */
        margin-bottom: 40px; /* Espaço abaixo do texto */
        font-weight: mixed;
        
    }
    </style>
    <div class="custom-subheader-tres">
        Insira as informações solicitadas abaixo para a previsão do modelo:
    </div>
    <div class="custom-text-tres">
        Aqui você consegue <strong>prever</strong> quais períodos o <strong>pico de atendimento</strong> será mais <strong>alto</strong>,<br>
        podendo assim <strong>alocar mais funcionários</strong> para essa demanda e otimizar a experiência.
    </div>
    """,
    unsafe_allow_html=True
)


with st.container():
    
    col1, col2 = st.columns(2)
    with col1:
        
        tipo_demanda = st.selectbox('Selecione o Tipo de Demanda', ['Pacotes', 'Cartas', 'Expressa', 'Outro'])
    with col2:
        horario = st.number_input('Selecione o Horário (horas)', 0, 23, 12)
    
    col4, col5 = st.columns(2)
    with col4:
        nota_avaliacao_ai = st.number_input('Nota de Avaliação AI', 0, 5, 3)
    with col5:
        tempo_medio_atendimento = st.number_input('Tempo Médio de Atendimento (min)', 0, 60, 15)
    
    col7, col8 = st.columns(2)
    with col7:
        local = st.selectbox('Selecione o Local', ['Agência Central', 'Agência Bairro', 'Centro de Distribuição'])
    with col8:
        estado = st.selectbox('Selecione o Estado', ['SP', 'MG', 'RJ', 'BA'])
    numero_funcionarios = st.slider('Número de Funcionários', 1, 100, 10)
    col10, col11, col12 = st.columns(3)
    with col10:
        mes = st.slider('Mês', 1, 12, 6)
    with col11:
        dia_semana = st.selectbox('Dia da Semana', ['Segunda', 'Terça', 'Quarta', 'Quinta', 'Sexta', 'Sábado', 'Domingo'])
    with col12:
        ano = st.slider('Ano', 2010, 2024, 2014)



input_data = prepare_input(tipo_demanda, horario, local, nota_avaliacao_ai, tempo_medio_atendimento, estado, numero_funcionarios, mes, dia_semana, ano)

try:
    if not input_data.empty:
        predicao = model.predict(input_data)
        st.write(f"Previsão de Volume de Atendimentos: {int(predicao[0])}")
    else:
        st.write("Não foi possível fazer a previsão devido a problemas com os dados de entrada.")
except Exception as e:
    st.write(f"Erro ao fazer a previsão: {e}")

st.markdown(
    """
    <style>
    .custom-subheader-quatro {
        margin-top: 20px;
        margin-bottom: 20px;
        text-align: center;
        font-size: 20px; /* Ajuste o tamanho da fonte conforme necessário */
        font-weight: bold; /* Define o peso da fonte */
        color: #034381; /* Define a cor azul */

    }
    </style>
    <div class="custom-subheader-quatro">
        Previsão de Picos de Atendimento - Base de Dados
    </div>
    """,
    unsafe_allow_html=True
)

df_base = pd.read_csv('dados_correios.csv')
with st.container():
    st.dataframe(df_base.head(10),1000,400)

    