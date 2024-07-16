# app/main.py
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import streamlit as st
from components.sidebar import sidebar  # Ajuste a importação para o novo caminho
from inserir import inserirDados
from visaoGeral import visaoGeral
from lib.csvdb import filter_by_date_range
import pandas as pd
from eficCom import eficienciaComunicação
from rotaAvanti import Point
from regPontualidade import Pontualidade
from indPassageiroRota import indPassageiro
# Título do aplicativo


# Labels para o menu
labels = ['Visão Geral', 'Inserir Dados', 'Análise de Error', 'Análise de Tráfego','Relatório de Pontualidade', 'Indíce de Passageiro Rota','Rota Avanti',]

# Chamar a função para criar o menu lateral e obter a seleção
option = sidebar("Escolha o dashboard", labels)

# Exibir o conteúdo baseado na opção selecionada
if option == 'Visão Geral':
    st.title("Dashboard de análise de tráfego")
    st.subheader("Visão Geral")
    st.write("Aqui vai a visão geral do tráfego.")
    # Adicione o conteúdo específico da Visão Geral

elif option == 'Inserir Dados':
    inserirDados()

elif option == 'Análise de Error':
    visaoGeral()
    # Adicione o conteúdo específico da Análise de Marketing

elif option == 'Análise de Tráfego':
    eficienciaComunicação()

elif option == 'Relatório de Pontualidade':
    Pontualidade()

elif option == 'Indíce de Passageiro Rota':
    indPassageiro()

elif option == 'Rota Avanti':
    Point()