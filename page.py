import streamlit as st 
from streamlit_option_menu import option_menu
import pandas as pd
import os
from datetime import datetime
import plotly.express as px
import numpy as np

st.set_page_config(layout="wide")

with st.sidebar:
    selected = option_menu(
        menu_title="Main Menu",
        options=["Relatorio Sonda", "Plotagem gráfica", "Chamados"],
        menu_icon="cast",
        default_index=0,
    )

if selected == "Relatorio Sonda":
    st.title("Adicionar Relatório ao Relatório Completo")
    
    csv_file = st.file_uploader("Selecione o arquivo CSV do relatório:", type=["csv"])
    relatorio_combinado_path = "relatorio_combinado.csv"
    if os.path.exists(relatorio_combinado_path):
        relatorio_combinado_df = pd.read_csv(relatorio_combinado_path, sep=";")
        st.write("Relatório Combinado Atual:")
        st.write(relatorio_combinado_df)
    else:
        st.write("Relatório Combinado ainda não existe. Você pode adicionar relatórios individualmente.")

    

    if csv_file is not None:
        novo_df = pd.read_csv(csv_file, sep=";")
        # Convertendo a coluna 'Observação' para o tipo de dados string
        novo_df['Observação'] = novo_df['Observação'].astype(str)
        # Se a coluna 'Observação' estiver vazia, 'CodError' também será vazia
        novo_df['CodError'] = novo_df['Observação'].apply(lambda x: x[:3].upper() if x else '')
        # Preenchendo os valores NaN na coluna 'CodError' com uma string vazia
        novo_df['CodError'] = novo_df['CodError'].fillna('')
        # Convertendo a coluna de data para formato de data
        novo_df["Data"] = pd.to_datetime(novo_df["Data"], format='%d/%m/%Y')
        # Converte a coluna "Data" para o formato "Y M D" (Ano Mês Dia)
        novo_df["Data"] = novo_df["Data"].dt.strftime("%Y-%m-%d")

        if os.path.exists(relatorio_combinado_path):
            relatorio_combinado_df = pd.concat([relatorio_combinado_df, novo_df], ignore_index=True)
        else:
            relatorio_combinado_df = novo_df

        # Salvando o DataFrame no arquivo CSV
        relatorio_combinado_df.to_csv(relatorio_combinado_path, sep=";", index=False)

        # Exibindo o DataFrame atualizado
        st.write("Relatório Combinado Atualizado:")
        st.write(relatorio_combinado_df)

