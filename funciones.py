"""Utilidades de la app: login, gestión de cuentas, encriptación y (des)encriptación."""
import random
import os
import platform
import excepciones
from datetime import datetime
from colorama import Fore, Style, init
init()

def log_event(evento, nivel="INFO", mensaje="", usuario="", funcion="", extra="", filename=None):
    """
Registra un evento en un CSV de logs (no interrumpe la app si falla).

Columnas del archivo: "fecha;gravedad;evento;usuario;funcion;mensaje;extra".

Parámetros:
    evento (str): Identificador o nombre del evento (p.ej., "login_ok").
    nivel (str): Severidad/gravidad del evento (p.ej., "INFO", "WARN", "ERROR").
    mensaje (str): Descripción legible del evento. Se compactan saltos de línea.
    usuario (str): Usuario asociado al evento (si aplica).
    funcion (str): Nombre de la función que originó el evento.
    extra (str): Información adicional (opcional).
    filename (str|None): Ruta del archivo de log. Si es None, usa "eventos_log.csv".

Returns:
    None: Escribe una línea en el CSV de logs. Si no existe, crea encabezado.

Notas:
    Cualquier OSError se ignora a propósito: un fallo de log nunca corta la app.
"""
    if filename is None:
        filename = "eventos_log.csv"  

    # Compacta saltos de línea
    if "\n" in mensaje:
        mensaje = "".join(mensaje.splitlines())
    if "\n" in extra:
        extra = "".join(extra.splitlines())

    fecha = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    linea = f"{fecha};{nivel};{evento};{usuario};{funcion};{mensaje};{extra}\n"

    try:
        # existe el archivo? si no, escribimos encabezado primero
        escribir_header = False
        try:
            with open(filename, "r", encoding="utf-8") as arch:
                pass
        except OSError:
            escribir_header = True

        with open(filename, "a", encoding="utf-8") as f:
            if escribir_header:
                f.write("fecha;gravedad;evento;usuario;funcion;mensaje;extra\n")
            f.write(linea)
    except OSError:
        # nunca cortamos la app por un fallo de log
        pass


#DATOS PRE-SETEADOS

letras_mayusculas = ('A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z','Á','É','Í','Ó','Ú','Ü','Ñ')
letras_minusculas = ('a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z','á','é','í','ó','ú','ü','ñ')
numeros = ('0','1','2','3','4','5','6','7','8','9')
caracteres_especiales = ('?','!','¡','¿','.',',',':','-','_','(',')','[',']','{','}','@','#','$','%','&','/','"',"'",'+','*','=','<','>','|','^','°','~','`')

COLORES = {
    "ok": Fore.GREEN,       
    "error": Fore.RED,      
    "alerta": Fore.YELLOW,  
    "info": Fore.CYAN,     
    "rosa":Fore.MAGENTA, 
    "reset": Style.RESET_ALL,
    "bright": Style.BRIGHT
}

limpiar_pantalla = lambda: os.system("cls") if platform.system()=="Windows" else os.system("clear")


