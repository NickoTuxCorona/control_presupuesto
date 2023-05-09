from django.urls import path
from .views.categoria import CategoriaAPIView
from .views.transaccion import TransaccionAPIView
from .views.operaciones import (TransaccionesCategoriaView,DetallesCategoriaView,
DetallesTransaccionView,FueraPresupuestoView)

app_name = 'presupuesto'

urlpatterns = [
    path('categorias/', CategoriaAPIView.as_view(), name='categorias'),
    path('categorias/<int:pk>/', CategoriaAPIView.as_view(), name='categorias'),
    path('transacciones/', TransaccionAPIView.as_view(), name='transacciones'),
    path('transacciones/<int:pk>/', TransaccionAPIView.as_view(), name='transacciones'),

    path('transacciones_categoria/', TransaccionesCategoriaView.as_view(), name='transacciones_categoria'),
    path('detalles_categorias/<int:pk>/', DetallesCategoriaView.as_view(), name='detalles_categorias'),
    path('detalles_transacciones/<int:pk>/', DetallesTransaccionView.as_view(), name='detalles_transacciones'),
    path('fuera_presupuesto/', FueraPresupuestoView.as_view(), name='fuera_presupuesto'),

]