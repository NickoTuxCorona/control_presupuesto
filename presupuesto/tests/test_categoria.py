from django.test import TestCase, Client
from django.urls import reverse
from django.http import JsonResponse
import json
from presupuesto.models import Categoria


class CategoriaViewsTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.categoria1 = Categoria.objects.create(name='Categoria1')
        self.categoria2 = Categoria.objects.create(name='Categoria2', limit=500)
        self.categoria3 = Categoria.objects.create(name='Categoria3', limit=1000)

    def test_set_categorias_POST(self):
        data = [
            {'name': 'Categoria4'},
            {'name': 'Categoria5', 'limit': 200},
            {'name': 'Categoria6', 'limit': 300},
        ]
        response = self.client.post(
            reverse('set_categorias'),
            data=json.dumps(data),
            content_type='application/json',
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {'status': 'success', 'message': 'Categorías creadas con éxito'})
        self.assertEqual(Categoria.objects.count(), 6)

    def test_set_categorias_GET(self):
        response = self.client.get(reverse('set_categorias'))
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {'status': 'error', 'message': 'Error en el envío'})
        self.assertEqual(Categoria.objects.count(), 3)

    def test_get_categorias(self):
        response = self.client.get(reverse('get_categorias'))
        self.assertEqual(response.status_code, 200)
        expected_data = {'categorias': [
            {'id': self.categoria1.id, 'name': 'Categoria1', 'limit': None},
            {'id': self.categoria2.id, 'name': 'Categoria2', 'limit': 500},
            {'id': self.categoria3.id, 'name': 'Categoria3', 'limit': 1000},
        ]}
        self.assertEqual(response.json(), expected_data)

    def test_get_categoria_exists(self):
        response = self.client.get(reverse('get_categoria', args=[self.categoria1.id]))
        self.assertEqual(response.status_code, 200)
        expected_data = {'categoria': {'id': self.categoria1.id, 'name': 'Categoria1', 'limit': None}}
        self.assertEqual(response.json(), expected_data)

    def test_get_categoria_does_not_exist(self):
        response = self.client.get(reverse('get_categoria', args=[999]))
        self.assertEqual(response.status_code, 404)
        expected_data = {'status': 'error', 'message': 'La Categoria no existe'}
        self.assertEqual(response.json(), expected_data)

    def test_update_categoria(self):
        data = {'name': 'Nueva Categoria', 'limit': 1500}
        response = self.client.patch(
            reverse('update_categoria', args=[self.categoria2.id]),
            data=json.dumps(data),
            content_type='application/json',
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {'status': 'success', 'message': 'Categoria actualizada con éxito'})
        self.categoria2.refresh_from_db()
        self.assertEqual(self.categoria2.name, 'Nueva Categoria')
        self.assertEqual(self.categoria2.limit, 1500)

    def test_update_categoria_does_not_exist(self):
        categoria_id = 9999
        url = reverse('update-categoria', kwargs={'categoria_id': categoria_id})
        data = {'name': 'Categoria de prueba', 'limit': 1000}
        response = self.client.patch(url, data=json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json(), {'status': 'error', 'message': 'La Categoria no existe'})

