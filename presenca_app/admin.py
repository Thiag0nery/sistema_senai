from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from django.shortcuts import render
from django.urls import path
import csv
from .models import RegistroProfessor

class CsvImportForm(forms.Form):
    csv_upload = forms.FileField()
class CsvRegistroProfessorForm(forms.Form):
    csv_upload = forms.FileField()
class CustomUserCreationForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=True, label='Nome do professor')
    username = forms.CharField(label='Usuário')
    password1 = forms.CharField(widget=forms.PasswordInput, label='Senha')
    password2 = forms.CharField(widget=forms.PasswordInput, label='Confirmação de Senha')

    class Meta:
        model = User
        fields = ('first_name', 'username', 'password1', 'password2')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['first_name'].required = True

    def save(self, commit=True):
        user = super(CustomUserCreationForm, self).save(commit=False)
        user.username = self.cleaned_data['username'].upper()  # Convertendo para maiúsculas
        if commit:
            user.save()
        return user

class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('first_name','username', 'password1', 'password2'),
        }),
    )
    def get_urls(self):
        urls = super().get_urls()
        new_urls = [path('upload-csv/', self.upload_csv),]
        return new_urls + urls
    def upload_csv(self, request):
        if request.method == 'POST':
            csv_upload = request.FILES['csv_upload']

            file = csv_upload.read().decode('utf-8').splitlines()

            reader = csv.reader(file)

            for tabela in reader:

                if tabela and tabela[0] != 'CÓDIGO DO PROFESSOR':

                    user = User.objects.create_user(username=tabela[0].upper(), first_name=str(tabela[1]),
                                                    password=tabela[2])
                    user.save()

        form = CsvImportForm()
        data ={'form': form}
        return render(request, 'admin/csv_upload_users.html', data)
class RegistroProfessorAdmin(admin.ModelAdmin):
    list_display = ('id', 'sala', 'curso', 'turma', 'professor', 'disciplina', 'data', 'turno')
    list_filter = ('sala', 'curso', 'turma', 'professor', 'disciplina', 'turno')
    ordering = ('-id',)

    def get_urls(self):
        urls = super().get_urls()
        new_urls = [path('upload-registro-csv/', self.upload_registro_csv),]
        return new_urls + urls
    def upload_registro_csv(self, request):


        if request.method == 'POST' and request.FILES['csv_upload']:
            arquivo = request.FILES['csv_upload']
            dados = []
            data = ''
            turno = ''
            file = arquivo.read().decode('latin-1').splitlines()

            reader = csv.reader(file, delimiter=';')

            next(reader)
            for linha, tabela in enumerate(reader):

                if tabela[0]:

                    if (tabela[0] == 'TURNO' or tabela[5]):
                        turno = tabela[1]
                        data = tabela[7]
                        continue
                    elif (tabela[0] == 'SALA'):
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

                    dados.append(registro_professor)

        RegistroProfessor.objects.bulk_create(dados)
        form = CsvRegistroProfessorForm()
        data ={'form': form}
        return render(request, 'admin/csv_upload_registro.html', data)

# Registrar o modelo User com o novo admin
admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)
admin.site.register(RegistroProfessor, RegistroProfessorAdmin)
