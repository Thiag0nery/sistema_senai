from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import RegistroProfessor 
from datetime import datetime
from django.db.models import Max
from unidecode import unidecode
import csv
from django.http import JsonResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate

from django.views.decorators.http import require_POST

def index(request):
    turno = 'MATUTINO'
    data_atual = datetime.now()
    hora = int(data_atual.strftime("%H"))
    if 12 <= hora < 18:
        turno = 'VESPERTINO'
    elif 18 <= hora or hora < 6:
        turno = 'NOTURNO'
    else:
        turno = 'MATUTINO'
    data_formatada = data_atual.strftime("%Y-%m-%d")

    data_banco = data_atual.strftime("%d/%m/%Y")

    registros_salvos = RegistroProfessor.objects.filter(data=data_banco, turno=turno)



    return render(request, 'index.html', {'registros_salvos': registros_salvos
        , 'data':data_formatada, 'turno': turno})

def pesquisa(request):
    try:
        turno = request.GET.get('turno')

        data_obj = datetime.strptime(request.GET.get('date'), "%Y-%m-%d")

        date = data_obj.strftime("%d/%m/%Y")

        registros_salvos = RegistroProfessor.objects.filter(data=date, turno=turno)
    except RegistroProfessor.DoesNotExist:

        registros_salvos = []

    return render(request, 'index.html', {'registros_salvos': registros_salvos})
def importar_csv(request):
    registros_salvos = []
    data_inicial = None

    if request.method == 'POST' and request.FILES['arquivo_csv']:
        arquivo = request.FILES['arquivo_csv']
        dados_csv = teste_arquivo_csv(arquivo)
        print(dados_csv)


        """for dado in dados_csv[2:]:
            print(dado['turno'])
            registro_professor = RegistroProfessor(
                sala=dado['sala'],
                curso=dado['curso'],
                turma=dado['turma'],
                professor=dado['professor'],
                disciplina=dado['disciplina'],
                data=dado['data'],
                turno=dado['turno']
            )
            registro_professor.save()
            registros_salvos.append(registro_professor)"""


    return redirect('index')

    
def processar_arquivo_csv(arquivo):

    dados = []
    reader = csv.reader(arquivo.read().decode('utf-8').splitlines())
    for row in reader:
        dados.append(row)
    
    return dados
def teste_arquivo_csv(arquivo):
    dados = []
    data = ''
    turno = ''
    file = arquivo.read().decode('latin-1').splitlines()

    reader = csv.reader(file, delimiter=';')

    next(reader)
    for linha,tabela in enumerate(reader):

        if tabela[0]:

            if(tabela[0] == 'TURNO' or tabela[5]):
                turno = tabela[1]
                data = tabela[7]
                continue
            elif(tabela[0] == 'SALA'):
                continue

            registro_professor = RegistroProfessor(
                sala=tabela[0],
                curso=tabela[2],
                turma=tabela[4],
                professor=tabela[6],
                disciplina=tabela[9],
                data=data,
                turno=turno
            )
            registro_professor.save()
    """for linha in enumerate(reader):
        print(linha[1][0])
        if len(linha[1]) >= 14 and linha[1][0]:
            if not(linha[1][0] == 'TURNO' or linha[1][0] == 'SALA'):
                sala = linha[1][0]

            if linha[1][2]:
                bool_turno =  linha[1][2]
            if linha[1][9]:
                data = linha[1][9]
            turno = bool_turno
            data = data
            turma =  linha[1][6]
            disciplina = linha[1][12]
            hora_inicial = linha[1][13]
            curso = linha[1][3]
            hora_final = linha[1][15]
            professor =  linha[1][8]
            sala = sala
            dados.append({
                'hora_inicial': hora_inicial,
                'hora_final': hora_final,
                'sala': sala,
                'curso': curso,
                'turma':turma,
                'turno':turno,
                'professor': professor,
                'disciplina': disciplina,
                'data': data
            })"""

    return dados

def salvar_hora(request):
    if request.method == 'POST':

        registro_id = request.POST.get('registro_id')
        tipo_hora = request.POST.get('tipo_hora')
        data_atual = datetime.now()
        hora = data_atual.strftime("%H:%M")
        print('Passou aqui no salvar_hora com o valor: ' + tipo_hora)
        try:
            registro = RegistroProfessor.objects.get(pk=registro_id)



            if tipo_hora == 'inicial':
                if not registro.hora_inicial:
                    registro.hora_inicial = datetime.now().time()
            elif tipo_hora == 'final':
                registro.hora_final = datetime.now().time()

            print(f'Hora Inicial: {registro.hora_inicial}, Hora Final: {registro.hora_final}')

            registro.save()


            return JsonResponse({'success': True, 'hora': hora})
        except RegistroProfessor.DoesNotExist:
            return JsonResponse({'success': False, 'error_message': 'Registro não encontrado'})
        except Exception as e:
            print(f'Erro: {e}')
            return JsonResponse({'success': False, 'error_message': str(e)})
    else:
        return JsonResponse({'success': False, 'error_message': 'Método não é POST'})

def user_authentication(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        exist = authenticate(request, username=username.upper(), password=password)

        if not exist:
            return JsonResponse({'success': False, 'error_message': 'Usuario ou senha incorretos'})
        else:
            registro_id = request.POST.get('registro_id')
            registro = RegistroProfessor.objects.filter(id=registro_id)[0]

            if not (unidecode(registro.professor.lower()) == unidecode(exist.first_name.lower())):
                return JsonResponse({'success': False,
                                     'error_message':
                                         'O nome do professor fornecido não corresponde ao registro'
                                         ' associado. Verifique suas credenciais e tente novamente.'})

        return JsonResponse({'success': True, 'success_message': 'Ação feita com sucesso'})

def redirecionar_para_admin(request):

    return redirect('admin:index')
