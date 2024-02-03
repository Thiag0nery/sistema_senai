from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from .models import RegistroProfessor
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
class RegistroProfessorAdmin(admin.ModelAdmin):
    list_display = ('id', 'sala', 'curso', 'turma', 'professor', 'disciplina', 'data', 'turno')
    list_filter = ('sala', 'curso', 'turma', 'professor', 'disciplina', 'turno')
    ordering = ('-id',)

# Registrar o modelo User com o novo admin
admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)
admin.site.register(RegistroProfessor, RegistroProfessorAdmin)
