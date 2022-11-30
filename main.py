
from json_convertidor import convertir_objeto
from busqueda_partidos import busqueda_partidos 
from busqueda_de_productos import realizar_busquedas
from comprar_entrada import comprar_entrada
from comprar_restaurante import comprar_restaurante
from inicializadores import inicializar_codigos_usados, inicializar_equipos, inicializar_estadios, inicializar_partidos, inicializar_clientes, inicializar_ventas, inicializar_productos, descargar_inventario_equipos, descargar_inventario_estadios,descargar_inventario_partidos
from estadisticas import promedio_gastos, grafico_gastos_vip,tabla_asistencia_partidos,grafico_asistencia_partidos,grafico_venta_productos,grafico_clientes
import os
import json



#En el main se encuentra el menú y algunas opciones principales que no son tan extensas, las funciones más específicas o largas se encuentran en otros archivos.
def main():
    #La primera parte del código se encarga de verificar si el archivo "guardado.txt" existe, de ser así descarga la información de este archivo. Sino, lo hace de la API.
    if os.path.isfile('guardado.txt'): #os sirve para verificar la existencia del archivo.
        cargado_guardado=None
        with open("guardado.txt","r") as f:
            cargado_guardado=json.loads(f.read())
        codigos_usados=inicializar_codigos_usados(cargado_guardado)
        inventario_equipos=inicializar_equipos(cargado_guardado)
        inventario_estadios=inicializar_estadios(cargado_guardado)
        inventario_partidos=inicializar_partidos(cargado_guardado,inventario_estadios, inventario_equipos, codigos_usados)
        lista_clientes=inicializar_clientes(cargado_guardado,inventario_partidos)
        productos_vendidos=inicializar_ventas(cargado_guardado)
    else:
        #Si no encontró el archivo, descarga los datos con ayuda de la API. 
        lista_clientes=[]
        codigos_usados=[]
        inventario_equipos= sorted(descargar_inventario_equipos("https://raw.githubusercontent.com/Algoritmos-y-Programacion-2223-1/api-proyecto/main/teams.json"), key=lambda x: int(x.id))
        inventario_estadios= sorted(descargar_inventario_estadios("https://raw.githubusercontent.com/Algoritmos-y-Programacion-2223-1/api-proyecto/main/stadiums.json"), key=lambda x: x.id)      
        inventario_partidos= sorted(descargar_inventario_partidos("https://raw.githubusercontent.com/Algoritmos-y-Programacion-2223-1/api-proyecto/main/matches.json",inventario_equipos, inventario_estadios), key=lambda x: int(x.id))
        productos_vendidos=inicializar_productos(inventario_estadios)
    print("Bienvenido al Sistema de Qatar 2022. A continuación seleccione una opción del menú \n")
    while True:
        #Se presenta el Menú
        print("\n************** Qatar 2022 **************")
        eleccion_menu= input("1-Realizar una búsqueda de partidos \n2-Comprar entradas\n3-Entrar a un partido\n4-Entrar a un restaurante\n5-Buscar productos en restaurantes\n6-Revisar estadísticas\n7-Reiniciar datos del sistema\n8-Cerrar Programa \n- ")

            #Cada opción del menú se encarga de llamar a la función destinada a cumplir con la orden señalada en eleccion_menu o directamente presenta el código para tal utilidad
        if eleccion_menu=="1":
            
            busqueda_partidos(inventario_equipos, inventario_estadios, inventario_partidos)
        
        elif eleccion_menu=="2":
            comprar_entrada(inventario_partidos,codigos_usados,lista_clientes)

        elif eleccion_menu=="3":
            while True:
                #Para validar una entrada, el cliente elije el partido y posteriormetne puede ingresar el código de su entrada.
                partido_ejecutandose= None
                print("\nA continuación los partidos disponibles: \n")
                for partido in inventario_partidos:
                    partido.mostrar_informacion()
                while True:
                    id_partido_seleccionado=input("\nIndique el Id del partido al que desea asistir: ")
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
                    entrada_valida=False
                    entrada_usada=False
                    codigo_validar=input("\nPara confirmar asistencia al partido, indique el código de su boleto a continuación o marque x para salir: ")
                    #Primero se valida que no tenga caracteres especiales, luego si hay una entrada con el mismo código en la lista de entradas no usadas de cada partido.
                    if not codigo_validar.isalnum():
                        print("El codigo debe ser alphanumérico")
                        continue
                    if codigo_validar=="x":
                        break
                    for entrada in partido_ejecutandose.entradas_asistencia_confirmada:
                        if entrada.codigo==codigo_validar:
                            print("El codigo corresponde a una entrada ya usada")
                            entrada_valida=True
                            entrada_usada=True
                    #Si el código es válido, el objeto entrada en cuestión pasa a la lista de entradas usadas y es eliminada de las no usadas.
                    if not entrada_usada:
                        for entrada in partido_ejecutandose.entradas_asistencia_no_confirmada:
                            if entrada.codigo==codigo_validar:
                                print("Entrada Valida. Su asistencia ha sido confirmada")
                                entrada_valida=True
                                partido_ejecutandose.entradas_asistencia_confirmada.append(entrada)
                                partido_ejecutandose.entradas_asistencia_no_confirmada.remove(entrada)
                   
                    if not entrada_valida:
                        print("El codigo no existe: ")
                        continue
                break
        elif eleccion_menu=="4":
                comprar_restaurante(inventario_partidos,lista_clientes,productos_vendidos)
                    
        elif eleccion_menu=="5":
            realizar_busquedas(inventario_estadios)
        elif eleccion_menu=="6":
            while True:
                opcion_estadistica=input("\nBienvenido al sistema de estadísticas. Indique la estadística que desea conocer: \n\t1-Promedio de gastos de un cliente Vip\n\t2-Tabla de asistencia a partidos\n\t3-Partido con mayor asistencia\n\t4-Partido con más boletos vendidos\n\t5-Productos más vendidos\n\t6-Mejores clientes\n\t7-Ver gráficos\n\t8-salir\n- ")
                if opcion_estadistica not in ["1","2","3","4","5","6","7","8"]:
                    print("Introduce una opción valida")
                    continue
                if opcion_estadistica =="8":
                    break
                elif opcion_estadistica=="1":
                    promedio=promedio_gastos(lista_clientes)
                    if not promedio:
                        print("No hay clientes VIP por los momentos")
                        continue
                    else:
                        print(f"\nEl promedio de gastos de un cliente VIP es {round(promedio,2)}$")
                  
                elif opcion_estadistica=="2":
                    print("\nA continuación la tabla de datos: \n")
                    df=tabla_asistencia_partidos(inventario_partidos)
                    print(df)
                    
                elif opcion_estadistica=="3":
                    #Se ordena la lista de partidos según el tamaño de su lista de entradas ya usadas.
                    inventario_ordenado_partidos=sorted(inventario_partidos,key=lambda x: len(x.entradas_asistencia_confirmada), reverse=True)
                    if len(inventario_ordenado_partidos[0].entradas_asistencia_confirmada)==0:
                        print("No hay asistencia confirmada para ningún partido")
                        continue
                    print(f"\n El partido con mayor asistencia es: \n")
                    inventario_ordenado_partidos[0].mostrar_resumen()
                elif opcion_estadistica=="4":
                    #Se ordena la lista de partidos según el tamaño de su lista de entradas ya usadas más el de la lista de no usadas.
                    print(f"\n El partido con mayores ventas es: \n")
                    inventario_ordenado_partidos=sorted(inventario_partidos,key=lambda x: len(x.entradas_asistencia_no_confirmada)+len(x.entradas_asistencia_confirmada), reverse=True)
                    if len(inventario_ordenado_partidos[0].entradas_asistencia_confirmada)+len(inventario_ordenado_partidos[0].entradas_asistencia_no_confirmada)==0:
                        print("No hay ventas registradas para ningún partido")
                        continue
                    inventario_ordenado_partidos[0].mostrar_resumen()
                elif opcion_estadistica=="5":
                    #Se ordena la lista de ventas según la cantidad de cada producto vendido. Hay que resaltar que la lista tiene un elemento por cada producto existente.
                    productos_vendidos_ordenados=sorted(productos_vendidos,key=lambda x: x.cantidad, reverse=True)
                    if productos_vendidos_ordenados[0].cantidad==0:
                        print("No se han registrado ventas")
                        continue
                    print("\nLos productos más vendidos son: ")
                    contador=1
                    for compra in productos_vendidos_ordenados[0:3]:
                        if compra.cantidad==0:
                            continue
                        print(f"{contador}",end="")
                        compra.mostrar_resumen()
                        contador+=1
                elif opcion_estadistica=="6":
                    #Se ordena la lista de clientes según el tamaño de su lista de entradas.
                    lista_clientes_ordenada=sorted(lista_clientes,key=lambda x: len(x.entradas), reverse=True)
                    if len(lista_clientes_ordenada)==0:
                        print("No hay clientes registrados")
                        continue
                    for cliente in lista_clientes_ordenada[0:3]:
                        cliente.resumen()
                elif opcion_estadistica=="7":
                    while True:
                        #En este apartado se llaman a las funciones para mostrar los gráficos
                        opcion_grafico=input("\nIndique el tipo de gráfico que desea ver: \n\t1-Promedio de gastos de un cliente VIP por partido\n\t2-Asistencia y boletos vendidos por partido\n\t3-Ventas de productos\n\t4-Entradas por cliente\n\t5-Salir\n- ")
                        if opcion_grafico=="1":
                            grafico_gastos_vip(lista_clientes)
                        elif opcion_grafico=="2":
                            grafico_asistencia_partidos(inventario_partidos)
                        elif opcion_grafico=="3":
                            grafico_venta_productos(productos_vendidos)
                        elif opcion_grafico=="4":
                            if len(lista_clientes)==0:
                                print("No hay clientes registrados")
                                continue
                            grafico_clientes(lista_clientes)
                        elif opcion_grafico=="5":
                            break
                        else:
                            print("Opción no válida")
                        
        elif eleccion_menu=="7":
            #En este apartado se reestablecen los valores de las listas usadas como inventario, volviendo a descargar los datos de la API y limpiando el contenido de las demás listas
            lista_clientes=[]
            codigos_usados=[]
            inventario_equipos= sorted(descargar_inventario_equipos("https://raw.githubusercontent.com/Algoritmos-y-Programacion-2223-1/api-proyecto/main/teams.json"), key=lambda x: int(x.id))
            inventario_estadios= sorted(descargar_inventario_estadios("https://raw.githubusercontent.com/Algoritmos-y-Programacion-2223-1/api-proyecto/main/stadiums.json"), key=lambda x: x.id)      
            productos_vendidos=inicializar_productos(inventario_estadios)
            inventario_partidos= sorted(descargar_inventario_partidos("https://raw.githubusercontent.com/Algoritmos-y-Programacion-2223-1/api-proyecto/main/matches.json",inventario_equipos, inventario_estadios), key=lambda x: int(x.id))
            print("Datos reiniciados exitosamente")
            continue
        elif eleccion_menu=="8":
            print("\nHasta luego. Vuelva Pronto")
            guardado=[codigos_usados, inventario_equipos, inventario_estadios, inventario_partidos, lista_clientes, productos_vendidos]
            with open("guardado.txt","w") as f:
                #Con esto se conviernten los objetos en diccionarios y se guarda esta información como caracteres en un txt
                f.write(json.dumps(guardado,default=convertir_objeto))
                #El "default" del método permite convertir automaticamente en diccionario los objetos que se encuentran dentro de otros objetos.
            break
        
        else:
            print("Opción no válida. Selecciona algo del menú")
            continue



                    

            
                

    
main()     