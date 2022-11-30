from Equipo import Equipo
from Restaurante import Restaurante
from Producto import Producto, Alimento, Bebida
from Estadio import Estadio
from Partido import Partido
from Cliente import Cliente
from Entrada import EntradaGeneral, EntradaVIP
from Venta import Compra, Venta
import requests
cargado_guardado=None
#Estas funciones se encargan de inicializar el programa, ya sea desde el guardado o la API
#Los inicializadores toman la lista guardada correspondiente y trasnforman esos datos a objetos.
#Hay un orden de armado específico, primero los partidos, luego los estadios y luego los partidos para poder añadir estos objetos como referencias a otros.
def inicializar_codigos_usados(cargado_guardado):
    codigos_usados=cargado_guardado[0]
    return codigos_usados
def inicializar_equipos(cargado_guardado):
    equipos=cargado_guardado[1]
    equipos_objetos=[]
    for equipo in equipos:
        equipos_objetos.append(Equipo(equipo["name"],equipo["flag"],equipo["fifa_code"],equipo["group"],equipo["id"]))
    return equipos_objetos
def inicializar_estadios(cargado_guardado):
    estadios_objetos=[]
    estadios=cargado_guardado[2]
    for estadio in estadios:
        restaurantes=[]
        for restaurante in estadio["restaurants"]:
            productos=[]
            for producto in restaurante["products"]:
                if producto["tipo"]=="Alimento":
                    producto_objeto=Alimento(producto["name"],producto["net_price"],producto["stock"],producto["forma_consumo"])
                    productos.append(producto_objeto)
                else:
                    producto_objeto=Bebida(producto["name"],producto["net_price"],producto["stock"],producto["alcohol"])
                    productos.append(producto_objeto)
            restaurantes.append(Restaurante(restaurante["name"], productos))
        estadios_objetos.append(Estadio(estadio["id"], estadio["name"], estadio["capacity"], estadio["location"], restaurantes))
    return estadios_objetos


def inicializar_partidos(cargado_guardado,estadios, equipos, codigos_usados):
    partidos=cargado_guardado[3]
    partidos_objetos=[]
    for partido in partidos:
        estadio_del_partido=None
        equipo_visitante=None
        equipo_local=None

        for estadio in estadios:
            if estadio.id==partido["stadium"]["id"]:
                estadio_del_partido=estadio
        for equipo in equipos:
            if equipo.name==partido["home_team"]["name"]:
                equipo_local=equipo
            if equipo.name==partido["away_team"]["name"]:
                equipo_visitante=equipo
        
        partido_obj=Partido(equipo_local, equipo_visitante, partido["date"], estadio_del_partido, partido["id"])
        partido_obj.asientos=partido["asientos"]
        for entrada in partido["entradas_asistencia_confirmada"]:
           
            if entrada["tipo"]=="General":
                entrada_objeto=EntradaGeneral(partido_obj.id, entrada["asiento"], codigos_usados , entrada["cedula_comprador"])
                entrada_objeto.codigo=entrada["codigo"]
                partido_obj.entradas_asistencia_confirmada.append(entrada_objeto)
            else:
                entrada_objeto=EntradaVIP(partido_obj.id, entrada["asiento"], codigos_usados , entrada["cedula_comprador"])
                entrada_objeto.gastos=entrada["gastos"]
                entrada_objeto.codigo=entrada["codigo"]
                partido_obj.entradas_asistencia_confirmada.append(entrada_objeto)

        for entrada in partido["entradas_asistencia_no_confirmada"]:
           
            if entrada["tipo"]=="General":
                entrada_objeto=EntradaGeneral(partido_obj.id, entrada["asiento"], codigos_usados , entrada["cedula_comprador"])
                entrada_objeto.codigo=entrada["codigo"]
                partido_obj.entradas_asistencia_no_confirmada.append(entrada_objeto)
            else:
                entrada_objeto=EntradaVIP(partido_obj.id, entrada["asiento"], codigos_usados , entrada["cedula_comprador"])
                entrada_objeto.gastos=entrada["gastos"]
                entrada_objeto.codigo=entrada["codigo"]
                partido_obj.entradas_asistencia_no_confirmada.append(entrada_objeto)
        
        partidos_objetos.append(partido_obj)
    return partidos_objetos
        
