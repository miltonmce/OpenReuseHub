from django.shortcuts import render

# Create your views here.
from django.views import View
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.urls import reverse

from ..application.use_cases import CrearClienteUseCase, ObtenerClientesUseCase,EliminarClienteUseCase, ObtenerClienteUseCase, ActualizarClienteUseCase
from ..application.dto import ClienteDTO
from ..infrastructure.repositories import DjangoClienteRepository

class ClienteListView(View):
    def get(self, request):
        use_case = ObtenerClientesUseCase(DjangoClienteRepository())
        clientes = use_case.execute()
        return render(request, 'clients/list.html', {'clientes': clientes})

class ClienteCreateView(View):
    def get(self, request):
        return render(request, 'clients/create.html')

    def post(self, request):
        nombre = request.POST.get('nombre')
        email = request.POST.get('email')
        telefono = request.POST.get('telefono')
        
        use_case = CrearClienteUseCase(DjangoClienteRepository())
        try:
            cliente = use_case.execute(ClienteDTO(nombre, email, telefono))
            return redirect('clientes:list')
        except ValueError as e:
            return render(request, 'clients/create.html', {'error': str(e)})

class ClienteEditView(View):
    def get(self, request, cliente_id):
        use_case = ObtenerClienteUseCase(DjangoClienteRepository())
        cliente = use_case.execute(cliente_id)
        
        if not cliente:
            return redirect('clientes:list')
            
        return render(request, 'clients/edit.html', {
            'cliente': cliente,
            'form_action': f'/clientes/editar/{cliente_id}/'
        })

    def post(self, request, cliente_id):
        cliente_dto = ClienteDTO(
            nombre=request.POST.get('nombre'),
            email=request.POST.get('email'),
            telefono=request.POST.get('telefono')
        )
        
        try:
            use_case = ActualizarClienteUseCase(DjangoClienteRepository())
            use_case.execute(cliente_id, cliente_dto)
            return redirect('clientes:list')
        except ValueError as e:
            return render(request, 'clients/edit.html', {
                'error': str(e),
                'cliente': cliente_dto,
                'form_action': f'/clientes/editar/{cliente_id}/'
            })
            
class ClienteDeleteView(View):
    def post(self, request, cliente_id):
        use_case = EliminarClienteUseCase(DjangoClienteRepository())
        success = use_case.execute(cliente_id)
        
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({'success': success})
        
        return redirect(reverse('clientes:list'))