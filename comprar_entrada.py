from Cliente import Cliente
from Entrada import EntradaGeneral, EntradaVIP
from descuento import descuento_entradas
#Esta sección se encarga de todo el módulo 2
def comprar_entrada(inventario_partidos,codigos_usados,lista_clientes):
    print("¡Haz tomado la mejor decisión de tu vida! \n")
    compra_cancelada=False
    partido_seleccionado=None
    cantidad_entradas_vip=0
    cantidad_entradas_generales=0
    puestos_seleccionados=[]
    entradas_compradas=[]
    #Se solicitan los datos del cliente, si su cédula ya está en la base de datos, pasa directamente a la compra.
    while True:
        cedula=input("Introduce los siguientes datos para continuar con la compra: \n\t-Cedula: ")
        if cedula.isnumeric():
            break
        else: 
            print("Tu cedula debe estar compuesta solo por numeros")
    cliente_nuevo=True
    for cliente in lista_clientes:
        if cliente.cedula==cedula:
            print(f"Bienvenido de nuevo {cliente.nombre}")
            cliente_nuevo=False
            nombre=cliente.nombre
            edad=cliente.edad
    if cliente_nuevo:
        while True:
            nombre=input("\t-Nombre: ")
            if nombre.replace(" ", "").isalpha():
                break
            else: 
                print("Tu nombre no puede contener números ni caracteres no alphabéticos")
        while True:
            edad=input("\t-Edad:")
            if edad.isnumeric():
                if int(edad) in range(14,130) and int(edad)==float(edad):
                    break 
                if int(edad) < 14:
                    print("Debes tener al menos 14 años para comprar una entrada")
                    continue
            print("Tu edad debe contener solo números enteros y encontrarse en un rango coherente")

    print(" \n")
    #Selecciona el partido al que desea asistir, el tipo de entrada y la cantidad
    print("Seleccione el id de uno de los partidos a continuación: \n")
    for partido in inventario_partidos:
        partido.mostrar_informacion()
    while True:
        id_partido_seleccionado=input("Indique el Id del partido al que desea asistir: ")
        try:
            if int(id_partido_seleccionado) not in range(1, len(inventario_partidos)+1):
                print("Opcion no valida")
                continue
        except:
            print("Opcion no valida")
            continue
        for partido in inventario_partidos:
            if int(partido.id)==int(id_partido_seleccionado):
                partido_seleccionado=partido
        while True:
            tipo_de_entrada= input("Seleccione el tipo de entrada: \n\t1-General 50$\n\t2-VIP 120$\n- ")
            try:
                if int(tipo_de_entrada) not in range(1,3):
                    print("Opcion no valida")
                    continue
            except:
                print("Opcion no valida")
                continue
            cantidad_de_entradas=input("Introduce cuantas entradas quieres: ")
            if not cantidad_de_entradas.isnumeric() or int(cantidad_de_entradas)!=float(cantidad_de_entradas):
                print("Introduce un valor válido")
                continue
            if tipo_de_entrada=="1":
                asientos_disponibles=partido_seleccionado.asientos[:int(partido_seleccionado.stadium.capacity[0]/10)]
                contador=0
                for fila in asientos_disponibles:
                    contador+=fila.count(False)
                if int(cantidad_de_entradas)+cantidad_entradas_generales > contador:
                    print("No hay suficientes asientos de ese tipo disponibles")
                    continue
            else:
                asientos_disponibles=partido_seleccionado.asientos[int(partido_seleccionado.stadium.capacity[0]/10):]
                contador=0
                for fila in asientos_disponibles:
                    contador+=fila.count(False)
                if int(cantidad_de_entradas)+cantidad_entradas_vip > contador:
                    print("No hay suficientes asientos de ese tipo disponibles")
                    continue
            if tipo_de_entrada=="1":
                cantidad_entradas_generales+=int(cantidad_de_entradas)
            else:
                cantidad_entradas_vip+=int(cantidad_de_entradas)
            while True:
                comprar_mas_entradas=input("¿Desea comprar más entradas? s/n: ")
                if comprar_mas_entradas.lower() not in ["s","n"]:
                    print("Opcion no valida")
                    continue
                else:
                    break
            if comprar_mas_entradas=="s": 
                continue
            break
            
            
        print("Proceda a selecionar sus asientos: ")
        
        #Se imprime un mapa del estadio con filas y columnas numeradas. La parte de abajo del estadio está reservada para los VIP. Primero selecciona sus asientos generales y luego VIP.
        partido_seleccionado.imprimir_mapa()
        while True:
            validador_asientos_generales=False
            if cantidad_entradas_generales!=0:
                #El cliente debe indicar la fila seguida de la columna y se valida que esta combinación exista
                preselecion_asientos=input("Introduzca los asientos para las entradas generales separados por espacios simples con el siguient formato fila-columna: ")
                try:
                    
                    if not preselecion_asientos.replace(" ","").replace("-","").isnumeric():
                        print("Introduce unicamente números en el formato señalado")
                        continue

                    for asiento in preselecion_asientos.split(" ") :
                        asiento_dividido=asiento.split("-")
                        
                        if int(asiento_dividido[0]) not in range(1,len(partido_seleccionado.asientos)+1) or int(asiento_dividido[1]) not in range(1,len(partido_seleccionado.asientos[0])+1):
                            print("El codigo de asiento no es válido")
                            validador_asientos_generales=True
                            break
                        if int(asiento_dividido[0]) not in range(1,int(partido_seleccionado.stadium.capacity[0]/10)+1):
                            print("Debes selecionar un asiento general")
                            validador_asientos_generales=True
                            break
                        if partido_seleccionado.asientos[int(asiento_dividido[0])-1][int(asiento_dividido[1])-1] or asiento in puestos_seleccionados:
                            print("Hay al menos un asiento ya ocupado")
                            validador_asientos_generales=True
                        
                            break
                except:
                    print("Seleccione códigos de asiento válidos")
                    continue
                if validador_asientos_generales:
                    continue
                if len(preselecion_asientos.split(" "))!=len(set(preselecion_asientos.split(" "))):
                    print("Debes seleccionar asientos distintos")
                    continue
                if len(preselecion_asientos.split(" "))!=cantidad_entradas_generales:
                    print(f"Debes seleccionar {cantidad_entradas_generales} asientos: ")
                    continue
                #Si el formato es válido, se crea una "Entrada" para posteriomente añadirla al cliente.
                for puesto_verificado in preselecion_asientos.split(" "):
                    puestos_seleccionados.append(puesto_verificado)
                    entradas_compradas.append(EntradaGeneral(partido_seleccionado.id,puesto_verificado,codigos_usados,cedula))
            break
        while True:
            validador_asientos_vip=False
            if cantidad_entradas_vip!=0:
                preselecion_asientos=input("Introduzca los asientos para las entradas VIP separados por espacios simples en el formato fila-columna: ")
                try:
                    if not preselecion_asientos.replace(" ","").replace("-","").isnumeric():
                        print("Introduce unicamente números en el formato señalado")
                        continue
                    for asiento in preselecion_asientos.split(" ") :
                        asiento_dividido=asiento.split("-")
                        if int(asiento_dividido[0]) not in range(1,len(partido_seleccionado.asientos)+1) or int(asiento_dividido[1]) not in range(1,len(partido_seleccionado.asientos[0])+1):
                            print("El codigo de asiento no es válido")
                            validador_asientos_vip=True
                            break
                        if int(asiento_dividido[0]) not in range(int(partido_seleccionado.stadium.capacity[0]/10)+1,len(partido_seleccionado.asientos)+1):
                            print("Debes selecionar un asiento VIP")
                            validador_asientos_vip=True
                            break
                        if  partido_seleccionado.asientos[int(asiento_dividido[0])-1][int(asiento_dividido[1])-1] or asiento in puestos_seleccionados:
                            print("Hay al menos un asiento ya ocupado")
                            validador_asientos_vip=True
                            break
                except:
                    print("Seleccione códigos de asientos válidos")
                    continue
                if validador_asientos_vip:
                    continue
                if len(preselecion_asientos.split(" "))!=len(set(preselecion_asientos.split(" "))):
                    print("Debes seleccionar asientos distintos")
                    continue
                if len(preselecion_asientos.split(" "))!=cantidad_entradas_vip:
                    print(f"Debes seleccionar {cantidad_entradas_vip} asientos: ")
                    continue
                #Si el formato es válido, se crea una "Entrada" para posteriomente añadirla al cliente.
                for puesto_verificado in preselecion_asientos.split(" "):
                    puestos_seleccionados.append(puesto_verificado)
                    entradas_compradas.append(EntradaVIP(partido_seleccionado.id,puesto_verificado,codigos_usados,cedula))
            break

        subtotal=0
        #Cada entrada tiene un atributo precio, se suman, se halla el descuento y luego se le agrega el IVA.
        for entrada in entradas_compradas:
            subtotal+=entrada.precio
        descuento_compra=descuento_entradas(cedula, subtotal)
        iva=(subtotal-descuento_compra)*0.16
        
        total=subtotal+iva-descuento_compra
        #Se imprime la factura
        print("Selección exitosa. A continuación su factura \n")
        print("**********************Factura**********************")
        print(f"Nombre: {nombre} \nCedula: {cedula} \nEdad: {edad} \nID del Partido: {id_partido_seleccionado}         Fecha: {partido_seleccionado.date} ")
        print("Entradas: \n")
        for entrada in entradas_compradas:
            entrada.mostrar_resumen()
        print("---------------------------------------------------")
        print(f"subtotal:\t\t\t\t{subtotal} \nIVA:\t\t\t\t\t{iva} \nDescuento:\t\t\t\t{descuento_compra} \nTotal:\t\t\t\t\t{total}")
        if descuento_compra:
            print("¡Obtuviste un descuento porque tu cedula es un número vampiro!")
        print("---------------------------------------------------")

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
       #Esta parte del código se encarga de crear el cliente y actualizar los asientos para registrarlos como ocupados.
        for asiento in puestos_seleccionados:
            fila_columna=asiento.split("-")
            partido_seleccionado.asientos[int(fila_columna[0])-1][int(fila_columna[1])-1]=True
        cliente_no_registrado=True
        for entrada in entradas_compradas:
            partido_seleccionado.entradas_asistencia_no_confirmada.append(entrada)
            codigos_usados.append(entrada.codigo)
        for cliente in lista_clientes:
            if cedula==cliente.cedula:
                for entrada in entradas_compradas:
                    cliente.entradas.append(entrada)
                    cliente_no_registrado=False
        if cliente_no_registrado:
            lista_clientes.append(Cliente(nombre,cedula,int(edad),entradas_compradas))
        break