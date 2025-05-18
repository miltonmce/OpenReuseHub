from dataclasses import dataclass
from datetime import datetime
from typing import Optional

@dataclass
class ClienteDTO:
    """
    Data Transfer Object para la entidad Cliente.
    Se utiliza para transferir datos entre capas sin exponer la entidad de dominio.
    """
    nombre: str
    email: str
    telefono: str
    id: Optional[int] = None
    fecha_creacion: Optional[datetime] = None
    activo: Optional[bool] = True

    @classmethod
    def from_domain(cls, cliente):
        """Factory method para crear DTO a partir de una entidad de dominio"""
        return cls(
            id=cliente.id,
            nombre=cliente.nombre,
            email=cliente.email,
            telefono=cliente.telefono,
            fecha_creacion=cliente.fecha_creacion,
            activo=cliente.activo
        )

    def to_domain(self):
        """Convierte el DTO a una entidad de dominio"""
        from ..domain.models import Cliente  # Import local para evitar dependencias circulares
        return Cliente(
            id=self.id,
            nombre=self.nombre,
            email=self.email,
            telefono=self.telefono,
            fecha_creacion=self.fecha_creacion,
            activo=self.activo
        )