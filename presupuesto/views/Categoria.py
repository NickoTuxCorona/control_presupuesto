from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from django.forms.models import model_to_dict
from django.http import JsonResponse
from presupuesto.models import Categoria
import json

################################################################
##                     CRUD Categorías                        ##
################################################################

# Vista para crear una nuevas categorias
@csrf_exempt
def set_categorias(request):
    if request.method == 'POST':
        categorias_json = json.loads(request.body)
        for categoria_json in categorias_json:
            name = categoria_json['name']
            limit = categoria_json['limit'] if 'limit' in categoria_json else None
            categoria = Categoria.objects.create(name=name, limit=limit)
        return JsonResponse(
            {'status': 'success', 'message': 'Categorías creadas con éxito'}
        )
    return JsonResponse({'status': 'error', 'message': 'Error en el envío'})

# Vista para leer todas las categorias
def get_categorias(request):
    categorias = Categoria.objects.all()
    data = {'categorias': list(categorias.values())}
    return JsonResponse(data)

# Vista para leer una categoria en particular
def get_categoria(request, categoria_id):
    try:
        categoria = Categoria.objects.get(id=categoria_id)
    except Categoria.DoesNotExist:
        return JsonResponse(
            {'status': 'error', 'message': 'La Categoria no existe'},
            status=404
        )
    data = {'categoria': model_to_dict(categoria)}
    return JsonResponse(data)

# Vista para actualizar una categoria
@csrf_exempt
@require_http_methods(['PATCH'])
def update_categoria(request, categoria_id):
    try:
        categoria = Categoria.objects.get(id=categoria_id)
    except Categoria.DoesNotExist:
        return JsonResponse(
            {'status': 'error', 'message': 'La Categoria no existe'},
            status=404
        )

    if request.body:
        data = json.loads(request.body)
        categoria.id = data.get('id', categoria.name)
        categoria.name = data.get('name', categoria.name)
        categoria.limit = data.get('limit', categoria.limit)
        categoria.save()

        return JsonResponse(
            {'status': 'success', 'message': 'Categoria actualizada con éxito'}
        )

    return JsonResponse(
        {'status': 'error', 'message': 'No se han proporcionado datos'},
        status=400
    )

# Vista para eliminar una categoria
@csrf_exempt
def delete_categoria(request, categoria_id):
    try:
        categoria = Categoria.objects.get(id=categoria_id)
    except Categoria.DoesNotExist:
        return JsonResponse(
            {'status': 'error', 'message': 'La categoria no existe'},
        status=404)

    if request.method == 'DELETE':
        categoria.delete()
        return JsonResponse(
            {'status': 'success', 'message': 'Categoria eliminada con éxito'})
    else:
        return JsonResponse(
            {'status': 'error', 'message': 'Método no permitido'}, status=405)
