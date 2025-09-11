BIENVENIDO A ~PASSLOGIC~
      by FormidableTech

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

Para la ejecución:
A. Ejecutar main.py
B. Iniciar sesión con el usuario administrador por defecto:
Usuario: admin
Contraseña: 1234
C. Uso del menú principal:
0 - Salir
1 - Agregar
2 - Editar
3 - Eliminar
4 - Mostrar

Ejemplo de flujo de uso
1.⁠ ⁠Seleccionar 'Agregar' (opción 1).
2.⁠ ⁠Ingresar el nombre de la aplicación, el usuario y la contraseña (manual o generada automáticamente).
3.⁠ ⁠Seleccionar 'Editar' para modificar un registro (opción 2).
4.⁠ ⁠Seleccionar 'Eliminar' para borrar un registro (opción 3).
   - Si eliminás todas las cuentas, agregá una nueva (opción 1) para poder probar la función 'Mostrar' con datos.
5.⁠ ⁠Seleccionar 'Mostrar' para listar todas las cuentas con la contraseña censurada por defecto.
6.⁠ ⁠Si querés ver las contraseñas en claro, deberás ingresar nuevamente la contraseña maestra de administrador.