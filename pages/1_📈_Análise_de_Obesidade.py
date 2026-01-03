#Importação das bibliotecas
import streamlit as st 
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
import joblib
from joblib import load
import time as t
import os
import warnings

warnings.filterwarnings("ignore")

df = pd.read_csv(r'https://raw.githubusercontent.com/marcelomguimaraes/tech4/refs/heads/main/dataset/df_clean.csv', sep=";")


#df = pd.read_excel(r'https://raw.githubusercontent.com/marcelomguimaraes/tech4/main/dataset/df_clean.xlsx')

st.set_page_config(page_title="Análise do Risco de Obesidade", page_icon="📈")

st.sidebar.success("☝️ Navegue pelas sessões.")
st.sidebar.info('Desenvolvido por Marcelo Luiz Mendes Guimarães no Tech Challenge da Fase 4 do curso de Data Analytics da FIAP. 🏆')


st.title('👨‍⚕️ Risco de Obesidade')

st.markdown(
    '''
    <p style="font-size: 16px; line-height: 1.6; text-align: justify"><strong>Que tal preencher o formulário abaixo para descobrir o risco de obesidade do paciente?</strong> Basta informar alguns dados sobre hábitos e características para receber uma avaliação simples e esclarecedora, que ajudará a entender melhor a saúde e identificar possíveis pontos de atenção.</p> 
    <p style="font-size: 16px; font-weight: 600">Vamos começar? 🚀✨</p>
    ''', unsafe_allow_html=True)

st.markdown(
    '''
    <div style="padding: 20px 0;">
        <h3>1º Passo | Características Pessoais </h3>
        <p style="text-align: justify; line-height: 1.6"><strong>Vamos começar preenchendo os dados pessoais?</strong> Essas informações são importantes para que possamos ter uma visão geral do paciente e oferecer uma avaliação mais completa.</p>
    </div>
    ''', unsafe_allow_html=True
)

col1, col2 = st.columns(2)

with col1:
    input_idade = int(st.slider('📅 Idade: ', 1, 120))

with col2:
    input_sexo = st.selectbox('♂️ Sexo: ', ['Feminino', 'Masculino'])
    input_sexo = 0 if input_sexo == 'Feminino' else 1

col1, col2 = st.columns(2)

with col1:
    input_altura = float(st.number_input(label='📏 Altura (em metros): ', min_value = 0.3, max_value = 2.5, value=1.5, step = 0.01, format='%.2f'))

with col2:
    input_peso = float(st.number_input(label='⚖️ Peso (em kgs): ', min_value = 1.0, max_value = 400.0, value=60.0, step = 0.01, format='%.2f'))
    
col1, col2 = st.columns(2)

with col1:
    input_hf = st.selectbox('👨‍👩‍👧‍👦 Há histórico na família? ', ['Não', 'Sim'])
    input_hf = 0 if input_hf == 'Não' else 1
    
st.markdown(
    '''
    <div style="padding: 20px 0;">
        <h3>2º Passo | Práticas Alimentares </h3>
        <p style="text-align: justify; line-height: 1.6">Agora que já conhecemos um pouco melhor o paciente, <strong>chegou o momento de falar sobre a alimentação.</strong> Nesta etapa, você irá informar alguns hábitos alimentares do dia a dia, como escolhas de alimentos e frequência das refeições.</p>
    </div>
    ''', unsafe_allow_html=True
)

col1, col2 = st.columns(2)

with col1:
    input_mcc = st.selectbox('🧮 Monitora a ingestão calórica? ', ['Não', 'Sim'])
    input_mcc = 0 if input_mcc == 'Não' else 1

with col2:
    input_ncp = st.selectbox('🍽️ Quantas Refeições Principais? ', ['Apenas uma', 'Duas Refeições', 'Três Refeições', 'Quatro ou mais'])
    if input_ncp == 'Apenas uma':
        input_ncp = 1
    elif input_ncp == 'Duas Refeições':
        input_ncp = 2
    elif input_ncp == 'Três Refeições':
        input_ncp = 3
    else:
        input_ncp = 4
    

col1, col2 = st.columns(2)

with col1:
    input_caec = st.selectbox('🍟 Hábito de comer lanches entre as refeições? ', ['Não', 'Sempre', 'Frequentemente', 'Ocasionalmente'])
    if input_caec == 'Sempre':
        input_caec = 3
    elif input_caec == 'Frequentemente':
        input_caec = 2
    elif input_caec == 'Ocasionalmente':
        input_caec = 1
    else:
        input_caec = 0

