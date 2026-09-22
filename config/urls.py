from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter

from core.views import ProdutoViewSet, VendedorViewSet, VendedoresComProdutosAPIView

router = DefaultRouter()
router.register('produtos',ProdutoViewSet)
router.register('vendedores', VendedorViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path(
        'api/vendedores/com-produtos/',
        VendedoresComProdutosAPIView.as_view(),
        name='vendedores-com-produtos'
        ),
    path('api/', include(router.urls)),
]
