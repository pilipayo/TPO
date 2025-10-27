import random
import os
import platform
from colorama import Fore, Back, Style, init
init(autoreset=True)

#USUARIO MAESTRO
user_admin="admin"
password_admin="1234"

#COLORES
def C(texto, fore=Fore.WHITE, back="", style=""):
    return f"{style}{fore}{back}{texto}{Style.RESET_ALL}"

# Paleta pre-seteada de colores
OK     = lambda texto: C(texto, Fore.GREEN, style=Style.BRIGHT)
WARN   = lambda texto: C(texto, Fore.YELLOW, style=Style.BRIGHT)
ERROR    = lambda texto: C(texto, Fore.RED, style=Style.BRIGHT)
INFO   = lambda texto: C(texto, Fore.CYAN)
TITULO  = lambda texto: C(texto, Fore.WHITE, Back.BLUE, Style.BRIGHT)
INPUT  = lambda texto: C(texto, Fore.MAGENTA, style=Style.BRIGHT)

#DATOS PRE-SETEADOS

letras_mayusculas = ('A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z','Á','É','Í','Ó','Ú','Ü','Ñ')
letras_minusculas = ('a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z','á','é','í','ó','ú','ü','ñ')
numeros = ('0','1','2','3','4','5','6','7','8','9')
caracteres_especiales = ('?','!','¡','¿','.',',',':','-','_','(',')','[',']','{','}','@','#','$','%','&','/','"',"'",'+','*','=','<','>','|','^','°','~','`')

def limpiar_pantalla():
    if platform.system() == "Windows":
        os.system("cls")
    else:
        os.system("clear") 

def login():
    """Solicitamos al usuario ingresar usuario y contraseña del administrador"""

    print("-----LOGIN-----")

    while True:
        user=input("Usuario: ")

        password=input("Contraseña: ")
        
        if user== user_admin and password == password_admin:
            print(f"\nBienvenido! {user_admin}")
            try:
                archivo = open(f"{user}.csv", mode = "wt", encoding="utf-8")
            
            except OSError:
                print("No se puede crear el archivo")
            finally:
                archivo.close()
            return True
        else:
            print("Usuario o contraseña equivocada. Volver a ingresar datos\n")
            
    

def menu():
    """Muestra el Menu con las 5 opciones posibles: Salir, Agregar, Editar, Eliminar y Mostrar"""

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
    

def crear_contraseña(largo_contraseña = 20):
    """Generamos una contraseña aleatoria de 20 caracteres que cumpla con: al menos una letra mayúscula, al menos una letra minúscula, 
    al menos un número, y al menos un carácter especial"""

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
    return contraseña

