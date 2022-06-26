import pandas as pd 
from gerador import total

#FILTROS
extrato_nubank  = ['saque -', 'tarifa', 'depósito recebido por boleto', 'compra no débito', 'pagamento da fatura', 'pagamento de fatura',
                'transferência recebida', 'transferência enviada', 'pagamento de boleto efetuado', 'débito em conta', 'crédito em conta']

#LENDO ARQUIVO JSON
def read_document():
    #df = pd.read_json(doc)
    df = pd.read_csv('./base/2022_03.csv')
    
    df = df.drop(columns=['Identificador'])
    
    search_filter(df)

#CALCULOS DO MES
def calculos_mes(df):
    entrada = df['Valor'].loc[df['Valor'] > 0].sum()    #ENTRADA
    saida = df['Valor'].loc[df['Valor'] < 0].sum()    #SAIDA
    saldo = entrada + saida                         #SALDO
    #fatura

    enviado = df[df['Descrição'].str.contains('Transferência Enviada|Transferência enviada')] #ENVIADO
    enviado = enviado['Valor'].sum()                

    recebido = df[df['Descrição'].str.contains('Transferência Recebida|Transferência recebida')] #RECEBIDO
    recebido = recebido['Valor'].sum()                

    compra_debito = df[df['Descrição'].str.contains('Compra no débito')] #COMPRA DEBITO
    compra_debito = compra_debito['Valor'].sum()        

    ifood = df[df['Descrição'].str.contains('Ifd*')] #IFOOD
    ifood = ifood['Valor'].sum()                        

#CALCULO CUSTO DE VIDA
def custo_vida(mes1, mes2, mes3):
    custo = (mes1 + mes2 + mes3)/ 3
    return custo

#CALCULO DIFERENÇA EM PORCENTAGEM
def dif_porcentagem(antigo, atual):
    porc = ((atual - antigo)/ antigo)*100
    return porc

#VERIFICANDO FILTROS
def search_filter(df):
    for doc in extrato_nubank:
        df_verificado = df[~df['Descrição'].str.contains(doc, case = False )]
        df = df_verificado
    print(df)


