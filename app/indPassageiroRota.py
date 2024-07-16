import streamlit as st
from lib.csvdb import filter_by_date_range
import pandas as pd
import plotly.express as px

def indPassageiro():
    col1, col2 = st.columns(2)
    col3, col4 = st.columns(2)
    with col1:
        data_inicio = pd.to_datetime(st.date_input("Selecione a data de início:"))
    with col2:
        data_fim = pd.to_datetime(st.date_input("Selecione a data de término:"))
    
    # Filtrar o relatório combinado pelo intervalo de datas
    relatorio_filtrado_df = filter_by_date_range(data_inicio, data_fim)
    
    if not relatorio_filtrado_df.empty:
       
        # Ajustar a condição de filtragem com base nas colunas corretas
        if 'Resultado da Linha' in relatorio_filtrado_df.columns and 'Status' in relatorio_filtrado_df.columns:
            relatorio_filtrado_df = relatorio_filtrado_df[~((relatorio_filtrado_df['Resultado da Linha'] == 0) & 
                                                            (relatorio_filtrado_df['Status'] == 'NÃO REALIZADA'))]
        
        # Criar uma tabela dinâmica (pivot table) para passageiros por data, usando 'Linha' e 'Tab' como índices
        pivot_df = pd.pivot_table(relatorio_filtrado_df, 
                                  values='Passageiros', 
                                  index=['Linha', 'Tab'], 
                                  columns='Data', 
                                  aggfunc='sum', 
                                  fill_value=0)
        
        # Exibir a tabela de passageiros por data, agrupada por Linha e Tab
        with col3:
            st.write(pivot_df)
    else:
        st.write("Não há dados disponíveis para o intervalo de datas selecionado.")
    if not relatorio_filtrado_df.empty:
       
        # Ajustar a condição de filtragem com base nas colunas corretas
        if 'Resultado da Linha' in relatorio_filtrado_df.columns and 'Status' in relatorio_filtrado_df.columns:
            relatorio_filtrado_df = relatorio_filtrado_df[~((relatorio_filtrado_df['Resultado da Linha'] == 0) & 
                                                            (relatorio_filtrado_df['Status'] == 'NÃO REALIZADA'))]
        
        # Criar uma tabela dinâmica (pivot table) para passageiros por data, usando 'Linha' e 'Tab' como índices
        pivot_df = pd.pivot_table(relatorio_filtrado_df, 
                                  values='Passageiros', 
                                  index=['Linha', 'Início Viagem Plan'], 
                                  columns='Data', 
                                  aggfunc='sum', 
                                  fill_value=0)
        
        # Exibir a tabela de passageiros por data, agrupada por Linha e Tab
        with col4:
            st.write(pivot_df)
    else:
        st.write("Não há dados disponíveis para o intervalo de datas selecionado.")

