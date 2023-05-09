from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from presupuesto.models import Categoria
from presupuesto.serializers import CategoriaSerializer

################################################################
##                     CRUD Categorías                        ##
################################################################
class CategoriaAPIView(APIView):

    def pk_exists(self, pk):
        if not pk:
            return Response("No se especificó un id de categoría en la petición", 
                status=status.HTTP_400_BAD_REQUEST)
        try:
            return Categoria.objects.get(pk=pk)
        except Categoria.DoesNotExist:
            return Response(f"No existe una categoría con el id {pk}",
                status=status.HTTP_404_NOT_FOUND)
        
    def get(self, request, pk=None):
        if pk:
            categoria = self.pk_exists(pk)
            if isinstance(categoria, Response):
                return categoria
            serializer = CategoriaSerializer(categoria)
            return Response(serializer.data)
        else:
            serializer = CategoriaSerializer(Categoria.objects.all(), many=True)
            return Response(serializer.data)

    def post(self, request):
        data_list = [request.data] if isinstance(request.data, dict) else request.data

        for data in data_list:
            serializer = CategoriaSerializer(data=data)
            if not serializer.categoria_exists(data.get('id')) or \
                not serializer.is_valid():
                return Response(serializer.errors, 
                    status=status.HTTP_400_BAD_REQUEST)
            serializer.create(data)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def put(self, request, pk=None):
        categoria = self.pk_exists(pk)
        if isinstance(categoria, Response):
            return categoria
 
        serializer = CategoriaSerializer(categoria, data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
        
    def patch(self, request, pk=None):
        categoria = self.pk_exists(pk)
        if isinstance(categoria, Response):
            return categoria

        serializer = CategoriaSerializer(categoria,data=request.data,partial=True)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

    def delete(self, request, pk=None):
        categoria = self.pk_exists(pk)
        if isinstance(categoria, Response):
            return categoria

        categoria.delete()
        return Response("La categoría ha sido eliminada exitosamente", 
            status=status.HTTP_200_OK)