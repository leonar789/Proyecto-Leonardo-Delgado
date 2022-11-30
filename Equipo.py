#Simplemente la clase que contituye a las instancias para los equipos.
class Equipo:
    def __init__(self, name, flag, fifa_code, group, id):
        self.name=name
        self.flag=flag
        self.fifa_code=fifa_code
        self.group=group
        self.id=id