#VALIDACIONES: 12 CARACTERES, 1 NUMERO, 1 CARACTER ESPECIAL, 1 MINUSCULA Y 1 MAYUSCULA
def validar(contraseña,largo_min = 12,numero = False,caracter_esp = False,letra_min = False,
            letra_may = False,largo_aceptado = False, palabras_autorizadas = True,contraseña_aceptada = False):
    """Validamos que se cumplan todas las condiciones.
        Devuelve True o False dependiendo si la contraseña es válida o no"""
    palabras_prohibidas = (f"password","admin","contraseña","claves","clave")
    secuencias_no_recomendadas = ("123","456","789","abc","ABC",)

    largo = len(contraseña)
    cantidad_mayusculas = 0
    cantidad_minusculas = 0
    cantidad_numeros = 0
    cantidad_especiales = 0

    for palabra in palabras_prohibidas:
        if palabra in contraseña:
            palabras_autorizadas = False

    if largo >= largo_min:
        largo_aceptado = True

    for caracter in contraseña:
        if caracter in numeros:
            numero = True
            cantidad_numeros += 1
        if caracter in caracteres_especiales:
            caracter_esp = True
            cantidad_especiales += 1
        if caracter in letras_mayusculas:
            letra_may = True
            cantidad_mayusculas += 1
        if caracter in letras_minusculas:
            letra_min = True
            cantidad_minusculas += 1
        
    if largo_aceptado == True and numero == True and caracter_esp == True and palabras_autorizadas == True and letra_min == True and letra_may == True:
        contraseña_aceptada = True
        puntaje = largo//2
        if largo <= 15:
            puntaje += 0
        elif largo <= 20:
            puntaje += 10
        else:
            puntaje += 15

        for palabra in secuencias_no_recomendadas:
            if palabra in contraseña:
                puntaje -= 7
        
        if cantidad_mayusculas > 3:
            puntaje += 2
        if cantidad_especiales > 3:
            puntaje += 2
        if cantidad_numeros > 3:
            puntaje += 2
        if cantidad_minusculas > 3:
            puntaje += 2

        if puntaje <= 12:
            nivel = "DEBIL"
        elif puntaje <= 25:
            nivel = "INTERMEDIA"
        else:
            nivel = "FUERTE"
        print("Tu contraseña tiene un nivel de seguridad: ", nivel )

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
            print("Va ingresar su propia contraseña. Tenga en cuenta que la misma debe tener como mínimo:")
            print(" 12 caracteres✅\n Una letra mayúscula✅\n Una letra minúscula✅\n Un número✅\n Un caracter especial.✅\n")
            contraseña = input("Ingrese la contraseña que quiere para esta app: ")
            if validar(contraseña) == True:
                print("%$%$%")
                contraseña_encriptada, lista_encriptacion = encriptar(contraseña)
                if fila == -1:
                    try:
                        with open(f"claves.csv", mode = "at", encoding="utf-8") as archivo:
                            archivo.write(contraseña_encriptada+";"+lista_encriptacion+"\n")
                    except OSError:
                        print("No se pudo abrir el archivo")
                else:
                    try:
                        with open("claves.csv", mode = "rt", encoding="utf-8") as archivo:
                            lineas = archivo.readlines()
                            linea_a_editar = lineas[fila-1]
                            linea_a_editar.strip()
                            app, usuario, contraseña, lista = linea_a_editar.split(";")
                            lineas.pop(fila-1)
                        with open("claves.csv", mode = "wt", encoding="utf-8") as archivo:
                            for i in lineas:
                                archivo.write(i)

                        with open("claves.csv", mode = "at", encoding="utf-8") as archivo:
                            archivo.write(app+";"+usuario+";"+contraseña_encriptada+";"+lista_encriptacion+"\n")
                            
                    except OSError:
                        print("No se pudo abrir el archivo")
                break
            else:
                print("Contraseña no valida.")
        else:
            while True:
                contraseña = crear_contraseña()
                if validar(contraseña) == True:
                    break
            contraseña_encriptada, lista_encriptacion = encriptar(contraseña)
            if fila == -1:
                try:
                    with open("claves.csv", mode = "at", encoding="utf-8") as archivo:
                        archivo.write(contraseña_encriptada+";"+lista_encriptacion+"\n")
                except OSError:
                    print("No se pudo abrir el archivo")
            else:
                try:
                    with open("claves.csv", mode = "rt", encoding="utf-8") as archivo:
                        lineas = archivo.readlines()
                        linea_a_editar = lineas[fila-1]
                        linea_a_editar.strip()
                        app, usuario, contraseña, lista = linea_a_editar.split(";")
                        lineas.pop(fila-1)
                    with open("claves.csv", mode = "wt", encoding="utf-8") as archivo:
                        for i in lineas:
                            archivo.write(i)

                    with open("claves.csv", mode = "at", encoding="utf-8") as archivo:
                        archivo.write(app+";"+usuario+";"+contraseña_encriptada+";"+lista_encriptacion+"\n")
                        
                except OSError:
                    print("No se pudo abrir el archivo")
            break


def ingresar_usuario(fila = -1):
    """Permite al usuario ingresar su nombre de usuario"""
    if fila == -1:
        try:
            with open("claves.csv", mode = "at", encoding="utf-8") as archivo:
                usuario = input("Ingrese el nombre de su usuario en la app: ")
                archivo.write(usuario+";")
        except OSError:
            print("No se pudo abrir el archivo")

    else:  
        try:
            with open("claves.csv", mode = "rt", encoding="utf-8") as archivo:
                lineas = archivo.readlines()
                linea_a_editar = lineas[fila-1]
                linea_a_editar.strip()
                app, usuario, contraseña, lista = linea_a_editar.split(";")
                usuario = input("Ingrese el nombre de su usuario en la app: ")
                lineas.pop(fila-1)
                print(lineas)
            with open("claves.csv", mode = "wt", encoding="utf-8") as archivo:
                for i in lineas:
                    archivo.write(i)

            with open("claves.csv", mode = "at", encoding="utf-8") as archivo:
                archivo.write(app+";"+usuario+";"+contraseña+";"+lista+"\n")
                
        except OSError:
            print("No se pudo abrir el archivo")




