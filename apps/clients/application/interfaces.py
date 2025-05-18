from abc import ABC, abstractmethod
from typing import List, Optional
from ..domain.models import Cliente

class IClienteRepository(ABC):
    @abstractmethod
    def obtener_por_id(self, cliente_id: int) -> Optional[Cliente]:
        pass
    
    @abstractmethod
    def obtener_todos(self) -> List[Cliente]:
        pass
    
    @abstractmethod
    def guardar(self, cliente: Cliente) -> Cliente:
        pass
    
    @abstractmethod
    def eliminar(self, cliente_id: int) -> bool:
        pass