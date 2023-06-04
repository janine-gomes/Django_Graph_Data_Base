import requests
from django.conf import settings
from isodate import parse_duration
from neo4j import GraphDatabase

#gettins e settings
cont = 0
t = 0
results = []
equipamento = None
problema = None

#cont
def set_cout(value):
    global cont
    cont = value

def get_cout():
    return cont
#T
def set_t(value):
    global t
    t = value

def get_t():
    return t
#Results
def set_results(value):
    global results
    results = value

def get_results():
    return results

#Equipamento
def set_equipamento(value):
    global equipamento
    equipamento = value

def get_equipamento():
    return equipamento

#Problema
def set_problema(value):
    global problema
    problema = value

def get_problema():
    return problema

def tamDicionario(results):
    t = len(results)
    return t
def crementador(cont):
    contador = cont + 1
    return contador 

#Conexão com banco de dados
def conectaBanco():
    driver = GraphDatabase.driver(settings.URI, auth=settings.AUTH)
    return driver

#Função realiza a consulta no banco de dados Neo4j, criando um dicionario de testes
def buscaTeste(query):
    retornoTestes=[]
    resultadoBanco=[]
    driverIn = conectaBanco()
    with driverIn.session() as session:
        info = session.run(query)
        for teste in info:
            #print(teste.value('t.code'), teste.value('t.teste'), teste.value('t.conhecimento'), teste.value('t.solucao'))
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
    results.reverse()
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



    