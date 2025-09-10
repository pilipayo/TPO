import random

#USUARIO MAESTRO
user_admin="admin"
password_admin="1234"


#DATOS PRE-SETEADOS
claves = []
letras_mayusculas = ['A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z','Á','É','Í','Ó','Ú','Ü','Ñ']
letras_minusculas = ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z','á','é','í','ó','ú','ü','ñ']
numeros = ['0','1','2','3','4','5','6','7','8','9']
caracteres_especiales = ['?','!','¡','¿','.',',',';',':','-','_','(',')','[',']','{','}','@','#','$','%','&','/','\\','"',"'",'+','*','=','<','>','|','^','°','~','`']

def login():
    print("-----LOGIN-----")

    """Solicitamos al usuario ingresar usuario y contraseña del administrador"""

    while True:
        user=input("Usuario: ")
        password=input("Contraseña: ")
        
        if user== user_admin and password == password_admin:
            print(f"\nBienvenido! {user_admin}")
            return True
        else:
            print("Usuario o contraseña equivocada. Volver a ingresar datos\n")
            
    

def menu():
    """Muestra el Menu con las 4 opciones posibles: Salir, Agregar, Editar, Eliminar y Mostrar"""

    print("\n\nElija una de las siguientes opciones")
    for i in range (5):
        if i == 0:
            opcion = "Salir"
        elif i == 1:
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
    

def crear_contraseña():
    """Generamos una contraseña aleatoria de 20 caracteres que cumpla con: al menos una letra mayúscula, al menos una letra minúscula, 
    al menos un número, y al menos un carácter especial"""

    largo_contraseña = 20
    while True:
        contraseña=[]
        for i in range(largo_contraseña):
            buscar_lista = random.randint(0,3)
            if buscar_lista == 0:
                caracter = letras_mayusculas[random.randint(0,len(letras_mayusculas)-1)]
            elif buscar_lista == 1:
                caracter = letras_minusculas[random.randint(0,len(letras_minusculas)-1)]
            elif buscar_lista == 2:
                caracter = numeros[random.randint(0,len(numeros)-1)]
            else:
                caracter = caracteres_especiales[random.randint(0,len(caracteres_especiales)-1)]
            contraseña.append(caracter)
        contraseña = "".join(contraseña)
        if validar(contraseña) == True:
            break
    return contraseña

#VALIDACIONES: 12 CARACTERES, 1 NUMERO, 1 CARACTER ESPECIAL, 1 MINUSCULA Y 1 MAYUSCULA
def validar(contraseña,largo_min = 12,numero = False,caracter_esp = False,letra_min = False,letra_may = False,largo_aceptado = False,contraseña_aceptada = False):
    """Validamos que se cumplan todas las condiciones y devuelve True o False dependiendo si la contraseña es válida o no"""

    if len(contraseña) >= largo_min:
        largo_aceptado = True
    for caracter in contraseña:
        if caracter in numeros:
            numero = True
        if caracter in caracteres_especiales:
            caracter_esp = True
        if caracter in letras_mayusculas:
            letra_may = True
        if caracter in letras_minusculas:
            letra_min = True
        
    if largo_aceptado == True and numero == True and caracter_esp == True and letra_min == True and letra_may == True:
        contraseña_aceptada = True
        
    return contraseña_aceptada
            


def ingresar_contraseña(fila = -1):
    """Le pedimos al usuario que ingrese su contraseña o que cree una contraseña aleatoria más segura"""
    while True:
        while True:
            try:
                eleccion = int(input("Ingrese '1' si quiere ingresar usted mismo la contraseña o '2' si quiere que se cree otra al azar: "))
                if  eleccion != 1 and eleccion != 2:
                    print("Debe ingresar una de las opciones mencionadas.")
                else:
                    break
            except ValueError:
                print("Debe ingresar un numero.")
            
            
        if eleccion == 1:
            contraseña = input("Ingrese la contraseña que quiere para esta app: ")
            if validar(contraseña) == True:
                if fila == -1:
                    claves[-1].append(contraseña)
                else:
                    claves[fila][2] = contraseña
                break
            else:
                print("Contraseña no valida.")
        else:
            contraseña = crear_contraseña()
            if fila == -1:
                claves[-1].append(contraseña)
            else:
                claves[fila][2] = contraseña
            break


def ingresar_usuario(fila = -1):
    usuario = input("Ingrese el nombre de su usuario en la app: ")
    if fila == -1:
        claves[fila].append(usuario)
    else:
        claves[fila][1] = usuario



def ingresar_aplicacion(posicion = -1):
    """Permite al usuario ingresar el nombre de la aplicación"""

    claves.append([])
    aplicacion = input("Ingrese el nombre de la nueva app: ")
    claves[posicion].append(aplicacion)



def nueva_cuenta():
    """Creamos una nueva cuenta utilizando las funciones creadas anteriormente"""
    ingresar_aplicacion()
    ingresar_usuario()
    ingresar_contraseña()
    
def editar():
    fila = buscar()
    if fila == -1:
        print("La cuenta que desea editar no existe.")
    else:
        print("Ingrese '1' si quiere editar el usuario o '2' si quiere editar la contraseña.")
        respuesta = int(input("Respuesta: "))
        while respuesta != 1 and respuesta != 2:
            print("Ingreso invalido. Responda nuevamente.")
            respuesta = int(input("Respuesta: "))
        if respuesta == 1:
            ingresar_usuario(fila)
        else:
            ingresar_contraseña(fila)            
    
    
def buscar():
    cuenta_a_buscar = input("Ingrese el nombre de la app que desea buscar: ").lower()
    encontrado = False
    for i in range(len(claves)):
        if cuenta_a_buscar == claves[i][0].lower():
            encontrado = True
            fila = i
    return fila if encontrado == True else -1
    
def eliminar():
    fila = buscar()
    if fila == -1:
        print("La cuenta que desea eliminar no existe.")
    else:
        claves.pop(fila)
        print("La cuenta fue eliminada.")

"""Oculatamos la contraseña con *"""
ocultar = lambda c: c[:1] + "*" * (len(c) - 1)   

def mostrar():
    if len(claves)==0:
        print("\nNo hay cuentas guardadas aún. Vuelve al menu")
        return
    else:
        print("\nEstas son tus cuentas guardadas")
        for app, usuario, cont in claves:
            print(f"App:{app}| Usuario: {usuario} | Contraseña: {ocultar(cont)}")
    
    seguir=input("\nSi queres ver las contraseñas ingresa la contraseña de administrador\n")

    if seguir==password_admin:
        #contraseña_admin= input("Ingrese la contraseña del usuario administrador para poder visualizar sus contraseñas guardadas: ")
        for app, usuario, cont in claves:
            print(f"App:{app}| Usuario: {usuario} | Contraseña: {cont}")
    else:
        print("Contraseña incorrecta. Acceso denegado")
    

