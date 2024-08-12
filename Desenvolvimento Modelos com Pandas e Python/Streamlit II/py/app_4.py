
import timeit
import pandas            as pd
import streamlit         as st


# Função para ler os dados
@st.cache
def load_data(file_data):
    return pd.read_csv(file_data, sep=';')




def main():

    st.write('# Telemarketing analisys')
    st.markdown("---")
    
    start = timeit.default_timer()
    # bank_raw = pd.read_csv('../data/input/bank-additional-full-40.csv', sep=';')
    bank_raw = load_data('../data/input/bank-additional-full-40.csv')

    st.write('Time: ', timeit.default_timer() - start)  

    st.write(bank_raw.head())

if __name__ == '__main__':
	main()
    









