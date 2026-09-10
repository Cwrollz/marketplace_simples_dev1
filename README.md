#marketplace simples - dev1 

Criando o ambiente virtual:
python -m venv .venv

Ativando o ambiente virtual
.venv\Scripts\activate

Instalando as dependencias
pip install -r requirements.txt

Executando as migracoes
python manage.py migrate

Iniciando o servidor
python manage.py runserver