if selected == "Plotagem gráfica":
    
    

    st.title(f"Plotagem dos gráficos")

    relatorio_combinado_path = "relatorio_combinado.csv"
    if os.path.exists(relatorio_combinado_path):
        relatorio_combinado_df = pd.read_csv(relatorio_combinado_path, sep=";")
    else:
        st.write("Relatório Combinado ainda não existe. Você pode adicionar relatórios individualmente.")
    
    data_inicio = st.date_input("Selecione a data de início:")
    data_fim = st.date_input("Selecione a data de término:")

    if data_inicio and data_fim:
        data_inicio = datetime.combine(data_inicio, datetime.min.time())
        data_fim = datetime.combine(data_fim, datetime.max.time())
        relatorio_combinado_df["Data"] = pd.to_datetime(relatorio_combinado_df["Data"])
        relatorio_combinado_df['Veículo Real'] = 'A ' + relatorio_combinado_df['Veículo Real'].astype(str)
        relatorio_combinado_df["Início Viagem Diff"].fillna(0, inplace=True)

        relatorio_filtrado_df = relatorio_combinado_df[
            (relatorio_combinado_df["Data"] >= data_inicio) & (relatorio_combinado_df["Data"] <= data_fim)
        ]
         
        selected_chart = st.selectbox(
            "Selecione o gráfico que deseja visualizar:",
            ("Porcentagem de Erro", "Contagem de Erro", "Agrupação de erro por data", "Erros TI", 
            "Viagem Realizada", "Atraso de Viagem","Viagens por Veículo")
        )

        if selected_chart == "Porcentagem de Erro":
            df=relatorio_filtrado_df
            df = df.dropna(subset=['CodError'])
            df = df[~df['CodError'].isin(['VIA', 'REF','NAN'])]
            porc_error = px.pie(df, names='CodError', title='Causas de erro no período')
            st.plotly_chart(porc_error, use_container_width=True)
        elif selected_chart == "Contagem de Erro":
            df=relatorio_filtrado_df
            df = df.dropna(subset=['CodError'])
            df = df[~df['CodError'].isin(['VIA', 'REF','NAN'])]
            count_error = px.bar(df, x='CodError', color='CodError',title='Causas de erro no período')
            st.plotly_chart(count_error, use_container_width=True)
        elif selected_chart == "Agrupação de erro por data":
            df=relatorio_filtrado_df
            df = df.dropna(subset=['CodError'])
            df = df[~df['CodError'].isin(['VIA', 'REF','NAN'])]
            trips_count = df.groupby([df['Data'].dt.date, df['CodError'].str[:1].str.upper()]).size().reset_index(name='Count')
            viagem_erro_data = px.bar(trips_count, x='Data', y='Count', color='CodError', title='Agrupação de erro por data')
            st.plotly_chart(viagem_erro_data, use_container_width=True)
        elif selected_chart == "Erros TI":
            df=relatorio_filtrado_df
            df = df.dropna(subset=['CodError'])
            df = df[~df['CodError'].isin(['VIA', 'REF','NAN'])]
            t_error_df = df[df['CodError'].str[:1].str.upper() == 'T']
            t_error_counts = t_error_df.groupby(t_error_df['Data']).size().reset_index(name='Counts')
            erros_ti = px.line(t_error_counts, x='Data', y='Counts', title='Número de Ocorrências de Código de Erro TI por Data')            
            st.plotly_chart(erros_ti, use_container_width=True)
        elif selected_chart == "Viagem Realizada":
            df=relatorio_filtrado_df
            df1 = df
            v_reali = df1[df1['CodError'].str[:3].str.upper() == 'VIA']
            v_reali_counts = v_reali.groupby(v_reali['Data']).size().reset_index(name='Counts')
            viagem_realizada = px.line(v_reali_counts, x='Data', y='Counts', title='Número de Ocorrências de Viagens Realizadas por Data')
            st.plotly_chart(viagem_realizada, use_container_width=True)
        elif selected_chart == "Atraso de Viagem":
            dftime=relatorio_filtrado_df
            selected_atraso = st.selectbox("Selecione qual a relação gerar:", ("Motorista", "Veículo Real", "Data"))

            # Definir cores com base nos valores de "Início Viagem Diff"
            colors = np.where(dftime["Início Viagem Diff"] == -3, 'green',
                            np.where(dftime["Início Viagem Diff"] == 10, 'yellow',
                                    np.where((dftime["Início Viagem Diff"] < -15) |
                                                (dftime["Início Viagem Diff"] > 15), 'red', 'grey')))

            # Criar o gráfico de dispersão
            scatter_fig = px.scatter(dftime, x="Início Viagem Diff", y=selected_atraso,
                                    color=colors,
                                    title="Distribuição das Viagens em relação ao Tempo de Início",
                                    labels={"Início Viagem Diff": "Tempo de Início da Viagem",
                                            "Duração da Viagem": "Duração da Viagem"})

            # Exibir o gráfico
            st.plotly_chart(scatter_fig)
            dftime