def ingresar_aplicacion(posicion = -1):
    """Permite al usuario ingresar el nombre de la aplicación"""
    with open("claves.csv", mode = "at") as archivo:
        aplicacion = input("Ingrese el nombre de la nueva app: ")
        archivo.write(aplicacion+";")


def nueva_cuenta():
    """Creamos una nueva cuenta utilizando las funciones creadas anteriormente"""
    ingresar_aplicacion()
    ingresar_usuario()
    ingresar_contraseña()
    
def editar():
    """Editamos el usuario o contraseña ya guardados"""
    fila = buscar()
    if fila == -1:
        print("La cuenta que desea editar no existe.")
    else:
        try:
            print("Ingrese '1' si quiere editar el usuario o '2' si quiere editar la contraseña.")
            respuesta = int(input("Respuesta: "))
            while respuesta != 1 and respuesta != 2:
                print("Ingreso invalido. Responda nuevamente.")
                respuesta = int(input("Respuesta: "))

            if respuesta == 1:
                ingresar_usuario(fila)
            else:
                ingresar_contraseña(fila) 
        except ValueError as cabeza:
            print("sos muy gay", cabeza)       


def buscar():
    "Busca la aplicación tanto en mayuscula como minuscula"
    print("Estas son las cuentas disponibles:")
    contador = 1
    encontrado = True
    try:
        with open("claves.csv", mode="r", encoding = "utf-8") as archivo:
            for linea in archivo:
                linea = linea.strip()
                linea = linea.split(";")
                if len(linea) == 4:
                    app, usuario, contraseña, lista = linea
                    print(f"{contador}. App:{app}| Usuario: {usuario}")
                    contador +=1
                else:
                    continue
    except OSError:
        print("No se pudo abrir el archivo.")

    while True:
        try:
            cuenta_a_buscar = int(input("Ingrese el numero de la app que desea editar o borrar: "))

            while cuenta_a_buscar < 1:
                cuenta_a_buscar = int(input("Ingrese un numero valido (mayor o igual a '1'): "))

            with open("claves.csv", mode="r", encoding="utf-8") as archivo:
                cantidad_registros = sum(1 for i in archivo)
            
            if cuenta_a_buscar > cantidad_registros:
                print("Numero invalido")
                encontrado = False
            break
        
        
        except ValueError:
            print("Debe ingresar un numero.")
        except OSError:
            print("Archivo no encontrado")
    
    return cuenta_a_buscar if encontrado == True else -1
    
    
    
def eliminar():
    "Eliminamos la cuenta buscada"
    fila = buscar()
    if fila == -1:
        print("La cuenta que desea eliminar no existe.")
    else:
        try:
            with open("claves.csv", mode = "rt", encoding="utf-8") as archivo:
                lineas = archivo.readlines()    
                lineas.pop(fila-1)
                print(lineas)
            with open("claves.csv", mode = "wt", encoding="utf-8") as archivo:
                for i in lineas:
                    archivo.write(i)
                
        except OSError:
            print("No se pudo abrir el archivo")

        print("La cuenta fue eliminada.")
  

