import pandas as pd
import tabula as tb
import datetime as dt
import re

#LENDO EXTRATO
def read_extrato():
    extrato = pd.read_csv('back/base/08.csv', parse_dates = ['Data'], dayfirst = True)
    extrato = extrato.drop(columns = ['Identificador'])

    return extrato

#TRATANDO MOVIMENTAÇÕES
def count_movimentacao(df):
    movimentacoes = df[df['Descrição'].str.contains('070.092.866-98', case = False)]
    sem_movimentacoes = df[~df['Descrição'].str.contains('070.092.866-98', case = False)]
    mov_picpay = movimentacoes[movimentacoes['Descrição'].str.contains('12393860-0', case = False)]
    mov_sicoob = movimentacoes[movimentacoes['Descrição'].str.contains('90616697-7', case = False)]
    mov_xp = movimentacoes[movimentacoes['Descrição'].str.contains('573447-2', case = False)]
    
    mov_dict = {
        'picpay': mov_picpay,
        'sicoob': mov_sicoob,
        'xp': mov_xp,
        'sem_mov': sem_movimentacoes
    }

    return mov_dict

#CALCULO DO EXTRATO
def calcula_extrato(_dict):
    extrato_real = _dict['sem_mov']
    movimentacoes = [_dict['picpay'], _dict['sicoob'], _dict['xp']] 

    entrada = extrato_real['Valor'].loc[extrato_real['Valor'] > 0].sum()
    saida = extrato_real['Valor'].loc[extrato_real['Valor'] < 0].sum()

    for i in movimentacoes:
        if i['Valor'].sum() > 0:
            entrada += i['Valor'].sum() #ENTRADA
        elif i['Valor'].sum() < 0:
            saida += i['Valor'].sum() #SAÍDA

    saldo = entrada + saida #SALDO

    enviado = extrato_real[extrato_real['Descrição'].str.contains('transferência enviada', case = False)] #ENVIADO
    enviado = enviado['Valor'].sum()                

    recebido = extrato_real[extrato_real['Descrição'].str.contains('transferencia recebida', case = False)] #RECEBIDO
    recebido = recebido['Valor'].sum()
    
    debito = extrato_real[extrato_real['Descrição'].str.contains('compra no débito', case = False)] #DÉBITO
    debito = debito['Valor'].sum()        

    deposito_boleto = extrato_real[extrato_real['Descrição'].str.contains('depósito recebido por boleto', case = False)] #DEPÓSITO BOLETO
    deposito_boleto = deposito_boleto['Valor'].sum() 

    pagamento_boleto = extrato_real[extrato_real['Descrição'].str.contains('pagamento de boleto efetuado', case = False)] #PAGAMENTO BOLETO
    pagamento_boleto = pagamento_boleto['Valor'].sum()

    saque = extrato_real[extrato_real['Descrição'].str.contains('saque -', case = False)] #SAQUE
    saque = saque['Valor'].sum() 

    tarifa = extrato_real[extrato_real['Descrição'].str.contains('tarifa', case = False)] #TARIFA
    tarifa = tarifa['Valor'].sum() 

    ifood = extrato_real[extrato_real['Descrição'].str.contains('ifd*', case = False)] #IFOOD
    ifood = ifood['Valor'].sum() 

    salario = extrato_real[extrato_real['Descrição'].str.contains('SOL PLACE', case = False)] #SALÁRIO
    salario = salario['Valor'].sum() 

    picpay = _dict['picpay']['Valor'].sum() #MOVIMENTAÇÕES PICPAY
    sicoob = _dict['sicoob']['Valor'].sum() #MOVIMENTAÇÕES SICOOB
    xp = _dict['xp']['Valor'].sum() #MOVIMENTAÇÕES XP

    #DIA DE SEMANA 
    df_util = pd.DataFrame()
    df_util = extrato_real.loc[extrato_real['Data'].map(lambda x: x.weekday() < 5)]#0 Mon, 1 Tue, 2 Wed, 3 Thu, 4 Fri
    
    soma_util = df_util['Valor'].loc[df_util['Valor'] < 0].sum() #TOTAL DE GASTO DURANTE SEMANA 
    qtde_util = len(df_util['Data'].unique())
    media_util = soma_util / qtde_util #MÉDIA DE GASTO DURANTE SEMANA
    
    #FINAL DE SEMANA
    df_fds = pd.DataFrame()
    df_fds = extrato_real.loc[extrato_real['Data'].map(lambda x: x.weekday() > 4)] #5 Sat, 6 Sun
    
    soma_fds = df_fds['Valor'].loc[df_fds['Valor'] < 0].sum() #TOTAL DE GASTO DURANTE FINAL DE SEMANA
    qtde_fds = len(df_fds['Data'].unique())
    media_fds = soma_fds / qtde_fds #MÉDIA DE GASTO DURANTE FINAL DE SEMANA
    
    dict_extrato = {
        'entrada': entrada,
        'saida': saida,
        'saldo': saldo,
        'enviado': enviado,
        'recebido': recebido,
        'debito': debito,
        'ifood': ifood,
        'saque': saque,
        'tarifa': tarifa,
        'deposito_boleto': deposito_boleto,
        'pagamento_boleto': pagamento_boleto,
        'salario': salario,
        'picpay': picpay,
        'sicoob': sicoob,
        'xp': xp,
    }
    
    return dict_extrato

#CALCULO DIFERENÇA EM PORCENTAGEM
def diff_porcentagem(antigo, atual):
    porc = ((atual - antigo) / antigo) * 100
    return porc

#VERIFICANDO FILTROS
def search_filter(df):
    extrato_nubank  = ['saque -', 'tarifa', 'depósito recebido por boleto', 'pagamento de boleto efetuado', 'compra no débito', 'pagamento da fatura',
                'pagamento de fatura', 'transferência recebida', 'transferência enviada', 'débito em conta', 'crédito em conta', 'ifd*']
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

def read_picpay():
    df = pd.DataFrame()
    doc = tb.read_pdf('./base/picjun.pdf', pages='all')
    for tabela in doc:
        df = pd.concat([df, tabela])
    
    df = df.iloc[:,[0,1,2]] #pegando as 3 primeiras colunas
    df.set_axis(['Data', 'Descrição', 'Valor'], axis='columns', inplace=True)
    df = df.reset_index(drop=True)

    df['Data'] = df['Data'].map(lambda x: x[0:10])
    df['Valor'] = df['Valor'].map(lambda x: re.sub('[^0-9-,]', '', x))
    df['Valor'] = df['Valor'].map(lambda x: re.sub(',', '.', x))
    df['Valor'] = df['Valor'].astype(float)
    
    #Calculo para remoção de movimentações
    df['Movimentação'] = (df['Valor'].shift(-1)) #subindo a coluna uma linha pra cima

    list_index = df.index[df['Valor'] == (df['Movimentação']*(-1))].tolist() #lista de movimentações
    print(list_index)
    
    for i in list_index:
        df = df.drop(i)
        df = df.drop(i+1)
    
    print(df)

def read_fatura():
    df = pd.DataFrame()
    doc = tb.read_pdf('./base/nu_mai.pdf', pages='all', pandas_options={'header': None})
    for tabela in doc:
        df = pd.concat([df, tabela])
    
    df = df.iloc[:,[0,2,3]] #pegando as 3 primeiras colunas
    df.set_axis(['Data', 'Descrição', 'Valor'], axis='columns', inplace=True)
    df = df.dropna()
    df = df.reset_index(drop=True)

    return df

if __name__ == "__main__":
    df = read_extrato()
    dict_mov = count_movimentacao(df)
    calcula_extrato(dict_mov)
