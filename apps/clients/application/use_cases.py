from typing import List
from ..domain.models import Cliente
from ..application.interfaces import IClienteRepository
from ..application.dto import ClienteDTO

class CrearClienteUseCase:
    def __init__(self, cliente_repository: IClienteRepository):
        self.cliente_repository = cliente_repository

    def execute(self, cliente_dto: ClienteDTO) -> Cliente:
        cliente = Cliente(
            nombre=cliente_dto.nombre,
            email=cliente_dto.email,
            telefono=cliente_dto.telefono
        )
        return self.cliente_repository.guardar(cliente)

class ObtenerClientesUseCase:
    def __init__(self, cliente_repository: IClienteRepository):
        self.cliente_repository = cliente_repository

    def execute(self) -> List[Cliente]:
        return self.cliente_repository.obtener_todos()

class ObtenerClienteUseCase:
    def __init__(self, cliente_repository: IClienteRepository):
        self.cliente_repository = cliente_repository

    def execute(self, cliente_id: int) -> Cliente:
        return self.cliente_repository.obtener_por_id(cliente_id)
    
class ActualizarClienteUseCase:
    def __init__(self, cliente_repository: IClienteRepository):
        self.cliente_repository = cliente_repository

    def execute(self, cliente_id: int, cliente_dto: ClienteDTO) -> ClienteDTO:
        # Obtener el cliente existente
        cliente_existente = self.cliente_repository.obtener_por_id(cliente_id)
        if not cliente_existente:
            raise ValueError("Cliente no encontrado")

        # Actualizar datos
        cliente_actualizado = cliente_dto.to_domain()
        cliente_actualizado.id = cliente_id  # Asegurar el ID
        
        # Guardar cambios
        cliente_guardado = self.cliente_repository.actualizar(cliente_actualizado)
        return ClienteDTO.from_domain(cliente_guardado)
    
class EliminarClienteUseCase:
    def __init__(self, cliente_repository: IClienteRepository):
        self.cliente_repository = cliente_repository

    def execute(self, cliente_id: int) -> bool:
        # Podríamos añadir lógica de negocio aquí si es necesario
        # Por ejemplo, verificar si el cliente tiene pedidos antes de eliminar
        return self.cliente_repository.eliminar(cliente_id)