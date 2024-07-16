import os
import pandas as pd
import streamlit as st

def get_relatorio_combinado_path():
    return os.path.join("..", "lib", "relatorio_combinado.csv")

def load_csv():
    path = get_relatorio_combinado_path()
    if os.path.exists(path):
        return pd.read_csv(path, sep=";")
    return pd.DataFrame()

def save_csv(df):
    path = get_relatorio_combinado_path()
    # Forçar nomes de coluna para string antes de salvar
    df.columns = df.columns.astype(str)
    df.to_csv(path, sep=";", index=False)

def display_relatorio_combinado():
    relatorio_combinado_df = load_csv()
    if not relatorio_combinado_df.empty:
        st.write("Relatório Combinado Atual:")
        st.write(relatorio_combinado_df)
    else:
        st.write("Relatório Combinado ainda não existe. Você pode adicionar relatórios individualmente.")
    return relatorio_combinado_df

def ensure_string_columns(df, columns):
    for col in columns:
        df[col] = df[col].apply(lambda x: str(x) if pd.notnull(x) else '')
    return df

def process_csv_file(csv_file, relatorio_combinado_df):
    print(f"Processando arquivo CSV: {csv_file.name}")
    novo_df = pd.read_csv(csv_file, sep=";")
    
    # Converte colunas para os tipos corretos
    novo_df['Observação'] = novo_df['Observação'].astype(str)
    novo_df['CodError'] = novo_df['Observação'].apply(lambda x: x[:3].upper() if x else '')
    novo_df['CodError'] = novo_df['CodError'].fillna('')
    
    # Trata a coluna 'Veículo Real' para garantir que todos os valores sejam strings
    novo_df = ensure_string_columns(novo_df, ['Veículo Real'])
    
    # Converte a coluna de data para o formato adequado
    novo_df["Data"] = pd.to_datetime(novo_df["Data"], format='%d/%m/%Y', errors='coerce')
    novo_df["Data"] = novo_df["Data"].dt.strftime("%Y-%m-%d")
    
    # Converter os tipos de dados de novo_df para tipos compatíveis com Arrow
    novo_df = novo_df.convert_dtypes()

    if relatorio_combinado_df is not None and not relatorio_combinado_df.empty:
        # Exclui entradas vazias ou totalmente NA antes de concatenar
        relatorio_combinado_df = pd.concat([relatorio_combinado_df.dropna(how='all'), novo_df.dropna(how='all')], ignore_index=True)
    else:
        relatorio_combinado_df = novo_df

    # Garantir que todos os tipos de coluna de relatorio_combinado_df são compatíveis com Arrow
    relatorio_combinado_df = ensure_string_columns(relatorio_combinado_df, ['Veículo Real'])
    relatorio_combinado_df = relatorio_combinado_df.convert_dtypes()

    save_csv(relatorio_combinado_df)
    print(f"Relatório Combinado Atualizado:\n{relatorio_combinado_df}")
    return relatorio_combinado_df

def filter_by_date_range(data_inicio, data_fim):
    df = load_csv()  # Carrega o DataFrame do CSV
    if not df.empty:
        df["Data"] = pd.to_datetime(df["Data"])  # Converte a coluna 'Data' para datetime
        df = ensure_string_columns(df, ['Veículo Real'])
        
        # Corrigindo o aviso de FutureWarning
        df.loc[:, "Início Viagem Diff"] = df["Início Viagem Diff"].fillna(0)
        
        relatorio_filtrado_df = df[
            (df["Data"] >= data_inicio) & (df["Data"] <= data_fim)
        ]
        return relatorio_filtrado_df
    else:
        st.write("O DataFrame está vazio. Não há dados para filtrar.")
        return pd.DataFrame()