def login():
    """
Autentica al usuario administrador o crea uno nuevo si no existe.

Flujo:
    - Pide nombre de usuario (no vacío).
    - Si existe "<user>.csv":
        * Lee la contraseña guardada (posiblemente encriptada) y la desencripta si corresponde.
        * Verifica hasta 3 intentos de contraseña ingresada.
        * Valida que el archivo corresponda al mismo usuario (detección de archivo ajeno).
    - Si NO existe:
        * Ofrece crear usuario.
        * Pide contraseña nueva, la valida y la guarda encriptada junto con el usuario encriptado.

Returns:
    tuple[str, str]: (user, contraseña_guardada_en_texto_plano)

Raises:
    excepciones.CredencialesInvalidasError: Si se exceden intentos o no puede desencriptar.
    excepciones.UsuarioNoExisteError: Si el usuario no existe y elige no crearlo.
    excepciones.ArchivoModificado: Si el archivo de credenciales no corresponde al usuario.
    excepciones.ArchivoNoAccesibleError: Si falla la creación de archivos al dar de alta.

Side effects:
    - Lee/escribe archivos "<user>.csv".
    - Puede loguear eventos con log_event().
"""

    print(COLORES["bright"] + "\n══════════════ LOGIN ══════════════" + COLORES["reset"])

    while True:
        user=input(COLORES["bright"] + "👤 Usuario: "+ COLORES["reset"]).strip()
        if user:
            break
        print(COLORES["alerta"]+"⚠ Debe ingresar un nombre de usuario."+ COLORES["reset"])
    archivo_usuario = f"{user}.csv"
        
    try:
        with open(archivo_usuario, mode="rt", encoding="utf-8") as archivo:
            contraseña_archivada= archivo.readline().strip()

            if ";" in contraseña_archivada:
                try:
                    encriptada, lista = contraseña_archivada.split(";", 1)
                    contraseña_guardada = desencriptar(encriptada, enlistar(lista))
                except Exception:
                    raise excepciones.CredencialesInvalidasError(COLORES["error"]+"✖ Error al desencriptar la contraseña guardada."+ COLORES["reset"])
                    #print(COLORES["error"]+"✖ Error al desencriptar la contraseña guardada."+ COLORES["reset"])
                    #return None, None
            else:
                contraseña_guardada= contraseña_archivada

            intentos=3
            linea = archivo.readline().strip().split(";")
            usuario_guardado_encriptado, lista_usuario_guardado = linea
            usuario_guardado = desencriptar(usuario_guardado_encriptado, enlistar(lista_usuario_guardado))

            while intentos>0:
                contraseña_ingresada = input(COLORES["bright"]+"🔐 Contraseña: "+COLORES["reset"])
            
                if contraseña_ingresada == contraseña_guardada:
                    if user == usuario_guardado:
                        print(COLORES["bright"]+f"\nBienvenido, {user}!"+COLORES["reset"])
                        return user, contraseña_guardada
                    else:
                        raise excepciones.ArchivoModificado(COLORES["error"]+ "El archivo está siendo accedido por un usuario no permitido."+ COLORES["reset"])


                else:
                    intentos-=1
                    if intentos>0:
                        print(COLORES["error"]+ "✖ Contraseña incorrecta."+ COLORES["reset"])
            else:
                log_event("login_attempts_exceeded", "WARN", "Excediste los 3 intentos.", usuario=user, funcion="login")
                raise excepciones.CredencialesInvalidasError(COLORES["error"]+ "Excediste los 3 intentos."+ COLORES["reset"])
                #print(COLORES["error"]+ "Excediste los 3 intentos."+ COLORES["reset"])
                #return None, None
        
    except OSError:

        print(COLORES["alerta"] + f"⚠ El usuario '{user}' no existe." + COLORES["reset"])
        respuesta = input("Queres crear un nuevo usuario? (s/n): ").lower()
        
        while respuesta !="s" and respuesta !="n":
            respuesta = input(COLORES["alerta"]+"✖ Respuesta INVALIDA, debe ingresar s o n: "+COLORES["reset"]).lower()
        
        if respuesta == "n":
            raise excepciones.UsuarioNoExisteError(COLORES["alerta"] + "⚠ No se creó el usuario. Saliendo del login."+ COLORES["reset"])
            #print(COLORES["alerta"] + "⚠ No se creó el usuario. Saliendo del login."+ COLORES["reset"])
            #return None, None

        print("Creando nueva cuenta...")
        while True:
            nuevaContraseña = input(COLORES["bright"]+ "🔑 Crea tu contraseña: "+ COLORES["reset"])
            
            #if not validar(nuevaContraseña):
            try:
                if validar(nuevaContraseña):        # <---- Puede levantar ContraseñaInvalidaError
                #print(COLORES["alerta"] + "⚠ No cumple con los requisitos. Intenta de nuevo" + COLORES["reset"])
                #continue
                    repetir=input("Repeti la contraseña ingresada: ")
            
                    if nuevaContraseña != repetir:
                        print(COLORES["alerta"] + "⚠ No coinciden las contraseñas. Intenta de nuevo"+ COLORES["reset"])
                        continue
                    break
            except excepciones.ContraseñaInvalidaError as e:
                print(COLORES["alerta"] + str(e) + COLORES["reset"])
                continue        

        try:
            encriptada, lista = encriptar(nuevaContraseña)
            user_encriptado, lista_user = encriptar(user)

            with open(archivo_usuario, mode = "wt", encoding="utf-8") as archivo:
                archivo.write(f"{encriptada};{lista}\n")
            with open(archivo_usuario, mode = "at", encoding="utf-8") as archivo:
                archivo.write(f"{user_encriptado};{lista_user}")
            print(COLORES["ok"]+"✅ Cuenta creada exitosamente!"+ COLORES["reset"])
            print(COLORES["bright"]+f"\nBienvenido, {user}!"+COLORES["reset"])
            return user, nuevaContraseña
        
        except OSError:
            raise excepciones.ArchivoNoAccesibleError(COLORES["error"]+"❌ No se pudo crear el archivo"+COLORES["reset"])
            #print(COLORES["error"]+"❌ No se pudo crear el archivo"+COLORES["reset"])
            #return None, None
            
    

