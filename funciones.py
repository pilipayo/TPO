import random
import os
import platform
import excepciones
from datetime import datetime
from colorama import Fore, Style, init
init()

def log_event(evento, nivel="INFO", mensaje="", usuario="", funcion="", extra="", filename=None):
    """
    Registramos eventos en nuestro .csv
    Columnas: fecha_iso;nivel;evento;usuario;funcion;mensaje;extra
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
    """Solicitamos al usuario ingresar usuario y contraseña del administrador"""

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
                    enc, lista = contraseña_archivada.split(";", 1)
                    contraseña_guardada = desencriptar(enc, enlistar(lista))
                except Exception:
                    raise excepciones.CredencialesInvalidasError(COLORES["error"]+"✖ Error al desencriptar la contraseña guardada."+ COLORES["reset"])
                    #print(COLORES["error"]+"✖ Error al desencriptar la contraseña guardada."+ COLORES["reset"])
                    #return None, None
            else:
                contraseña_guardada= contraseña_archivada

            intentos=3

            while intentos>0:
                contraseña_ingresada = input(COLORES["bright"]+"🔐 Contraseña: "+COLORES["reset"])
            
                if contraseña_ingresada == contraseña_guardada:
                    print(COLORES["bright"]+f"\nBienvenido, {user}!"+COLORES["reset"])
                    return user, contraseña_guardada
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
            enc, lista = encriptar(nuevaContraseña)

            with open(archivo_usuario, mode = "wt", encoding="utf-8") as archivo:
                archivo.write(f"{enc};{lista}\n")
            print(COLORES["ok"]+"✅ Cuenta creada exitosamente!"+ COLORES["reset"])
            print(COLORES["bright"]+f"\nBienvenido, {user}!"+COLORES["reset"])
            return user, nuevaContraseña
        
        except OSError:
            raise excepciones.ArchivoNoAccesibleError(COLORES["error"]+"❌ No se pudo crear el archivo"+COLORES["reset"])
            #print(COLORES["error"]+"❌ No se pudo crear el archivo"+COLORES["reset"])
            #return None, None
            
    

def menu():
    """Muestra el Menu con las 5 opciones posibles: Salir, Agregar, Editar, Eliminar y Mostrar"""

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


def validar(contraseña, largo_min=12):
    """
    Valida que la contraseña cumpla con todos los requisitos mínimos.
    Si falta alguno, levanta ContraseñaInvalidaError con detalles.
    Si pasa, calcula y muestra el nivel de robustez: Débil / Intermedia / Fuerte.
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
    """Le pedimos al usuario que ingrese su contraseña o que cree una contraseña aleatoria más segura"""
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
                        with open(f"{user}claves.csv", mode = "rt", encoding="utf-8") as archivo:
                            lineas = archivo.readlines()
                            linea_a_editar = lineas[fila-1]
                            linea_a_editar = linea_a_editar.strip()
                            app, usuario, contraseña, lista = linea_a_editar.split(";")
                            lineas.pop(fila-1)
                        with open(f"{user}claves.csv", mode = "wt", encoding="utf-8") as archivo:
                            for i in lineas:
                                archivo.write(i)

                        with open(f"{user}claves.csv", mode = "at", encoding="utf-8") as archivo:
                            archivo.write(app+";"+usuario+";"+contraseña_encriptada+";"+lista_encriptacion+"\n")
                            
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
                    with open(f"{user}claves.csv", mode = "rt", encoding="utf-8") as archivo:
                        lineas = archivo.readlines()
                        linea_a_editar = lineas[fila-1]
                        linea_a_editar = linea_a_editar.strip()
                        app, usuario, contraseña, lista = linea_a_editar.split(";")
                        lineas.pop(fila-1)
                    with open(f"{user}claves.csv", mode = "wt", encoding="utf-8") as archivo:
                        for i in lineas:
                            archivo.write(i)

                    with open(f"{user}claves.csv", mode = "at", encoding="utf-8") as archivo:
                        archivo.write(app+";"+usuario+";"+contraseña_encriptada+";"+lista_encriptacion+"\n")
                        
                except OSError:
                    raise excepciones.ArchivoNoAccesibleError(COLORES["error"]+"No se pudo abrir el archivo"+COLORES["reset"])
                    #print(COLORES["error"]+"No se pudo abrir el archivo"+COLORES["reset"])
            break


