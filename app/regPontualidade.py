import streamlit as st
from lib.csvdb import filter_by_date_range
import pandas as pd
import plotly.express as px

def Pontualidade():
    col1, col2 = st.columns(2)
    with col1:
        data_inicio = pd.to_datetime(st.date_input("Selecione a data de início:"))
    with col2:
        data_fim = pd.to_datetime(st.date_input("Selecione a data de término:"))
    
    # Filtrar o relatório combinado pelo intervalo de datas
    relatorio_filtrado_df = filter_by_date_range(data_inicio, data_fim)
    
    if not relatorio_filtrado_df.empty:
        # Aplicar o filtro adicional para "Início Viagem Diff"
        filtered_df = relatorio_filtrado_df[
            (relatorio_filtrado_df['Início Viagem Diff'] < -3) | 
            (relatorio_filtrado_df['Início Viagem Diff'] > 10)
        ]
        
        if not filtered_df.empty:
            # Exibir as colunas específicas do DataFrame filtrado
            st.write(filtered_df[['Linha', 'Início Viagem Diff', 'Motorista']])
            
            # Calcular a porcentagem de viagens pontuais por dia
            filtered_df['Data'] = pd.to_datetime(filtered_df['Data'])
            total_viagens_df = relatorio_filtrado_df.groupby(relatorio_filtrado_df['Data'].dt.date).size().reset_index(name='Total')
            punctual_viagens_df = filtered_df.groupby(filtered_df['Data'].dt.date).size().reset_index(name='Punctual')
            
            efficiency_df = pd.merge(total_viagens_df, punctual_viagens_df, on='Data', how='left')
            efficiency_df['Punctual'] = efficiency_df['Punctual'].fillna(0)
            efficiency_df['Efficiency (%)'] = 100-((efficiency_df['Punctual'] / efficiency_df['Total']) * 100)
            
            # Gerar o gráfico de eficiência de pontualidade por dia
            fig = px.line(efficiency_df, x='Data', y='Efficiency (%)', title='Eficiência de Pontualidade por Dia (%)')
            st.plotly_chart(fig)
            
            # Adicionar seletor de motorista
            motoristas = relatorio_filtrado_df['Motorista'].unique()
            motorista_selecionado = st.selectbox("Selecione o motorista:", motoristas)
            
            # Filtrar os dados pelo motorista selecionado
            motorista_df = filtered_df[filtered_df['Motorista'] == motorista_selecionado]
            
            if not motorista_df.empty:
                # Calcular a porcentagem de viagens pontuais por dia para o motorista selecionado
                total_viagens_motorista_df = relatorio_filtrado_df[relatorio_filtrado_df['Motorista'] == motorista_selecionado].groupby(relatorio_filtrado_df['Data'].dt.date).size().reset_index(name='Total')
                punctual_viagens_motorista_df = motorista_df.groupby(motorista_df['Data'].dt.date).size().reset_index(name='Punctual')
                
                efficiency_motorista_df = pd.merge(total_viagens_motorista_df, punctual_viagens_motorista_df, on='Data', how='left')
                efficiency_motorista_df['Punctual'] = efficiency_motorista_df['Punctual'].fillna(0)
                efficiency_motorista_df['Efficiency (%)'] = 100- ((efficiency_motorista_df['Punctual'] / efficiency_motorista_df['Total']) * 100)
                
                # Gerar o gráfico de eficiência de pontualidade por dia para o motorista selecionado
                fig_motorista = px.line(efficiency_motorista_df, x='Data', y='Efficiency (%)', title=f'Eficiência de Pontualidade por Dia - Motorista: {motorista_selecionado} (%)')
                st.plotly_chart(fig_motorista)
            else:
                st.write("Não há dados disponíveis para o motorista selecionado.")
        else:
            st.write("Não há dados que atendem aos critérios de filtro.")
    else:
        st.write("Não há dados disponíveis para o intervalo de datas selecionado.")