def menu():
    """
Muestra el menú principal por consola con 5 opciones (0-4) y estilos de color.

Returns:
    None
"""

    print(COLORES["bright"] + "\n══════════════ MENÚ PRINCIPAL ══════════════" + COLORES["reset"])
    print("\nElija una de las siguientes opciones")

    for i in range (5):
        if i == 0:
            opcion = COLORES["error"]+ "🏃🚪  Salir" + COLORES["reset"]
        elif i == 1:
            opcion =COLORES["ok"]+ "➕ Agregar cuenta" + COLORES["reset"]
        elif i == 2:
            opcion =COLORES["info"]+ "📝  Editar cuenta"+ COLORES["reset"]
        elif i == 3:
            opcion =COLORES["alerta"] + "🗑  Eliminar cuenta" + COLORES["reset"]
        else:
            opcion =COLORES["rosa"]+ "👀 Mostrar cuentas"  + COLORES["reset"]

        print(i,"-", opcion)
    
    print(COLORES["bright"] + "\n════════════════════════════════════════════" + COLORES["reset"])
    print("\n")
    
def crear_contraseña(largo_contraseña = 20):
    """
Genera una contraseña aleatoria de longitud dada utilizando 4 conjuntos de caracteres.

Parámetros:
    largo_contraseña (int): Longitud deseada. Por defecto, 20.

Returns:
    str: Contraseña generada (puede o no cumplir requisitos; se valida luego con validar()).

Notas:
    Selecciona cada carácter eligiendo aleatoriamente entre:
    mayúsculas, minúsculas, números o especiales.
"""

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


def validar(contraseña, largo_min=12):
    """
Valida requisitos mínimos y calcula un nivel de robustez (Débil/Intermedia/Fuerte).

Parámetros:
    contraseña (str): Contraseña a verificar.
    largo_min (int): Longitud mínima requerida. Por defecto, 12.

Returns:
    bool: True si cumple todos los requisitos (también imprime el nivel).

Raises:
    excepciones.ContraseñaInvalidaError: Si falta longitud, variedad o contiene palabras prohibidas.

Notas:
    - El puntaje se basa en longitud, conteo de clases de caracteres y penaliza secuencias comunes.
    - Imprime el nivel de seguridad con colores.
"""
    # ---- 1. Validaciones básicas ----
    requisitos_faltantes = []

    if len(contraseña) < largo_min:
        requisitos_faltantes.append(f"- Tener al menos {largo_min} caracteres.")

    if not any(c in numeros for c in contraseña):
        requisitos_faltantes.append("- Contener al menos un número (0-9).")

    if not any(c in caracteres_especiales for c in contraseña):
        requisitos_faltantes.append("- Incluir al menos un caracter especial (%, &, !, etc.).")

    if not any(c in letras_mayusculas for c in contraseña):
        requisitos_faltantes.append("- Tener al menos una letra mayúscula (A-Z).")

    if not any(c in letras_minusculas for c in contraseña):
        requisitos_faltantes.append("- Tener al menos una letra minúscula (a-z).")

    palabras_prohibidas = ("password", "admin", "contraseña", "clave", "claves")
    if any(p.lower() in contraseña.lower() for p in palabras_prohibidas):
        requisitos_faltantes.append("- No contener palabras prohibidas como 'password', 'admin', 'clave', etc.")

    if requisitos_faltantes:
        mensaje = "❌ La contraseña no cumple con los siguientes requisitos:\n" + "\n".join(requisitos_faltantes)
        raise excepciones.ContraseñaInvalidaError(mensaje)

    # ---- 2. Si pasa todo, calculamos robustez ----
    largo = len(contraseña)
    cantidad_mayusculas = sum(1 for c in contraseña if c in letras_mayusculas)
    cantidad_minusculas = sum(1 for c in contraseña if c in letras_minusculas)
    cantidad_numeros = sum(1 for c in contraseña if c in numeros)
    cantidad_especiales = sum(1 for c in contraseña if c in caracteres_especiales)

    # Puntaje base según largo
    puntaje = largo // 2
    if largo <= 15:
        puntaje += 0
    elif largo <= 20:
        puntaje += 10
    else:
        puntaje += 15

    # Bonificaciones
    if cantidad_mayusculas > 3:
        puntaje += 2
    if cantidad_minusculas > 3:
        puntaje += 2
    if cantidad_numeros > 3:
        puntaje += 2
    if cantidad_especiales > 3:
        puntaje += 2

    # Penalizaciones
    secuencias_no_recomendadas = ("123", "456", "789", "abc", "ABC")
    for palabra in secuencias_no_recomendadas:
        if palabra in contraseña:
            puntaje -= 7

    # Determinamos el nivel
    if puntaje <= 12:
        nivel = COLORES["alerta"] + "⚠ DÉBIL" + COLORES["reset"]
    elif puntaje <= 25:
        nivel = COLORES["info"] + "INTERMEDIA" + COLORES["reset"]
    else:
        nivel = COLORES["ok"] + "FUERTE" + COLORES["reset"]

    print(f"Tu contraseña tiene un nivel de seguridad: {nivel}")
    return True