def ingresar_usuario(user, fila = -1):
    """Permite al usuario ingresar su nombre de usuario"""
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
            with open(f"{user}claves.csv", mode = "rt", encoding="utf-8") as archivo:
                lineas = archivo.readlines()
                linea_a_editar = lineas[fila-1]
                linea_a_editar = linea_a_editar.strip()
                app, usuario, contraseña, lista = linea_a_editar.split(";")
                usuario = input("➤ Ingrese el nombre de su usuario en la app: ")
                lineas.pop(fila-1)
                print(lineas)
            with open(f"{user}claves.csv", mode = "wt", encoding="utf-8") as archivo:
                for i in lineas:
                    archivo.write(i)

            with open(f"{user}claves.csv", mode = "at", encoding="utf-8") as archivo:
                archivo.write(app+";"+usuario+";"+contraseña+";"+lista+"\n")
                
        except OSError:
            raise excepciones.ArchivoNoAccesibleError(COLORES["error"]+"No se pudo abrir el archivo"+COLORES["reset"])
            #print(COLORES["error"]+"No se pudo abrir el archivo"+COLORES["reset"])




def ingresar_aplicacion(user):
    """Permite al usuario ingresar el nombre de la aplicación"""
    with open(f"{user}claves.csv", mode = "at") as archivo:
        aplicacion = input("\n➤ Ingrese el nombre de la nueva app o '-1' si quiere salir: ")
        if aplicacion == "-1":
            return -1
        else:
            archivo.write(aplicacion+";")



def nueva_cuenta(user):
    """Creamos una nueva cuenta utilizando las funciones creadas anteriormente"""
    if ingresar_aplicacion(user) == -1:
        return
    ingresar_usuario(user)
    ingresar_contraseña(user)
    
def editar(user):
    """Editamos el usuario o contraseña ya guardados"""
    fila = buscar(user)

    if fila is None:
        return
    if fila == -1:
        print(COLORES["alerta"]+"La cuenta que desea editar no existe."+COLORES["reset"])
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
    "Busca la aplicación tanto en mayuscula como minuscula"
    contador = 1
    encontrado = True
    try:
        with open(f"{user}claves.csv", mode="r", encoding = "utf-8") as archivo:
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
        raise excepciones.ArchivoNoAccesibleError(COLORES["error"]+"No se pudo abrir el archivo"+COLORES["reset"])
        #print(COLORES["alerta"]+"⚠ No se pudo abrir el archivo"+ COLORES["reset"])

    while True:
        try:
            cuenta_a_buscar = int(input("➤ Ingrese el numero de la app que desea editar o borrar o '-1' si desea salir: "))

            if cuenta_a_buscar == -1:
                return

            while cuenta_a_buscar < 1:
                cuenta_a_buscar = int(input(COLORES["alerta"]+"Ingrese un numero valido (mayor o igual a '1'): "+COLORES["reset"]))

            with open(f"{user}claves.csv", mode="r", encoding="utf-8") as archivo:
                cantidad_registros = sum(1 for i in archivo)
            
            if cuenta_a_buscar > cantidad_registros:
                raise excepciones.CuentaNoEncontradaError("❌ Número inválido. No existe esa cuenta.")
            
                '''print("❌ Numero inválido")
                encontrado = False'''
            break
        
        
        except ValueError:
            raise excepciones.EntradaInvalidaError(COLORES["error"]+"Debe ingresar un numero."+COLORES["reset"])
            #print(COLORES["error"]+"Debe ingresar un numero."+COLORES["reset"])
        except OSError:
            raise excepciones.ArchivoNoAccesibleError(COLORES["alerta"]+"⚠ Archivo no encontrado"+ COLORES["reset"])
            #print(COLORES["alerta"]+"⚠ Archivo no encontrado"+ COLORES["reset"])
    
    return cuenta_a_buscar #if encontrado == True else -1 --- Sale por excepciones
    
    
    
