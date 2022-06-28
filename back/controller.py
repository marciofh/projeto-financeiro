import pandas as pd

#FILTROS
extrato_nubank  = ['saque -', 'tarifa', 'depósito recebido por boleto', 'pagamento de boleto efetuado', 'compra no débito', 'pagamento da fatura',
                'pagamento de fatura', 'transferência recebida', 'transferência enviada', 'débito em conta', 'crédito em conta', 'ifd*']

#LENDO ARQUIVO JSON
def read_document():
    #df = pd.read_json(doc)
    df1 = pd.read_csv('./base/2022_03.csv', parse_dates = ['Data'], dayfirst = True)
    df1 = df1.drop(columns = ['Identificador'])
    df2 = pd.read_csv('./base/2022_04.csv', parse_dates = ['Data'], dayfirst = True)
    df2 = df2.drop(columns = ['Identificador'])
    df = pd.concat([df1, df2])
    
    check_date(df)
    return df

#CALCULO EXTRATO
def calculos_extrato(df):
    entrada = df['Valor'].loc[df['Valor'] > 0].sum()    #ENTRADA
    saida = df['Valor'].loc[df['Valor'] < 0].sum()      #SAIDA
    saldo = entrada + saida                             #SALDO
    #pag_fatura                                         #FATURA

    enviado = df[df['Descrição'].str.contains('transferência enviada', case = False)] #ENVIADO
    enviado = enviado['Valor'].sum()                

    recebido = df[df['Descrição'].str.contains('transferencia recebida', case = False)] #RECEBIDO
    recebido = recebido['Valor'].sum()                

    compra_debito = df[df['Descrição'].str.contains('compra no débito', case = False)] #COMPRA DEBITO
    compra_debito = compra_debito['Valor'].sum()        

    ifood = df[df['Descrição'].str.contains('ifd*', case = False)] #COMPRA IFOOD
    ifood = ifood['Valor'].sum()

    #SAQUE
    #TARIFA
    #DEPOSITO BOLETO
    #PAGAMENTO DE BOLETO    
    
    return 

#CALCULO CUSTO DE VIDA
def custo_vida(mes1, mes2, mes3):
    custo = (mes1 + mes2 + mes3) / 3
    return custo

#CALCULO DIFERENÇA EM PORCENTAGEM
def diff_porcentagem(antigo, atual):
    porc = ((atual - antigo) / antigo) * 100
    return porc

#VERIFICANDO FILTROS
def search_filter(df):
    for filtro in extrato_nubank:
        df_verificado = df[~df['Descrição'].str.contains(filtro, case = False )]
        df = df_verificado
    
    return df

#CHECAGEM DE DATA
def check_date(df):
    df['ano']  = df['Data'].dt.strftime('%Y')
    df['mes'] = df['Data'].dt.strftime('%m')
    array_mes = df['mes'].unique()
    array_ano = df['ano'].unique()

    print(array_mes, array_ano)
    return 

if __name__ == "__main__":
    read_document()