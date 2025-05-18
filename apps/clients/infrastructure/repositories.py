from django.core.exceptions import ObjectDoesNotExist
from typing import Optional
from ..application.interfaces import IClienteRepository
from ..domain.models import Cliente
from ..infrastructure.models import Cliente as ClienteModel
from typing import Optional, List
class DjangoClienteRepository(IClienteRepository):
    def obtener_por_id(self, cliente_id: int) -> Optional[Cliente]:
        try:
            cliente_db = ClienteModel.objects.get(id=cliente_id)
            return self._to_domain(cliente_db)
        except ObjectDoesNotExist:
            return None

    def obtener_todos(self) -> List[Cliente]:
        return [self._to_domain(c) for c in ClienteModel.objects.all()]

    def guardar(self, cliente: Cliente) -> Cliente:
        if cliente.id:
            cliente_db = ClienteModel.objects.get(id=cliente.id)
            cliente_db.nombre = cliente.nombre
            cliente_db.email = cliente.email
            cliente_db.telefono = cliente.telefono
            cliente_db.save()
        else:
            cliente_db = ClienteModel.objects.create(
                nombre=cliente.nombre,
                email=cliente.email,
                telefono=cliente.telefono,
                activo=cliente.activo
            )
        return self._to_domain(cliente_db)

    def _to_domain(self, cliente_db) -> Cliente:
        return Cliente(
            id=cliente_db.id,
            nombre=cliente_db.nombre,
            email=cliente_db.email,
            telefono=cliente_db.telefono,
            fecha_creacion=cliente_db.fecha_creacion,
            activo=cliente_db.activo
        )

    def eliminar(self, cliente_id: int) -> bool:
        try:
            ClienteModel.objects.get(id=cliente_id).delete()
            return True
        except ObjectDoesNotExist:
            return False
        
    def actualizar(self, cliente: Cliente) -> Cliente:
        cliente_db = ClienteModel.objects.get(id=cliente.id)
        cliente_db.nombre = cliente.nombre
        cliente_db.email = cliente.email
        cliente_db.telefono = cliente.telefono
        cliente_db.save()
        return self._to_domain(cliente_db)