with col2:
    input_fcvc = st.selectbox('🥕 Qual a frequência de vegetais nas refeições? ', ['Sempre', 'Ocasionalmente', 'Muito difícil'])
    if input_fcvc == 'Sempre':
        input_fcvc = 3
    elif input_fcvc == 'Ocasionalmente':
        input_fcvc = 2
    else:
        input_fcvc = 1    


col1, col2 = st.columns(2)

with col1:
    input_favc = st.selectbox('🍕 Hábito de consumir alimentos altamente calóricos? ', ['Não', 'Sim'])
    input_favc = 0 if input_favc == 'Não' else 1

with col2:
    input_ca = st.selectbox('🫗 Qual é o consumo diário de água? ', ['Acima de 2 litros', 'Entre 1 litro e 2 litros','Até 1 litro'])
    if input_ca == 'Até 1 litro':
        input_ca = 1
    elif input_ca == 'Entre 1 litro e 2 litros':
        input_ca = 2
    else:
        input_ca = 3    

col1, col2 = st.columns(2)

with col1:
    input_calc = st.selectbox('🍷 Hábito de consumir bebidas alcoólicas? ', ['Não', 'Sempre', 'Frequentemente', 'Ocasionalmente'])
    if input_calc == 'Sempre':
        input_calc = 3
    elif input_calc == 'Frequentemente':
        input_calc = 2
    elif input_calc == 'Ocasionalmente':
        input_calc = 1
    else:
        input_calc = 0

with col2:
    input_fumante = st.selectbox('🚬 Hábito de fumar? ', ['Não', 'Sim'])
    input_fumante = 0 if input_fumante == 'Não' else 1

st.markdown(
    '''
    <div style="padding: 20px 0;">
        <h3>3º Passo | Estilo de Vida </h3>
        <p style="text-align: justify; line-height: 1.6"><strong>Ah, e ainda falta falar sobre o estilo de vida do paciente!</strong> Nesta etapa final, pedimos que você preencha as informações abaixo relacionadas à rotina, como nível de atividade física e outros hábitos do dia a dia.</p>
    </div>
    ''', unsafe_allow_html=True
)

input_faf = st.selectbox('🏃 Qual é frequência de atividade física? ', ['De 1 a 2 vezes por semana', 'De 3 a 4 vezes por semana', '5 vezes ou mais', 'Não Pratica'])
if input_faf == 'Não Pratica':
    input_faf = 0
elif input_faf == 'De 1 a 2 vezes por semana':
    input_faf = 1
elif input_faf == 'De 3 a 4 vezes por semana':
    input_faf = 2
else:
    input_faf = 3  


input_tue = st.selectbox('💻 Qual é tempo médio gasto em dispositivos eletrônicos? ', ['Até 2h', 'De 2h a 5h', 'Acima de 5h'])
if input_tue == 'Até 2h':
    input_tue = 0
elif input_tue == 'De 2h a 5h':
    input_tue = 1
else:
    input_tue = 2 


input_mtrans = st.selectbox('🚌 Qual é meio de transporte que mais utiliza? ', ['Transporte Público', 'Carro', 'Moto', 'Bicicleta', 'Caminhada'])
if input_mtrans == 'Transporte Público':
    input_mtrans = 2
elif input_mtrans == 'Carro':
    input_mtrans = 4
elif input_mtrans == 'Moto':
    input_mtrans = 3
elif input_mtrans == 'Bicicleta':
    input_mtrans = 1
else:
    input_mtrans = 0

imc = round(input_peso / (input_altura ** 2), 1)

paciente = [input_sexo, input_idade, input_peso, input_hf, input_favc, input_fcvc, input_ncp, input_caec, input_fumante, input_ca, input_mcc, input_faf, input_tue, input_calc, input_mtrans, imc, 0]

def data_split(df, test_size):
    SEED = 42
    treino_df, teste_df = train_test_split(df, test_size=test_size, random_state=SEED)
    return treino_df.reset_index(drop=True), teste_df.reset_index(drop=True)

treino_df, teste_df = data_split(df, 0.2)

