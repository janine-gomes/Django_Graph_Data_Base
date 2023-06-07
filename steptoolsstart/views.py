from django.shortcuts import render
from . import models
  
#Chama a pagina inicial Index
def index(request):
    print(models.get_results())
    print(models.get_cout())
    print(models.get_t())
    print(models.get_equipamento())
    print(models.get_problema())
    return render(request,'index.html')

#Chama a pagina para selecionar o equipamento em falha
def selecionaEquipamento(request):
    return render(request,'equipamento.html')

#Chama a pagina para selecionar o problema enfrentado
def selecionaProblema(request):
    #Pega o equipamento que o usuário selecionou
    if request.method=='POST':
        models.set_equipamento(request.POST.get('equipamento'))
        print(models.get_equipamento())
    return render(request,'problema.html')

def coletaDadosTeste(request):
     #Pega o problema que o usuário selecionou
     if request.method=='POST':
        models.set_problema(request.POST.get('exampleRadios'))
        print(models.get_problema())
       
        if models.get_problema() == 'digitar':
            return render(request,'digita.html')
        else:
            context = models.coletaDado(models.get_equipamento(), models.get_problema())
            models.set_results(models.preparaTeste(models.get_equipamento(), models.get_problema()))
            models.set_t(0)
            models.set_t(models.tamDicionario(models.get_results()))
            models.set_cout(0)
            
        return render(request, 'confirmaDados.html', {'context':context})

#Chama pagina Detelhe do Teste, mostrando teste por teste ao usuario
def iniciaTeste(request):
     #Zero a lista de recomendação
    recomendacao = []
    print(models.get_equipamento())
    print(models.get_problema())
    print(models.get_results())
    print(models.get_cout(),models.get_t())

    if request.method == 'POST':
        resultado = request.POST.get('botao')
        print(resultado)
        
        #Começo a contar o teste a partir do 1, porque o teste 0 ja foi mostrado
        if resultado == 'sim':
            print(models.get_cout(),models.get_t())
            return render(request,'final.html', {'teste': models.get_results()[models.get_cout()]})
        elif (resultado == 'nao') or (resultado =='nao se aplica'):
            models.set_cout(models.incrementador(models.get_cout()))
            print(models.get_cout(),models.get_t())
            if models.get_cout() < models.get_t():
                print('passouuuuuuu')
                print(models.get_cout(),models.get_t())
                return render(request,'teste.html', {'teste': models.get_results()[models.get_cout()]})
            elif models.get_cout() >= models.get_t():
                print('final dos testes')
                if models.get_problema() == 'no_power':
                    print('final dos testes')
                    texto = '{} não liga'.format(models.get_equipamento())
                    recomendacao = models.buscaVideosAPI(texto)
                    print(texto)                        
                   
                    return render(request,'recomendacao.html', {'recomendacao': recomendacao})
                elif models.get_problema() == 'no_video':
                    print('final dos testes')
                    texto = '{} não liga a tela'.format(models.get_equipamento())
                    recomendacao = models.buscaVideosAPI(texto)
                    print(texto)                        
                    
                    return render(request,'recomendacao.html', {'recomendacao': recomendacao})
                elif models.get_problema() == 'no_post':
                    print('final dos testes')
                    texto = '{} liga led mas não inicia'.format(models.get_equipamento())
                    recomendacao = models.buscaVideosAPI(texto)
                    print(texto)                        
                    
                    return render(request,'recomendacao.html', {'recomendacao': recomendacao})
                elif models.get_problema() == 'no_boot':
                    print('final dos testes')
                    texto = '{} falha no boot'.format(models.get_equipamento())
                    recomendacao = models.buscaVideosAPI(texto)
                    print(texto)                        
                    #
                    return render(request,'recomendacao.html', {'recomendacao': recomendacao})
        else:      
            return render(request,'teste.html', {'teste':'nada'})
    #Apresento aqui o primeiro teste ou o teste atual caso atulize a pagina
    print("AQUI",models.get_cout(),models.get_t())
    return render(request,'teste.html', {'teste': models.get_results()[models.get_cout()]})         

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
                models.set_problema(s['nome'])
                models.set_results(models.preparaTeste(models.get_equipamento(), models.get_problema()))
                models.set_t(models.tamDicionario(models.get_results()))
                models.set_cout(0)
                context={
                    'equipamento': models.get_equipamento(),
                    'problema': texto
                }
                return render(request, 'confirmaDados.html', {'context': context})
    recomendacaoTexto = models.buscaVideosAPI(texto)
    return render(request,'recomendacao.html', {'recomendacao': recomendacaoTexto})