def ingresar_contraseña(user, fila = -1):
    """
Solicita una contraseña para una app (manual o aleatoria), la valida y la persiste encriptada.

Parámetros:
    user (str): Usuario propietario del archivo "<user>claves.csv".
    fila (int): -1 para alta (agrega una nueva línea). >=0 para editar esa fila existente.

Returns:
    None

Raises:
    excepciones.ContraseñaInvalidaError: Si la contraseña ingresada no cumple requisitos.
    excepciones.ArchivoNoAccesibleError: Si no puede leer/escribir los archivos de claves.

Efectos:
    - En alta: agrega "…;contraseña_encriptada;cadena_encriptacion".
    - En edición: reescribe la fila indicada con la nueva contraseña encriptada.
"""
    salir = False
    primera_escritura = True
    contador = 1
    while True:
        while True:
            try:
                eleccion = int(input("Ingrese '1' si quiere ingresar usted mismo la contraseña o '2' si quiere que se cree otra al azar: "))
                if  eleccion != 1 and eleccion != 2:
                    print("❌ Debe ingresar una de las opciones mencionadas.")
                else:
                    break
            except ValueError:
                print("Debe ingresar un numero.")
                
            
        if eleccion == 1:
            print("Va ingresar su propia contraseña. Tenga en cuenta que la misma debe tener como mínimo:")
            print(" 12 caracteres✅\n Una letra mayúscula✅\n Una letra minúscula✅\n Un número✅\n Un caracter especial.✅\n")
            contraseña = input("Ingrese la contraseña que quiere para esta app: ")
            
            #if validar(contraseña) == True:
            try:
                if validar(contraseña):       # <--- Levanta ContraseñaInvalidaError
                    contraseña_encriptada, lista_encriptacion = encriptar(contraseña)
                if fila == -1:
                    try:
                        with open(f"{user}claves.csv", mode = "at", encoding="utf-8") as archivo:
                            archivo.write(contraseña_encriptada+";"+lista_encriptacion+"\n")
                    except OSError:
                        raise excepciones.ArchivoNoAccesibleError(COLORES["error"]+"No se pudo abrir el archivo"+COLORES["reset"])
                        #print(COLORES["error"]+"No se pudo abrir el archivo"+COLORES["reset"])
                else:
                    try:
                        with open(f"{user}claves.csv", mode="r", encoding="utf-8") as archivo:
                            while True:
                                lineas = []
                                for i in range(10):
                                    linea = archivo.readline()
                                    if linea == "":
                                            salir = True
                                            break
                                    lineas.append(linea)

                                if primera_escritura == True:
                                    with open(f"{user}claves2.csv", mode="wt", encoding="utf-8") as archivo2:
                                        for linea in lineas:
                                            if fila == contador:
                                                linea = linea.strip().split(";")
                                                app, usuario, contraseña, lista = linea
                                                archivo2.write(app+";"+usuario+";"+contraseña_encriptada+";"+lista_encriptacion+"\n")
                                            else:
                                                archivo2.write(linea)
                                            contador += 1
                                    primera_escritura = False
                                else:
                                    with open(f"{user}claves2.csv", mode="at", encoding="utf-8") as archivo2:
                                        for linea in lineas:
                                            if fila == contador:
                                                linea = linea.strip().split(";")
                                                app, usuario, contraseña, lista = linea
                                                archivo2.write(app+";"+usuario+";"+contraseña_encriptada+";"+lista_encriptacion+"\n")
                                            else:
                                                archivo2.write(linea)
                                            contador += 1
                                if salir == True:
                                    break
                        os.replace(f"{user}claves2.csv",f"{user}claves.csv")
                            
                    except OSError:
                        raise excepciones.ArchivoNoAccesibleError(COLORES["error"]+"No se pudo abrir el archivo"+COLORES["reset"])
                        #print(COLORES["alerta"]+"⚠ No se pudo abrir el archivo"+ COLORES["reset"])
                break

            except excepciones.ContraseñaInvalidaError as msg:
                print(COLORES["alerta"] + str(msg) + COLORES["reset"])
                continue        #VUELVE A PEDIR
                #print("❌ Contraseña no valida.")

        else:   # eleccion == 2
            while True:
                contraseña = crear_contraseña()
                #if validar(contraseña) == True:
                try:
                    if validar(contraseña):
                        break
                except excepciones.ContraseñaInvalidaError:
                    continue

            contraseña_encriptada, lista_encriptacion = encriptar(contraseña)
            if fila == -1:
                try:
                    with open(f"{user}claves.csv", mode = "at", encoding="utf-8") as archivo:
                        archivo.write(contraseña_encriptada+";"+lista_encriptacion+"\n")
                except OSError:
                    raise excepciones.ArchivoNoAccesibleError(COLORES["error"]+"No se pudo abrir el archivo"+COLORES["reset"])
                    #print(COLORES["error"]+"No se pudo abrir el archivo"+COLORES["reset"])
            else:
                try:
                    with open(f"{user}claves.csv", mode="r", encoding="utf-8") as archivo:
                        while True:
                            lineas = []
                            for i in range(10):
                                linea = archivo.readline()
                                if linea == "":
                                        salir = True
                                        break
                                lineas.append(linea)

                            if primera_escritura == True:
                                with open(f"{user}claves2.csv", mode="wt", encoding="utf-8") as archivo2:
                                    for linea in lineas:
                                        if fila == contador:
                                            linea = linea.strip().split(";")
                                            app, usuario, contraseña, lista = linea
                                            archivo2.write(app+";"+usuario+";"+contraseña_encriptada+";"+lista_encriptacion+"\n")
                                        else:
                                            archivo2.write(linea)
                                        contador += 1
                                primera_escritura = False
                            else:
                                with open(f"{user}claves2.csv", mode="at", encoding="utf-8") as archivo2:
                                    for linea in lineas:
                                        if fila == contador:
                                            linea = linea.strip().split(";")
                                            app, usuario, contraseña, lista = linea
                                            archivo2.write(app+";"+usuario+";"+contraseña_encriptada+";"+lista_encriptacion+"\n")
                                        else:
                                            archivo2.write(linea)
                                        contador += 1
                            if salir == True:
                                break
                    os.replace(f"{user}claves2.csv",f"{user}claves.csv")
                        
                except OSError:
                    raise excepciones.ArchivoNoAccesibleError(COLORES["error"]+"No se pudo abrir el archivo"+COLORES["reset"])
                    #print(COLORES["error"]+"No se pudo abrir el archivo"+COLORES["reset"])
            break


