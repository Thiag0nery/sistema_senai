Bem vindo a instalação do projeto!!!

Primeiros passos:

1 - Venv(ambiente virtual), abra o terminal e siga os seguintes passos:

1.1 - Criação do ambiente virtual:

```python
python -m venv venv
```
 1.2 - Rodando do ambiente virtual:
 ```python
  .\venv\Scripts\activate  
 ```
2 - Com o ambiente virtual criado, instale as dependencias do projeto:
```python
pip install -r requirements.txt
```
3 - Crie um arquivo .env na raiz do projeto, isso para rodar as viaveis de ambiente:
```env
DEBUG=True
SECRET_KEY='django-insecure-eux4ptvn4dx_ddjg@585he_lc6$i)a#4uzq4^w-o5#(r95k#m5'
DB_ENGINE=Qual banco de dados você usa
DB_NAME=Nome da tabela
DB_USER=Nome do usuario
DB_PASSWORD=Senha do banco
DB_HOST=localhost
DB_PORT=Porta do banco
``` 
4- Logo apos a instalação das dependencias rode o projeto localmente com:
```python
python manage.py runserver
```

PARABENS projeto rodado com sucesso! Qualquer problema conectar com o desenvolvedor do sistema