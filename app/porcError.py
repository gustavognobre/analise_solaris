import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))       

import streamlit as st
import pandas as pd
import plotly.express as px

def porcError(df):
    df = df.dropna(subset=['CodErrorDescri'])
    df = df[~df['CodErrorDescri'].isin(['VIA', 'REF','NAN'])]
    porc_error = px.pie(df, names='CodErrorDescri', title='Causas de erro no período')
    st.plotly_chart(porc_error, use_container_width=True)
def contError(df):
    df = df.dropna(subset=['CodErrorDescri'])
    df = df[~df['CodErrorDescri'].isin(['VIA', 'REF','NAN'])]
    count_error = px.bar(df, x='CodErrorDescri', color='CodErrorDescri',title='Causas de erro no período')
    st.plotly_chart(count_error, use_container_width=True)

def errorTI(df):
    df = df.dropna(subset=['CodErrorDescri'])
    df = df[~df['CodError'].isin(['VIA', 'REF','NAN'])]
    t_error_df = df[df['CodError'].str[:1].str.upper() == 'T']
    t_error_counts = t_error_df.groupby(t_error_df['Data']).size().reset_index(name='Counts')
    erros_ti = px.line(t_error_counts, x='Data', y='Counts', title='Número de Ocorrências de Código de Erro TI por Data')            
    st.plotly_chart(erros_ti, use_container_width=True)