def mostrar():
    """Mostramos todas las contraseñas, primero ocultas y cuando ingrese la contraseña maestra se muestran completas."""
    contador = 1
    print("\nEstas son tus cuentas guardadas:")
    try:
        with open("claves.csv", mode="r", encoding="utf-8") as archivo:
            for linea in archivo:
                if linea[0]=="":
                    print("\nNo hay cuentas guardadas aún. Vuelve al menu")
                    return
                linea = linea.strip()
                linea = linea.split(";")
                if len(linea) == 4:
                    app, usuario, contraseña, lista = linea
                    print(f"{contador}. App:{app}| Usuario: {usuario} | Contraseña: {contraseña}")
                    contador +=1
                else:
                    continue
                
    except OSError:
        print("No se pudo abrir el archivo.")
    
    seguir=input("\nSi queres ver las contraseñas ingresa la contraseña de administrador\n")

    if seguir==password_admin:
        contador = 1
        try:
            with open("claves.csv", mode="r", encoding = "utf-8") as archivo:
                for linea in archivo:
                    linea = linea.strip()
                    linea = linea.split(";")
                    if len(linea) == 4:
                        app, usuario, contraseña, lista = linea
                        print(f"{contador}. App:{app}| Usuario: {usuario} | Contraseña: {desencriptar(contraseña, enlistar(lista))}")
                        contador +=1
                    else:
                        continue
        except OSError:
            print("No se pudo abrir el archivo.")

    else:
        print("Contraseña incorrecta. Acceso denegado")


    
def encriptar(clave_original):
    largo_clave_original= len(clave_original)
    clave_encriptada = crear_contraseña(largo_clave_original)
    
    lista_encriptacion = []
    
    for i in range(0,largo_clave_original):
        caracter = clave_original[i]
        for j in range(0,4):
            if caracter in letras_mayusculas:
                tupla_original = 0
                posicion_original = letras_mayusculas.index(caracter)
            elif caracter in letras_minusculas:
                tupla_original = 1
                posicion_original = letras_minusculas.index(caracter)
            elif caracter in numeros:
                tupla_original = 2
                posicion_original = numeros.index(caracter)
            else: 
                tupla_original = 3
                posicion_original = caracteres_especiales.index(caracter)
                
                
        caracter = clave_encriptada[i]
        for j in range(0,4):
            if caracter in letras_mayusculas:
                tupla_encriptada = 0
                posicion_encriptada = letras_mayusculas.index(caracter)
            elif caracter in letras_minusculas:
                tupla_encriptada = 1
                posicion_encriptada = letras_minusculas.index(caracter)
            elif caracter in numeros:
                tupla_encriptada = 2
                posicion_encriptada = numeros.index(caracter)
            else: 
                tupla_encriptada = 3
                posicion_encriptada = caracteres_especiales.index(caracter)
                
        lista_encriptacion.append(tupla_encriptada-tupla_original)
        lista_encriptacion.append("|")
        lista_encriptacion.append(posicion_encriptada - posicion_original)
        lista_encriptacion.append("|")
        cadena_encriptada = "".join(map(str, lista_encriptacion))

    
    return clave_encriptada,cadena_encriptada
    
  
def desencriptar(clave_encriptada, lista_encriptacion):
    largo_clave_encriptada= len(clave_encriptada)
    clave_original = []
    
    for i in range(0,largo_clave_encriptada):
        caracter = clave_encriptada[i]
        for j in range(0,4):
            if caracter in letras_mayusculas:
                tupla_encriptada = 0
                posicion_encriptada = letras_mayusculas.index(caracter)
            elif caracter in letras_minusculas:
                tupla_encriptada = 1
                posicion_encriptada = letras_minusculas.index(caracter)
            elif caracter in numeros:
                tupla_encriptada = 2
                posicion_encriptada = numeros.index(caracter)
            else: 
                tupla_encriptada = 3
                posicion_encriptada = caracteres_especiales.index(caracter)
                
        if i == 0:
            tupla_original =  tupla_encriptada - lista_encriptacion[0]
            posicion_original = posicion_encriptada - lista_encriptacion[1]
        else:
            tupla_original =  tupla_encriptada - lista_encriptacion[i*2]
            posicion_original = posicion_encriptada - lista_encriptacion[i*2+1]
            
        if tupla_original == 0:
            caracter = letras_mayusculas[posicion_original]
        elif  tupla_original == 1:
            caracter = letras_minusculas[posicion_original]
        elif  tupla_original == 2:
            caracter = numeros[posicion_original]
        else: 
            caracter = caracteres_especiales[posicion_original]
                
        
        clave_original.append(caracter)
    clave_original = "".join(clave_original)
    return clave_original


def enlistar(cadena):
    lista = cadena.split("|")   
    lista = [int(x) for x in lista if x != ""]

    return lista