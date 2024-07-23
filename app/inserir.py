import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import streamlit as st
import pandas as pd
from lib.csvdb import display_relatorio_combinado, process_csv_file 


def inserirDados():
    st.title("Adicionar Relatórios ao Relatório Completo")
    csv_files = st.file_uploader("Selecione os arquivos CSV do relatório:", type=["csv"], accept_multiple_files=True)
    
    relatorio_combinado_df = display_relatorio_combinado()

    if csv_files:
        progress_bar = st.progress(0)
        progress_text = st.empty()
        
        total_files = len(csv_files)
        processed_files = 0
        
        for idx, csv_file in enumerate(csv_files):
            progress_bar.progress((processed_files / total_files))
            relatorio_combinado_df = process_csv_file(csv_file, relatorio_combinado_df)
            processed_files += 1
            # Atualizar a barra de progresso

            progress_text.text(f"Processando arquivo {processed_files} de {total_files}")
        
        # Após o processamento, exibir o relatório combinado atualizado
        st.write("Relatório Combinado Atualizado:")
    else:
        st.write("Nenhum arquivo CSV selecionado.")