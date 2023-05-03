from django.urls import path
from .views import gastos_por_categoria,detalle_categoria

app_name = 'interfaces'

urlpatterns = [
    path('gastos-por-categoria/', gastos_por_categoria, name='gastos_por_categoria'),
    path('detalle-categoria/<int:categoria_id>/', detalle_categoria, name='detalle_categoria'),
]