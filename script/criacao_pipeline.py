import math
import matplotlib.pyplot as plt
import pandas as pd

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler, OneHotEncoder, OrdinalEncoder
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer

from imblearn.over_sampling import SMOTE
from imblearn.pipeline import Pipeline as ImbPipeline

from sklearn import metrics
from sklearn.metrics import classification_report, ConfusionMatrixDisplay, RocCurveDisplay, confusion_matrix, accuracy_score, precision_score, recall_score, f1_score, roc_auc_score, classification_report

#modelos
from sklearn.linear_model import LogisticRegression

import joblib

#VARIÁVEIS GLOBAIS
SEED = 42

#FUNÇÕES DE PADRONIZAÇÃO DAS VARIÁVEIS ORDINAIS
def padronizar_nivel_obesidade(nivel_obesidade):
    dict_obesidade = {
        'Insufficient_Weight':0,
        'Normal_Weight':1,
        'Overweight_Level_I':2,
        'Overweight_Level_II':3,
        'Obesity_Type_I':4,
        'Obesity_Type_II':5,
        'Obesity_Type_III':6
    }
    return dict_obesidade[nivel_obesidade]

def padronizar_consumo_bebida_alcoolica(frequencia):
    dict_frequencia_consumo = {
        'no':0,
        'Sometimes':1,
        'Frequently':2,
        'Always':3
    }
    return dict_frequencia_consumo[frequencia]

def padronizar_consumo_lanches_entre_refeicoes(caec):
    dict_consumo_lanches_entre_refeicoes = {
        'no':0,
        'Sometimes':1,
        'Frequently':2,
        'Always':3
    }
    return dict_consumo_lanches_entre_refeicoes[caec]


#FUNÇÕES DE PADRONIZAÇÃO DAS VARIÁVEIS NOMINAIS
def padronizar_meio_transporte(meio_transporte):
    dict_meio_transporte = {
        'Walking':0,
        'Bike':1,
        'Public_Transportation':2,
        'Motorbike':3,
        'Automobile':4
    }
    return dict_meio_transporte[meio_transporte]


#FUNÇÕES DE PADRONIZAÇÃO DAS VARIÁVEIS BINÁRIAS: Y | N --> 1 | 0
def padronizar_sexo(sexo):
    dict_sexo = {'Female':0, 'Male':1}
    return dict_sexo[sexo]

def padronizar_historico_familiar(hf):
    dict_historico_familiar = {'no': 0, 'yes':1}
    return dict_historico_familiar[hf]

def padronizar_consumo_alimentos_alta_caloria(favc):
    dict_consumo_alimentos_alta_caloria = {'no': 0, 'yes':1}
    return dict_consumo_alimentos_alta_caloria[favc]

def padronizar_fumante(fumante):
    dict_fumante = {'no':0, 'yes':1}
    return dict_fumante[fumante]

def padronizar_monitorar_consumo_calorico(mcc):
    dict_mcc = {'no':0, 'yes':1}
    return dict_mcc[mcc]


# FUNÇÕES PARA ORGANIZAÇÃO DOS DADOS
def df_importacao_dados():
    df = pd.read_csv(r'https://raw.githubusercontent.com/marcelomguimaraes/fiap/refs/heads/main/tech4/dataset/raw/obesity.csv', sep=',')
    return df

def df_renomear_colunas(df):
    # SEXO: informa o sexo;
    # IDADE: traz a idade;
    # ALTURA: traz a altura, em m;
    # PESO: traz o peso, em kg;
    # HF: indica se há histórico de obesidade na família;
    # FAVC: indica se há consumo frequente de alimentos calóricos;
    # FCVC: indica se há consumo frequente de vegetais;
    # NCP: indica a quantidade de refeições principais ao longo do dia;
    # CAEC: indica se há consumo de lanches entre as refeições (snack food);
    # FUMANTE: Indica se a pessoa é fumante;
    # CA: Indica o consumo de água por dia;
    # MCC: indica se a pessoa monitora o consumo de calorias;
    # FAF: indica a frequência semanal de atividade física;
    # TUE: indica o tempo diário de uso de dispositivos eletrônicos;
    # CALC: indica a frequência do consumo de bebida alcoólica;
    # MTRANS: indica qual é o meio de transporte que a pessoa utiliza; e
    # NO: indica o grau de obesidade.
    
    
    df.columns = ['SEXO', 'IDADE', 'ALTURA', 'PESO', 'HF', 'FAVC', 'FCVC', 'NCP', 'CAEC', 'FUMANTE', 'CA', 'MCC', 'FAF', 'TUE', 'CALC', 'MTRANS', 'NO']
    return df

