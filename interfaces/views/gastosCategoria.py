from django.shortcuts import render
from presupuesto.views.operaciones import TransaccionesCategoriaView

def transacciones_categoria_template(request):
    transacciones_categoria_view = TransaccionesCategoriaView.as_view()
    response = transacciones_categoria_view(request=request)
    data = response.data
    return render(
        request, 'gastos_por_categoria.html',
        {'data': data}
    )

