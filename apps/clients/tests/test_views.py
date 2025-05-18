from django.test import TestCase, RequestFactory
from django.urls import reverse
from django.http import JsonResponse
from unittest.mock import MagicMock, patch

from apps.clients.presentation.views import (
    ClienteListView,
    ClienteCreateView,
    ClienteEditView,
    ClienteDeleteView
)
from apps.clients.application.dto import ClienteDTO
from apps.clients.domain.models import Cliente

class BaseTestCase(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.cliente_data = {
            'id': 1,
            'nombre': 'Test Cliente',
            'email': 'test@example.com',
            'telefono': '123456789'
        }
        self.cliente_dto = ClienteDTO(**self.cliente_data)
        self.cliente_entity = Cliente(**self.cliente_data)
        
class ClienteListViewTests(BaseTestCase):
    def test_get_returns_200(self):
        request = self.factory.get(reverse('clientes:list'))
        
        with patch('apps.clients.presentation.views.ObtenerClientesUseCase') as mock_use_case:
            mock_use_case.return_value.execute.return_value = [self.cliente_entity]
            response = ClienteListView.as_view()(request)
            
        self.assertEqual(response.status_code, 200)
        
    def test_get_uses_correct_template(self):
        request = self.factory.get(reverse('clientes:list'))
        
        with patch('apps.clients.presentation.views.ObtenerClientesUseCase') as mock_use_case:
            mock_use_case.return_value.execute.return_value = []
            response = ClienteListView.as_view()(request)
            
        self.assertTemplateUsed(response, 'clients/list.html')
        
    def test_get_passes_clientes_to_template(self):
        request = self.factory.get(reverse('clientes:list'))
        
        with patch('apps.clients.presentation.views.ObtenerClientesUseCase') as mock_use_case:
            mock_use_case.return_value.execute.return_value = [self.cliente_entity]
            response = ClienteListView.as_view()(request)
            
        self.assertIn('clientes', response.context_data)
        self.assertEqual(len(response.context_data['clientes']), 1)
        
class ClienteCreateViewTests(BaseTestCase):
    def test_get_returns_200(self):
        request = self.factory.get(reverse('clientes:create'))
        response = ClienteCreateView.as_view()(request)
        self.assertEqual(response.status_code, 200)
        
    def test_post_creates_cliente_and_redirects(self):
        data = {
            'nombre': 'Nuevo Cliente',
            'email': 'nuevo@example.com',
            'telefono': '987654321'
        }
        request = self.factory.post(reverse('clientes:create'), data)
        
        with patch('apps.clients.presentation.views.CrearClienteUseCase') as mock_use_case:
            mock_use_case.return_value.execute.return_value = self.cliente_entity
            response = ClienteCreateView.as_view()(request)
            
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse('clientes:list'))
        
    def test_post_with_invalid_data_returns_form_with_errors(self):
        data = {
            'nombre': '',  # Inválido
            'email': 'invalido',
            'telefono': ''
        }
        request = self.factory.post(reverse('clientes:create'), data)
        
        with patch('apps.clients.presentation.views.CrearClienteUseCase') as mock_use_case:
            mock_use_case.return_value.execute.side_effect = ValueError('Error de validación')
            response = ClienteCreateView.as_view()(request)
            
        self.assertEqual(response.status_code, 200)
        self.assertIn('error', response.context_data)
        
class ClienteEditViewTests(BaseTestCase):
    def test_get_returns_200_with_existing_cliente(self):
        request = self.factory.get(reverse('clientes:edit', args=[1]))
        
        with patch('apps.clients.presentation.views.ObtenerClienteUseCase') as mock_use_case:
            mock_use_case.return_value.execute.return_value = self.cliente_entity
            response = ClienteEditView.as_view()(request, cliente_id=1)
            
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context_data['cliente'], self.cliente_entity)
        
    def test_get_redirects_if_cliente_not_found(self):
        request = self.factory.get(reverse('clientes:edit', args=[99]))
        
        with patch('apps.clients.presentation.views.ObtenerClienteUseCase') as mock_use_case:
            mock_use_case.return_value.execute.return_value = None
            response = ClienteEditView.as_view()(request, cliente_id=99)
            
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse('clientes:list'))
        
    def test_post_updates_cliente_and_redirects(self):
        data = {
            'nombre': 'Cliente Actualizado',
            'email': 'actualizado@example.com',
            'telefono': '555555555'
        }
        request = self.factory.post(reverse('clientes:edit', args=[1]), data)
        
        with patch('apps.clients.presentation.views.ActualizarClienteUseCase') as mock_use_case:
            response = ClienteEditView.as_view()(request, cliente_id=1)
            
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse('clientes:list'))
        
    def test_post_with_invalid_data_returns_form_with_errors(self):
        data = {
            'nombre': '',  # Inválido
            'email': 'invalido',
            'telefono': ''
        }
        request = self.factory.post(reverse('clientes:edit', args=[1]), data)
        
        with patch('apps.clients.presentation.views.ActualizarClienteUseCase') as mock_use_case:
            mock_use_case.return_value.execute.side_effect = ValueError('Error de validación')
            response = ClienteEditView.as_view()(request, cliente_id=1)
            
        self.assertEqual(response.status_code, 200)
        self.assertIn('error', response.context_data)
        
class ClienteDeleteViewTests(BaseTestCase):
    def test_post_returns_json_for_ajax(self):
        request = self.factory.post(
            reverse('clientes:delete', args=[1]),
            HTTP_X_REQUESTED_WITH='XMLHttpRequest'
        )
        
        with patch('apps.clients.presentation.views.EliminarClienteUseCase') as mock_use_case:
            mock_use_case.return_value.execute.return_value = True
            response = ClienteDeleteView.as_view()(request, cliente_id=1)
            
        self.assertIsInstance(response, JsonResponse)
        self.assertEqual(response.json(), {'success': True})
        
    def test_post_redirects_for_non_ajax(self):
        request = self.factory.post(reverse('clientes:delete', args=[1]))
        
        with patch('apps.clients.presentation.views.EliminarClienteUseCase') as mock_use_case:
            mock_use_case.return_value.execute.return_value = True
            response = ClienteDeleteView.as_view()(request, cliente_id=1)
            
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse('clientes:list'))
        
    def test_post_handles_delete_failure(self):
        request = self.factory.post(
            reverse('clientes:delete', args=[99]),
            HTTP_X_REQUESTED_WITH='XMLHttpRequest'
        )
        
        with patch('apps.clients.presentation.views.EliminarClienteUseCase') as mock_use_case:
            mock_use_case.return_value.execute.return_value = False
            response = ClienteDeleteView.as_view()(request, cliente_id=99)
            
        self.assertEqual(response.json(), {'success': False})