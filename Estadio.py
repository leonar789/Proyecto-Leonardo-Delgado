#Simplemente la clase que contituye a las instancias para los estadios.
class Estadio:
    def __init__(self, id, name, capacity, location, restaurants):
        self.name=name
        self.capacity=capacity
        self.location=location
        self.restaurants=restaurants
        self.id=id
    def mostrar_resumen_restaurantes(self):
        contador=1
        for restaurante in self.restaurants:
            print(f"{contador}-{restaurante.name}")
            contador+=1
    

