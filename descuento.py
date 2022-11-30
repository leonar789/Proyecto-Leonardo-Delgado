from itertools import permutations
#Este apartado se encarga de calcular los descuentos.
def numero_vampiro(numero):
    if len(numero)%2==0:
        posibles_permutaciones=permutations(numero) #Para saber si es número vampiro, se calculan las permutaciones del número y luego se estudia cada permutación.
        for permutacion in posibles_permutaciones:
            #Se divide en dos grupos iguales de cifras y luego se multiplican. Si el producto iguala al número, retorna True.
            if int( "".join(permutacion[int(len(numero)/2):]))*int("".join(permutacion[:int(len(numero)/2)]))==int(numero):
                return True

def descuento_entradas(cedula, monto): #Retorna el descuento para las entradas
    if numero_vampiro(cedula):
        return monto*0.5
    return 0

def numero_perfecto(numero): 
    divisores=[]
    acumulador=0
    #Mete todos los divisores del número en una lista, luego los suma para ver si es igual al número, de ser así retorna True.
    for i in range(1,int(numero)):
        if int(numero)%i==0:
            divisores.append(i)
    for divisor in divisores:
        acumulador+=divisor

    if acumulador==int(numero) and numero!="1":
        return True

def descuento_restaurante(cedula, monto):#Retorna el descuento para los productos
    if numero_perfecto(cedula):
        return round(monto*0.15/1.16, 2)
    return 0