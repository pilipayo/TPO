import funciones

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
                funciones.nueva_cuenta() 
            elif accion == 2:
                funciones.editar()
            elif accion == 3:
                funciones.eliminar()
            elif accion == 4:
                funciones.mostrar()
            elif accion == 0: 
                print("\nSALISTE DEL SISTEMA\n")
                break
            else:
                print("Opción invalida")
        
if __name__ == "__main__": 
    main()