import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import streamlit as st
import pandas as pd
from lib.csvdb import filter_by_date_range, display_relatorio_combinado
from porcError import porcError, contError, errorTI

# Dicionário de descrições de erros
error_dict = {
    'M1 ': 'Problemas Mecânicos',
    'T1 ': 'Validador',
    'T2 ': 'Problema de Comunicação GPS',
    'T3 ': 'Catraca',
    'T4 ': 'Comunicação em Ponto Final',
    'O1 ': 'Recolhimento para a Garagem',
    'O2 ': 'Retorno ao ponto final',
    'O3 ': 'Atraso motorista',
    '04 ': 'Problema com passageiro',
    'O5 ': 'Viagem em tempo limite',
    'O6 ': 'Sinistro',
    'O7 ': 'Erro Operacional',
    'O8 ': 'Aguardando Horário de Saída',
    'S1 ': 'Parte da Viagem',
    'S2 ': 'Ralocamento',
    'S3 ': 'Erro de Tabela',
    'S4 ': 'Falha no Sonda',
    'REF': 'REF',
    'VIA': 'VIA',
    # Adicione mais códigos de erro conforme necessário
    '': 'NAN'  # Descrição padrão para outros casos
}

def add_cod_error_descri_column(df, error_dict):
    df['CodErrorDescri'] = df['CodError'].apply(lambda x: error_dict.get(x, error_dict['']))
    return df

def visaoGeral():
    st.subheader("Análise de Erros")
    col1, col2 = st.columns(2)
    with col1:
        data_inicio = pd.to_datetime(st.date_input("Selecione a data de início:"))
    with col2:
        data_fim = pd.to_datetime(st.date_input("Selecione a data de término:"))
    
    # Filtrar o relatório combinado pelo intervalo de datas
    relatorio_filtrado_df = filter_by_date_range(data_inicio, data_fim)
    
    # Adicionar a coluna CodErrorDescri usando o dicionário de erros
    relatorio_filtrado_df = add_cod_error_descri_column(relatorio_filtrado_df, error_dict)
    
    col3, col4 = st.columns(2)
    col5, col6 = st.columns(2)
    with col3:
        porcError(relatorio_filtrado_df)
    with col4:
        contError(relatorio_filtrado_df)
    errorTI(relatorio_filtrado_df)
