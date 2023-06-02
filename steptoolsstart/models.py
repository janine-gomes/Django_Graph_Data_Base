import requests
from django.conf import settings
from isodate import parse_duration
from neo4j import GraphDatabase

def tamDicionario(results):
    t = len(results)-1
    return t
def decrementador(cont):
    contador = cont - 1
    return contador 

#Conexão com banco de dados
def conectaBanco():
    URI = 'neo4j+s://05f1f611.databases.neo4j.io'
    AUTH = 'neo4j', 'auNorvZxoEhF44NVrXuexB0fOs7JSGOeKlUL23mNo70'
    driver = GraphDatabase.driver(URI, auth=AUTH)
    return driver

#Função realiza a consulta no banco de dados Neo4j, criando um dicionario de testes
def buscaTeste(query):
    retornoTestes=[]
    resultadoBanco=[]
    driverIn = conectaBanco()
    with driverIn.session() as session:
        info = session.run(query)
        for teste in info:
            print(teste.value('t.code'), teste.value('t.teste'), teste.value('t.conhecimento'), teste.value('t.solucao'))
            resultadoBanco = {
                'id': teste.value('t.code'),
                'teste': teste.value('t.teste'),
                'componente': teste.value('t.componente'),
                'conhecimento': teste.value('t.conhecimento'),
                'solucao': teste.value('t.solucao')
            }
            retornoTestes.append(resultadoBanco)
    session.close()
    driverIn.close()
    return retornoTestes

#Função realiza consulta pelas chaves dentro da categoria de problema
def buscaKeyCategoria():
    query = "match (p:Problema) return p.key, p.nomeCategoria"
    r=[]
    driver = conectaBanco()
    with driver.session() as session:
        info = session.run(query)
        for teste in info:
            #print(teste.value('p.key'), teste.value('p.nomeCategoria'))
            results = {
                'key': teste.value('p.key'),
                'nome': teste.value('p.nomeCategoria')
            }
            r.append(results)
    session.close()
    driver.close()
    return r

def coletaDado(equipamento, problema):
    if problema == 'no_video':
        context = {
            'equipamento': equipamento,
            'problema': 'Equipamento liga mas não gera vídeo na tela.'
        }
    elif problema == 'no_power':
        context = {
            'equipamento': equipamento,
            'problema': 'Equipamento não liga, sem nenhum sinal de energia.'
        }
    elif problema == 'no_post':
        context = {
            'equipamento': equipamento,
            'problema': 'Equipamento liga o LED do botão por alguns segundos e apaga ou LED fica piscando.'
        }
    elif problema == 'no_boot':
        context = {
            'equipamento': equipamento,
            'problema': 'Equipamento apresenta mensagem de "no device bootable found".'
        }
    return context    
        
def preparaTeste(equipamento,problema):
    #Pega o problema que o usuário selecionou
    results=[]
    #DESKTOP
    #Inicia a verificação do equipamento igual a Desktop 
    if equipamento == 'desktop':
        #Inicia a verificação do problema
        if problema == 'no_video':
            query = "match (t:Testes)-[:ATUA]-(p:Problema {nomeCategoria:'no_video'}) WHERE t.equipamento CONTAINS 'desktop' or t.equipamento CONTAINS 'ambos' RETURN t.code, t.teste, t.componente, t.conhecimento, t.solucao"
            results = buscaTeste(query)
            #print(results)

        elif problema == 'no_power':
            query = "match (t:Testes)-[:ATUA]-(p:Problema {nomeCategoria:'no_power'}) WHERE t.equipamento CONTAINS 'desktop' or t.equipamento CONTAINS 'ambos' RETURN t.code, t.teste, t.componente, t.conhecimento, t.solucao"
            results = buscaTeste(query)
            #print(results)

        elif problema == 'no_post':
            query = "match (t:Testes)-[:ATUA]-(p:Problema {nomeCategoria:'no_post'}) WHERE t.equipamento CONTAINS 'desktop' or t.equipamento CONTAINS 'ambos' RETURN t.code, t.teste, t.componente, t.conhecimento, t.solucao"
            results = buscaTeste(query)
            #print(results)

        elif problema == 'no_boot':
            query = "match (t:Testes)-[:ATUA]-(p:Problema {nomeCategoria:'no_boot'}) WHERE t.equipamento CONTAINS 'desktop' or t.equipamento CONTAINS 'ambos' RETURN t.code, t.teste, t.componente, t.conhecimento, t.solucao"
            results = buscaTeste(query)
            #print(results)

    #NOTEBOOK
    #Inicia a verificação do equipamento igual a Notebook
    elif equipamento == 'notebook':
        #Inicia a verificação do problema
        if problema == 'no_video':
            query = "match (t:Testes)-[:ATUA]-(p:Problema {nomeCategoria:'no_video'}) WHERE t.equipamento CONTAINS 'notebook' or t.equipamento CONTAINS 'ambos' RETURN t.code, t.teste, t.componente, t.conhecimento, t.solucao"
            results = buscaTeste(query)
            #print(results)

        elif problema == 'no_power':
            query = "match (t:Testes)-[:ATUA]-(p:Problema {nomeCategoria:'no_power'}) WHERE t.equipamento CONTAINS 'notebook' or t.equipamento CONTAINS 'ambos' RETURN t.code, t.teste, t.componente, t.conhecimento, t.solucao"
            results = buscaTeste(query)
            #print(results)

        elif problema == 'no_post':
            query = "match (t:Testes)-[:ATUA]-(p:Problema {nomeCategoria:'no_post'}) WHERE t.equipamento CONTAINS 'notebook' or t.equipamento CONTAINS 'ambos' RETURN t.code, t.teste, t.componente, t.conhecimento, t.solucao"
            results = buscaTeste(query)
            #print(results)

        elif problema == 'no_boot':
            query = "match (t:Testes)-[:ATUA]-(p:Problema {nomeCategoria:'no_boot'}) WHERE t.equipamento CONTAINS 'notebook' or t.equipamento CONTAINS 'ambos' RETURN t.code, t.teste, t.componente, t.conhecimento, t.solucao"
            results = buscaTeste(query)
            #print(results)      
    #Retorna o dicionario com os testes
    
    return results        

# Busca API Youtube
#Função conecta a API do youtube para os vídeos de recomendação/pesquisa
def buscaVideosAPI(texto):
    videos=[]
    search_url = 'https://www.googleapis.com/youtube/v3/search'
    video_url = 'https://www.googleapis.com/youtube/v3/videos'
    search_params = {
            'part' : 'snippet',
            'q' : texto,
            'key' : settings.YOUTUBE_DATA_API_KEY,
            'maxResults' : 6,
            'topicId':'computador',
            'type' : 'video'
        }

    r = requests.get(search_url, params=search_params)

    results = r.json()['items']

    video_ids = []
    for result in results:
        video_ids.append(result['id']['videoId'])

    video_params = {
        'key' : settings.YOUTUBE_DATA_API_KEY,
        'part' : 'snippet,contentDetails',
        'id' : ','.join(video_ids),
        'maxResults' : 6
    }

    r = requests.get(video_url, params=video_params)

    results = r.json()['items']
        
    for result in results:
        video_data = {
            'title' : result['snippet']['title'],
            'id' : result['id'],
            'url' : f'https://www.youtube.com/watch?v={ result["id"] }',
            'duration' : int(parse_duration(result['contentDetails']['duration']).total_seconds() / 60),
            'thumbnail' : result['snippet']['thumbnails']['high']['url']
         }

        videos.append(video_data)
    return videos



    