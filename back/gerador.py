import pandas as pd 

#EXTRATO NUBANK
#2019
ago_19 = pd.read_csv('./base/2019_08.csv')
set_19 = pd.read_csv('./base/2019_09.csv')
out_19 = pd.read_csv('./base/2019_10.csv')
nov_19 = pd.read_csv('./base/2019_11.csv')
dez_19 = pd.read_csv('./base/2019_12.csv')
ano_2019 = pd.concat([ago_19, set_19, out_19, nov_19, dez_19])

#2020
jan_20 = pd.read_csv('./base/2020_01.csv')
fev_20 = pd.read_csv('./base/2020_02.csv')
mar_20 = pd.read_csv('./base/2020_03.csv')
abr_20 = pd.read_csv('./base/2020_04.csv')
mai_20 = pd.read_csv('./base/2020_05.csv')
jun_20 = pd.read_csv('./base/2020_06.csv')
jul_20 = pd.read_csv('./base/2020_07.csv')
ago_20 = pd.read_csv('./base/2020_08.csv')
set_20 = pd.read_csv('./base/2020_09.csv')
out_20 = pd.read_csv('./base/2020_10.csv')
nov_20 = pd.read_csv('./base/2020_11.csv')
dez_20 = pd.read_csv('./base/2020_12.csv')
ano_2020 = pd.concat([jan_20, fev_20, mai_20, abr_20, mai_20, jun_20, jul_20, ago_20, set_20, out_20, nov_20, dez_20])

#2021
jan_21 = pd.read_csv('./base/2021_01.csv')
fev_21 = pd.read_csv('./base/2021_02.csv')
mar_21 = pd.read_csv('./base/2021_03.csv')
abr_21 = pd.read_csv('./base/2021_04.csv')
mai_21 = pd.read_csv('./base/2021_05.csv')
jun_21 = pd.read_csv('./base/2021_06.csv')
jul_21 = pd.read_csv('./base/2021_07.csv')
ago_21 = pd.read_csv('./base/2021_08.csv')
set_21 = pd.read_csv('./base/2021_09.csv')
out_21 = pd.read_csv('./base/2021_10.csv')
nov_21 = pd.read_csv('./base/2021_11.csv')
dez_21 = pd.read_csv('./base/2021_12.csv')
ano_2021 = pd.concat([jan_21, fev_21, mar_21, abr_21, mai_21, jun_21, jul_21, ago_21, set_21, out_21, nov_21, dez_21])

#2022
jan_22 = pd.read_csv('./base/2022_01.csv')
fev_22 = pd.read_csv('./base/2022_02.csv')
mar_22 = pd.read_csv('./base/2022_03.csv')
abr_22 = pd.read_csv('./base/2022_04.csv')
mai_22 = pd.read_csv('./base/2022_05.csv')
jul_22 = pd.read_csv('./base/2022_07.csv')
ano_2022 = pd.concat([jan_22, fev_22, mar_22, abr_22, mai_22])

total = pd.concat([ano_2019, ano_2020, ano_2021, ano_2022])

with pd.ExcelWriter('EXTRATO_TOTAL.xlsx') as writer:  #NOME ARQUIVO
    mar_22.to_excel(writer, sheet_name='mar')
    abr_22.to_excel(writer, sheet_name='abr')
    jul_22.to_excel(writer, sheet_name='jul')