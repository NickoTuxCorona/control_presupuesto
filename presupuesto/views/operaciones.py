from django.utils import timezone
from django.db.models import Sum, Count, F, Q
from rest_framework.views import APIView
from rest_framework.response import Response
from presupuesto.models import Categoria, Transaccion


class TransaccionesCategoriaView(APIView):
    def get(self, request):
        data = []
        for categoria in Categoria.objects.all():
            transacciones_categoria = Transaccion.objects.filter(
                category=categoria,
                date__month=timezone.now().month
            ).aggregate(
                total_gastado=Sum('amount'),
                cantidad_movimientos=Count('id')
            )
            importe_limite = categoria.limit
            porcentaje_gastado = None
            if categoria.limit:
                try:
                    porcentaje_gastado = (transacciones_categoria['total_gastado'] / categoria.limit) * 100
                except:
                    porcentaje_gastado = 0
            data.append({
                'nombre_categoria': categoria.name,
                'importe_total_gastado': transacciones_categoria['total_gastado'] \
                    if transacciones_categoria['total_gastado'] is not None else 0,
                'cantidad_movimientos': transacciones_categoria['cantidad_movimientos'],
                'importe_limite_categoria': importe_limite,
                'porcentaje_gastado': porcentaje_gastado
            })
        return Response(data)


class DetallesCategoriaView(APIView):
    def get(self, request, categoria_id):
        categoria = Categoria.objects.get(id=categoria_id)
        transacciones_categoria = Transaccion.objects.filter(
            category=categoria,
            date__month=timezone.now().month,
            ignore=False
        ).aggregate(
            total_gastado=Sum('amount'),
            cantidad_movimientos=Count('id')
        )
        importe_total_gastado = transacciones_categoria['total_gastado']
        cantidad_movimientos = transacciones_categoria['cantidad_movimientos']
        importe_limite = categoria.limit
        importe_disponible = None
        porcentaje_gastado = None
        if importe_limite:
            importe_disponible = importe_limite - importe_total_gastado
            porcentaje_gastado = (importe_total_gastado / importe_limite) * 100
        movimientos = Transaccion.objects.filter(
            category=categoria,
            date__month=timezone.now().month
        ).values(
            'description',
            'date',
            'amount'
        )
        return Response({
            'nombre_categoria': categoria.name,
            'importe_total_gastado': importe_total_gastado,
            'cantidad_movimientos': cantidad_movimientos,
            'importe_limite_categoria': importe_limite,
            'importe_disponible': importe_disponible,
            'porcentaje_gastado': porcentaje_gastado,
            'movimientos': movimientos
        })


class DetallesTransaccionView(APIView):
    def get(self, request, transaccion_id):
        transaccion = Transaccion.objects.get(id=transaccion_id)
        return Response({
            'id': transaccion_id,
            'nombre_negocio': transaccion.description,
            'fecha': transaccion.date.date(),
            'hora': transaccion.date.time(),
            'importe': transaccion.amount,
            'categoria': transaccion.category.name,
            'ignorado': transaccion.ignore
        })

    def put(self, request, transaccion_id):
        transaccion = Transaccion.objects.get(id=transaccion_id)
        transaccion.ignore = not transaccion.ignore
        transaccion.save()
        return Response({'ignorado': transaccion.ignore})


class FueraPresupuestoView(APIView):
    def get(self, request):
        categorias = Categoria.objects.annotate(
            total_gastado=Sum('transaccion__amount', 
                filter=Q(transaccion__date__month=timezone.now().month)),
        ).annotate(
            excedido=F('limit') < F('total_gastado'),
            dentro=F('limit') >= F('total_gastado')
        )

        excedido = categorias.filter(excedido=True).values('name', 'total_gastado', 'limit')
        dentro = categorias.filter(dentro=True).values('name', 'total_gastado', 'limit')

        return Response({
            'excedido': excedido,
            'dentro': dentro
        })

