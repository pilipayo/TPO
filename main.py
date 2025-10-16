import funciones
import os
import platform

def limpiar_pantalla():
    if platform.system() == "Windows":
        os.system("cls")
    else:
        os.system("clear")

def main():
    if funciones.login():
        while True:
            funciones.menu()        
            """while accion < 0 or accion > 5"""
            try:
                accion = int(input("Ingrese el número de la tarea que desea realizar: "))
            except ValueError:
                print("Ingrese nuevamente: ")
                continue

            if accion == 1:
                limpiar_pantalla()
                funciones.nueva_cuenta()
            elif accion == 2:
                limpiar_pantalla()
                funciones.editar()
            elif accion == 3:
                limpiar_pantalla()
                funciones.eliminar()
            elif accion == 4:
                limpiar_pantalla()
                funciones.mostrar()
            elif accion == 0:
                limpiar_pantalla()
                print("\nSALISTE DEL SISTEMA\n")
                break
            else:
                print("Opción invalida")
        
if __name__ == "__main__": 
    main()