def eliminar(user):
    "Eliminamos la cuenta buscada"
    fila = buscar(user)

    if fila is None:
        return
    '''if fila == -1:
        print(COLORES["error"]+"La cuenta que desea eliminar no existe."+COLORES["reset"])''' #---- BUSCAR SE ENCARGA DE VALIDAR

    try:
        with open(f"{user}claves.csv", mode = "rt", encoding="utf-8") as archivo:
            lineas = archivo.readlines()
            # ------ PARA EL LOG, capturamos detalle de cuenta a eliminar:
            detalle = ""
            try:
                partes = lineas[fila-1].strip().split(";")   # si tu código usa fila-1, mantenelo así
                if len(partes) == 4:
                    app, usuario_cuenta, _contraseña, _lista = partes
                    detalle = "app=" + app + ";usuario_cuenta=" + usuario_cuenta
            except Exception:
                detalle = ""
                    
            lineas.pop(fila-1)
        with open(f"{user}claves.csv", mode = "wt", encoding="utf-8") as archivo:
            for i in lineas:
                archivo.write(i)
            
    except OSError:
        raise excepciones.ArchivoNoAccesibleError(COLORES["alerta"]+"⚠ No se pudo abrir el archivo"+ COLORES["reset"])
        #print(COLORES["alerta"]+"⚠ No se pudo abrir el archivo"+ COLORES["reset"])

    print("🗑 ✔ La cuenta fue eliminada.")


def mostrar(user):
    """Mostramos todas las contraseñas, primero ocultas y cuando ingrese la contraseña maestra se muestran completas."""
    contador = 1
    print("\nEstas son tus cuentas guardadas:")
    try:
        with open(f"{user}claves.csv", mode="r", encoding="utf-8") as archivo:
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
        raise excepciones.ArchivoNoAccesibleError(COLORES["alerta"]+"⚠ No se pudo abrir el archivo"+ COLORES["reset"])
        #print(COLORES["error"]+"No se pudo abrir el archivo"+COLORES["reset"])
    
    usuario_admin = input("\nSi queres ver las contraseñas ingresa el usuario administrador: ").strip()
    archivo_usuario = f"{usuario_admin}.csv"

    try:
        with open(archivo_usuario, mode="rt", encoding="utf-8") as f:
            contraseña = f.readline().strip()
    except OSError:
        raise excepciones.UsuarioNoExisteError(COLORES["alerta"]+"Usuario administrador no encontrado."+COLORES["reset"])
        #print(COLORES["alerta"]+"Usuario administrador no encontrado."+COLORES["reset"])
        #return
    
    if ";" in contraseña:
        try:
            enc, lista = contraseña.split(";", 1)
            contraseña_guardada = desencriptar(enc, enlistar(lista))
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
            with open(f"{user}claves.csv", mode="r", encoding = "utf-8") as archivo:
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
            raise excepciones.ArchivoNoAccesibleError(COLORES["alerta"]+"⚠ No se pudo abrir el archivo"+ COLORES["reset"])
            #print(COLORES["alerta"]+"⚠ No se pudo abrir el archivo"+ COLORES["reset"])

    else:
        log_event("admin_password_incorrect", "WARN", "Intento de ver contraseñas con admin incorrecto.", usuario=usuario_admin, funcion="mostrar")
        raise excepciones.CredencialesInvalidasError("❌ Contraseña incorrecta. Acceso denegado")
        #print("❌ Contraseña incorrecta. Acceso denegado")

    
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

enlistar = lambda cadena: [int(x) for x in cadena.split("|") if x!=""]