def df_arredondar_valores_numericos(df):
    df['IDADE'] = df['IDADE'].map(lambda x : math.floor(x))
    df['ALTURA'] = df['ALTURA'].map(lambda x : round(x, 2))
    df['PESO'] = df['PESO'].map(lambda x : round(x, 1))
    df['CA'] = df['CA'].map(lambda x : math.ceil(x))
    df['FAF'] = df['FAF'].map(lambda x : math.floor(x))
    df['TUE'] = df['TUE'].map(lambda x : math.floor(x))
    df['FCVC'] = df['FCVC'].map(lambda x : math.floor(x)) 
    df['NCP'] = df['NCP'].map(lambda x : math.floor(x)) 
    return df

def df_criar_colunas(df):
    df['IMC'] = round(df['PESO'] / (df['ALTURA'] ** 2), 1)
    df['RISCO'] = df.apply(calcular_risco_obesidade, axis=1)
    return df

def calcular_risco_obesidade(df):
    # Tendo-se como objeto de análise o fator da obesidade, segundo a Organização Mundial da Saúde, os fatores que levam a uma vida saudável consistem nos seguintes aspectos: 
    
    # 1) Prática de atividade física (150 minutos/semana); 
    # 2) Alimentação Saudável (Redução de consumo de alimentos altamente calóricos); 
    # 3) Evitar consumo de álcool e cigarro; 
    # 4) Limitar o tempo em dispositivos eletrônicos (screen time) e entre outros hábitos, conforme expostos nos links: 
    
    # <https://www.who.int/news-room/fact-sheets/detail/obesity-and-overweight> e 
    # <https://www.who.int/health-topics/obesity#tab=tab_3>. 
    
    # Por este motivo e também levando em consideração entre as variáveis, criei um indicador que apresenta se o individual tem risco de obesidade a partir dos seus hábitos, considerando: 
    
    # 1) Índice de Massa Corpórea (IMC); 
    # 2) Frequência de atividade física (FAF); 
    # 3) Histórico familiar (HF); 
    # 4) Ingestão de snack foods entre refeições, que comumente são alimentos ultraprocessados e altamente calóricos; e
    # 5) Consumo de bebiba alcoólica.

    if df['IMC'] < 25:
            return 0
    elif df['IMC'] >= 30:
        return 1
    elif (df['IMC'] >= 25 and df['IMC'] < 30 and 
        (
            df['FAF'] in (0, 1) or 
            df['CAEC'] == 3 or 
            df['CALC'] > 0 or
            df['HF'] == 1
        )
    ):
        return 1 
    else:
        return 0


def df_padronizar_colunas(df):
    df['NO'] = df['NO'].map(lambda x : padronizar_nivel_obesidade(x))
    df['SEXO'] = df['SEXO'].map(lambda x : padronizar_sexo(x))
    df['CALC'] = df['CALC'].map(lambda x : padronizar_consumo_bebida_alcoolica(x))
    df['MTRANS'] = df['MTRANS'].map(lambda x : padronizar_meio_transporte(x))
    df['HF'] = df['HF'].map(lambda x : padronizar_historico_familiar(x))
    df['FAVC'] = df['FAVC'].map(lambda x : padronizar_consumo_alimentos_alta_caloria(x))
    df['CAEC'] = df['CAEC'].map(lambda x : padronizar_consumo_lanches_entre_refeicoes(x))
    df['FUMANTE'] =  df['FUMANTE'].map(lambda x : padronizar_fumante(x))
    df['MCC'] =  df['MCC'].map(lambda x : padronizar_monitorar_consumo_calorico(x))
    return df

def df_definir_colunas(df):
    df = df[['SEXO', 'IDADE', 'PESO', 'HF', 'FAVC', 'FCVC', 'NCP', 'CAEC', 'FUMANTE', 'CA', 'MCC', 'FAF', 'TUE', 'CALC', 'MTRANS', 'IMC', 'RISCO']]
    return df

def criar_df():
    df = df_importacao_dados()
    df = df_renomear_colunas(df)
    df = df_arredondar_valores_numericos(df)
    df = df_padronizar_colunas(df)
    df = df_criar_colunas(df)
    df = df_definir_colunas(df)
    return df

