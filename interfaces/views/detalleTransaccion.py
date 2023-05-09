from django.shortcuts import render
from django.http import HttpResponseServerError,HttpResponse
from json import dumps
from presupuesto.views.operaciones import DetallesTransaccionView

import logging
logger = logging.getLogger(__name__)

def detalles_transaccion_template(request, transaccion_id):
    detalles_transaccion_view = DetallesTransaccionView.as_view()
    response = detalles_transaccion_view(request=request, transaccion_id=transaccion_id)
    transaccion_data = response.data
    if request.method == "GET":
        return render(
            request, 'detalle_transaccion.html', 
            {'transaccion_data': transaccion_data}
        )
    if request.method == "PUT":
        try:
            return HttpResponse(dumps(response.data))
        except:
            return HttpResponseServerError(
                'Ha ocurrido un error al actualizar la transacción')
