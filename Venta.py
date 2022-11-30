#Estas clases sirven para organizar el proceso de compra y llevar un inventario de las ventas. 
class Venta:
    def __init__(self, producto, cantidad):
        self.producto=producto
        self.cantidad=cantidad
    def mostrar_resumen(self):
        
        print(f"-Producto: {self.producto}\n\tCantidad vendida: {self.cantidad}\n")
        
class Compra(Venta):
    def __init__(self, producto, cantidad):
        super().__init__(producto, cantidad)
        self.subtotal=float(producto.net_price)*cantidad
    def mostrar_compra(self):
        print(f"\n{self.cantidad}-{self.producto.name}\n\t{self.producto.net_price}$ * {self.cantidad} = {self.subtotal}$")
    def mostrar_resumen(self):
        print(f"\n-Producto: {self.producto.name}\n\tPrecio: {self.producto.net_price}$\n\tCantidad: {self.cantidad}")
