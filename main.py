import random

claves = [["APLICACION", "USUARIO", "CLAVE"]]

def menu():
    print("\n\nElija una de las siguientes opciones")
    for i in range (5):
        if i == 0:
            opcion = "Salir"
        elif i == 1
            opcion = "Agregar"
        elif i == 2:
            opcion = "Editar"
        elif i == 3:
            opcion = "Eliminar"
        else:
            opcion = "Mostrar"
        print("-------------")
        print(i,"-", opcion)
    print("\n")
    

def ingresar_contraseña(posicion = -1):
    contraseña = input("Ingrese la contraseña que quiere para esta app: ")
    claves[-1].append(contraseña)


def ingresar_usuario(posicion = -1):
    usuario = input("Ingrese el nombre de su usuario en la app: ")
    claves[-1].append(usuario)

def ingresar_aplicacion(posicion = -1):
    claves.append([])
    aplicacion = input("Ingrese el nombre de la nueva app: ")
    claves[posicion].append(aplicacion)
    
def nueva_cuenta():
    ingresar_aplicacion()
    ingresar_usuario()
    ingresar_contraseña()
    
def editar():
    posicion = buscar()
    if posicion == -1:
        print("La cuenta que desea editar no existe.")
    else:
        print("Ingrese '1' si quiere editar el usuario o '2' si quiere editar la contraseña.")
        respuesta = int(input("Respuesta: "))
        while respuesta != 1 and respuesta != 2:
            print("Ingreso invalido. Responda nuevamente.")
            respuesta = int(input("Respuesta: "))
        if respuesta == 1:
            claves[posicion][1] = input("Ingrese el nuevo nombre de usuario: ")
        else:
            claves[posicion][2] = input("Ingrese la nueva contraseña: ")
    
    
def buscar():
    cuenta_a_buscar = input("Ingrese el nombre de la app que desea buscar: ").lower()
    encontrado = False
    for i in range(len(claves)):
        if cuenta_a_buscar == claves[i][0].lower():
            encontrado = True
            posicion = i
    return posicion if encontrado == True else -1
    
def eliminar():
    posicion = buscar()
    if posicion == -1:
        print("La cuenta que desea editar no existe.")
    else:
        claves.pop(posicion)

while True:
    menu()
    accion = int(input("Ingrese el número de la tarea que desea realizar: "))
    
    while accion < 0 or accion > 5:
        print("Nummero ingresado invalido, ingrese nuevamente: ")
        accion = int(input())
    if accion == 1:
        nueva_cuenta() 
    elif accion == 2:
        editar()
    elif accion == 3:
        eliminar()
    elif accion == 4:
        for i in range(len(claves)):
            print(claves[i])
    else:
        break
    
    