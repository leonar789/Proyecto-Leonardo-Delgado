
import pandas as pd
import numpy as np

#La clase de partido incluye los asientos en forma de matriz, para saber si estan ocupados o no.
#También las entradas para ese partido, para así poder llevar las estadísticas por partido.
class Partido:
    
    def __init__(self, home_team, away_team, date, stadium, id):
        self.home_team=home_team
        self.away_team=away_team
        self.date=date
        self.stadium=stadium
        self.asientos=self.asientos_generador(self.stadium)
        self.id=id
        self.entradas_asistencia_confirmada=[]
        self.entradas_asistencia_no_confirmada=[]
    def mostrar_informacion(self):
        print(f"\n-Id del partido: {self.id}\n\tEquipo Local: {self.home_team.name}\n\tEquipo Visitante: {self.away_team.name}\n\tFecha: {self.date}\n\tEstadio: {self.stadium.name}")
    def asientos_generador(self,estadio):
        #Genera una matriz con los asientos disponibles. Un False en la posicion del asiento indica que está libre
        capacity=estadio.capacity
        asientos=[]
        for i in range(1,int(capacity[0]/10)+1):
            columnas=[]
            for j in range(10):
                columnas.append(False)
            asientos.append(columnas)
        for i in range(1,int(capacity[1]/10)+1):
            columnas=[]
            for j in range(10):
                columnas.append(False)
            asientos.append(columnas)
        return asientos
    def imprimir_mapa(self):
        #Crea filas y columnas numeradas. Luego crea una tabla en Pandas para imprimir bonito el estadio
        columnas=np.arange(1,11).flatten().tolist()
        for i, j in enumerate(columnas):
            if i<9:
                columnas[i]=f"- {str(i+1)} - " 
            else:
                columnas[i]=f"- {str(i+1)} -"

        filas=np.arange(1,int((self.stadium.capacity[0]+self.stadium.capacity[1])/10)+1).flatten().tolist()
        for i,j in enumerate(filas):
            if i<9:
                filas[i]=f"{str(i+1)}  |"
            else:
                filas[i]=f"{str(i+1)} |"
        cierre1=np.arange(1,int(self.stadium.capacity[0]/10)+1).flatten().tolist()
        for i, j in enumerate(cierre1):
            cierre1[i]="|"
        cierre2=np.arange(1,int(self.stadium.capacity[1]/10)+1).flatten().tolist()
        for i, j in enumerate(cierre2):
            cierre2[i]="|"
        #Todo esto imprime el estadio y los asientos, si el asiento está ocupado imprime __x__ para indicarle al usuario que no puede ocuparlo.
        mapa1=pd.DataFrame(self.asientos[0:int((self.stadium.capacity[0])/10)], index=filas[0:int(self.stadium.capacity[0]/10)], columns=columnas).replace({True:"|__X__|", False:"|_____|"})
        mapa1.insert(int(len(columnas)/2),"   ","       ")
        mapa1.insert(int(len(columnas)/2)," ","       ")
        mapa1["  "]=cierre1
        print(mapa1)
        #Estos print son la cancha
        print("    "+"---------"*(len(columnas)+2)+"--")
        for i in range(3):
            print("   "+"|"+" "+"         "*(int((len(columnas)+2)/2))+" | "+"             "*(int((len(columnas)+4)/3))+"|")
        print(" -- "+" "+"         "*(int((len(columnas)+2)/2))+" | "+"             "*(int((len(columnas)+4)/3))+" --")
        for i in range(2):
            print("|"+"    "+"         "*(int((len(columnas)+2)/2))+" | "+"             "*(int((len(columnas)+4)/3))+"   |")
        print(" -- "+" "+"         "*(int((len(columnas)+2)/2))+" | "+"             "*(int((len(columnas)+4)/3))+" --")
        for i in range(3):
            print("   "+"|"+" "+"         "*(int((len(columnas)+2)/2))+" | "+"             "*(int((len(columnas)+4)/3))+"|")
        print("    "+"---------"*(len(columnas)+2)+"--")
        mapa2=pd.DataFrame(self.asientos[int((self.stadium.capacity[0])/10):], index=filas[int(self.stadium.capacity[0]/10):], columns=columnas).replace({True:"|__X__|", False:"|_____|"})
        mapa2.insert(int(len(columnas)/2),"   ","   ")
        mapa2.insert(int(len(columnas)/2)," ","       ")
        mapa2.iat[0,5]="  Zona "
        mapa2.iat[0,6]="  Vip  "
        mapa2["  "]=cierre2
        print(mapa2)
    def mostrar_resumen(self):
         print(f"\n-Id del partido: {self.id}\n\tEquipo Local: {self.home_team.name}\n\tEquipo Visitante: {self.away_team.name}\n\tFecha: {self.date}\n\tEstadio: {self.stadium.name}\n\tAsistencia:{len(self.entradas_asistencia_confirmada)}\n\tEntradas vendidas:{len(self.entradas_asistencia_confirmada)+len(self.entradas_asistencia_no_confirmada)} ")
