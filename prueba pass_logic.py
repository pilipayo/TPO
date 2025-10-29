import pass_logic

try:
    user = "Luis"
    contraseña, lista = pass_logic.ingresar_contraseña()

    print(contraseña)

    contraseña1= pass_logic.crear_contraseña()

    print(contraseña1)

    print(pass_logic.desencriptar(contraseña,pass_logic.enlistar(lista)))

except pass_logic.ContraseñaInvalidaError as e:
    pass_logic.log_event("weak_password", "WARN", str(e), usuario=user, funcion="menu")
    print(pass_logic.COLORES["alerta"], str(e), pass_logic.COLORES["reset"])
except pass_logic.CuentaNoEncontradaError as e:
    pass_logic.log_event("account_not_found", "WARN", str(e), usuario=user, funcion="menu")
    print(pass_logic.COLORES["error"], str(e), pass_logic.COLORES["reset"])
except pass_logic.EntradaInvalidaError as e:
    pass_logic.log_event("invalid_input", "WARN", str(e), usuario=user, funcion="menu")
    print(pass_logic.COLORES["alerta"], str(e), pass_logic.COLORES["reset"])
except pass_logic.CredencialesInvalidasError as e:
    pass_logic.log_event("admin_password_incorrect", "WARN", str(e), usuario=user, funcion="mostrar")
    print(pass_logic.COLORES["error"], str(e), pass_logic.COLORES["reset"])
except pass_logic.UsuarioNoExisteError as e:
    pass_logic.log_event("login_user_not_found", "WARN", str(e), usuario=user, funcion="mostrar")
    print(pass_logic.COLORES["error"], str(e), pass_logic.COLORES["reset"])
except pass_logic.ArchivoNoAccesibleError as e:
    pass_logic.log_event("io_error", "ERROR", str(e), usuario=user, funcion="*")
    print(pass_logic.COLORES["error"], str(e), pass_logic.COLORES["reset"])
except Exception as e:
    pass_logic.log_event("unespected_error", "ERROR", str(e), usuario=user, funcion="*")
    print(pass_logic.COLORES["error"], f"Error inesperado: {e}", pass_logic.COLORES["reset"]) 