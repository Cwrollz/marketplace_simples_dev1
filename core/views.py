from rest_framework import viewsets
from .models import Produto, Vendedor
from .serializers import ProdutoSerializer, VendedorSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from django.db.models import Count
from rest_framework.permissions import IsAuthenticated

class ProdutoViewSet(viewsets.ModelViewSet):
    queryset = Produto.objects.all()
    serializer_class = ProdutoSerializer

class VendedorViewSet(viewsets.ModelViewSet):
    queryset = Vendedor.objects.all()
    serializer_class = VendedorSerializer
    permission_classes = [IsAuthenticated]

class VendedoresComProdutosAPIView(APIView):
    def get(self, request):
        vendedores = Vendedor.objects.annotate(
            total_produtos=Count('produtos')
        )
        dados = [
            {
                'nome': vendedor.nome,
                'total_produtos': vendedor.total_produtos
            }
            for vendedor in vendedores
        ]
        return Response(dados)