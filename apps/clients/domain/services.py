class ClienteService:
    @staticmethod
    def activar_cliente(cliente):
        if not cliente.activo:
            cliente.activo = True

    @staticmethod
    def desactivar_cliente(cliente):
        if cliente.activo:
            cliente.activo = False