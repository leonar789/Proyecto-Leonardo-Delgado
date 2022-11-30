from Venta import Venta, Compra
from descuento import descuento_restaurante
#Este apartado es usado para realizar compras a restaurantes
def comprar_restaurante(inventario_partidos,lista_clientes,productos_vendidos):
    while True:
    
        partido_ejecutandose= None
        entrada_vip=False
        cliente_compra=None
        #Se selecciona el partido y posteriormente se le solicita al cliente su cédula
        print("\nSeleccione el id del partido al que hayas confirmado asistencia: \n")
        for partido in inventario_partidos:
            partido.mostrar_informacion()
        while True:
            id_partido_seleccionado=input("Indique el Id del partido en el que te encuentras: ")
            try:
                if int(id_partido_seleccionado) not in range(1, len(inventario_partidos)+1):
                    print("Opcion no valida")
                    continue
            except:
                print("Opcion no valida")
                continue
            for partido in inventario_partidos:
                if partido.id==id_partido_seleccionado:
                    partido_ejecutandose=partido
            break
        while True:
            input_entrar_restaurante=input("\nBienvenido a la sección de restaurantes. Para ingresar a un restaurante, indique su cédula. Introduzca x para salir: \n- ")

            if input_entrar_restaurante=="x":
                break
            if not input_entrar_restaurante.isnumeric():
                print("Debes introducir tu cédula solo con números")
                continue
            entrada_compra=None
            #Se verifica que exista una entrada VIP que tenga como cédula del dueño la cédula del cliente
            for cliente in lista_clientes:
                if cliente.cedula==input_entrar_restaurante:
                    for entrada in cliente.entradas:
                        if entrada in partido_ejecutandose.entradas_asistencia_confirmada:
                            if entrada.vip==True:
                                print("\nEntrada VIP valida. Disfrute de los restaurantes")
                                cliente_compra=cliente
                                entrada_vip=True
                                entrada_compra=entrada
            if not entrada_vip:
                print("\nNo hay entradas vip registradas en la asistencia del partido bajo ese número de cédula")
                continue

            partido_ejecutandose.stadium.mostrar_resumen_restaurantes()
            while True:
                #Selecionas el restaurante
                seleccion_restaurante=input("\nIndique el ID del restaurante al que desea entrar: ")
                try:
                    if int(seleccion_restaurante)-1 not in range(0,len(partido_ejecutandose.stadium.restaurants)) or "." in seleccion_restaurante:
                        print("Introduzca una elección válida")
                        continue
                except:
                    print("Introduce un número")
                    continue
                break
            compra_cancelada=False
            
            restaurante_accedido=partido_ejecutandose.stadium.restaurants[int(seleccion_restaurante)-1]
            carrito_compras=[] #Todas las compras no confirmadas se guardan en un carrito para llevar un control.
            monto_neto=0
            descuento_compra=0
            while True:
                #Se muestran los productos de ese restaurante y el cliente selecciona lo que desea comprar.
                print("\nA continuación los productos disponibles:\n")
                restaurante_accedido.mostrar_productos(carrito_compras)
                while True:
                    inventario_previo=0
                    producto_compra=input("\nSelecciona el producto a comprar: ")
                    try:
                        if int(producto_compra)-1 not in range(0,len(restaurante_accedido.products)) or "." in producto_compra:
                            print("Introduzca una elección válida")
                            continue
                    except:
                        print("Introduce un número")
                        continue
                    break
                producto_seleccionado=restaurante_accedido.products[int(producto_compra)-1]
                try:
                    if producto_seleccionado.alcohol==True and cliente_compra.edad<18:
                        print("Eres menor de edad, no puedes comprar bebidas alcoholicas")
                        continue
                except:
                    pass

                for compra in carrito_compras: 
                    if compra.producto==producto_seleccionado:
                        inventario_previo+=compra.cantidad #Esto se encarga de llevar un registro de los productos preseleccionados por el usuario para evitar que supere el stock
                while True:
                    cantidad_compra=input(f"Introduce las unidades de {producto_seleccionado.name} que deseas: ")
                    try:
                        if int(cantidad_compra)<1 or "." in producto_compra:
                            print("Introduzca una elección válida")
                            continue
                    except:
                        print("Introduce un número")
                        continue
                    break
                if inventario_previo+int(cantidad_compra)<=producto_seleccionado.stock:
                    print("\nAñadido a la compra\n")
                    ya_en_carrito=False
                    for compra in carrito_compras:
                        if compra.producto==producto_seleccionado:
                            compra.cantidad+=int(cantidad_compra)
                            ya_en_carrito=True
                    if not ya_en_carrito:
                        carrito_compras.append(Compra(producto_seleccionado, int(cantidad_compra)))
                else:
                    print("\nNo hay suficiente inventario\n")
                
                validar_seguir_comprando=False
                while True:
        
                    seguir_comprando=input("Seguir Comprando s/n: ")
                    if seguir_comprando.lower() not in ["s","n"]:
                        print("Opcion no valida")
                        continue
                    if seguir_comprando.lower()=="s":
                        validar_seguir_comprando=True
                    break
                   
                if validar_seguir_comprando:
                    continue

                break
                        
            #Se muestra un resumen previo
            print("\n****************Resumen de Compra previo*****************")
            for compra in carrito_compras:
                compra.mostrar_compra()
                monto_neto+=compra.subtotal
            print("\n*********************************************************")
            descuento_compra=descuento_restaurante(input_entrar_restaurante, monto_neto) #Se realizan los cálculos del descuento y el IVA.
            iva=round(monto_neto*0.16,2)
            total=monto_neto-descuento_compra+iva
            print(f"IVA: \t\t{iva}$")
            print(f"Total: \t\t{total}$",end=" ")
            if descuento_compra:
                print(f"¡Obtuviste un descuento de {descuento_compra}$!")
            else:
                print("")
            print("\n*********************************************************")
                
            while True:
                confirmar_compra=input("¿Desea concretar la compra? s/n: ")
                if confirmar_compra not in ["s","n"]:
                    print("Opcion no valida")
                    continue
                
                if confirmar_compra=="n":
                    compra_cancelada=True 
                    break
                else:
                    break
            if compra_cancelada:
                break
            #Se imprime la factura con los datos de cada compra en carrito y luego el resumen
            print("\n**************************Factura**************************")
            print(f"{restaurante_accedido.name}\nNombre: {cliente_compra.nombre}\nCedula: {cliente_compra.cedula}")
            print("\n*************************Productos*************************")
            for compra in carrito_compras:
                compra.mostrar_compra()
            print("\n*********************************************************")
            
            
            print(f"\nMonto Neto: \t{monto_neto}$")
            print(f"Descuento: \t{descuento_compra}$", end="\t")
            if descuento_compra:
                print("¡El descuento es porque tu CI es un número perfecto!")
            else:
            
                print("")
            print(f"IVA: \t{iva}$")
            print(f"Total: \t\t{total}$")
            print("\n*********************************************************")
            for compra in carrito_compras:
                for producto in restaurante_accedido.products:
                    if compra.producto==producto:
                        producto.stock-=compra.cantidad
            entrada_compra.gastos+=total
            
            for compra in carrito_compras:
                ya_en_inventario=False
                for inventario in productos_vendidos:
                    if compra.producto.name==inventario.producto:
                        inventario.cantidad+=compra.cantidad
                        ya_en_inventario=True
                if not ya_en_inventario:
                    venta_producto_nuevo=Venta(compra.producto.name,compra.cantidad)
                    productos_vendidos.append(venta_producto_nuevo)

        break