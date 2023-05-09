import json
from django.test import TestCase, Client
from rest_framework import status
from presupuesto.models import Categoria
from presupuesto.serializers import CategoriaSerializer
from django.urls import reverse


client = Client()

class GetSingleCategoriaTest(TestCase):

    def setUp(self):
        self.categoria1 = Categoria.objects.create(nombre="Categoria1", descripcion="Descripción de Categoría1")
        self.serializer = CategoriaSerializer(instance=self.categoria1)

    def test_get_valid_single_categoria(self):
        response = client.get('/categorias/' + str(self.categoria1.pk) + '/')
        categoria = Categoria.objects.get(pk=self.categoria1.pk)
        serializer = CategoriaSerializer(categoria)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_invalid_single_categoria(self):
        response = client.get('/categorias/99/')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class CreateNewCategoriaTest(TestCase):

    def setUp(self):
        self.valid_payload = {
            'nombre': 'Categoria2',
            'descripcion': 'Descripción de Categoría2'
        }
        self.invalid_payload = {
            'nombre': '',
            'descripcion': ''
        }

    def test_create_valid_categoria(self):
        response = client.post(
            '/categorias/',
            data=json.dumps(self.valid_payload),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_invalid_categoria(self):
        response = client.post(
            '/categorias/',
            data=json.dumps(self.invalid_payload),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class UpdateSingleCategoriaTest(TestCase):

    def setUp(self):
        self.categoria1 = Categoria.objects.create(nombre="Categoria1", 
            descripcion="Descripción de Categoría1")
        self.valid_payload = {
            'nombre': 'Categoria1 Actualizada',
            'descripcion': 'Descripción de Categoría1 Actualizada'
        }
        self.invalid_payload = {
            'nombre': '',
            'descripcion': ''
        }

    def test_valid_update_categoria(self):
        response = client.put(
            '/categorias/' + str(self.categoria1.pk) + '/',
            data=json.dumps(self.valid_payload),
            content_type='application/json'
        )
        categoria = Categoria.objects.get(pk=self.categoria1.pk)
        serializer = CategoriaSerializer(categoria)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_invalid_update_categoria(self):
        response = client.put(
            '/categorias/' + str(self.categoria1.pk) + '/',
            data=json.dumps(self.invalid_payload),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class PartialUpdateSingleCategoriaTest(TestCase):

    def setUp(self):
        self.categoria1 = Categoria.objects.create(nombre="Categoria1", 
                descripcion="Descripción de Categoría1")
        self.valid_payload = {
            'descripcion': 'Descripción de Categoría1 Actualizada'
        }
        self.invalid_payload = {
            'nombre': '',
            'descripcion': ''
        }

    def test_valid_partial_update_categoria(self):
        response = self.client.patch(
            reverse('categoria-detail', kwargs={'pk': self.categoria1.pk}),
            data=self.valid_payload,
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['descripcion'], 
            self.valid_payload['descripcion'])

    def test_invalid_partial_update_categoria(self):
        response = self.client.patch(
            reverse('categoria-detail', kwargs={'pk': self.categoria1.pk}),
            data=self.invalid_payload,
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
