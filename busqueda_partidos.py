def busqueda_partidos(inventario_equipos, inventario_estadios, inventario_partidos):
    while True:
        #Esta función contiene al menú de búsqueda de partidos.
        print("\n--------- Módulo de Búsqueda de Partidos ---------\n")
        eleccion_busqueda= input("Elija un método de búsqueda:\n\t1-Pais\n\t2-Estadio\n\t3-Fecha\n\t4-Salir \n- ")
        if eleccion_busqueda=="1":
            #Búsqueda por equipo. Como hay muchos equipos, se muestra un menú de los mismos para que el cliente elija. Luego se busca su id en la base de datos.
            print("A continuación los equipos participantes:\n ")
            for equipo in inventario_equipos:
                print(f"{equipo.id}-{equipo.name}")
            while True:
                equipo_a_buscar=input("\n Indique el id del equipo o introduzca x para volver al menu: ")
                if equipo_a_buscar=="x":
                    break
                if not equipo_a_buscar.isnumeric() or int(equipo_a_buscar)!=float(equipo_a_buscar) or (int(equipo_a_buscar) not in range(1,len(inventario_equipos)+1)):
                    print("Introduce un id válido. Asegúrate que sea un entero positivo")
                    continue
                for partido in inventario_partidos: 
                    if partido.home_team.id==equipo_a_buscar or partido.away_team.id==equipo_a_buscar:
                        partido.mostrar_informacion()
        if eleccion_busqueda=="2":
            #Como en la opción anterior, se muestra un resumen de los estadios y luego se busca el id seleccionado en la base de datos.
            print("A continuación los estadios disponibles:\n ")
            for estadio in inventario_estadios:
                print(f"{estadio.id}-{estadio.name}")
            while True:
                estadio_a_buscar=input("\nIndique el id del estadio o introduzca x para volver al menu: ")
                if estadio_a_buscar=="x":
                    break
                if not estadio_a_buscar.isnumeric() or int(estadio_a_buscar)!=float(estadio_a_buscar) or (int(estadio_a_buscar) not in range(1,len(inventario_estadios)+1)):
                    print("Introduce un id válido. Asegúrate que sea un entero positivo")
                    continue
                for partido in inventario_partidos: 
                    if partido.stadium.id==int(estadio_a_buscar):
                        partido.mostrar_informacion()
        

        if eleccion_busqueda=="3":
            #Se muestra un resumen de las fechas disponibles y el usuario escribe la fecha que desea consultar.
            while True:
                lista_fechas=set()
                partido_encontrado=False
                for partido in inventario_partidos:
                    division=partido.date.split(" ")
                    lista_fechas.add(division[0])
                print("\nA continuación las fechas disponibles")
                for fecha in sorted(lista_fechas):
                    print(f"-{fecha}")
                fecha_a_buscar=input("\nIndique la fecha del partido en el siguiente formato MM/DD/YYYY o introduzca x para volver al menu: ")
                if fecha_a_buscar=="x":
                    break
                if not fecha_a_buscar.replace("/","").isnumeric() or fecha_a_buscar.count("/")!=2:
                    print("Introduce el formato adecuado")
                    continue
                inventario_ordenado=sorted(inventario_partidos, key=lambda x:x.date)
                for partido in inventario_ordenado: 
                    if fecha_a_buscar in partido.date:
                        partido.mostrar_informacion()
                        partido_encontrado=True
                if not partido_encontrado:
                    print("No hay partidos en esa fecha")
        if eleccion_busqueda=="4":
            break
        else:
            print("Introduce una opción válida del menú")