#Marketplace Simples - DEV1

#Criando o ambiente virtual:
python -m venv .venv

#Ativando o ambiente virtual
.venv\Scripts\activate

#Instalando as dependencias
pip install -r requirements.txt

#Executando as migracoes
python manage.py migrate

#Iniciando o servidor
python manage.py runserver

#Criando o nosso app core
python manage.py startapp core

#Instalando Django REST Framework
pip install djangorestframework
pip freeze > requirements.txt

#consultas
python manage.py shell
from core.models import Vendedor, Produto

vendedor = Vendedor.objects.create(
    nome="Ana",
    email="ana@email.com"
)

Produto.objects.create(
    nome="Notebook",
    descricao="Notebook para estudos",
    preco=2500,
    estoque=5,
    vendedor=vendedor
)

Produto.objects.create(
    nome="Mouse",
    descricao="Mouse sem fio",
    preco=80,
    estoque=10,
    vendedor=vendedor
)

vendedor.produtos.all()

from core.models import Tag

tag1 = Tag.objects.create(nome="Eletrônicos")

tag2 = Tag.objects.create(nome="Informática")

Produto.objects.get(nome="Notebook").tags.add(tag1, tag2)

Produto.objects.get(nome="Notebook").tags.all()

#Criando um Manager customizado para produtos

class ProdutoQuerySet(models.QuerySet):
    def disponiveis(self):
        return self.filter(estoque__gt=0)

class ProdutoManager(models.Manager):
def get_queryset(self):
    return ProdutoQuerySet(self.model, using=self._db)

def disponiveis(self):
    return self.get_queryset().disponiveis()

#Consulta dos produtos disponíveis
Produto.objects.disponiveis()

#O método disponiveis() retorna apenas produtos com estoque maior que 0.

#Teste do Signal

Foi criado um Signal com post_save para atualizar o estoque quando um Pedido é confirmado.
Durante o teste, o estoque passou de 5 para 3 após a confirmação de um pedido com 2 unidades.

#Problema encontrado

A mensagem do Signal não aparecia porque o shell estava usando a versão antiga da função.
A solução foi fechar e abrir novamente o shell do Django. Após isso, o teste exibiu:
[log] Pedido confirmado: 2

#Criando serializers

Foi criado um serializer para Produto e um serializer para Tag.

O ProdutoSerializer utiliza o TagSerializer como serializer aninhado (nested), permitindo visualizar as tags relacionadas ao produto.

#Teste do serializer aninhado

O teste retornou as tags do Notebook dentro do produto:

'tags': [
    {'id': 1, 'nome': 'Eletrônicos'},
    {'id': 2, 'nome': 'Informática'}
]