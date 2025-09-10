BIENVENIDO A ~PASSLOGIC~

Este proyecto es un gestor de contraseñas simple en consola escrito en Python.
Permite crear, almacenar, editar y eliminar contraseñas de manera segura, además de generar contraseñas aleatorias robustas con criterios de seguridad.

Integrantes del equipo 4:
-IGNACIO STAMATI
-PAYO MARIA DEL PILAR
-PLUT JUAN IGNACIO
-SCIOLETTI NICOLAS


Características:

-Login de administrador (usuario y contraseña predefinidos).

-Gestión de cuentas: agregar, editar, eliminar y mostrar cuentas guardadas.

-Generación automática de contraseñas seguras: incluye mayúsculas, minúsculas, números y caracteres especiales.

-Validación de contraseñas:

    Mínimo 12 caracteres.

    Al menos 1 número.

    Al menos 1 carácter especial.

    Al menos 1 letra minúscula.

    Al menos 1 letra mayúscula.

-Protección extra: se requiere la clave del administrador para visualizar las contraseñas guardadas.


Estructura del Código:

login(): Ingreso al sistema como administrador.

menu(): Menú principal con opciones.

crear_contraseña(): Genera una contraseña aleatoria segura.

validar(): Verifica que una contraseña cumpla con los criterios de seguridad.

nueva_cuenta(): Permite registrar una nueva aplicación, usuario y contraseña.

editar(): Modifica usuario o contraseña de una app registrada.

eliminar(): Elimina una cuenta.

mostrar(): Muestra todas las cuentas guardadas (solo con validación de admin).


Para la ejecución:
Ingresa con el usuario maestro:

Usuario: admin
Contraseña: 1234