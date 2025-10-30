# ==== Excepciones personalizadas ====
class UsuarioNoExisteError(Exception):
    """Se dispara cuando el usuario administrador no existe en el sistema."""
    pass

class CredencialesInvalidasError(Exception):
    """Se dispara cuando la contraseña es incorrecta o no se puede validar/desencriptar."""
    pass

class ArchivoNoAccesibleError(Exception):
    """Se dispara cuando no se puede leer/escribir un archivo requerido."""
    pass

class CuentaNoEncontradaError(Exception):
    """Se dispara cuando la cuenta solicitada no existe o el índice es inválido."""
    pass

class EntradaInvalidaError(Exception):
    """Se dispara cuando el usuario ingresa un dato con formato inválido."""
    pass
class ContraseñaInvalidaError(Exception):
    """Se dispara cuando la contraseña no cumple los requisitos mínimos."""
    pass
class ArchivoModificado(Exception):
    """Se dispara cuando el archivo está siendo abierto por otro usuario."""
    pass