if selected == "Chamados":
    # Função para editar um chamado existente
    def editar_chamado(chamado, df):
        # Preenche o formulário com os dados do chamado selecionado
        with st.form(key='editar_chamado_form'):
            st.write("Edite os detalhes do chamado:")
            # Verifica se o valor de data é um objeto de data válido
            if pd.notnull(chamado["Data"]):
                # Campo para data
                data = st.date_input("Data do Chamado", pd.to_datetime(chamado["Data"]))
            else:
                # Se não for válido, define a data como None
                data = st.date_input("Data do Chamado", None)
            # Verifica se o valor de hora é um objeto de hora válido
            if pd.notnull(chamado["Hora"]):
                # Campo para hora
                hora = st.time_input("Hora do Chamado", pd.to_datetime(chamado["Hora"]).time())
            else:
                # Se não for válido, define a hora como None
                hora = st.time_input("Hora do Chamado", None)
            # Campo para serviço realizado
            servico = st.text_input("Serviço Realizado", chamado["Serviço Realizado"])
            # Campo para local onde foi realizado
            local = st.text_input("Local do Serviço", chamado["Local"])
            # Campo para aparelho consertado
            aparelho = st.text_input("Aparelho Consertado", chamado["Aparelho"])
            # Botão para submeter as edições
            submit_button = st.form_submit_button(label='Salvar Alterações')

        # Verifica se o formulário foi submetido
        if submit_button:
            # Atualiza os dados do chamado no DataFrame
            index = df[df["Número do Chamado"] == chamado["Número do Chamado"]].index[0]
            df.at[index, "Data"] = data.strftime('%Y-%m-%d') if data is not None else None
            df.at[index, "Hora"] = hora.strftime('%H:%M:%S') if hora is not None else None
            df.at[index, "Serviço Realizado"] = servico
            df.at[index, "Local"] = local
            df.at[index, "Aparelho"] = aparelho
            # Salva o DataFrame atualizado no arquivo CSV
            df.to_csv("relatorio_os.csv", sep=";", index=False)
            # Mensagem de confirmação
            st.success("Chamado atualizado com sucesso!")

    # Verifica se o arquivo relatorio_os.csv existe, caso não exista, cria um novo dataframe vazio
    if not os.path.exists("relatorio_os.csv"):
        df = pd.DataFrame(columns=["Número do Chamado", "Data", "Hora", "Serviço Realizado", "Local", "Aparelho"])
    else:
        df = pd.read_csv("relatorio_os.csv", sep=";")

    # Título da aplicação
    st.title("Registro de Chamados de Serviço")

    # Formulário para registro de chamados
    with st.form(key='chamado_form'):
        st.write("Por favor, preencha o formulário abaixo:")
        # Campo para data
        data = st.date_input("Data do Chamado")
        # Campo para hora
        hora = st.time_input("Hora do Chamado")
        # Campo para serviço realizado
        servico = st.text_input("Serviço Realizado")
        # Campo para local onde foi realizado
        local = st.text_input("Local do Serviço")
        # Campo para aparelho consertado
        aparelho = st.text_input("Aparelho Consertado")
        # Botão para submeter o formulário
        submit_button = st.form_submit_button(label='Registrar Chamado')

    # Verifica se o formulário foi submetido
    if submit_button:
        # Adiciona os dados do chamado ao dataframe
        novo_chamado = pd.DataFrame({"Número do Chamado": [len(df)+1], "Data": [data], "Hora": [hora], "Serviço Realizado": [servico], "Local": [local], "Aparelho": [aparelho]})
        df = pd.concat([df, novo_chamado], ignore_index=True)
        # Salva o DataFrame atualizado no arquivo CSV
        df.to_csv("relatorio_os.csv", sep=";", index=False)
        # Mensagem de confirmação
        st.success("Chamado registrado com sucesso!")

    # Exibe os dados do dataframe
    st.write("Chamados Registrados:")
    for index, chamado in df.iterrows():
        # Exibe os detalhes do chamado
        st.write(f"Chamado {chamado['Número do Chamado']}:")
        st.write(f"Data: {chamado['Data']}, Hora: {chamado['Hora']}")
        st.write(f"Serviço Realizado: {chamado['Serviço Realizado']}")
        st.write(f"Local: {chamado['Local']}, Aparelho: {chamado['Aparelho']}")
        # Adiciona botões para editar e apagar o chamado
        if st.button(f"Editar Chamado {chamado['Número do Chamado']}"):
            editar_chamado(chamado, df)
        if st.button(f"Apagar Chamado {chamado['Número do Chamado']}"):
            df.drop(index, inplace=True)
            df.to_csv("relatorio_os.csv", sep=";", index=False)
            st.success("Chamado apagado com sucesso!")