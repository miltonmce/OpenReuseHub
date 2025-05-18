from django.urls import path
from .presentation.views import ClienteListView, ClienteCreateView, ClienteDeleteView, ClienteEditView
app_name = 'clientes'
urlpatterns = [
    path('clientes/', ClienteListView.as_view(), name='list'),
    path('clientes/nuevo/', ClienteCreateView.as_view(), name='create'),
    path("clientes/<int:cliente_id>/editar/", ClienteEditView.as_view(), name='edit'),
    path('clientes/<int:cliente_id>/eliminar/', ClienteDeleteView.as_view(), name='delete'),
    # Agrega más URLs para editar y eliminar
]