import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
#Estas funciones están dedicadas a las estadísticas y los gráficos
def promedio_gastos(lista_clientes,diccionario=[]):
    #El código busca las entradas vip de cada cliente y las compara con las existentes para cada partido. Si pertenecen a un mismo partido y dueño, entonces sus gastos se suman.
    acumulador=0
    gastos_clientes_vip=[]
    for cliente in lista_clientes:
        for entrada in cliente.entradas:
            if entrada.vip==True:
                gastos_clientes_vip.append(entrada)
    lista_indices=[]
    for entrada_vip in gastos_clientes_vip:
        if gastos_clientes_vip.index(entrada_vip) in lista_indices:
            continue
        acumulador+=entrada_vip.gastos
        for entrada_vip_2 in gastos_clientes_vip:
            if entrada_vip.partido_id==entrada_vip_2.partido_id and entrada_vip.cedula_comprador==entrada_vip_2.cedula_comprador and entrada_vip!=entrada_vip_2:
                acumulador+=entrada_vip_2.gastos
                lista_indices.append(gastos_clientes_vip.index(entrada_vip_2))
    #Se sacan las entradas VIP que sean de un mismo dueño en cada partido, se deja una sola. Un cliente cuenta como 1 aunque tenga varias entradas para un mismo partido.
    for i in lista_indices[::-1]:
        gastos_clientes_vip.pop(i)
        
        
    if len (gastos_clientes_vip)==0:
        return 0
    promedio=acumulador/len(gastos_clientes_vip)
    #Se saca el promedio entre los gastos con las entradas de clientes y partidos diferentes.
    for entrada_vip in gastos_clientes_vip:
        gasto=entrada_vip.gastos
        for cliente in lista_clientes:
            if cliente.cedula==entrada_vip.cedula_comprador:
                for entrada_cliente in cliente.entradas:
                    if entrada_cliente.partido_id == entrada_vip.partido_id and entrada_vip!=entrada_cliente and entrada_cliente.vip:
                        gasto+=entrada_cliente.gastos
        cliente_partido=f"{entrada_vip.partido_id}-{entrada_vip.cedula_comprador}"

        diccionario.append({"Id partido-CI Cliente":cliente_partido, "Gastos":gasto})
    return promedio

def grafico_gastos_vip(lista_clientes):
    if len(lista_clientes)==0:
        print("No hay clientes registrados")
        return None
    #Esto aplica para todos los gráficos. Se contruye una tabla en Pandas de los inventarios respectivos y luego el gráfico con ayuda de matplotlib.
    clientes_diccionario=[]
    promedio=promedio_gastos(lista_clientes,diccionario=clientes_diccionario)
    gastos_clientes_vip=[]
    fig = plt.figure()
    fig.clf()
    ax = fig.subplots(1,1)
    df=pd.DataFrame(clientes_diccionario)
    ax.scatter( x=df["Id partido-CI Cliente"], y=df["Gastos"])
    for x, y in zip(range(0,len(df["Id partido-CI Cliente"])), df["Gastos"]):
        ax.text(x+0.05, y + 0.05, round(y,1), ha='center', va= 'bottom')
    ax.plot([0,len(gastos_clientes_vip)+1.05], [round(promedio,2),round(promedio,2)], label="Promedio")
    ax.text((len(df["Id partido-CI Cliente"])-1)/2, promedio-0.05, round(promedio,2), ha='center', va= 'bottom' ) #Todo esto es solo para ajustar la apariencia de la tabla
    fig.legend(loc='lower right', frameon=False)
    fig.tight_layout()
    ax.set_xlabel("ID Partido - CI Cliente")
    ax.set_ylabel("Gastos($)")
    fig.show()

def tabla_asistencia_partidos(inventario_partidos):
    #Se ordena el inventario de partidos según la asistencia, se convierte en diccionario y luego en una tabla en pandas y se imprime
    inventario_ordenado_partidos=sorted(inventario_partidos,key=lambda x: len(x.entradas_asistencia_confirmada), reverse=True)
    inventario_en_diccionario=[]
    for partido in inventario_ordenado_partidos:
        nombre=f"{partido.home_team.name} Vs. {partido.away_team.name}"
        estadio=partido.stadium.name
        boletos_vendidos=len(partido.entradas_asistencia_no_confirmada)+len(partido.entradas_asistencia_confirmada)
        asistencia=len(partido.entradas_asistencia_confirmada)
        try:
            relacion=len(partido.entradas_asistencia_confirmada)/(len(partido.entradas_asistencia_no_confirmada)+len(partido.entradas_asistencia_confirmada))
        except:
            relacion=0
        inventario_en_diccionario.append({"Partido L/V":nombre, "Estadio": estadio, "Boletos Vendidos": boletos_vendidos, "Asistentes": asistencia, "Relación asistencia/venta": relacion})
    
    df=pd.DataFrame(inventario_en_diccionario,index=np.arange(1,len(inventario_en_diccionario)+1))
    return df
def grafico_asistencia_partidos(inventario_partidos):
    df=tabla_asistencia_partidos(inventario_partidos)
    df.plot(kind="bar", x="Partido L/V", y=["Boletos Vendidos","Asistentes"], position= 1,fontsize= 8,title="Grafica de Asistencia y Ventas por Partido", ylabel="Ventas-Asitentes", yticks=range(0,max(df["Boletos Vendidos"]+1)), rot=90)
    plt.gcf().subplots_adjust(bottom=0.25)
    plt.show()



    
def grafico_venta_productos(productos_vendidos):
    #Sigue la misma lógica que el gráfico antes explicado
    lista_dict_productos=[]
    productos_ordenados=sorted(productos_vendidos, key=lambda x: x.cantidad, reverse=True)
    for producto in productos_ordenados:
        lista_dict_productos.append(producto.__dict__)
    
    fig = plt.figure()
    fig.clf()
    ax = fig.subplots(1,1)
    df=pd.DataFrame(lista_dict_productos)
    ax.bar(df["producto"], df["cantidad"])
    for x, y in zip(range(0,len(df["producto"])), df["cantidad"]):
        ax.text(x+0.05, y + 0.05, y, ha='center', va= 'top')
    
    fig.legend(loc='lower right')
    fig.tight_layout()
    ax.set_xlabel("Productos")
    ax.set_ylabel("Unidades Vendidas")
    fig.show()
    
def grafico_clientes(lista_clientes):
    #Sigue la misma lógica que el gráfico antes explicado
    lista_ordenada=sorted(lista_clientes, key=lambda x: len(x.entradas),reverse=True)
    lista_dic=[]
    for cliente in lista_ordenada:
        lista_dic.append(cliente.__dict__)
    df=pd.DataFrame(lista_dic)
    fig = plt.figure()
    fig.clf()
    ax = fig.subplots(1,1)
    columna=[]
    for entradas_totales in df["entradas"]:
        columna.append(len(entradas_totales))
    ax.bar(df["cedula"], columna)
    fig.show()
    for x, y in zip(range(0,len(df["cedula"])), df["entradas"]):
        ax.text(x, len(y) + 0.05, len(y), ha='center', va= 'top')
    
    fig.legend(loc='lower right')
    fig.tight_layout()
    ax.set_xlabel("Cedula del Comprador")
    ax.set_ylabel("Entradas Compradas")
    plt.gcf().subplots_adjust(bottom=0.25)
    fig.show()