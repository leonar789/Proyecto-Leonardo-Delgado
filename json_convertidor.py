#Solo se encarga de transformar un objeto a diccionario para el guardado en txt. Va en el json.dump(default=) del main para que convierta los objetos que están dentro de otros
def convertir_objeto(objeto):
    return objeto.__dict__