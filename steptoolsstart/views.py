from django.shortcuts import render
import requests
from django.conf import settings
from isodate import parse_duration
from neo4j import GraphDatabase
#driver = GraphDatabase.driver('neo4j+s://5841d246.databases.neo4j.io', auth=('neo4j', 'GnhHM-cz_eYV6H9Z-eiEczqG_1BptzeoDAK8C68ak38'))


URI = 'neo4j+s://05f1f611.databases.neo4j.io'
AUTH = 'neo4j', 'auNorvZxoEhF44NVrXuexB0fOs7JSGOeKlUL23mNo70'
with GraphDatabase.driver(URI, auth=AUTH) as driver:
    driver.verify_connectivity()

#Função conecta a API do youtube para os vídeos de recomendação/pesquisa
def buscaVideos(texto):
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
#Função realiza a consulta no banco de dados Neo4j, criando um dicionario de testes
def buscaTeste(query):
    r=[]
    with driver.session() as session:
        info = session.run(query)
        for teste in info:
            print(teste.value('t.code'), teste.value('t.teste'), teste.value('t.conhecimento'), teste.value('t.solucao'))
            results = {
                'id': teste.value('t.code'),
                'teste': teste.value('t.teste'),
                'componente': teste.value('t.componente'),
                'conhecimento': teste.value('t.conhecimento'),
                'solucao': teste.value('t.solucao')
            }
            r.append(results)
    session.close()
    driver.close()
    return r

#Função realiza consulta pelas chaves dentro da categoria de problema
def buscaKeyCategoria():
    query = "match (p:Problema) return p.key, p.nomeCategoria"
    r=[]
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

#Função que realiza verificação do problema e equipamento para chamar a função buscaTeste
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
            print(results)

        elif problema == 'no_power':
            query = "match (t:Testes)-[:ATUA]-(p:Problema {nomeCategoria:'no_power'}) WHERE t.equipamento CONTAINS 'desktop' or t.equipamento CONTAINS 'ambos' RETURN t.code, t.teste, t.componente, t.conhecimento, t.solucao"
            results = buscaTeste(query)
            print(results)

        elif problema == 'no_post':
            query = "match (t:Testes)-[:ATUA]-(p:Problema {nomeCategoria:'no_post'}) WHERE t.equipamento CONTAINS 'desktop' or t.equipamento CONTAINS 'ambos' RETURN t.code, t.teste, t.componente, t.conhecimento, t.solucao"
            results = buscaTeste(query)
            print(results)

        elif problema == 'no_boot':
            query = "match (t:Testes)-[:ATUA]-(p:Problema {nomeCategoria:'no_boot'}) WHERE t.equipamento CONTAINS 'Desktop' or t.equipamento CONTAINS 'ambos' RETURN t.code, t.teste, t.componente, t.conhecimento, t.solucao"
            results = buscaTeste(query)
            print(results)

    #NOTEBOOK
    #Inicia a verificação do equipamento igual a Notebook
    elif equipamento == 'notebook':
        #Inicia a verificação do problema
        if problema == 'no_video':
            query = "match (t:Testes)-[:ATUA]-(p:Problema {nomeCategoria:'no_video'}) WHERE t.equipamento CONTAINS 'notebook' or t.equipamento CONTAINS 'ambos' RETURN t.code, t.teste, t.componente, t.conhecimento, t.solucao"
            results = buscaTeste(query)
            print(results)

        elif problema == 'no_power':
            query = "match (t:Testes)-[:ATUA]-(p:Problema {nomeCategoria:'no_power'}) WHERE t.equipamento CONTAINS 'notebook' or t.equipamento CONTAINS 'ambos' RETURN t.code, t.teste, t.componente, t.conhecimento, t.solucao"
            results = buscaTeste(query)
            print(results)

        elif problema == 'no_post':
            query = "match (t:Testes)-[:ATUA]-(p:Problema {nomeCategoria:'no_post'}) WHERE t.equipamento CONTAINS 'notebook' or t.equipamento CONTAINS 'ambos' RETURN t.code, t.teste, t.componente, t.conhecimento, t.solucao"
            results = buscaTeste(query)
            print(results)

        elif problema == 'no_boot':
            query = "match (t:Testes)-[:ATUA]-(p:Problema {nomeCategoria:'no_boot'}) WHERE t.equipamento CONTAINS 'notebook' or t.equipamento CONTAINS 'ambos' RETURN t.code, t.teste, t.componente, t.conhecimento, t.solucao"
            results = buscaTeste(query)
            print(results)
        
    #Zero as variaveis contadoras das listas
    global t
    global cont
    t=len(results)
    cont = t
    print(cont, t)
    
    #Retorna o dicionario com os testes
    return results

