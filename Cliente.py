class Cliente:
    #La clase cliente tiene la finalidad de organizar la base de datos de clientes para agrupar su información y llevar un registro de sus entradas compradas
    def __init__(self, nombre, cedula, edad, entradas) -> None:
        self.nombre=nombre
        self.cedula=cedula
        self.edad=edad
        self.entradas=entradas
    def resumen(self):
        print(f"\nNombre: {self.nombre}\ncedula: {self.cedula}\nEdad: {self.edad}\nEntradas compradas: {len(self.entradas)}")