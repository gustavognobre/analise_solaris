import streamlit as st
import pandas as pd
from lib.csvdb import filter_by_date_range

# Função para adicionar coluna de tipo de dia
def add_day_type_column(df):
    df['Data'] = pd.to_datetime(df['Data'])  # Certificar que a coluna 'Data' é do tipo datetime
    df['Dia da Semana'] = df['Data'].apply(lambda x: 'Sábado' if x.weekday() == 5 else ('Domingo' if x.weekday() == 6 else 'Dia Útil'))
    return df

# Função para adicionar coluna de peso
def add_weight_column(df):
    peso_dia_util = 0.17211704  # Para 581 Viagens
    peso_sabado = 0.34129693    # Para 293 Viagens 
    peso_domingo = 0.97087379   # Para 103 Viagens

    def calculate_weight(row):
        if row['Status'] in ['NÃO REALIZADA', 'CANCELADA']:
            if row['Dia da Semana'] == 'Dia Útil':
                return peso_dia_util
            elif row['Dia da Semana'] == 'Sábado':
                return peso_sabado
            elif row['Dia da Semana'] == 'Domingo':
                return peso_domingo
        elif row['Status'] in ['VIAGEM PLANEJADA E REALIZADA', 'REALIZADA']:
            if row['Dia da Semana'] == 'Dia Útil':
                return 1
            elif row['Dia da Semana'] == 'Sábado':
                return 1
            elif row['Dia da Semana'] == 'Domingo':
                return 1
        return 0  # Caso o status não seja um dos especificados acima

    df['Peso'] = df.apply(calculate_weight, axis=1)
    
    # Calcular a soma total de viagens realizadas por carro
    viagens_realizadas = df[df['Status'].isin(['VIAGEM PLANEJADA E REALIZADA', 'REALIZADA'])].groupby('Veículo Plan').size()
    df['Total Viagens Realizadas'] = df['Veículo Plan'].map(viagens_realizadas).fillna(0)
    
    return df


def sum_by_day(df):
    df['Data'] = pd.to_datetime(df['Data'])
    
    # Filtrar apenas as viagens não realizadas (status 'NÃO REALIZADA' ou 'CANCELADA')
    df_nao_realizadas = df[df['Status'].isin(['NÃO REALIZADA', 'CANCELADA'])]
    
    # Agrupar por 'Data' e somar os pesos das viagens não realizadas
    grouped = df_nao_realizadas.groupby('Data').agg({'Peso': 'sum'}).reset_index()
    grouped['Peso Resto'] = 100 - grouped['Peso']
    
    return grouped

def sum_by_car(df):
    df['Data'] = pd.to_datetime(df['Data'])
    
    # Agrupar por 'Veículo Plan' e somar os pesos das viagens realizadas e canceladas
    grouped = df.groupby('Veículo Plan').agg({'Peso': 'sum'}).reset_index()
    
    # Calcular a soma de viagens realizadas (não canceladas)
    df_realizadas = df[df['Status'].isin(['VIAGEM PLANEJADA E REALIZADA', 'REALIZADA'])]
    realizadas = df_realizadas.groupby('Veículo Plan').agg({'Peso': 'sum'}).reset_index()
    realizadas.rename(columns={'Peso': 'Total Viagens Realizadas'}, inplace=True)
    
    # Mesclar as informações de viagens realizadas com o dataframe agrupado original
    grouped = pd.merge(grouped, realizadas, on='Veículo Plan', how='left')
    grouped['Total Viagens Realizadas'].fillna(0, inplace=True)  # Preencher com zero onde não há viagens realizadas
    
    # Adicionar uma coluna com a soma total de viagens canceladas por carro
    canceladas = df[df['Status'].isin(['NÃO REALIZADA', 'CANCELADA'])].groupby('Veículo Plan').agg({'Peso': 'sum'}).reset_index()
    canceladas.rename(columns={'Peso': 'Total Viagens Canceladas'}, inplace=True)
    
    # Mesclar as informações de viagens canceladas com o dataframe agrupado original
    grouped = pd.merge(grouped, canceladas, on='Veículo Plan', how='left')
    grouped['Total Viagens Canceladas'].fillna(0, inplace=True)  # Preencher com zero onde não há viagens canceladas
    
    # Remover a coluna de peso agora que não é mais necessária
    grouped.drop(columns=['Peso'], inplace=True)
    
    return grouped

def eficienciaComunicação():
    st.write("Eficiência de Comunicação")
    col1, col2 = st.columns(2)
    
    # Selecionar o intervalo de datas
    with col1:
        data_inicio = pd.to_datetime(st.date_input("Selecione a data de início:"))
    with col2:
        data_fim = pd.to_datetime(st.date_input("Selecione a data de término:"))
    
    # Botão de seleção
    option = st.selectbox('Escolha a somatória:', ('Por Dia', 'Por Carro'))
    
    # Filtrar o relatório combinado pelo intervalo de datas
    relatorio_filtrado_df = filter_by_date_range(data_inicio, data_fim)
    
    # Adicionar a coluna de tipo de dia
    relatorio_filtrado_df = add_day_type_column(relatorio_filtrado_df)
    
    # Adicionar a coluna de peso
    relatorio_filtrado_df = add_weight_column(relatorio_filtrado_df)
    
    # Exibir o DataFrame atualizado
    if option == 'Por Dia':
        resultado = sum_by_day(relatorio_filtrado_df)
        st.write("Somatória por Dia:")
    else:
        resultado = sum_by_car(relatorio_filtrado_df)
        st.write("Somatória por Carro:")
    
    st.write(resultado)