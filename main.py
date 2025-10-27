import funciones


def main():
    
    user, contraseña_guardada = funciones.login()        

    if user is None:
        print(funciones.COLORES["error"] + "⛔ Acceso denegado." + funciones.COLORES["reset"])
        return
    
    while True:
        funciones.menu()        
        try:
            accion = int(input( "👉 Ingrese el número de la tarea que desea realizar: " ))
        except ValueError:
            print(funciones.COLORES["alerta"] + "⚠ Ingrese nuevamente un número válido." + funciones.COLORES["reset"])
            continue

        if accion == 1:
            funciones.limpiar_pantalla()
            funciones.nueva_cuenta()
        elif accion == 2:
            funciones.limpiar_pantalla()
            funciones.editar()
        elif accion == 3:
            funciones.limpiar_pantalla()
            funciones.eliminar()
        elif accion == 4:
            funciones.limpiar_pantalla()
            funciones.mostrar()
        elif accion == 0:
            funciones.limpiar_pantalla()
            print(funciones.COLORES["bright"]+"\n👋 SALISTE DEL SISTEMA\n"+funciones.COLORES["reset"])
            break
        else:
            print(funciones.COLORES["error"] +"❌ Opción invalida"+funciones.COLORES["reset"])
        
if __name__ == "__main__": 
    main()
