from functions import *

#armazenar todos os dataframes dentro de variáveis
eleitor_mun = eleitor_municipio()
apur_votos = apuracao_votos()


#pergunta ao usuário quais dados ele deseja coletar do arquivo "sp_turno_1.xlsx"
print('\n Esse é o coletor de dados do arquivo "sp_turno_1.xlsx".')

#------saber apuração dos votos----------------------------------------------------------------------------------------------------------

resposta = input('\n Deseja saber a apuração dos votos em cada município? [S/ N]: ').upper()
#cria um laço de repetição pra garantir que o usuário responda apenas sim ou não
while resposta not in ('S', 'N', 'SIM', 'NAO', 'NÃO'):
    resposta = input('\n Deseja saber a apuração dos votos em cada município? [S/ N]: ').upper()

#se a resposta for sim, o usuário vai receber as informações requisitadas no arquivo "dados-eleições-2020.xlsx"
if resposta in ('S', 'SIM'):
    apur_votos.to_excel('apuração-votos-2020.xlsx', sheet_name="apuração votos")
    print('\n Os dados requisitados foram salvos no arquivo "apuração_votos2020.xlsx". ')

print('\n', '---'*40)


#------saber quantos eleitores tem em cada município/ quantos compareceram/ quantos se abstiveram----------------------------------------

resposta = input('\n Deseja saber quantos eleitores tem em cada município/ quantos compareceram/ quantos se abstiveram? [S/ N]: ').upper()
#cria um laço de repetição pra garantir que o usuário responda apenas sim ou não
while resposta not in ('S', 'N', 'SIM', 'NAO', 'NÃO'):
    resposta = input('\n Deseja saber quantos eleitores tem em cada município/ quantos compareceram/quantos se abstiveram? [S/ N]: ').upper()

#se a resposta for sim, o usuário vai receber as informações requisitadas no arquivo "dados-eleições-2020.xlsx"
if resposta in ('S', 'SIM'):
    eleitor_mun.to_excel('comparecimentos-abstenções-2020.xlsx', sheet_name="comparecimentos-abstenções")
    print('\n Os dados requisitados foram salvos no arquivo "comparecimentos/abstenções.xlsx".')

print('\n', '---'*40)


