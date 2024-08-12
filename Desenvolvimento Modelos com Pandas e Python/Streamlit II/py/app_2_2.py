
import pandas            as pd
import streamlit         as st
import seaborn           as sns
import matplotlib.pyplot as plt
from PIL                 import Image

custom_params = {"axes.spines.right": False, "axes.spines.top": False}
sns.set_theme(style="ticks", rc=custom_params)

def multiselect_filter(relatorio, col, selecionados):
    if 'all' in selecionados:
        return relatorio
    else:
        return relatorio[relatorio[col].isin(selecionados)].reset_index(drop=True)

def main():
    st.set_page_config(page_title = 'Telemarketing analisys', \
        page_icon = '../img/telmarketing_icon.png',
        layout="wide",
        initial_sidebar_state='expanded'
    )
    st.write('# Telemarketing analisys')
    st.markdown("---")
    
    image = Image.open("../img/Bank-Branding.jpg")
    st.sidebar.image(image)

    
    bank_raw = pd.read_csv('../data/input/bank-additional-full.csv', sep=';')
    bank = bank_raw.copy()

    st.write('## Antes dos filtros')
    st.write(bank_raw.head())

    with st.sidebar.form(key='my_form'):
    
        # IDADES
        max_age = int(bank.age.max())
        min_age = int(bank.age.min())
        idades = st.slider(label='Idade', 
                            min_value = min_age,
                            max_value = max_age, 
                            value = (min_age, max_age),
                            step = 1)
        st.write('IDADES:', idades)
        st.write('IDADE MIN:', idades[0])
        st.write('IDADE MAX:', idades[1])

        # PROFISSÕES
        jobs_list = bank.job.unique().tolist()
        st.write('PROFISSÕES DISPONIVEIS:', jobs_list)
        jobs_list.append('all')
        jobs_selected =  st.multiselect("Profissão", jobs_list, ['all'])
        st.write('PROFISSÕES SELECIONADAS:', jobs_selected)

        # bank = (bank.query("age >= @idades[0] and age <= @idades[1]")
        #             .pipe(multiselect_filter, 'job', jobs_selected)
        # )

        bank = bank[(bank['age'] >= idades[0]) & (bank['age'] <= idades[1])]
        bank = multiselect_filter(bank, 'job', jobs_selected)

        submit_button = st.form_submit_button(label='Aplicar')
    
    st.write('## Após os filtros')
    st.write(bank.head())
    st.markdown("---")

    # PLOTS    
    fig, ax = plt.subplots(1, 2, figsize = (5,3))

    bank_raw_target_perc = bank_raw.y.value_counts(normalize = True).to_frame()*100
    bank_raw_target_perc = bank_raw_target_perc.sort_index()
    sns.barplot(x = bank_raw_target_perc.index, 
                y = 'y',
                data = bank_raw_target_perc, 
                ax = ax[0])
    ax[0].bar_label(ax[0].containers[0])
    ax[0].set_title('Dados brutos',
                    fontweight ="bold")
    
    try:
        bank_target_perc = bank.y.value_counts(normalize = True).to_frame()*100
        bank_target_perc = bank_target_perc.sort_index()
        sns.barplot(x = bank_target_perc.index, 
                    y = 'y', 
                    data = bank_target_perc, 
                    ax = ax[1])
        ax[1].bar_label(ax[1].containers[0])
        ax[1].set_title('Dados filtrados',
                        fontweight ="bold")
    except:
        st.error('Erro no filtro')
    
    st.write('## Proporção de aceite')

    st.pyplot(plt)


if __name__ == '__main__':
	main()
    