def inicializar_clientes(cargado_guardado, partidos):
    clientes=cargado_guardado[4]
    clientes_objetos=[]
    
    for cliente in clientes:
        cliente_objeto=Cliente(cliente["nombre"],cliente["cedula"],cliente["edad"],[])
        for partido in partidos:
            for entrada in partido.entradas_asistencia_confirmada + partido.entradas_asistencia_no_confirmada:
                if entrada.cedula_comprador==cliente_objeto.cedula:
                    cliente_objeto.entradas.append(entrada)
        clientes_objetos.append(cliente_objeto)
    return clientes_objetos

def inicializar_ventas(cargado_guardado):
    ventas=cargado_guardado[5]
    ventas_objetos=[]
    
    for venta in ventas:
        venta_objeto=Venta(venta["producto"],venta["cantidad"])
        ventas_objetos.append(venta_objeto)
    return ventas_objetos
#Los de descarga toman los datos de la API.
def descargar_inventario_equipos(url):
        inventario=[]
        response=requests.get(url)
        if response.status_code==200:
            base_de_datos=response.json()
            try:
                for equipo in base_de_datos:
                    inventario.append(Equipo(equipo["name"], equipo["flag"], equipo["fifa_code"], equipo["group"],equipo["id"]))
            except:
    
                print("Error durante el proceso de carga de datos. Por favor revisar el estado de los servidores, el programa se cerrará")
                return False
        else:
            print("Respuesta no positiva del servidor. No se pudo completar la carga de datos. Codigo de error: ", response.status_code )
            return False
        return inventario

def descargar_inventario_estadios(url):
        inventario=[]
        response=requests.get(url)
        if response.status_code==200:
            base_de_datos=response.json()
            try:
                for estadio_for in base_de_datos:
                    restaurantes=[]
                    for restaurante in estadio_for["restaurants"]:
                        productos=[]
                        for producto in restaurante["products"]:
                            if producto["type"]=="food":
                                productos.append(Alimento(producto["name"], producto["price"], producto["quantity"],producto["adicional"]))
                            else:
                                if producto["adicional"]=="alcoholic":
                                    productos.append(Bebida(producto["name"], producto["price"], producto["quantity"], True))
                                else:
                                    productos.append(Bebida(producto["name"], producto["price"], producto["quantity"], False ))
                        restaurantes.append(Restaurante(restaurante["name"], productos))
                    inventario.append(Estadio(estadio_for["id"], estadio_for["name"], estadio_for["capacity"], estadio_for["location"], restaurantes))
                            
            except:
                print("Error durante el proceso de carga de datos. Por favor revisar el estado de los servidores, el programa se cerrará")
                return False
        else:   
            print("Respuesta no positiva del servidor. No se pudo completar la carga de datos. Codigo de error: ", response.status_code )
            return False
        return inventario

def descargar_inventario_partidos(url, equipos, estadios):
    inventario=[]
    
    response=requests.get(url)
    if response.status_code==200:
        base_de_datos=response.json()
        try:
            for partido in base_de_datos:
                estadio_del_partido=None
                equipo_visitante=None
                equipo_local=None
                for estadio in estadios:
                    if estadio.id==partido["stadium_id"]:
                        estadio_del_partido=estadio
                for equipo in equipos:
                    if equipo.name==partido["home_team"]:
                        equipo_local=equipo
                    if equipo.name==partido["away_team"]:
                        equipo_visitante=equipo

                inventario.append(Partido(equipo_local, equipo_visitante, partido["date"], estadio_del_partido, partido["id"]))
        except:
            print("Error durante el proceso de carga de datos. Por favor revisar el estado de los servidores, el programa se cerrará")
            return False
    else:
        print("Respuesta no positiva del servidor. No se pudo completar la carga de datos. Codigo de error: ", response.status_code )
        return False
    return inventario

def inicializar_productos(inventario_estadios):
    productos=[]
    productos_ya_registrados=[]
    for estadio in inventario_estadios:
        for restaurante in estadio.restaurants:
            for producto in restaurante.products:
                    if producto.name in productos_ya_registrados:
                        continue
                    else:
                        venta_objeto=Venta(producto.name,0)
                        productos.append(venta_objeto)
                        productos_ya_registrados.append(producto.name)
    return productos