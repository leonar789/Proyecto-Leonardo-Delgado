def buscar_producto_restaurante(estadios, criterio, informacion):
    #Esta es la función central que se encarga de realizar las búsquedas. Dependiendo del criterio que se ingrese, busca según cierta característica del producto
    print("\n A continuación los productos encontrados:\n")
    producto_encontrado=False
    for estadio in estadios:
        impresion_estadio=True
        for restaurante in estadio.restaurants:
            impresion_restaurante=True
            for producto_verificar in restaurante.products:
                #Las lineas anteriores acceden al inventario de todos los restaurantes.
                if criterio=="1": #Busqueda por Nombre
                    #Se compara el nombre indicado con el inventario de los restaurantes. Si coincide, imprime un resumen. 
                    if producto_verificar.name.lower()==informacion.lower():
                        if impresion_estadio:
                            print(f"Estadio: {estadio.name}\n")
                            impresion_estadio=False
                            producto_encontrado=True
                            print(f"\t-Restaurante: {restaurante.name}\n\t\tStock: {producto_verificar.stock} \n\t\tPrecio: {producto_verificar.price}$\n")
                            #Decidí imprimir el precio aunque en este caso sea igual para todos, ya que en la vida real es muy posible que varíen. 
                        else:
                            print(f"\t-Restaurante: {restaurante.name}\n\t\tStock: {producto_verificar.stock} \n\t\tPrecio: {producto_verificar.price}$\n")
                elif criterio=="2":#Busqueda por tipo

                    if informacion=="1":
                        #Busca los productos cuyo tipo sea "Alimento" e imprime un resumen
                        if producto_verificar.tipo=="Alimento":
                            if impresion_estadio:
                                print(f"Estadio: {estadio.name}\n")
                                impresion_estadio=False
                                producto_encontrado=True
                                impresion_restaurante=False
                                print(f"\t-Restaurante: {restaurante.name}\n\t\tProducto: {producto_verificar.name}\n\t\tStock: {producto_verificar.stock} \n\t\tPrecio: {producto_verificar.price}$\n")
                            
                            else:
                                if impresion_restaurante:
                                    print(f"\t-Restaurante: {restaurante.name}\n\t\tProducto: {producto_verificar.name}\n\t\tStock: {producto_verificar.stock}  \n\t\tPrecio: {producto_verificar.price}$\n")
                                    impresion_restaurante=False
                                else:
                                    print(f"\t\tProducto: {producto_verificar.name}\n\t\tStock: {producto_verificar.stock}  \n\t\tPrecio: {producto_verificar.price}$\n")
                    elif informacion=="2":
                         #Busca los productos cuyo tipo sea "Bebida" e imprime un resumen
                        if producto_verificar.tipo=="Bebida":
                            if impresion_estadio:
                                print(f"Estadio: {estadio.name}\n")
                                impresion_estadio=False
                                producto_encontrado=True
                                impresion_restaurante=False
                                print(f"\t-Restaurante: {restaurante.name}\n\t\tProducto: {producto_verificar.name}\n\t\tStock: {producto_verificar.stock} \n\t\tPrecio: {producto_verificar.price}$\n")
                            
                            else:
                                if impresion_restaurante:
                                    print(f"\t-Restaurante: {restaurante.name}\n\t\tProducto: {producto_verificar.name}\n\t\tStock: {producto_verificar.stock}  \n\t\tPrecio: {producto_verificar.price}$\n")
                                    impresion_restaurante=False
                                else:
                                    print(f"\t\tProducto: {producto_verificar.name}\n\t\tStock: {producto_verificar.stock}  \n\t\tPrecio: {producto_verificar.price}$\n")
                elif criterio=="3": #Busca por rango de precio
                    #El usuario indica dos números separados por "-", el primero debe ser menor. Luego imprime un resumen de los productos que entren en ese rango y su ubicación.
                    rango=informacion.split("-")
                    if producto_verificar.price <= float(rango[1]) and producto_verificar.price >= float(rango[0]) :
                            if impresion_estadio:
                                print(f"Estadio: {estadio.name}\n")
                                impresion_estadio=False
                                producto_encontrado=True
                                impresion_restaurante=False 
                                print(f"\t-Restaurante: {restaurante.name} \n\t\tProducto: {producto_verificar.name}\n\t\tStock: {producto_verificar.stock}  \n\t\tPrecio: {producto_verificar.price}$\n")
                            else:
                                if impresion_restaurante:
                                    print(f"\t-Restaurante: {restaurante.name}\n\t\tProducto: {producto_verificar.name}\n\t\tStock: {producto_verificar.stock}  \n\t\tPrecio: {producto_verificar.price}$\n")
                                    impresion_restaurante=False
                                else:
                                    print(f"\t\tProducto: {producto_verificar.name}\n\t\tStock: {producto_verificar.stock}  \n\t\tPrecio: {producto_verificar.price}$\n")
    if not producto_encontrado:
        print("Producto no encontrado")

def realizar_busquedas(inventario_estadios):
     while True:
        #Esta función se encarga de desplegar el menú de búsqueda y realizar validaciones.
        print("\n--------- Módulo de Búsqueda de Productos ---------\n")
        tipo_de_busqueda=input("Seleccione el criterio de búsqueda: \n\t1-Nombre\n\t2-Tipo\n\t3-Rango de precios\n\t4-Salir\n- ")
        try:
            if not tipo_de_busqueda.isnumeric() or int(tipo_de_busqueda) not in range(1,5):
                print("Introduzca una opción valida")
                continue
        except:
            print("Introduzca una opción valida")
            continue
        if tipo_de_busqueda=="1":
            while True:
                
                nombre_producto=input("Indique el nombre del producto: ")
                if not nombre_producto.isalpha():
                    print("Introduzca un nombre válido, solo con letras")
                break
            buscar_producto_restaurante(inventario_estadios,tipo_de_busqueda,nombre_producto)
        if tipo_de_busqueda=="2":
            while True:
                tipo_producto=input("Indique el tipo de producto: \n\t1-Alimento\n\t2-Bebida\n- ")
                if tipo_producto not in ["1","2"]:
                    print("Introduzca una opción válida")
                    continue
                break
            buscar_producto_restaurante(inventario_estadios,tipo_de_busqueda, tipo_producto)
        if tipo_de_busqueda=="3":
            while True:
                rango=input("Introduzca el rango de precios en el siguiente formato x-y: ")
                try:
                    if rango.replace("-","").replace(".","",2).isnumeric():
                        if float(rango.split("-")[0])<=float(rango.split("-",)[1]):
                            break
                        else:
                            print("El valor x debe ser menor que y")
                            continue
                    print("Introduce unicamente números")
                    continue
                except:
                    print("Emplea el formato señalado")
            buscar_producto_restaurante(inventario_estadios,tipo_de_busqueda, rango)
        if tipo_de_busqueda=="4":
            break