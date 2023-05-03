from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.forms.models import model_to_dict
from presupuesto.models import Transaccion,Categoria
from datetime import datetime
import json

################################################################
##                   CRUD Transacciones                       ##
################################################################

# Vista para crear nuevas transacciones
@csrf_exempt
def set_transacciones(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        for transaccion_json in data:
            description = transaccion_json['description']
            category_id = transaccion_json['category']
            try:
                category = Categoria.objects.get(id=category_id)
            except Categoria.DoesNotExist:
                return JsonResponse(
                    {
                        'status': 'error', 
                        'message': f'La Categoria {category_id} no existe'
                    },
                    status=404
                )
            amount = transaccion_json['amount']
            date = transaccion_json['date'] if 'date' in transaccion_json\
                else datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            ignore = transaccion_json.get('ignore', False)
            transaccion = Transaccion.objects.create(
                description=description,
                category=category,
                amount=amount,
                date=date,
                ignore=ignore,
            )
        return JsonResponse(
            {'status': 'success', 'message': 'Transacciones creadas con éxito'}
        )
    return JsonResponse({'status': 'error', 'message': 'Error en el envío'})


# Vista para leer todas las transacciones
def get_transacciones(request):
    transacciones = Transaccion.objects.all()
    data = {'transacciones': list(transacciones.values())}
    return JsonResponse(data)


# Vista para leer una transaccion en particular
def get_transaccion(request, transaccion_id):
    try:
        transaccion = Transaccion.objects.get(id=transaccion_id)
    except Categoria.DoesNotExist:
        return JsonResponse(
            {'status': 'error', 'message': 'La Transacción no existe'},
            status=404
        )
    data = {'transaccion': model_to_dict(transaccion)}
    return JsonResponse(data)


# Vista para actualizar una transaccion
@csrf_exempt
@require_http_methods(['PATCH'])
def update_transaccion(request, transaccion_id):
    try:
        transaccion = Transaccion.objects.get(id=transaccion_id)
    except Categoria.DoesNotExist:
        return JsonResponse(
            {'status': 'error', 'message': 'La Transacción no existe'},
            status=404
        )
    if request.body:
        data = json.loads(request.body)
        transaccion.description = data.get(
            'description', 
            transaccion.description
        )
        if 'category' in data:
            category_id = data['category']
            try:
                category = Categoria.objects.get(id=category_id)
            except Categoria.DoesNotExist:
                return JsonResponse(
                    {
                        'status': 'error', 
                        'message': f'La Categoria {category_id} no existe'
                    },
                    status=404
                )
            transaccion.category = category
        transaccion.amount = data.get('amount', transaccion.amount)
        transaccion.date = data.get('date', transaccion.date)
        transaccion.ignore = data.get('ignore', transaccion.ignore)
        transaccion.save()

        return JsonResponse(
            {'status': 'success', 'message': 'Transacción actualizada con éxito'}
        )

    return JsonResponse(
        {'status': 'error', 'message': 'No se han proporcionado datos'},
        status=400
    )


# Vista para eliminar una transaccion
@csrf_exempt
def delete_transaccion(request, transaccion_id):
    try:
        transaccion = Transaccion.objects.get(id=transaccion_id)
    except Transaccion.DoesNotExist:
        return JsonResponse(
            {'status': 'error', 'message': 'La transacción no existe'},
            status=404
        )

    if request.method == 'DELETE':
        transaccion.delete()
        return JsonResponse(
            {'status': 'success', 'message': 'Transacción eliminada con éxito'}
        )
    else:
        return JsonResponse(
            {'status': 'error', 'message': 'Método no permitido'},
            status=405
        )
