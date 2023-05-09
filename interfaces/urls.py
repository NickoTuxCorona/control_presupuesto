from django.urls import path
from .views.detalleTransaccion import detalles_transaccion_template
from .views.detalleCategoria import detalles_categoria_template
from .views.gastosCategoria import transacciones_categoria_template

app_name = 'interfaces'

urlpatterns = [
    path(
        'transacciones/detalle/<int:transaccion_id>/', 
        detalles_transaccion_template, 
        name='detalle_transaccion'
    ),
    path(
        'categorias/detalle/<int:categoria_id>/', 
        detalles_categoria_template, 
        name='detalle_transaccion'
    ),
    path(
        'categorias/gastos/', 
        transacciones_categoria_template, 
        name='detalle_transaccion'
    ),
]