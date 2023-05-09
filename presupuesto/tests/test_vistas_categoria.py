from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from presupuesto.models import Categoria
from presupuesto.serializers import CategoriaSerializer
from presupuesto.views import CategoriaAPIView

class CategoriaAPIViewTestCase(APITestCase):

    def setUp(self):
        self.view = CategoriaAPIView.as_view()
        self.categoria = Categoria.objects.create(nombre='Test', descripcion='Test')
        self.url = reverse('categoria-detail', args=[self.categoria.pk])
        self.serializer = CategoriaSerializer(instance=self.categoria)

    def test_get(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, self.serializer.data)

    def test_post(self):
        data = {'nombre': 'Nueva Categoría', 'descripcion': 'Descripción de la nueva categoría'}
        response = self.client.post(reverse('categoria-list'), data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        categoria = Categoria.objects.get(nombre=data['nombre'])
        serializer = CategoriaSerializer(instance=categoria)
        self.assertEqual(response.data, serializer.data)

    def test_put(self):
        data = {'nombre': 'Categoría Actualizada', 'descripcion': 'Descripción de la categoría actualizada'}
        response = self.client.put(self.url, data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.categoria.refresh_from_db()
        serializer = CategoriaSerializer(instance=self.categoria)
        self.assertEqual(serializer.data, data)

    def test_patch(self):
        data = {'descripcion': 'Descripción actualizada'}
        response = self.client.patch(self.url, data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.categoria.refresh_from_db()
        serializer = CategoriaSerializer(instance=self.categoria)
        self.assertEqual(serializer.data, data)

    def test_delete(self):
        response = self.client.delete(self.url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        with self.assertRaises(Categoria.DoesNotExist):
            Categoria.objects.get(pk=self.categoria.pk)