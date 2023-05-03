from django.shortcuts import render,get_object_or_404
from presupuesto.models import Categoria,Transaccion
from django.db.models import Sum

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


def detalle_categoria(request, categoria_id):
    categoria = get_object_or_404(Categoria, pk=categoria_id)
    transacciones = Transaccion.objects.filter(category=categoria)

    importe_total_gastado = transacciones.aggregate(Sum('amount'))['amount__sum'] or 0
    cantidad_movimientos = transacciones.count()

    # Si la categoria tiene presupuesto, calcula el importe límite y disponible
    if categoria.limit:
        importe_limite_presupuesto = categoria.limit
        importe_disponible = importe_limite_presupuesto - importe_total_gastado
        porcentaje_gastado = (importe_total_gastado / importe_limite_presupuesto) * 100
    else:
        importe_limite_presupuesto = 0
        importe_disponible = 0
        porcentaje_gastado = 0

    context = {
        'categoria': categoria,
        'importe_total_gastado': importe_total_gastado,
        'cantidad_movimientos': cantidad_movimientos,
        'importe_limite_presupuesto': importe_limite_presupuesto,
        'importe_disponible': importe_disponible,
        'porcentaje_gastado': porcentaje_gastado,
    }
    return render(request, 'detalle_categoria.html', context)