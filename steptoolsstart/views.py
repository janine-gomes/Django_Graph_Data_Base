from django.shortcuts import render
from . import models

#Zero as variaveis contadoras das listas
cont = None
t = None
results = []
equipamento = None
problema = None

#Count
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
        set_equipamento(request.POST.get('equipamento'))
        print(get_equipamento())
    return render(request,'problema.html')

def coletaDadosTeste(request):
     #Pega o problema que o usuário selecionou
     if request.method=='POST':
        set_problema(request.POST.get('exampleRadios'))
        print(get_problema())
        if get_problema() == 'digitar':
            return render(request,'digita.html')
        else:
            context = models.coletaDado(get_equipamento(), get_problema())
            set_results(models.preparaTeste(get_equipamento(), get_problema()))
            print(get_results())
            set_t(models.tamDicionario(get_results()))
            set_cout(0)
            print(get_results())
        return render(request, 'confirmaDados.html', {'context':context})

#Chama pagina Detelhe do Teste, mostrando teste por teste ao usuario
def iniciaTeste(request):
     #Zero a lista de recomendação
    recomendacao = []
    xResults = []
    texto = None
    resultado = None
    
    xResults = (get_results())
    print((xResults))

    if request.method == 'POST':
        resultado = request.POST.get('botao')
        print(resultado)
        
        #Começo a contar o teste a partir do 1, porque o teste 0 ja foi mostrado
        if resultado == 'sim':
            print(get_cout(),get_t())
            return render(request,'final.html', {'teste': xResults[get_cout()]})
        if (resultado == 'nao') or (resultado =='nao se aplica'):
            print('passouuuuuuu')
            set_cout(models.crementador(get_cout()))
            if get_cout()<get_t():
                print(get_cout(),get_t())
                return render(request,'teste.html', {'teste': xResults[get_cout()]})
            else:
                if get_problema() == 'no_power':
                    texto = '{} não liga'.format(get_equipamento())
                    recomendacao = models.buscaVideosAPI(texto)
                    print(texto)                        
                    #set_cout(get_t())
                    return render(request,'recomendacao.html', {'recomendacao': recomendacao})
                elif get_problema() == 'no_video':
                    texto = '{} não liga a tela'.format(get_equipamento())
                    recomendacao = models.buscaVideosAPI(texto)
                    print(texto)                        
                    #set_cout(get_t())
                    return render(request,'recomendacao.html', {'recomendacao': recomendacao})
                elif get_problema() == 'no_post':
                    texto = '{} liga led mas não inicia'.format(get_equipamento())
                    recomendacao = models.buscaVideosAPI(texto)
                    print(texto)                        
                    #set_cout(get_t())
                    return render(request,'recomendacao.html', {'recomendacao': recomendacao})
                elif get_problema() == 'no_boot':
                    texto = '{} falha no boot'.format(get_equipamento())
                    recomendacao = models.buscaVideosAPI(texto)
                    print(texto)                        
                    #set_cout(get_t())
                    return render(request,'recomendacao.html', {'recomendacao': recomendacao})
        else:      
            return render(request,'teste.html', {'teste':'nada'})
    #Apresento aqui o primeiro teste ou o teste atual caso atulize a pagina
    print("AQUI",get_cout(),get_t())
    return render(request,'teste.html', {'teste': xResults[get_cout()]})         

#Chama pagina para digitação do problema quando o usuário seleciona "Problema não listado"
def pesquisa(request):
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
                set_problema(s['nome'])
                set_results(models.preparaTeste(get_equipamento(), get_problema()))
                set_t(models.tamDicionario(get_results()))
                set_cout(0)
                context={
                    'equipamento': get_equipamento(),
                    'problema': texto
                }
                return render(request, 'confirmaDados.html', {'context': context})
    recomendacaoTexto = models.buscaVideosAPI(texto)
    return render(request,'recomendacao.html', {'recomendacao': recomendacaoTexto})