def ingresar_usuario(user, fila = -1):
    """
Solicita y persiste el nombre de usuario de la app (alta o edición).

Parámetros:
    user (str): Usuario propietario del archivo "<user>claves.csv".
    fila (int): -1 para alta (completa el campo usuario de la nueva línea).
                >=0 para editar el usuario de la fila indicada.

Returns:
    None

Raises:
    excepciones.ArchivoNoAccesibleError: Si hay problemas de lectura/escritura de archivos.
"""
    if fila == -1:
        try:
            with open(f"{user}claves.csv", mode = "at", encoding="utf-8") as archivo:
                usuario = input("➤ Ingrese el nombre de su usuario en la app: ")
                archivo.write(usuario+";")
        except OSError:
            raise excepciones.ArchivoNoAccesibleError(COLORES["error"]+"No se pudo abrir el archivo"+COLORES["reset"])
            #print(COLORES["error"]+"No se pudo abrir el archivo"+COLORES["reset"])

    else:
        try:
            salir = False
            primera_escritura = True
            contador = 1
            with open(f"{user}claves.csv", mode="r", encoding="utf-8") as archivo:
                while True:
                    lineas = []
                    for i in range(10):
                        linea = archivo.readline()
                        if linea == "":
                                salir = True
                                break
                        lineas.append(linea)

                    if primera_escritura == True:
                        with open(f"{user}claves2.csv", mode="wt", encoding="utf-8") as archivo2:
                            for linea in lineas:
                                if fila == contador:
                                    linea = linea.strip().split(";")
                                    app, usuario, contraseña, lista = linea
                                    usuario = input("➤ Ingrese el nombre de su usuario en la app: ")
                                    archivo2.write(app+";"+usuario+";"+contraseña+";"+lista+"\n")
                                else:
                                    archivo2.write(linea)
                                contador += 1
                        primera_escritura = False
                    else:
                        with open(f"{user}claves2.csv", mode="at", encoding="utf-8") as archivo2:
                            for linea in lineas:
                                if fila == contador:
                                    linea = linea.strip().split(";")
                                    app, usuario, contraseña, lista = linea
                                    usuario = input("➤ Ingrese el nombre de su usuario en la app: ")
                                    archivo2.write(app+";"+usuario+";"+contraseña+";"+lista+"\n")
                                else:
                                    archivo2.write(linea)
                                contador += 1
                    if salir == True:
                        break
            os.replace(f"{user}claves2.csv",f"{user}claves.csv")
        
                
        except OSError:
            raise excepciones.ArchivoNoAccesibleError(COLORES["error"]+"No se pudo abrir el archivo"+COLORES["reset"])
            #print(COLORES["error"]+"No se pudo abrir el archivo"+COLORES["reset"])




