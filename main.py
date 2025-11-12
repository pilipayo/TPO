import funciones
import excepciones


def main():
    try:
        user, contraseña_guardada = funciones.login()
        funciones.log_event("login_ok", "INFO", "Ingreso correcto.", usuario=user, funcion="login")        
    except excepciones.ContraseñaInvalidaError as e:
        funciones.log_event("weak_pw", "ADV", str(e), usuario="", funcion="login")
        print(funciones.COLORES["alerta"], str(e), funciones.COLORES["reset"])
        return
    except excepciones.UsuarioNoExisteError as e:
        funciones.log_event("login_user_not_found", "WARN", str(e), usuario="", funcion="login")
        print(funciones.COLORES["error"], str(e), funciones.COLORES["reset"])
        return
    except excepciones.CredencialesInvalidasError as e:
        funciones.log_event("login_attempts", "WARN", str(e), usuario="", funcion="login")
        print(funciones.COLORES["error"], str(e), funciones.COLORES["reset"])
        return
    except excepciones.ArchivoNoAccesibleError as e:
        funciones.log_event("io_error", "ERROR", str(e), usuario="", funcion="login")
        print(funciones.COLORES["error"], str(e), funciones.COLORES["reset"])
        return
    except excepciones.ArchivoModificado as e:
        funciones.log_event("io_error", "WARN", str(e), usuario="", funcion="login")
        print(funciones.COLORES["error"], str(e), funciones.COLORES["reset"])
        return
        
        #Entramos correctamente en la app.

    while True:
        funciones.menu()        
        try:
            accion = int(input( "👉 Ingrese el número de la tarea que desea realizar: " ))
        except ValueError:
            print(funciones.COLORES["alerta"] + "⚠ Ingrese nuevamente un número válido." + funciones.COLORES["reset"])
            continue
        try:
            if accion == 1:
                funciones.limpiar_pantalla()
                funciones.nueva_cuenta(user)
                funciones.log_event("account_added", "INFO", "Cuenta agregada.", usuario=user, funcion="nueva_cuenta")
            elif accion == 2:
                funciones.limpiar_pantalla()
                funciones.editar(user)
                funciones.log_event("account_edited", "INFO", "Cuenta editada.", usuario=user, funcion="editar")
            elif accion == 3:
                funciones.limpiar_pantalla()
                funciones.eliminar(user)
                funciones.log_event("account_deleted", "INFO", "Cuenta eliminada.", usuario=user, funcion="eliminar")
            elif accion == 4:
                funciones.limpiar_pantalla()
                funciones.mostrar(user)
            elif accion == 0:
                funciones.limpiar_pantalla()
                print(funciones.COLORES["bright"]+"\n👋 SALISTE DEL SISTEMA\n"+funciones.COLORES["reset"])
                break
            else:
                print(funciones.COLORES["error"] +"❌ Opción invalida"+funciones.COLORES["reset"])

        except excepciones.ContraseñaInvalidaError as e:
            funciones.log_event("weak_password", "WARN", str(e), usuario=user, funcion="menu")
            print(funciones.COLORES["alerta"], str(e), funciones.COLORES["reset"])
        except excepciones.CuentaNoEncontradaError as e:
            funciones.log_event("account_not_found", "WARN", str(e), usuario=user, funcion="menu")
            print(funciones.COLORES["error"], str(e), funciones.COLORES["reset"])
        except excepciones.EntradaInvalidaError as e:
            funciones.log_event("invalid_input", "WARN", str(e), usuario=user, funcion="menu")
            print(funciones.COLORES["alerta"], str(e), funciones.COLORES["reset"])
        except excepciones.CredencialesInvalidasError as e:
            funciones.log_event("admin_password_incorrect", "WARN", str(e), usuario=user, funcion="mostrar")
            print(funciones.COLORES["error"], str(e), funciones.COLORES["reset"])
        except excepciones.UsuarioNoExisteError as e:
            funciones.log_event("login_user_not_found", "WARN", str(e), usuario=user, funcion="mostrar")
            print(funciones.COLORES["error"], str(e), funciones.COLORES["reset"])
        except excepciones.ArchivoNoAccesibleError as e:
            funciones.log_event("io_error", "ERROR", str(e), usuario=user, funcion="*")
            print(funciones.COLORES["error"], str(e), funciones.COLORES["reset"])
        except Exception as e:
            funciones.log_event("unespected_error", "ERROR", str(e), usuario=user, funcion="*")
            print(funciones.COLORES["error"], f"Error inesperado: {e}", funciones.COLORES["reset"])     #---- por las dudas
    

if __name__ == "__main__": 
    main()