#FUNÇÕES PARA CRIAÇÃO DO MODELO
def analisar_modelo_ml(modelo, x_treino, y_treino, x_teste, y_teste):
    modelo.fit(x_treino, y_treino)
    y_pred = modelo.predict(x_teste)
    y_proba = modelo.predict_proba(x_teste)[:, 1]

    # ------------- Resultado das Métricas -------------
    acuracia = accuracy_score(y_teste, y_pred)
    precisao = precision_score(y_teste, y_pred)
    recall = recall_score(y_teste, y_pred)
    score_f1 = f1_score(y_teste, y_pred)
    score_auc = roc_auc_score(y_teste, y_proba)

    # Apresentar graficamente a matriz de confusão
    matriz = confusion_matrix(y_teste, y_pred, normalize='true')
    disp = ConfusionMatrixDisplay(confusion_matrix=matriz)
    disp.plot(cmap=plt.cm.Blues)
    plt.xlabel('Label Predita', fontsize=18)
    plt.ylabel('Label Verdadeira', fontsize=18)
    plt.title("Matriz de Confusão")
    plt.show()

    # Apresentar os resultados da Classification Report
    predicao = modelo.predict(x_teste)
    print(f"\n|------------- CLASSIFICATION REPORT -------------|")
    print(classification_report(y_teste, predicao))
    
    # Apresentar graficamente a Curva ROC
    RocCurveDisplay.from_predictions(y_teste, y_proba, name=f"Resultado AUC = {score_auc:.2f})")
    plt.plot([0, 1], [0, 1], linestyle="--", linewidth=1, color="red")
    plt.tight_layout()
    plt.xlabel('Taxa de Falsos Positivos (FPR)')
    plt.ylabel('Taxa de Verdadeiros Positivos (TPR)')
    plt.show()

    # Apresentação dos Resultados do modelo
    print(f"\n|------------- RESULTADOS DO MODELO -------------|")
    print(f"Acurácia do modelo : {acuracia:.2f}")
    print(f"Precisão do modelo : {precisao:.2f}")
    print(f"Recall   : {recall:.2f}")
    print(f"F1-score : {score_f1:.2f}")
    print(f"AUC-ROC  : {score_auc:.2f}")



# BASE DE TESTE E TREINO
def criar_base_teste_treino(df):
    x = df.drop('RISCO', axis=1)
    y = df['RISCO']
    x_treino, x_teste, y_treino, y_teste = train_test_split(x, y, test_size=0.2, stratify=y, random_state=42)
    return (x_treino, x_teste, y_treino, y_teste)


# CRIAÇÃO DO PIPELINE
def criar_pipeline():
    ##definição do tipo de variável
    variaveis_numericas = ['IDADE', 'IMC']
    variaveis_binarias = ['SEXO', 'FUMANTE', 'MCC', 'FAVC', 'HF']
    variaveis_nominais = ['NCP', 'FCVC', 'CA', 'FAF', 'TUE', 'MTRANS']
    variaveis_ordinais = ['CAEC', 'CALC']

    ##transformação das variáveis
    numerica_transformacao = Pipeline(steps=[('scaler', MinMaxScaler())])
    binario_transformacao = 'passthrough'
    nominais_transformacao = Pipeline(steps=[('onehot', OneHotEncoder(handle_unknown='ignore'))])
    ordinais_transformacao = Pipeline(steps=[('encoder', OrdinalEncoder(categories=[[0, 1, 2, 3], [0, 1, 2,3]]))])

    preprocessador = ColumnTransformer(
        transformers=[
            ('num', numerica_transformacao, variaveis_numericas),
            ('bin', binario_transformacao, variaveis_binarias),
            ('nom', nominais_transformacao, variaveis_nominais),
            ('ord', ordinais_transformacao, variaveis_ordinais)
        ]
    )
    
    return preprocessador


def criar_modelo_regressao(preprocessador):
    regressao_logistica = ImbPipeline(
        steps=[
            ('preprocess', preprocessador),
            ('smote', SMOTE(random_state=42)),
            ('clf', LogisticRegression(
                max_iter=1000,
                class_weight='balanced',
                solver='lbfgs',
                random_state=SEED
            ))
        ])
    return regressao_logistica


#ORGANIZAR A EXECUÇÃO DO CÓDIGO
def main():
    df = criar_df()
    x_treino, x_teste, y_treino, y_teste = criar_base_teste_treino(df)
    modelo = criar_modelo_regressao(criar_pipeline())
    analisar_modelo_ml(modelo, x_treino, y_treino, x_teste, y_teste)

    joblib.dump(modelo, 'xgb.joblib')
    df.to_excel(r'C:\Users\Estudos\Desktop\FIAP\FASE 4\TECH4\aplicacao\dataset\df_clean.xlsx', index=False)

main()