def ingresar_aplicacion(user):
    """
Solicita el nombre de la aplicación y lo persiste; permite salir con '-1'.

Parámetros:
    user (str): Usuario propietario del archivo "<user>claves.csv".

Returns:
    int: -1 si el usuario ingresa '-1' para salir; de lo contrario None (efecto: escribe 'app;').

Raises:
    OSError: Si hay problemas de escritura (se maneja aguas arriba con excepciones propias).
"""
    with open(f"{user}claves.csv", mode = "at") as archivo:
        aplicacion = input("\n➤ Ingrese el nombre de la nueva app o '-1' si quiere salir: ")
        if aplicacion == "-1":
            return -1
        else:
            archivo.write(aplicacion+";")



def nueva_cuenta(user):
    """
Orquesta el alta de una cuenta: app → usuario → contraseña.

Parámetros:
    user (str): Usuario propietario del archivo "<user>claves.csv".

Returns:
    None: Sale temprano si el usuario cancela en 'ingresar_aplicacion'.

Notas:
    Cada paso escribe/actualiza la línea correspondiente en "<user>claves.csv".
"""
    if ingresar_aplicacion(user) == -1:
        return
    ingresar_usuario(user)
    ingresar_contraseña(user)
    
def editar(user):
    """
Edita el usuario o la contraseña de una cuenta existente.

Flujo:
    - Llama a buscar(user) para listar y elegir una fila.
    - Pide si se edita usuario (1) o contraseña (2).
    - Delega en ingresar_usuario(...) o ingresar_contraseña(...).

Parámetros:
    user (str): Usuario propietario del archivo "<user>claves.csv".

Returns:
    None

Raises:
    ValueError: Si la opción ingresada no es un entero (se maneja localmente).
    excepciones.ArchivoNoAccesibleError: En caso de I/O al editar.
"""
    fila = buscar(user)

    if fila is None:
        return
    if fila == -1:
        """print(COLORES["alerta"]+"La cuenta que desea editar no existe."+COLORES["reset"])"""
        return
    else:
        try:
            print("Ingrese '1' si quiere editar el usuario o '2' si quiere editar la contraseña.")
            respuesta = int(input("Respuesta: "))
            while respuesta != 1 and respuesta != 2:
                print("❌ Ingreso invalido. Responda nuevamente.")
                respuesta = int(input("Respuesta: "))

            if respuesta == 1:
                ingresar_usuario(user, fila)
            else:
                ingresar_contraseña(user, fila) 
        except ValueError as error2:
            print("Error", error2)       


def buscar(user):
    """
Lista las cuentas disponibles y solicita el índice de la cuenta a operar.

Flujo:
    - Si el archivo no existe o está vacío, informa y devuelve None.
    - Muestra las líneas como "n. App: <app> | Usuario: <usuario>".
    - Pide el número de cuenta o '-1' para salir.
    - Verifica rango válido y existencia de la línea.

Parámetros:
    user (str): Usuario propietario del archivo "<user>claves.csv".

Returns:
    int | None:
        - None si no hay registros.
        - -1 si el usuario cancela.
        - Un entero >= 1 con la fila elegida en caso de éxito.

Raises:
    excepciones.CuentaNoEncontradaError: Si el número elegido excede los registros.
    excepciones.EntradaInvalidaError: Si la entrada no es un número.
    excepciones.ArchivoNoAccesibleError: Si no puede acceder al archivo.
"""
    contador = 1
    encontrado = True

    try:
        with open(f"{user}claves.csv", mode="r", encoding = "utf-8") as archivo:
            
            primera=archivo.readline()
            
            if primera == "" or primera.strip() == "":
                print(COLORES["alerta"] + "⚠ No tenés cuentas guardadas todavía." + COLORES["reset"])
                return None
        
        with open(f"{user}claves.csv", mode="r", encoding="utf-8") as archivo:
            salir = False
            while True:
                lineas = []
                for i in range(10):
                    linea = archivo.readline()
                    if linea == "":
                            salir = True
                            break
                    lineas.append(linea)
                for linea in lineas:
                    linea = linea.strip().split(";")
                    app, usuario, contraseña, lista = linea
                    print(f"{contador}. App:{app}| Usuario: {usuario}")
                    contador +=1
                if salir == True:
                    break
            
    except OSError:
        print(COLORES["alerta"] + "⚠ No tenés cuentas guardadas todavía." + COLORES["reset"])
        return None

    while True:
        try:
            cuenta_a_buscar = int(input("➤ Ingrese el numero de la app que desea editar o borrar o '-1' si desea salir: "))

            if cuenta_a_buscar == -1:
                return -1

            while cuenta_a_buscar < 1:
                cuenta_a_buscar = int(input(COLORES["alerta"]+"Ingrese un numero valido (mayor o igual a '1'): "+COLORES["reset"]))

            with open(f"{user}claves.csv", mode="r", encoding="utf-8") as archivo:
                cantidad_registros = sum(1 for i in archivo)
            
            if cuenta_a_buscar > cantidad_registros:
                raise excepciones.CuentaNoEncontradaError("❌ Número inválido. No existe esa cuenta.")
            
            break
        
        
        except ValueError:
            raise excepciones.EntradaInvalidaError(COLORES["error"]+"Debe ingresar un numero."+COLORES["reset"])
            #print(COLORES["error"]+"Debe ingresar un numero."+COLORES["reset"])
        except OSError:
            raise excepciones.ArchivoNoAccesibleError(COLORES["alerta"]+"⚠ Archivo no encontrado"+ COLORES["reset"])
            #print(COLORES["alerta"]+"⚠ Archivo no encontrado"+ COLORES["reset"])
    
    return cuenta_a_buscar #if encontrado == True else -1 --- Sale por excepciones
    
    
    
