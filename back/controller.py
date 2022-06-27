import pandas as pd 
from gerador import total

#FILTROS
extrato_nubank  = ['saque -', 'tarifa', 'depósito recebido por boleto', 'pagamento de boleto efetuado', 'compra no débito', 'pagamento da fatura',
                'pagamento de fatura', 'transferência recebida', 'transferência enviada', 'débito em conta', 'crédito em conta', 'ifd*']

#LENDO ARQUIVO JSON
def read_document():
    #df = pd.read_json(doc)
    df = pd.read_csv('./base/2022_03.csv')
    df = df.drop(columns=['Identificador'])
    
    calculos_mes(df)
    return df

#CALCULOS DO MES
def calculos_mes(df):
    entrada = df['Valor'].loc[df['Valor'] > 0]    #ENTRADA
    saida = df['Valor'].loc[df['Valor'] < 0].sum()    #SAIDA
    saldo = entrada + saida                         #SALDO
    #FATURA

    enviado = df[df['Descrição'].str.contains('transferência enviada', case = False)] #ENVIADO
    enviado = enviado['Valor'].sum()                

    recebido = df[df['Descrição'].str.contains('transferencia recebida', case = False)] #RECEBIDO
    recebido = recebido['Valor'].sum()                

    compra_debito = df[df['Descrição'].str.contains('compra no débito', case = False)] #COMPRA DEBITO
    compra_debito = compra_debito['Valor'].sum()        

    ifood = df[df['Descrição'].str.contains('Ifd*')] #COMPRA IFOOD
    ifood = ifood['Valor'].sum()

    #SAQUE
    #TARIFA
    #DEPOSITO BOLETO
    #PAGAMENTO DE BOLETO    
    
    return 

#CALCULO CUSTO DE VIDA
def custo_vida(mes1, mes2, mes3):
    custo = (mes1 + mes2 + mes3)/ 3
    return print(custo)

#CALCULO DIFERENÇA EM PORCENTAGEM
def dif_porcentagem(antigo, atual):
    porc = ((atual - antigo)/ antigo)*100
    return print(porc)


#VERIFICANDO FILTROS
def search_filter(df):
    for doc in extrato_nubank:
        df_verificado = df[~df['Descrição'].str.contains(doc, case = False )]
        df = df_verificado
    
    return print(df)

#CHECAGEM DE DATA
def check_date(df):
    pass

if __name__ == "__main__":
    read_document()
