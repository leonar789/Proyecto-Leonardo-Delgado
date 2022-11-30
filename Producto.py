class Producto:
    #Estas clases sirven para llevar un control de los productos y poder calcular la estadística.
    def __init__(self, name, net_price,stock):
        self.name=name
        self.price=round(net_price*1.16,2)
        self.net_price=net_price
        self.stock=stock
    def actualizar_inventario(self, cantidad):
        #Actualiza el inventario.
        if int(cantidad) <= self.stock:
            self.stock-=int(cantidad)
    def mostrar_informacion(self, compras_no_confirmadas):
            for compra in compras_no_confirmadas:
                if compra.producto==self:
                    print(f"- {self.name} \n\tPrecio: {self.net_price}\n\tCantidad Disponible: {self.stock-compra.cantidad}")
                else:
                    print(f"- {self.name} \n\tPrecio: {self.net_price}\n\tCantidad Disponible: {self.stock}")
                    
class Alimento(Producto):
    
    def __init__(self, name, price,stock, forma_consumo):
        super().__init__(name, price,stock)
        self.forma_consumo=forma_consumo
        self.tipo="Alimento"
    
class Bebida(Producto):
    
    def __init__(self, name, price,stock, alcohol):
        super().__init__(name, price,stock)
        self.alcohol=alcohol
        self.tipo="Bebida"