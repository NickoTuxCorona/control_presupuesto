from django.contrib import admin
from django.urls import path

from presupuesto.views.Categoria import (get_categoria,get_categorias,
set_categorias,update_categoria,delete_categoria)

from presupuesto.views.Transaccion import (get_transaccion,get_transacciones,
set_transacciones,update_transaccion,delete_transaccion)

urlpatterns = [
    # --------------------------------------------------------------------------
    # Ruta para crear categorías
    path('categorias/set/', set_categorias, name='set_categorias'),
    # Ruta para obtener todas las categorías
    path('categorias/', get_categorias, name='get_categorias'),
    # Ruta para obtener una categoría en particular
    path('categorias/<int:categoria_id>/', get_categoria, name='get_categoria'),
    # Ruta para actualizar una categoría
    path('categorias/update/<int:categoria_id>/', update_categoria, name='update_categoria'),
    # Ruta para eliminar una categoría
    path('categorias/delete/<int:categoria_id>/', delete_categoria, name='delete_categoria'),
    # --------------------------------------------------------------------------
    # Ruta para crear transacciones
    path('transacciones/set/', set_transacciones, name='set_transacciones'),
    # Ruta para obtener todas las transacciones
    path('transacciones/', get_transacciones, name='get_transacciones'),
    # Ruta para obtener una transacción en particular
    path('transacciones/<int:transaccion_id>/', get_transaccion, name='get_transaccion'),
    # Ruta para actualizar una transacción
    path('transacciones/update/<int:transaccion_id>/', update_transaccion, name='update_transaccion'),
    # Ruta para eliminar una transacción
    path('transacciones/delete/<int:transaccion_id>/', delete_transaccion, name='delete_transaccion'),
]