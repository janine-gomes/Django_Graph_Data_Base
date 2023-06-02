from django.shortcuts import render
from . import models

#Zero as variaveis contadoras das listas
global t, cont, results
    
  
#Chama a pagina inicial Index
def index(request):
    return render(request,'index.html')

#Chama a pagina para selecionar o equipamento em falha
def selecionaEquipamento(request):
    return render(request,'equipamento.html')

#Chama a pagina para selecionar o problema enfrentado
def selecionaProblema(request):
    #Pega o equipamento que o usuário selecionou
    if request.method=='POST':
        global equipamento 
        equipamento = request.POST.get('equipamento')
        print(equipamento)
    return render(request,'problema.html')

def coletaDadosTeste(request):
     #Pega o problema que o usuário selecionou
     if request.method=='POST':
        global problema, equipamento
        problema = request.POST.get('exampleRadios')
        print(problema)
        if problema == 'digitar':
            return render(request,'digita.html')
        else:
            context = models.coletaDado(equipamento, problema)
            global results, t, cont
            results = models.preparaTeste(equipamento, problema)
            t = int(models.tamDicionario(results))
            cont = int(t)
            print(results)
        return render(request, 'confirmaDados.html', {'context':context})

#Chama pagina Detelhe do Teste, mostrando teste por teste ao usuario
def iniciaTeste(request):
    global t, cont, results
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
            return render(request,'final.html', {'teste': results[cont]})
        if (resultado == 'nao') or (resultado =='nao se aplica'):
            print('passouuuuuuu')
            cont = models.decrementador(cont)
            if cont>=0:
                print(cont,t)
                return render(request,'teste.html', {'teste': results[cont]})
            else:
                if problema == 'no_power':
                    texto = '{} não liga'.format(equipamento)
                    recomendacao = models.buscaVideosAPI(texto)
                    print(texto)                        
                    cont = t
                    return render(request,'recomendacao.html', {'recomendacao': recomendacao})
                elif problema == 'no_video':
                    texto = '{} não liga a tela'.format(equipamento)
                    recomendacao = models.buscaVideosAPI(texto)
                    print(cont)                        
                    cont = t
                    return render(request,'recomendacao.html', {'recomendacao': recomendacao})
                elif problema == 'no_post':
                    texto = '{} liga led mas não inicia'.format(equipamento)
                    recomendacao = models.buscaVideosAPI(texto)
                    print(texto)                        
                    cont = t
                    return render(request,'recomendacao.html', {'recomendacao': recomendacao})
                elif problema == 'no_boot':
                    texto = '{} falha no boot'.format(equipamento)
                    recomendacao = models.buscaVideosAPI(texto)
                    print(texto)                        
                    cont = t
                    return render(request,'recomendacao.html', {'recomendacao': recomendacao})
        else:      
            return render(request,'teste.html', {'teste':'nada'})
    #Apresento aqui o primeiro teste ou o teste atual caso atulize a pagina
    print("AQUI",cont,t)
    return render(request,'teste.html', {'teste': results[cont]})         

#Chama pagina para digitação do problema quando o usuário seleciona "Problema não listado"
def pesquisa(request):
    global problema
    global equipamento
    recomendacaoTexto=[]
    compara=[]
    texto = request.POST['digita']
    compara = models.buscaKeyCategoria()
    
    for s in compara:
        a = s['key'].split(',')
        print ('keys',a)
        for p in a:
            #print(p)
            b = p.strip()
            if b.find(texto)==0:
                print ('deu match')
                problema = s['nome']
                global results, t, cont
                results = models.preparaTeste(equipamento, problema)
                t = int(models.tamDicionario(results))
                cont = int(t)
                context={
                    'equipamento': equipamento,
                    'problema': texto
                }
                return render(request, 'confirmaDados.html', {'context': context})
    recomendacaoTexto = models.buscaVideosAPI(texto)
    return render(request,'recomendacao.html', {'recomendacao': recomendacaoTexto})