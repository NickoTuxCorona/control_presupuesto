from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from presupuesto.models import Categoria, Transaccion
from presupuesto.serializers import TransaccionSerializer
import logging

logger = logging.getLogger(__name__)

################################################################
##                   CRUD Transacciones                       ##
################################################################

class TransaccionAPIView(APIView):

    def pk_exists(self, pk):
        if not pk:
            return Response("No se especificó un id de transacción en la petición", 
                status=status.HTTP_400_BAD_REQUEST)
        try:
            return Transaccion.objects.get(pk=pk)
        except Categoria.DoesNotExist:
            return Response(f"No existe una transacción con el id {pk}",
                status=status.HTTP_404_NOT_FOUND)

    def get(self, request, pk=None):
        if pk:
            transaccion = self.pk_exists(pk)
            if isinstance(transaccion, Response):
                return transaccion
            serializer = TransaccionSerializer(transaccion)
            return Response(serializer.data)
        else:
            serializer = TransaccionSerializer(Transaccion.objects.all(), many=True)
            return Response(serializer.data)

    def post(self, request):
        data_list = [request.data] if isinstance(request.data, dict) else request.data
        
        for data in data_list:
            serializer = TransaccionSerializer(data=data)
            if not serializer.transaccion_exists(data.get('id')) or \
                not serializer.is_valid():
                return Response(serializer.errors, 
                    status=status.HTTP_400_BAD_REQUEST)
            serializer.create(data)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def put(self, request, pk=None):
        transaccion = self.pk_exists(pk)
        if isinstance(transaccion, Response):
            return transaccion
        
        serializer = TransaccionSerializer(transaccion, data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
        serializer.update(transaccion,serializer.validated_data)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def patch(self, request, pk=None):
        transaccion = self.pk_exists(pk)
        if isinstance(transaccion, Response):
            return transaccion

        serializer = TransaccionSerializer(transaccion,data=request.data,partial=True)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        serializer.update(transaccion,serializer.validated_data)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def delete(self, request, pk=None):
        transaccion = self.pk_exists(pk)
        if isinstance(transaccion, Response):
            return transaccion
        
        transaccion.delete()
        return Response("La transacción ha sido eliminada exitosamente", 
            status=status.HTTP_204_NO_CONTENT)