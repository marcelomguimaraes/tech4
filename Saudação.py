import streamlit as st

st.set_page_config(
    page_title="Primeiros Passos",
    page_icon="👋",
)


st.sidebar.success("☝️ Navegue pelas sessões.")
st.sidebar.info('Desenvolvido por Marcelo Luiz Mendes Guimarães no Tech Challenge da Fase 4 do curso de Data Analytics da FIAP. 🏆')

st.markdown(
    """
    <h2>👩‍⚕️✨ É muito bom ter você aqui!</h2>
    <p>Sabemos que <strong>cuidar da saúde</strong> é um ato que requer atenção, empatia e ciência — e é por isso que preparamos uma ferramenta especialmente para você <strong>aprimorar a análise do risco de obesidade</strong> dos seus pacientes.</p>

    <p>Tudo foi cuidadosamente desenvolvido com o olhar voltado para o dia a dia clínico, com uma <strong>interface amigável</strong> e focada em <strong>facilitar o seu trabalho.</strong> Você conseguirá identificar pacientes em situação de risco de obesidade com base em hábitos alimentares e estilo de vida.</p>
    
    <p>Além disso, você poderá consultar informações a partir de um estudo realizado. Muito legal, não é?</p>
    
    <p>Por isso, organizamos esta ferramenta em duas sessões, nas quais você encontrará:</p>
    
    <p>📈 <strong>1. Análise de Obesidade:</strong> ao preencher o formulário, você terá uma resposta assertiva do risco de obesidade do seu paciente.</p>
    <p>📊 <strong>2. Painel Analítico:</strong> com base em um estudo feito, você encontrará insights sobre os principais comportamentos que levam a obesidade.</p>
    
    <p style="font-weight: 600">💬 Em um mundo onde a saúde é prioridade, essa ferramenta é um convite: para entender mais, prevenir mais e cuidar ainda melhor.</p>
    
    <p><strong>Vamos começar?</strong> É só navegar nas páginas ao lado. 🤗</p>
""",unsafe_allow_html=True
)
