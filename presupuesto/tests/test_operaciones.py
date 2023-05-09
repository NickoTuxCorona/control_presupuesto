from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from django.utils import timezone
from presupuesto.models import Categoria, Transaccion

class TransaccionesCategoriaViewTestCase(APITestCase):
    def setUp(self):
        self.categoria = Categoria.objects.create(name='Compras', limit=1000)
        self.transaccion1 = Transaccion.objects.create(description='Compra en el super', amount=500, date=timezone.now(), category=self.categoria)
        self.transaccion2 = Transaccion.objects.create(description='Compra en el super', amount=600, date=timezone.now(), category=self.categoria)

    def test_transacciones_categoria_view(self):
        url = reverse('transacciones-categoria')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['nombre_categoria'], 'Compras')
        self.assertEqual(response.data[0]['importe_total_gastado'], 1100)
        self.assertEqual(response.data[0]['cantidad_movimientos'], 2)
        self.assertEqual(response.data[0]['importe_limite_categoria'], 1000)
        self.assertEqual(response.data[0]['porcentaje_gastado'], 110)

class DetallesCategoriaViewTestCase(APITestCase):
    def setUp(self):
        self.categoria = Categoria.objects.create(name='Compras', limit=1000)
        self.transaccion1 = Transaccion.objects.create(description='Compra en el super', amount=500, date=timezone.now(), category=self.categoria)
        self.transaccion2 = Transaccion.objects.create(description='Compra en el super', amount=600, date=timezone.now(), category=self.categoria)

    def test_detalles_categoria_view(self):
        url = reverse('detalles-categoria', kwargs={'categoria_id': self.categoria.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['nombre_categoria'], 'Compras')
        self.assertEqual(response.data['importe_total_gastado'], 1100)
        self.assertEqual(response.data['cantidad_movimientos'], 2)
        self.assertEqual(response.data['importe_limite_categoria'], 1000)
        self.assertEqual(response.data['importe_disponible'], -100)
        self.assertEqual(response.data['porcentaje_gastado'], 110)
        self.assertEqual(len(response.data['movimientos']), 2)

class DetallesTransaccionViewTestCase(APITestCase):
    def setUp(self):
        self.categoria = Categoria.objects.create(name='Compras', limit=1000)
        self.transaccion = Transaccion.objects.create(description='Compra en el super', amount=500, date=timezone.now(), category=self.categoria)

    def test_detalles_transaccion_view(self):
        url = reverse('detalles-transaccion', kwargs={'transaccion_id': self.transaccion.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['nombre_negocio'], 'Compra en el super')
        self.assertEqual(response.data['fecha'], str(timezone.now().date()))
        self.assertEqual(response.data['importe'], 500)
        self.assertEqual(response.data['categoria'], 'Compras')
        self.assertFalse(response.data['ignorado'])

    def test_actualizar_estado_ignorado(self):
        url = reverse('detalles-transaccion', kwargs={'transaccion_id': self.transaccion1.pk})
        response = self.client.put(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.transaccion1.refresh_from_db()
        self.assertEqual(response.data, {'ignorado': True})
        self.assertTrue(self.transaccion1.ignore)
    
    def test_obtener_fuera_de_presupuesto(self):
        url = reverse('fuera-presupuesto')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.data,
            {
                'dentro': [
                    {
                        'name': self.categoria1.name,
                        'total_gastado': self.transaccion1.amount,
                        'limit': self.categoria1.limit
                    }
                ],
                'excedido': []
            }
        )

