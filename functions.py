import pandas as pd


#ler banco de dados 'sp_turno_1.xlsx'
planilha = pd.read_excel('teste.xlsx')

#formatar casas decimais da planilha
def formata(valor):
    return f'{valor:.2f}'


# cada função é um data frame criado
#---saber quantos eleitores tem em cada municipio/ quantos compareceram/quantos se abstiveram-------------------------------

def eleitor_municipio():
    #criar uma nova tabela para armazenar as informações coletadas
    eleitor_municipio = pd.DataFrame({'': [], 'NM_MUNICIPIO': [], 'QT_APTOS': [], 'QT_ABSTENCOES': [], 'QT_COMPARECIMENTO': []})

    #variável guia
    secao = 0

    #inteirar sobre cada linha do banco de dados 'sp_turno_1.xlsx' procurando todas as 'NR_SECAO' 
    for linha in planilha.itertuples(index=True):
        if linha.NR_SECAO != secao:
            secao = linha.NR_SECAO

            #verificar se o municipio ja consta na nova planilha criada
            resultado = eleitor_municipio.loc[eleitor_municipio['NM_MUNICIPIO'] == linha.NM_MUNICIPIO]

            #se o municipio NÃO constar na planilha de dados coletados, adicionar o mesmo.
            if len(resultado) == 0:
                nova_linha = pd.DataFrame({'': [''],'NM_MUNICIPIO': [linha.NM_MUNICIPIO], 'QT_APTOS': [linha.QT_APTOS], 'QT_ABSTENCOES': [linha.QT_ABSTENCOES], 'QT_COMPARECIMENTO': [linha.QT_COMPARECIMENTO]})
                eleitor_municipio = eleitor_municipio._append(nova_linha)
            
            #se o municipio constar na planilha de dados coletados, somar cada eleitor de cada seção eleitoral do municipio 
            if len(resultado) == 1:
                eleitor_municipio.loc[eleitor_municipio['NM_MUNICIPIO'] == linha.NM_MUNICIPIO, 'QT_APTOS'] += linha.QT_APTOS
                eleitor_municipio.loc[eleitor_municipio['NM_MUNICIPIO'] == linha.NM_MUNICIPIO, 'QT_ABSTENCOES'] += linha.QT_ABSTENCOES
                eleitor_municipio.loc[eleitor_municipio['NM_MUNICIPIO'] == linha.NM_MUNICIPIO, 'QT_COMPARECIMENTO'] += linha.QT_COMPARECIMENTO

    #ordenar a planilha de dados coletados com base na quantidade de comparecimento de eleitores, do maior para o menor
    eleitor_municipio = eleitor_municipio.sort_values(by= 'QT_COMPARECIMENTO', ascending=False)


    #adicionar uma nova linha no final da planilha de dados coletados com o total de eleitores no estado de SP
    nova_linha = pd.DataFrame({'': ['TOTAL ESTADO SP'], 'NM_MUNICIPIO': '--', 'QT_APTOS': [eleitor_municipio['QT_APTOS'].sum()], 'QT_ABSTENCOES': [eleitor_municipio['QT_ABSTENCOES'].sum()], 'QT_COMPARECIMENTO': [eleitor_municipio['QT_COMPARECIMENTO'].sum()]})
    eleitor_municipio = eleitor_municipio._append(nova_linha)

    return eleitor_municipio


#--------apuracao_votos--------------------------------------------------------------------------------------------------------------

def apuracao_votos():
    apuracao_votos = pd.DataFrame({'NM_MUNICIPIO': [], 'SG_PARTIDO': [], 'NM_CANDIDATO': [], 'DS_CARGO': [], 'QT_VOTOS': []})
    #inteirar sobre cada linha do banco de dados 'sp_turno_1.xlsx' procurando todas as 'NM_VOTAVEL' 
    for linha in planilha.itertuples(index=True):
        #comparar cada candidato do banco de dados 'sp_turno_1.xlsx' com a planilha de dados coletados
        candidato = apuracao_votos.loc[(apuracao_votos['NM_CANDIDATO'] == linha.NM_VOTAVEL) & (apuracao_votos['NM_MUNICIPIO'] == linha.NM_MUNICIPIO) & (apuracao_votos['DS_CARGO'] == linha.DS_CARGO_PERGUNTA)]
        
        
        #se o candidato NÃO constar na planilha de dados coletados, adicionar o mesmo.
        if len(candidato) == 0:
            nova_linha = pd.DataFrame({'NM_MUNICIPIO': [linha.NM_MUNICIPIO], 'SG_PARTIDO': [linha.SG_PARTIDO], 'NM_CANDIDATO': [linha.NM_VOTAVEL], 'DS_CARGO': [linha.DS_CARGO_PERGUNTA], 'QT_VOTOS': [linha.QT_VOTOS]})
            apuracao_votos = apuracao_votos._append(nova_linha)
            
        #se o candidato constar na planilha de dados coletados, somar cada voto de cada seção eleitoral do municipio
        if len(candidato) == 1:
            apuracao_votos.loc[(apuracao_votos['NM_CANDIDATO'] == linha.NM_VOTAVEL) & (apuracao_votos['NM_MUNICIPIO'] == linha.NM_MUNICIPIO) & (apuracao_votos['DS_CARGO'] == linha.DS_CARGO_PERGUNTA), 'QT_VOTOS'] += linha.QT_VOTOS

    #tratamento de dados nulos
    #procurar todos os candidatos com nomes nulos/branco e colocar o nome do partido 'N/A'
    apuracao_votos.loc[(apuracao_votos['NM_CANDIDATO'] == 'Nulo') | (apuracao_votos['NM_CANDIDATO'] == 'Branco'), 'SG_PARTIDO'] = 'NaN'
    
    #cria data frame com quantidades total de votos por cargo/ municipio
    apuracao_votos2 = pd.pivot_table(apuracao_votos,values= 'QT_VOTOS', index=['NM_MUNICIPIO', 'DS_CARGO'],  aggfunc='sum')
    apuracao_votos2 = apuracao_votos2.rename(columns={'QT_VOTOS': '% VOTO/_CANDIDATO'})
    
    #mesclar data frames "apuracao_votos2" + "apuracao_votos" preservando suas colunas
    apuracao_votos = pd.merge(apuracao_votos2, apuracao_votos, on=['NM_MUNICIPIO','DS_CARGO'] )

    # criar a porcentagem de votos que cada candidato recebeu
    apuracao_votos['% VOTO/_CANDIDATO'] = apuracao_votos['QT_VOTOS']/apuracao_votos['% VOTO/_CANDIDATO']*100
    apuracao_votos['% VOTO/_CANDIDATO'] = apuracao_votos['% VOTO/_CANDIDATO'].apply(formata)


    #criando tabela dinâmica p/ agrupar os resultados
    apuracao_votos = pd.pivot_table(apuracao_votos, index=['NM_MUNICIPIO', 'DS_CARGO', 'SG_PARTIDO', 'NM_CANDIDATO'],columns=[], )
    
    #organizar os dados por municipio/ cargo do mais votado ao menos
    apuracao_votos = apuracao_votos.sort_values(by=['NM_MUNICIPIO', 'DS_CARGO',  'QT_VOTOS'], ascending= [True,  True, False], )
    


    return apuracao_votos



    
