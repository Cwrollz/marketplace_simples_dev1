from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Pedido

@receiver(post_save, sender=Pedido)
def pedido_salvo(sender, instance, created, **kwargs):
    if instance.status == "confirmado":
        print(f"[log] Pedido confirmado: {instance.id}")
        for item in instance.itens.all():
            produto = item.produto
            produto.estoque -= item.quantidade
            produto.save()