def eliminar(user):
    """
Elimina la cuenta seleccionada reescribiendo el archivo sin esa línea.

Flujo:
    - Llama a buscar(user) y obtiene la fila (o None/-1).
    - Copia por bloques a "<user>claves2.csv" omitiendo la fila elegida.
    - Reemplaza "<user>claves.csv" por el temporal.

Parámetros:
    user (str): Usuario propietario del archivo "<user>claves.csv".

Returns:
    None

Raises:
    excepciones.ArchivoNoAccesibleError: Si hay errores de lectura/escritura.
"""
    fila = buscar(user)

    if fila is None:
        return
    '''if fila == -1:
        print(COLORES["error"]+"La cuenta que desea eliminar no existe."+COLORES["reset"])''' #---- BUSCAR SE ENCARGA DE VALIDAR

    try:
        salir = False
        primera_escritura = True
        contador = 1
        with open(f"{user}claves.csv", mode="r", encoding="utf-8") as archivo:
            while True:
                lineas = []
                for i in range(10):
                    linea = archivo.readline()
                    if linea == "":
                            salir = True
                            break
                    lineas.append(linea)

                if primera_escritura == True:
                    with open(f"{user}claves2.csv", mode="wt", encoding="utf-8") as archivo2:
                        for linea in lineas:
                            if fila == contador:
                                pass
                            else:
                                archivo2.write(linea)
                            contador += 1
                    primera_escritura = False
                else:
                    with open(f"{user}claves2.csv", mode="at", encoding="utf-8") as archivo2:
                        for linea in lineas:
                            if fila == contador:
                                pass
                            else:
                                archivo2.write(linea)
                            contador += 1
                if salir == True:
                    break
        os.replace(f"{user}claves2.csv",f"{user}claves.csv")
            
    except OSError:
        raise excepciones.ArchivoNoAccesibleError(COLORES["alerta"]+"⚠ No se pudo abrir el archivo"+ COLORES["reset"])
        #print(COLORES["alerta"]+"⚠ No se pudo abrir el archivo"+ COLORES["reset"])

    print("🗑 ✔ La cuenta fue eliminada.")


