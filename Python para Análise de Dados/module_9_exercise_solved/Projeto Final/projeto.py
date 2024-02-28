from functools import reduce

import pandas as pd  # data processing, CSV file I/O (e.g. pd.read_csv)
import os
import csv
import seaborn as sns
import matplotlib.pyplot as plt

df = pd.read_csv('Python_M10_support material.csv', na_values='na')
fn = lambda valor: float(valor.replace(".", "").replace(",", "."))
df['valor_transacoes_12m'] = df['valor_transacoes_12m'].apply(fn)
df['limite_credito'] = df['limite_credito'].apply(fn)
df.dropna(inplace=True)

sns.set_style("whitegrid")
df_adimplente = df[df['default'] == 0]
df_inadimplente = df[df['default'] == 1]



def grafico_barra(coluna=str):
    titulos = [f'{coluna} dos Clientes', f'{coluna} dos Clientes Adimplentes', f'{coluna} dos Clientes Inadimplentes']
    max = df.select_dtypes('object').describe()[coluna]['freq'] * 1.1
    eixo = 0
    max_y = 0
    figura, eixos = plt.subplots(1, 3, figsize=(20, 6), sharex=True)
    for dataframe in [df, df_adimplente, df_inadimplente]:
        df_to_plot = dataframe[coluna].value_counts()
        dfd = list(df_to_plot.keys())
        print(dfd[0])
        print(df_to_plot[dfd[0]])


        f = sns.barplot(x=dfd, y=df_to_plot[dfd], ax=eixos[eixo])
        f.set(title=titulos[eixo], xlabel=coluna.capitalize(), ylabel='Frequência Absoluta')
        f.set_xticklabels(labels=f.get_xticklabels(), rotation=90)

        _, max_y_f = f.get_ylim()
        max_y = max_y_f if max_y_f > max_y else max_y
        f.set(ylim=(0, max_y))

        eixo += 1
    figura.show()
    plt.savefig(f"{coluna}_barplot.png")


def grafico_barra_porcentagem(coluna=str):

    dfd = df[coluna].value_counts()
    dfd = list(dfd.keys())

    df_to_adimplente = list(df_adimplente[coluna].value_counts())
    df_to_inadimplente = list(df_inadimplente[coluna].value_counts())
    total_adimplente = reduce(lambda a, b: a + b, df_to_adimplente)
    total_inadimplente = reduce(lambda a, b: a + b, df_to_inadimplente)
    dfpercent_adimplente = list(map(lambda x: (float(x)*100)/total_adimplente, df_to_adimplente))
    print(dfpercent_adimplente)
    dfpercent_inadimplente = list(map(lambda x: (float(x) * 100) / total_inadimplente, df_to_inadimplente))
    print(dfpercent_inadimplente)
    total_diff = list(map(lambda a, b: b - a, dfpercent_adimplente,dfpercent_inadimplente))
    print(total_diff)

    f = sns.barplot(x=dfd, y=total_diff)

    f.set(title=f"Diferença na representatividade de inadimplencia por {coluna} ", xlabel=coluna.capitalize(), ylabel='Porcentagem')
    f.set_xticklabels(labels=f.get_xticklabels(), rotation=90)
    plt.tight_layout()


    plt.show()
    plt.savefig(f"{coluna}_Percent_barplot.png")




def grafico_hist(coluna = str):
    titulos = [f'{coluna} no Último Ano', f'{coluna} no Último Ano de Adimplentes', f'{coluna} no Último Ano de Inadimplentes']

    eixo = 0
    max_y = 0
    figura, eixos = plt.subplots(1,3, figsize=(20, 5), sharex=True)

    for dataframe in [df, df_adimplente, df_inadimplente]:

      f = sns.histplot(x=coluna, data=dataframe, stat='count', ax=eixos[eixo])
      f.set(title=titulos[eixo], xlabel=coluna.capitalize(), ylabel='Frequência Absoluta')

      _, max_y_f = f.get_ylim()
      max_y = max_y_f if max_y_f > max_y else max_y
      f.set(ylim=(0, max_y))

      eixo += 1

    figura.show()
    plt.savefig(f"{coluna}_hist.png")

# grafico_barra('escolaridade')
# grafico_barra('salario_anual')
# grafico_hist('qtd_transacoes_12m')

grafico_barra_porcentagem('escolaridade')
grafico_barra_porcentagem('salario_anual')
