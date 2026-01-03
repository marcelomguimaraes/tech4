#Importação das bibliotecas
import streamlit as st 
import pandas as pd

st.set_page_config(page_title="Painel Analítico", page_icon="📊")

st.sidebar.success("☝️ Navegue pelas sessões.")
st.sidebar.info('Desenvolvido por Marcelo Luiz Mendes Guimarães no Tech Challenge da Fase 4 do curso de Data Analytics da FIAP. 🏆')

st.title('📊 Painel Analítico do Estudo')

st.markdown(
    '''
<iframe title="dashboard" width="100%" height="500" src="https://app.powerbi.com/view?r=eyJrIjoiOTU4YTNkNTItZTU5NS00MTZlLWJlOGYtOTViYWRlODU1MTBmIiwidCI6IjExZGJiZmUyLTg5YjgtNDU0OS1iZTEwLWNlYzM2NGU1OTU1MSIsImMiOjR9" frameborder="0" allowFullScreen="true"></iframe>
    ''',unsafe_allow_html=True
)