def mostrar(user):
    """
Muestra cuentas guardadas y, si se autentica un admin válido, revela las contraseñas originales.

Flujo:
    - Lista "App/Usuario" de "<user>claves.csv".
    - Pide usuario administrador y lee su "<admin>.csv".
    - Verifica la contraseña admin (desencriptándola si corresponde).
    - Si es correcta, recorre "<user>claves.csv" y para cada línea:
        * Parsear cadena_encriptacion → lista de ints (enlistar)
        * desencriptar(contraseña_encriptada, lista) → mostrar en claro.

Parámetros:
    user (str): Usuario cuyas cuentas se mostrarán.

Returns:
    None

Raises:
    excepciones.UsuarioNoExisteError: Si el admin ingresado no existe.
    excepciones.CredencialesInvalidasError: Si la contraseña admin es incorrecta
        o si falla la desencriptación de la contraseña admin.
    excepciones.ArchivoNoAccesibleError: Si no se puede leer "<user>claves.csv".
"""
    contador = 1

    try:
        with open(f"{user}claves.csv", mode="r", encoding="utf-8") as archivo:
            primera=archivo.readline()
            if primera == "" or primera.strip() == "":
                print(COLORES["alerta"] + "⚠ No tenés cuentas guardadas todavía." + COLORES["reset"])
                return
            
            print("\nEstas son tus cuentas guardadas:")

        with open(f"{user}claves.csv", mode="r", encoding="utf-8") as archivo:
            salir = False
            while True:
                lineas = []
                for i in range(10):
                    linea = archivo.readline()
                    if linea == "":
                            salir = True
                            break
                    lineas.append(linea)
                for linea in lineas:
                    linea = linea.strip().split(";")
                    app, usuario, contraseña, lista = linea
                    print(f"{contador}. App:{app}| Usuario: {usuario}")
                    contador +=1
                if salir == True:
                    break

                
    except OSError:
        raise excepciones.ArchivoNoAccesibleError(COLORES["alerta"]+"⚠ No tenés cuentas guardadas todavía"+ COLORES["reset"])
        #print(COLORES["error"]+"No se pudo abrir el archivo"+COLORES["reset"])
    
    usuario_admin = input("\nSi queres ver las contraseñas ingresa el usuario administrador o -1 si queres salir: ").strip()
    if usuario_admin == "-1":
        return
    
    archivo_usuario = f"{usuario_admin}.csv"

    try:
        with open(archivo_usuario, mode="rt", encoding="utf-8") as archivo:
            contraseña = archivo.readline().strip()
    except OSError:
        raise excepciones.UsuarioNoExisteError(COLORES["alerta"]+"Usuario administrador no encontrado."+COLORES["reset"])
    
    if ";" in contraseña:
        try:
            encriptada, lista = contraseña.split(";", 1)
            contraseña_guardada = desencriptar(encriptada, enlistar(lista))
        except Exception:
            raise excepciones.CredencialesInvalidasError(COLORES["error"]+"No se pudo desencriptar la contraseña del usuario administrador."+COLORES["reset"])
            #print(COLORES["error"]+"No se pudo desencriptar la contraseña del usuario administrador."+COLORES["reset"])
            #return
    else:
        contraseña_guardada = contraseña
    
    seguir = input(COLORES["bright"]+"🔐 Contraseña de administrador: "+COLORES["reset"])

    if seguir==contraseña_guardada:
        contador = 1
        try:
            with open(f"{user}claves.csv", mode="r", encoding="utf-8") as archivo:
                salir = False
                while True:
                    lineas = []
                    for i in range(10):
                        linea = archivo.readline()
                        if linea == "":
                                salir = True
                                break
                        lineas.append(linea)
                    for linea in lineas:
                        linea = linea.strip().split(";")
                        app, usuario, contraseña, lista = linea
                        print(f"{contador}. App:{app}| Usuario: {usuario} | Contraseña: {desencriptar(contraseña, enlistar(lista))}")
                        contador +=1
                    if salir == True:
                        break
            
        except OSError:
            raise excepciones.ArchivoNoAccesibleError(COLORES["alerta"]+"⚠ No se pudo abrir el archivo"+ COLORES["reset"])
            #print(COLORES["alerta"]+"⚠ No se pudo abrir el archivo"+ COLORES["reset"])

    else:
        log_event("admin_password_incorrect", "WARN", "Intento de ver contraseñas con admin incorrecto.", usuario=usuario_admin, funcion="mostrar")
        raise excepciones.CredencialesInvalidasError("❌ Contraseña incorrecta. Acceso denegado")
        #print("❌ Contraseña incorrecta. Acceso denegado")

    
def encriptar(clave_original):
    """
Encripta una contraseña generando:
- una clave encriptada aleatoria de igual longitud
- una cadena de deltas (Δtupla|Δpos|Δtupla|Δpos|...) para poder revertirla.

Definiciones:
    - Cada carácter pertenece a una de 4 tuplas: mayúsculas, minúsculas, números, especiales.
    - Para el carácter original y el encriptado de la misma posición i:
        * (t0, p0): índices (tupla, posición) del original.
        * (t1, p1): índices del encriptado.
        * Se guardan Δt = t1 - t0 y Δp = p1 - p0.

Parámetros:
    clave_original (str): Contraseña en texto plano.

Returns:
    tuple[str, str]: (clave_encriptada, cadena_encriptacion)
        - cadena_encriptacion es "Δt0|Δp0|Δt1|Δp1|...".

Notas:
    Este esquema es reversible (ofuscación), no criptografía segura.
"""
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
    """
Revierte la encriptación y reconstruye la contraseña original.

Parámetros:
    clave_encriptada (str): Contraseña encriptada (misma longitud que la original).
    lista_encriptacion (list[int]): Lista de enteros [Δt0, Δp0, Δt1, Δp1, ...],
        obtenida al parsear la cadena "Δt|Δp|...".

Returns:
    str: Contraseña original en texto plano.

Raises:
    ValueError: Si la lista no coincide con 2 * len(clave_encriptada).
"""
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

enlistar = lambda cadena: [int(x) for x in cadena.split("|") if x!=""]
"""
Convierte una cadena 'a|b|c|...' en una lista de enteros [a, b, c, ...], ignorando vacíos.

Parámetros:
    cadena (str): Cadena con enteros separados por '|'.

Returns:
    list[int]: Lista de enteros parseados.
"""