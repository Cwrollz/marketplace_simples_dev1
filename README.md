#Marketplace Simples - DEV1

#Tecnologias utilizadas

- Python
- Django
- Django REST Framework
- Django REST Framework Simple JWT
- SQLite
- Postman

#Criando o ambiente virtual

```bash
python -m venv .venv
```

#Ativando o ambiente virtual

```bash
.venv\Scripts\activate
```

#Instalando as dependências

```bash
pip install -r requirements.txt
```

#Executando as migrações

```bash
python manage.py migrate
```

#Iniciando o servidor

```bash
python manage.py runserver
```

#Criando o app core

```bash
python manage.py startapp core
```

#Instalando Django REST Framework

```bash
pip install djangorestframework
pip freeze > requirements.txt
```

#Consultas

Para realizar as consultas, foi utilizado:

```bash
python manage.py shell
```

##Criando vendedor

```python
from core.models import Vendedor, Produto

vendedor = Vendedor.objects.create(
    nome="Ana",
    email="ana@email.com"
)
```

##Criando produtos

```python
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
```

##Consulta utilizando related_name

```python
vendedor.produtos.all()
```

##Criando e relacionando tags

```python
from core.models import Tag

tag1 = Tag.objects.create(nome="Eletrônicos")
tag2 = Tag.objects.create(nome="Informática")

Produto.objects.get(nome="Notebook").tags.add(tag1, tag2)

Produto.objects.get(nome="Notebook").tags.all()
```

#Manager customizado

Foi criado um Manager customizado para consultar produtos disponíveis em estoque.

```python
class ProdutoQuerySet(models.QuerySet):
    def disponiveis(self):
        return self.filter(estoque__gt=0)


class ProdutoManager(models.Manager):
    def get_queryset(self):
        return ProdutoQuerySet(self.model, using=self._db)

    def disponiveis(self):
        return self.get_queryset().disponiveis()
```

Consulta:

```python
Produto.objects.disponiveis()
```

O método `disponiveis()` retorna apenas produtos com estoque maior que 0.

#Signal

Foi criado um Signal com `post_save` para atualizar o estoque quando um Pedido é confirmado.

Durante o teste, o estoque passou de 5 para 3 após a confirmação de um pedido com 2 unidades.

Resultado:

```text
[log] Pedido confirmado: 2
```

#Serializers

Foi criado um serializer para `Produto` e um serializer para `Tag`.

O `ProdutoSerializer` utiliza o `TagSerializer` como serializer aninhado (nested), permitindo visualizar as tags relacionadas ao produto.

Exemplo:

```json
"tags": [
    {
        "id": 1,
        "nome": "Eletrônicos"
    },
    {
        "id": 2,
        "nome": "Informática"
    }
]
```

#ViewSet e Router

Foi criado o `ProdutoViewSet` utilizando `ModelViewSet` para disponibilizar o CRUD de Produto.

O ViewSet foi registrado no Router, criando as rotas da API.

#Teste da API de Produtos

```text
GET /api/produtos/
```

Resultado:

```text
HTTP 200 OK
```

O teste também confirmou o funcionamento do serializer aninhado, exibindo as tags relacionadas ao Notebook.

#Teste do CRUD de Produto

```text
GET /api/produtos/
Resultado: HTTP 200 OK
```

```text
POST /api/produtos/
```

Body:

```json
{
    "nome": "Teclado",
    "descricao": "Teclado mecânico",
    "preco": "100.00",
    "estoque": 10,
    "vendedor": 1
}
```

Resultado:

```text
HTTP 201 Created
Produto criado: Teclado
```

Resposta:

```json
{
    "id": 3,
    "nome": "Teclado",
    "descricao": "Teclado mecânico",
    "preco": "100.00",
    "estoque": 10,
    "vendedor": 1,
    "tags": []
}
```

```text
PUT /api/produtos/3/
Resultado: HTTP 200 OK
```

```text
DELETE /api/produtos/3/
Resultado: HTTP 204 No Content
```

#Teste do CRUD de Vendedor

Os testes foram realizados utilizando autenticação JWT.

```text
GET /api/vendedores/
Resultado: HTTP 200 OK
```

```text
POST /api/vendedores/
```

Body:

```json
{
    "nome": "Breno",
    "email": "breno@email.com"
}
```

Resultado:

```text
HTTP 201 Created
Vendedor criado: Breno
```

Resposta:

```json
{
    "id": 2,
    "nome": "Breno",
    "email": "breno@email.com"
}
```

```text
PUT /api/vendedores/2/
Resultado: HTTP 200 OK
```

```text
DELETE /api/vendedores/2/
Resultado: HTTP 204 No Content
```

#Endpoint de agregação de vendedores

Foi criada uma consulta com `annotate()` e `Count()` para calcular a quantidade de produtos de cada vendedor.

```text
GET /api/vendedores/com-produtos/
```

Resultado:

```text
HTTP 200 OK
```

Exemplo de resposta:

```json
[
    {
        "nome": "Ana",
        "total_produtos": 2
    }
]
```

#JWT

Foi utilizada a biblioteca Django REST Framework Simple JWT.

##Instalação

```bash
pip install djangorestframework-simplejwt
```

##Configuração

No arquivo `config/settings.py`:

```python
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
}
```

Essa configuração permite que a API reconheça tokens JWT nas requisições.

#Endpoints de autenticação

```text
POST /api/token/
POST /api/token/refresh/
```

O endpoint `/api/token/` é utilizado para obter os tokens de acesso e de renovação.

O endpoint `/api/token/refresh/` é utilizado para obter um novo token de acesso a partir do refresh token.

#Teste de obtenção do token

Foi realizado um teste utilizando o Postman.

```text
POST /api/token/
```

Body:

```json
{
    "username": "usuario_de_teste",
    "password": "senha_de_teste"
}
```

Resultado:

```text
HTTP 200 OK
```

Resposta:

```json
{
    "refresh": "...",
    "access": "..."
}
```

#Teste de renovação do token

```text
POST /api/token/refresh/
```

Body:

```json
{
    "refresh": "..."
}
```

Resultado:

```text
HTTP 200 OK
```

Resposta:

```json
{
    "access": "..."
}
```

#Permissões

Foi utilizado o `IsAuthenticated` para proteger o endpoint de vendedores.

No arquivo `core/views.py`:

```python
permission_classes = [IsAuthenticated]
```

#Teste sem token

```text
GET /api/vendedores/
```

Resultado:

```text
HTTP 401 Unauthorized
```

Resposta:

```json
{
    "detail": "As credenciais de autenticação não foram fornecidas."
}
```

#Teste com token

Foi utilizado um access token JWT válido no cabeçalho da requisição.

```text
GET /api/vendedores/
```

Resultado:

```text
HTTP 200 OK
```

Exemplo de resposta:

```json
[
    {
        "id": 1,
        "nome": "Ana",
        "email": "ana@email.com"
    }
]
```

#Evidências

Os testes de autenticação e permissões foram realizados utilizando o Postman.

Foram realizados testes de:

- obtenção do token JWT;
- renovação do token;
- acesso sem token, retornando `401 Unauthorized`;
- acesso com token, retornando `200 OK`.

As evidências dos testes estão disponíveis na pasta `evidencias/`, junto com a coleção exportada do Postman.