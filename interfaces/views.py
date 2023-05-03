from django.shortcuts import render
from presupuesto.models import Categoria,Transaccion

def gastos_por_categoria(request):
    categorias = Categoria.objects.all()
    for categoria in categorias:
        transacciones = Transaccion.objects.filter(category=categoria.id)
        gastado = sum(x.amount for x in transacciones)
        if categoria.limit:
            porcentaje = round(gastado / categoria.limit * 100, 2)
        else:
            transacciones = Transaccion.objects.filter(category=categoria.id).count()
    return render(request, 'gastos_por_categoria.html', {'categorias': categorias})