#Criando novo paciente
paciente_predict_df = pd.DataFrame([paciente], columns=teste_df.columns)
print(paciente_predict_df['IMC'])

#Concatenando novo paciente ao dataframe dos dados de teste
teste_novo_paciente  = pd.concat([teste_df, paciente_predict_df], ignore_index=True)

paciente_predito = teste_novo_paciente.drop(['RISCO'], axis=1)

def acao_botao():
    print(paciente)
    modelo = joblib.load(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'model', 'xgb.joblib'))
    final_pred = modelo.predict(paciente_predito)
    imc_paciente = paciente_predict_df.loc[0, 'IMC']
    faf_paciente = paciente_predict_df.loc[0, 'FAF']
    calc_paciente = paciente_predict_df.loc[0, 'CALC']
    fumante_paciente = paciente_predict_df.loc[0, 'FUMANTE']
    caec_paciente = paciente_predict_df.loc[0, 'CAEC']
    favc_paciente = paciente_predict_df.loc[0, 'FAVC']
    hf_paciente = paciente_predict_df.loc[0, 'HF']

    st.markdown(
        '''
        <h2>📊 Resultado da avaliação</h2>
        ''',unsafe_allow_html=True
    )
    if final_pred[-1] == 0:

        st.success('Ebba, o paciente apresenta BAIXO RISCO de obesidade. Os fatores que contribuem para este resultado são:')
        
        if imc < 25:
            st.markdown(f'''<p>✅ O IMC está ótimo, com um resultado de: {imc_paciente:.1f}. Possuir um peso equilibrado é fundamental para uma boa qualidade de vida.</p>''', unsafe_allow_html=True)
        
        if faf_paciente >= 2:
            st.markdown(f'''<p>✅ Pratica atividade com frequência: 3x ou mais por semana, favorecendo a manutenção de um peso coerente à altura, além de proporcionar melhor qualidade de vida.</p>''', unsafe_allow_html=True)

        if favc_paciente == 0:
            st.markdown(f'''<p>✅ Não tem o hábito de consumir alimentos altamente calóricos, o que contribui para uma alimentação mais balanceada.</p>''', unsafe_allow_html=True)
        
        if caec_paciente <= 1:
            st.markdown(f'''<p>✅ Consome lanches entre as refeições principais, mas de forma controlada. Tudo é uma questão de equilíbrio.</p>''', unsafe_allow_html=True)           
        
        if fumante_paciente == 0:
            st.markdown(f'''<p>✅ Não tem hábito de fumar, o que proporciona melhor qualidade de vida e evita problemas respiratórios no futuro.</p>''', unsafe_allow_html=True)
        
        if calc_paciente < 2:
            st.markdown(f'''<p>✅ Não tem hábito de consumir bebida alcoólica em demasia.</p>''', unsafe_allow_html=True)
        
        if imc >= 25 or faf_paciente < 2 or fumante_paciente == 1 or favc_paciente == 1:
            st.info(
                '''Ahh, mas nem tudo são flores. Aqui, seguem alguns pontos de acompanhamento:'''
            )
            if imc >= 25:
                st.markdown(
                    '''
                    ⚠️ O IMC está em uma faixa que índica um leve sobrepeso, mas controlado. É importante ficar de olho na evolução do peso do paciente nos próximos meses.
                    ''', unsafe_allow_html=True
                )
            
            if faf_paciente < 2:
                st.markdown(
                    '''
                    ⚠️ A frequência de atividade física não está legal. A OMS sugere a prática de 150 minutos semanais, de forma espaçada, para uma vida saudável. Não é sobre quantidade, mas consistência. 😉
                    ''', unsafe_allow_html=True
                )         
            
            if favc_paciente == 1:
                st.markdown(f'''<p>⚠️ O consumo de alimentos altamente calóricos não pode ser tão frequente. É necessário buscar um equilíbrio entre o prazeroso e o saudável.</p>''', unsafe_allow_html=True)
            
            if fumante_paciente == 1:
                st.markdown(
                    '''
                    ⚠️ O consumo de cigarro pode contribuir para o desenvolvimento não somente da obesidade, mas, sobretudo, de doenças respiratórias. É importante tratar o vício do paciente para uma melhor qualidade de vida. 👊
                    ''', unsafe_allow_html=True
                )  
            
                    
            if calc_paciente >= 2:
                st.markdown(f'''<p>⚠️ Consumir bebida alcoólica ocasionalmente e com prudência pode ser bem-vindo em situações sociais, mas não com alta frequência. Além de ocasionar diversos problemas de saúde à longo prazo, o álcool é altamente calórico e, portanto, prejudica uma ingestão equilibrada de calorias.</p>''', unsafe_allow_html=True)
                
            
            
        st.balloons()
    else:
        st.error('🚨 Ahh, o paciente apresenta um ALTO RISCO de obesidade. Os fatores que contribuem são:')  
        if imc >= 25:
            st.markdown(
                f'''
                ⛔ O IMC está em uma faixa acima do limite considerado normal (até 24.9), o que indica claramente que o peso está descompassado, resgistrando um resultado de: {imc_paciente:.1f}.
                ''', unsafe_allow_html=True
            )
            
            if faf_paciente < 2:
                st.markdown(
                    '''
                    ⛔ A frequência de atividade física está baixa. Aqui é um dos pilares para contornar a situação e alcançar um equilíbrio na vida do paciente. Lembrando que, a OMS sugere a prática de 150 minutos semanais. 😉
                    ''', unsafe_allow_html=True
                )         
            
            if hf_paciente == 1:
                st.markdown(f'''<p>⛔ Há histórico de obesidade na família. Trata-se de um problema crônico e, por isso, deve-se avaliar o contexto na qual o paciente está inserido com a finalidade de buscar alternativas reais, trazendo motivação em um cenário que promoverá mudança de hábitos.</p>''', unsafe_allow_html=True)
            
            if favc_paciente == 1:
                st.markdown(f'''<p>⛔ O consumo de alimentos altamente calóricos não pode ser tão frequente. É necessário buscar um equilíbrio entre o prazeroso e o saudável. É necessário rever a alimentação com o objetivo de reduzir a ingestão calórica.</p>''', unsafe_allow_html=True)
            
            if fumante_paciente == 1:
                st.markdown(
                    '''
                    ⛔ O consumo de cigarro pode contribuir para o desenvolvimento não somente da obesidade, mas, sobretudo, de doenças respiratórias. É importante tratar o vício do paciente para uma melhor qualidade de vida. 👊
                    ''', unsafe_allow_html=True
                )  
            
                    
            if calc_paciente >= 2:
                st.markdown(f'''<p>⛔ Consumir bebida alcoólica não é interessante neste contexto, visto que o álcool é altamente calórico e, portanto, compromete diretamente a ingestão diária. Além disso, estudos sugerem que o álcool, em excesso, compromete o ritmo do metabolismo.</p>''', unsafe_allow_html=True)
                
            if faf_paciente >= 2 or fumante_paciente == 0 or favc_paciente == 0 or calc_paciente == 0 or caec_paciente == 0:
                st.success(
                    '''Eeei, mas nem tudo está perdido. Aqui, seguem hábitos que o paciente deve continuar fazendo:'''
                )
                        
                if faf_paciente >= 2:
                    st.markdown(f'''<p>✅ Pratica atividade com frequência. É essencial manter a frequência e, talvez, pensar em aumentar a intensidade.</p>''', unsafe_allow_html=True)

                if favc_paciente == 0:
                    st.markdown(f'''<p>✅ Não consumir alimentos altamente calóricos é um ponto muito importante. Será necessário manter este comportamento para minimizar o quadro atual.</p>''', unsafe_allow_html=True)
                
                if caec_paciente ==  0:
                    st.markdown(f'''<p>✅ Não consome lanches entre as refeições principais. Manter o foco nas refeições principais pode ser uma boa estratégia.</p>''', unsafe_allow_html=True)           
                
                if fumante_paciente == 0:
                    st.markdown(f'''<p>✅ Não tem hábito de fumar. Que continue assim! Alterar este comportamento poderá agravar severamente a vida do paciente.</p>''', unsafe_allow_html=True)
                
                if calc_paciente == 0:
                    st.markdown(f'''<p>✅ Não tem hábito de consumir bebida alcoólica. É importante manter este hábito porque bebiba alcoólica é altamente calórica e somente prejudicaria o paciente em um cenário de reversão.</p>''', unsafe_allow_html=True)
        
    
if st.button(label='Exibir Resultado da Análise de Obesidade', icon="🔥", type='primary', width="stretch"):
    acao_botao()







