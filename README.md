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

#Criando ViewSet de Produto

Foi criado o ProdutoViewSet utilizando ModelViewSet para preparar o CRUD completo de Produto.

O ViewSet utiliza o ProdutoSerializer e o modelo Produto.

#Criando ViewSet e Router de Produto

Foi criado o ProdutoViewSet utilizando ModelViewSet para disponibilizar o CRUD de Produto.

O ViewSet foi registrado no Router, criando as rotas da API.

#Teste da API de Produtos

Acessando /api/produtos/, a API retornou os produtos cadastrados com HTTP 200 OK.

O teste também confirmou o funcionamento do serializer aninhado, exibindo as tags relacionadas ao Notebook dentro do resultado do produto.

#Teste do POST

Foi realizado um POST em /api/produtos/ para criar um novo produto.

Resultado: HTTP 201 Created.

Produto criado:
Nome: Teclado
Preço: 100.00
Estoque: 10
Vendedor: Ana
Tags: nenhuma

obs: No campo Vendedor aparece apenas "Ana" porque, até o momento, existe somente um Vendedor cadastrado no banco de dados.

#Em resumo: Teste do CRUD de Produto

GET /api/produtos/
Resultado: HTTP 200 OK

POST /api/produtos/
Resultado: HTTP 201 Created
Foi criado o produto Teclado.

PUT /api/produtos/3/
Resultado: HTTP 200 OK
O produto foi atualizado.

DELETE /api/produtos/3/
Resultado: HTTP 204 No Content
O produto foi excluído com sucesso.

#Teste do CRUD de Vendedor

GET /api/vendedores/
Resultado: HTTP 200 OK
Foi exibido o vendedor Ana.

POST /api/vendedores/
Resultado: HTTP 201 Created
Foi criado o vendedor Breno.

PUT /api/vendedores/2/
Resultado: HTTP 200 OK
O vendedor foi atualizado para Breno da Silva.

DELETE /api/vendedores/2/
Resultado: HTTP 204 No Content
O vendedor foi excluído com sucesso.

#Endpoint de agregação de vendedores

Foi criada uma consulta com annotate() e Count() para calcular a quantidade de produtos de cada vendedor.

GET /api/vendedores/com-produtos/

Resultado: HTTP 200 OK

[
    {
        "nome": "Ana",
        "total_produtos": 2
    }
]

#jwt

instalando o simpleJWT:
pip install djangorestframework-simplejwt


#Configuração do JWT

No arquivo config/settings.py foi configurado o JWTAuthentication:

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
}

Essa configuração permite que a API reconheça tokens JWT nas requisições.

#Endpoints de autenticação

Foram adicionados dois endpoints em config/urls.py:

POST /api/token/
POST /api/token/refresh/

O endpoint /api/token/ é utilizado para obter os tokens de acesso e de renovação.

O endpoint /api/token/refresh/ é utilizado para obter um novo token de acesso a partir do refresh token.

#Teste de obtenção do token

Foi realizado um teste utilizando o Postman.

POST /api/token/

Body:

{
    "username": "teste",
    "password": "123456"
}

Resultado: HTTP 200 OK

A resposta retornou os campos:

{
    "refresh": "...",
    "access": "..."
}

#Teste de renovação do token

Também foi testado o endpoint:

POST /api/token/refresh/

Body:

{
    "refresh": "..."
}

Resultado: HTTP 200 OK

A resposta retornou um novo token:

{
    "access": "..."
}

#Permissões

Foi utilizado o IsAuthenticated para proteger o endpoint de vendedores.

No arquivo core/views.py, o VendedorViewSet foi configurado para exigir autenticação:

permission_classes = [IsAuthenticated]

#Teste sem token

GET /api/vendedores/

Resultado: HTTP 401 Unauthorized

Resposta:

{
    "detail": "As credenciais de autenticação não foram fornecidas."
}

O resultado confirmou que o endpoint não pode ser acessado sem autenticação.

#Teste com token

GET /api/vendedores/

Foi utilizado um access token JWT válido no cabeçalho da requisição.

Resultado: HTTP 200 OK

Resposta:

[
    {
        "id": 1,
        "nome": "Ana",
        "email": "ana@email.com"
    }
]

O resultado confirmou que o endpoint pode ser acessado quando o usuário fornece um token JWT válido.