from django.conf import settings
from django.db import models

class Vendedor(models.Model):
    nome = models.CharField(max_length=100)
    email = models.EmailField(unique=True)

    def __str__(self):
        return self.nome


class PerfilVendedor(models.Model):
    usuario = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )
    vendedor = models.OneToOneField(
        Vendedor,
        on_delete=models.CASCADE
    )


class Tag(models.Model):
    nome = models.CharField(max_length=100)

    def __str__(self):
        return self.nome


class Produto(models.Model):
    nome = models.CharField(max_length=100)
    descricao = models.TextField()
    preco = models.DecimalField(max_digits=10, decimal_places=2)
    estoque = models.IntegerField()

    vendedor = models.ForeignKey(
        Vendedor,
        on_delete=models.CASCADE,
        related_name="produtos"
    )

    tags = models.ManyToManyField(
        Tag,
        related_name="produtos"
    )


class Pedido(models.Model):
    usuario = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete= models.CASCADE
    )
    status = models.CharField(max_length=30)

    produtos = models.ManyToManyField(
        Produto,
        through="ItemPedido"
    )


class ItemPedido(models.Model):
    pedido = models.ForeignKey(
        Pedido,
        on_delete=models.CASCADE,
        related_name="itens"
    )
    produto = models.ForeignKey(
        Produto,
        on_delete=models.CASCADE,
        related_name="itens_pedido"
    )
    quantidade = models.IntegerField()
    preco_unitario = models.DecimalField(max_digits=10,decimal_places=2)