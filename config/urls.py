from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter

from core.views import ProdutoViewSet, VendedorViewSet, VendedoresComProdutosAPIView

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

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
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
