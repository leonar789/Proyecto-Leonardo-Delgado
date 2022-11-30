import random
#La clase para entradas facilita el control de estadísticas.
class EntradaGeneral:
   #Para llevar un mejor control del inventario, cada entrada generada es un objeto individual.
    def __init__(self, partido_id, asiento, codigos_usados_constructor, cedula_comprador):
        self.asiento=asiento
        self.codigo= self.generador_codigo(codigos_usados_constructor)
        self.partido_id=partido_id
        self.cedula_comprador=cedula_comprador
        self.precio=50
        self.vip=False
        self.tipo="General"
    def generador_codigo(self,codigos_usados):
        while True:
            #Genera un código al azar eligiendo entre letras y números, verifica si ya existe, de ser así calcula otro.
            abecedario_y_numeros=["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z", "1","2", "3", "4", "5", "6", "7", "8","9"]
            codigo=random.choices(population= abecedario_y_numeros, k = 5)
            if codigo in codigos_usados:
                continue
            else:
                break
        return "".join(codigo)
    def mostrar_resumen(self):
        print(f"- {self.tipo}: {self.precio}$\n\tAsiento: {self.asiento}\n\tCodigo: {self.codigo}\n\t")
class EntradaVIP(EntradaGeneral):
    
    def __init__(self, partido_id, asiento, codigos_usados_constructor,cedula_comprador):
        super().__init__(partido_id, asiento, codigos_usados_constructor,cedula_comprador)
        self.gastos=120*1.16 #Para llevar el conteo de cuanto gasta un cliente VIP, sus gastos se agregan directamente a su entrada para llevar la cuenta.
        self.precio=120
        self.vip=True
        self.tipo="VIP"
    