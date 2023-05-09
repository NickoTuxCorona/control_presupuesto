from django.shortcuts import render
from presupuesto.views.operaciones import DetallesCategoriaView

def detalles_categoria_template(request, categoria_id):
    detalles_categoria_view = DetallesCategoriaView.as_view()
    response = detalles_categoria_view(request=request, categoria_id=categoria_id)
    categoria_data = response.data
    return render(
        request, 'detalle_categoria.html',
        {'categoria_data': categoria_data}
    )
