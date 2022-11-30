#Esta clase tiene una finalidad organizativa para controlar los productos y su stock.
class Restaurante:
    def __init__(self, name, products):
        self.name=name
        self.products=products
    def mostrar_productos(self,compras_no_completadas):
        #Esta función muestra los productos de un restaurante durante una compra.
        contador=1
        for producto in self.products:
            ya_impreso=False
            for compra in compras_no_completadas:
                if compra.producto==producto:
                    print(f"{contador}-{producto.name} \n\tPrecio: {producto.net_price}\n\tCantidad Disponible: {producto.stock-compra.cantidad}")
                    ya_impreso=True
                    break
            if not ya_impreso:  
                print(f"{contador}-{producto.name} \n\tPrecio: {producto.net_price}\n\tCantidad Disponible: {producto.stock}")
            contador+=1