#Criando Variaveis Globais para manipulação
equipamento = None
problema = None
results=[]
cont=0
t=0

#Chama a pagina inicial Index
def index(request):
    #Zera as variaveis de coleta dos dados do usuario
    global problema
    global equipamento
    global results
    results = []
    problema = None
    equipamento = None
    return render(request,'index.html')

#Chama a pagina para selecionar o equipamento em falha
def selecionaEquipamento(request):
    #Pega o equipamento que o usuário selecionou
    if request.method=='POST':
        global equipamento 
        equipamento = request.POST.get('equipamento')
        print(equipamento)
        return render(request,'problema.html')
    return render(request,'equipamento.html')

#Chama a pagina para selecionar o problema enfrentado
def selecionaProblema(request):
    if request.method=='POST':
        global problema
        problema = request.POST.get('exampleRadios')
        print(problema)
        if problema == 'digitar':
            return render(request,'digita.html')
        else:
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
            global results
            results = preparaTeste(equipamento, problema)
            print(results)
            return render(request, 'testes.html', {'context':context})
    return render(request,'problema.html')

#Chama pagina Detelhe do Teste, mostrando teste por teste ao usuario
def iniciaTeste(request):
    #Seto a varivavel para tamanho da lista
    global t
    global cont
    #t=len(results)
    #Zero a lista de recomendação
    recomendacao = []
    texto = None
    resultado = None
    
    if request.method == 'POST':
        resultado = request.POST.get('botao')
        print(resultado)
        #Começo a contar o teste a partir do 1, porque o teste 0 ja foi mostrado
        if resultado == 'sim':
            print(cont,t)
            resultado = None
            return render(request,'final.html', {'teste': results[cont]})
        if (resultado == 'nao') or (resultado=='nao se aplica'):
            print('passei aqui')
            cont=cont-1
            if cont>=0:
                print(cont)
                return render(request,'testeDetail.html', {'teste': results[cont]})
            else:
                if problema == 'no_power':
                    texto = '{} não liga'.format(equipamento)
                    recomendacao = buscaVideos(texto)
                    print(texto)                        
                    cont = t-1
                    return render(request,'recomendacao.html', {'recomendacao': recomendacao})
                elif problema == 'no_video':
                    texto = '{} não liga a tela'.format(equipamento)
                    recomendacao = buscaVideos(texto)
                    print(cont)                        
                    cont = t-1
                    return render(request,'recomendacao.html', {'recomendacao': recomendacao})
                elif problema == 'no_post':
                    texto = '{} liga led mas não inicia'.format(equipamento)
                    recomendacao = buscaVideos(texto)
                    print(texto)                        
                    cont = t-1
                    return render(request,'recomendacao.html', {'recomendacao': recomendacao})
                elif problema == 'no_boot':
                    texto = '{} falha no boot'.format(equipamento)
                    recomendacao = buscaVideos(texto)
                    print(texto)                        
                    cont = t-1
                    return render(request,'recomendacao.html', {'recomendacao': recomendacao})
        else:      
            return render(request,'testeDetail.html', {'teste':'nada'})
    #Apresento aqui o primeiro teste ou o teste atual caso atulize a pagina
    cont=t-1
    print(cont,t)
    return render(request,'testeDetail.html', {'teste': results[cont]})         

#Chama pagina para digitação do problema quando o usuário seleciona "Problema não listado"
def pesquisa(request):
    global problema
    global equipamento
    recomendacaoTexto=[]
    compara=[]
    texto = request.POST['digita']
    compara=buscaKeyCategoria()
    
    for s in compara:
        a = s['key'].split(',')
        print (a)
        for p in a:
            print(p)
            b = p.strip()
            if b.find(texto)==0:
                print ('passou aqui')
                problema = s['nome']
                global results
                results = preparaTeste(equipamento, problema)
                context={
                    'equipamento': equipamento,
                    'problema': texto
                }
                return render(request, 'testes.html', {'context': context})
    recomendacaoTexto = buscaVideos(texto)
    return render(request,'recomendacao.html', {'recomendacao': recomendacaoTexto})