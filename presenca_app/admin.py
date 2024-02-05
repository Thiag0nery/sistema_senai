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

                    user = User.objects.create_user(username=tabela[0], first_name=str(tabela[1]),
                                                    password=tabela[2])
                    user.save()

        form = CsvImportForm()
        data ={'form': form}
        return render(request, 'admin/csv_upload_users.html', data)
class RegistroProfessorAdmin(admin.ModelAdmin):
    list_display = ('id', 'sala', 'curso', 'turma', 'professor', 'disciplina', 'data', 'turno')
    list_filter = ('sala', 'curso', 'turma', 'professor', 'disciplina', 'turno')
    ordering = ('-id',)

# Registrar o modelo User com o novo admin
admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)
admin.site.register(RegistroProfessor, RegistroProfessorAdmin)
