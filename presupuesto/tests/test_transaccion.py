from django.test import TestCase
from presupuesto.models import Categoria, Transaccion
from presupuesto.serializers import TransaccionSerializer
from rest_framework.test import APIClient
from rest_framework import status
from django.urls import reverse
import json


class TransaccionAPIViewTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.categoria1 = Categoria.objects.create(nombre="Categoria1", descripcion="Descripción de Categoría1")
        self.transaccion1 = Transaccion.objects.create(nombre="Transaccion1", categoria=self.categoria1, descripcion="Descripción de Transacción1", monto=100)
        self.transaccion2 = Transaccion.objects.create(nombre="Transaccion2", categoria=self.categoria1, descripcion="Descripción de Transacción2", monto=200)

    def test_get_transaccion(self):
        response = self.client.get(reverse('transaccion', kwargs={'pk': self.transaccion1.pk}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, TransaccionSerializer(self.transaccion1).data)

    def test_get_transacciones(self):
        response = self.client.get(reverse('transacciones'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, TransaccionSerializer(Transaccion.objects.all(), many=True).data)

    def test_create_valid_transaccion(self):
        data = {'nombre': 'Transaccion3', 'categoria': self.categoria1.pk, 'descripcion': 'Descripción de Transacción3', 'monto': 300}
        response = self.client.post(reverse('transacciones'), data=json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data, TransaccionSerializer(Transaccion.objects.get(nombre='Transaccion3')).data)

    def test_create_invalid_transaccion(self):
        data = {'nombre': '', 'categoria': self.categoria1.pk, 'descripcion': '', 'monto': -300}
        response = self.client.post(reverse('transacciones'), data=json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        
    def test_update_valid_transaccion(self):
        data = {'nombre': 'Transaccion1 Actualizada', 'descripcion': 'Descripción de Transacción1 Actualizada', 'monto': 150}
        response = self.client.put(reverse('transaccion', kwargs={'pk': self.transaccion1.pk}), data=json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, TransaccionSerializer(Transaccion.objects.get(pk=self.transaccion1.pk)).data)

    def test_update_invalid_transaccion(self):
        data = {'nombre': '', 'categoria': self.categoria1.pk, 'descripcion': '', 'monto': -150}
        response = self.client.put(reverse('transaccion', kwargs={'pk': self.transaccion1.pk}), data=json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_partial_update_valid_transaccion(self):
        data = {'monto': 250}
        response = self.client.patch(reverse('transaccion', kwargs={'pk': self.transaccion1.pk}), data=json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, TransaccionSerializer(Transaccion.objects.get(pk=self.transaccion1.pk)).data)

    def test_partial_update_invalid_transaccion(self):
        data = {'monto': 'abc'}
        response = self.client.patch(reverse('transaccion', kwargs={'pk': self.transaccion1.pk}), data=json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_delete_valid_transaccion(self):
        response = self.client.delete(reverse('transaccion', kwargs={'pk': self.transaccion1.pk}))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Transaccion.objects.filter(pk=self.transaccion1.pk).exists())

    def test_delete_invalid_transaccion(self):
        response = self.client.delete(reverse('transaccion', kwargs={'pk': 123456}))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)