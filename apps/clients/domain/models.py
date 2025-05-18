from dataclasses import dataclass
from datetime import datetime
from typing import Optional

@dataclass
class Cliente:
    id: Optional[int] = None
    nombre: str = ""
    email: str = ""
    telefono: str = ""
    fecha_creacion: datetime = datetime.now()
    activo: bool = True

    def __post_init__(self):
        self._validar()

    def _validar(self):
        if not self.nombre:
            raise ValueError("El nombre del cliente no puede estar vacío")
        if "@" not in self.email:
            raise ValueError("El email debe ser válido")