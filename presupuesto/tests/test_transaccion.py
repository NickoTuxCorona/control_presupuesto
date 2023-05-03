from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from presupuesto.models import Categoria, Transaccion
import json


class TransaccionTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.categoria1 = Categoria.objects.create(nombre='Categoria 1')
        self.categoria2 = Categoria.objects.create(nombre='Categoria 2')
        self.transaccion1 = Transaccion.objects.create(
            description='Transaccion 1',
            category=self.categoria1,
            amount=100,
            date='2022-05-03'
        )
        self.transaccion2 = Transaccion.objects.create(
            description='Transaccion 2',
            category=self.categoria2,
            amount=200,
            date='2022-05-04',
            ignore=True
        )
        self.valid_payload = [
            {
                'description': 'Transaccion 3',
                'category': self.categoria1.id,
                'amount': 300,
                'date': '2022-05-05'
            },
            {
                'description': 'Transaccion 4',
                'category': self.categoria2.id,
                'amount': 400,
                'date': '2022-05-06',
                'ignore': True
            }
        ]
        self.invalid_payload = [
            {
                'description': 'Transaccion 3',
                'category': 100, # Categoria que no existe
                'amount': 300,
                'date': '2022-05-05'
            }
        ]

    def test_set_transacciones(self):
        response = self.client.post(
            reverse('set_transacciones'),
            data=json.dumps(self.valid_payload),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json(), {'status': 'success', 'message': 'Transacciones creadas con éxito'})
        self.assertEqual(Transaccion.objects.count(), 4)

        response = self.client.post(
            reverse('set_transacciones'),
            data=json.dumps(self.invalid_payload),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.json(), {'status': 'error', 'message': 'La Categoria 100 no existe'})

    def test_get_transacciones(self):
        response = self.client.get(reverse('get_transacciones'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json(), {'transacciones': [
            {
                'id': self.transaccion1.id,
                'description': 'Transaccion 1',
                'category': self.categoria1.id,
                'amount': 100,
                'date': '2022-05-03T00:00:00Z',
                'ignore': False
            },
            {
                'id': self.transaccion2.id,
                'description': 'Transaccion 2',
                'category': self.categoria2.id,
                'amount': 200,
                'date': '2022-05-04T00:00:00Z',
                'ignore': True
            }
        ]})