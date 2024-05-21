import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import sys
import os

sns.set()
def plota_pivot_table(df, value, index, func, ylabel, xlabel, opcao='nada'):
    if opcao == 'nada':
        pd.pivot_table(df, values=value, index=index,aggfunc=func).plot(figsize=[15, 5])
    elif opcao == 'unstack':
        pd.pivot_table(df, values=value, index=index,aggfunc=func).unstack().plot(figsize=[15, 5])
    elif opcao == 'sort':
        pd.pivot_table(df, values=value, index=index,aggfunc=func).sort_values(value).plot(figsize=[15, 5])
    plt.ylabel(ylabel)
    plt.xlabel(xlabel)
    return None
meses = []
for arg in sys.argv[1:]:
    meses.append(arg)

for mes in meses:
    sinasc = pd.read_csv('./input/SINASC_RO_2019_'+mes+'.csv')
    max_data = sinasc.DTNASC.max()[:7]
    os.makedirs('./output/figs/'+max_data, exist_ok=True)

    plota_pivot_table(sinasc, 'IDADEMAE', 'DTNASC', 'mean', 'média idade mãe por data', 'data nascimento', 'nada')
    plt.savefig('./output/figs/'+max_data+'/media idade mae por data.png')
    plt.close()

    plota_pivot_table(sinasc, 'IDADEMAE', ['DTNASC', 'SEXO'], 'mean', 'media idade mae','data de nascimento','unstack')
    plt.savefig('./output/figs/'+max_data+'/media idade mae por sexo.png')
    plt.close()

    plota_pivot_table(sinasc, 'PESO', ['DTNASC', 'SEXO'], 'mean', 'media peso bebe','data de nascimento','unstack')
    plt.savefig('./output/figs/'+max_data+'/media peso bebe por sexo.png')
    plt.close()

    plota_pivot_table(sinasc, 'PESO', 'ESCMAE', 'median', 'PESO mediano','escolaridade mae','sort')
    plt.savefig('./output/figs/'+max_data+'/PESO mediano por escolaridade mae.png')
    plt.close()

    plota_pivot_table(sinasc, 'APGAR1', 'GESTACAO', 'mean', 'apgar1 medio','gestacao','sort')
    plt.savefig('./output/figs/'+max_data+'/media apgar1 por gestacao.png')
    plt.close()
