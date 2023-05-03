from django.urls import path
from .views import gastos_por_categoria

app_name = 'interfaces'

urlpatterns = [
    path('gastos-por-categoria/', gastos_por_categoria, name='gastos_por_categoria'),
]