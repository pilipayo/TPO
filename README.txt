PROYECTO: Gestor de Contraseñas con Encriptación y Manejo de Usuarios
=====================================================================

DESCRIPCIÓN GENERAL
────────────────────
Este programa permite gestionar contraseñas personales de manera segura. 
Cada usuario tiene su propio archivo cifrado donde se guardan las credenciales 
de distintas aplicaciones. El sistema ofrece funciones para crear, editar, 
eliminar y mostrar cuentas, así como validar la seguridad de las contraseñas 
y generar nuevas de forma automática.

El proyecto se compone de tres módulos:
- main.py → Punto de entrada del programa.
- funciones.py → Lógica principal (login, validación, encriptación, manejo de archivos, menú, etc.).
- excepciones.py → Definición de excepciones personalizadas para el control de errores.

CARACTERÍSTICAS PRINCIPALES
────────────────────────────
• Login seguro con encriptación de usuario y contraseña.
• Creación automática de contraseñas aleatorias y seguras.
• Validación de contraseñas con nivel de robustez (Débil, Intermedia, Fuerte).
• Gestión de cuentas por aplicación (agregar, editar, eliminar, mostrar).
• Acceso restringido a contraseñas mediante usuario administrador.
• Registro de eventos (logs) en archivo CSV con nivel de severidad y timestamp.
• Interfaz de consola con colores gracias a Colorama.
• Manejo robusto de errores mediante excepciones personalizadas.

REQUISITOS DEL SISTEMA
──────────────────────
- Python 3.8 o superior
- Librerías externas:
    colorama

INSTALACIÓN DE DEPENDENCIAS
────────────────────────────
Ejecutar en la terminal:
    pip install colorama

ARQUITECTURA DEL PROYECTO
──────────────────────────
📁 Proyecto/
│
├── main.py             → Archivo principal, contiene la función main().
├── funciones.py        → Funciones auxiliares y lógica del programa.
├── excepciones.py      → Excepciones personalizadas.
│
├── eventos_log.csv     → Archivo generado automáticamente con registros del sistema.
├── [usuario].csv       → Archivo cifrado del administrador.
├── [usuario]claves.csv → Archivo de contraseñas del usuario.
└── [usuario]claves2.csv→ Archivo temporal para operaciones de edición o eliminación.

EJECUCIÓN
─────────
1. Abrir una terminal en la carpeta del proyecto.
2. Ejecutar:
       python main.py
3. Iniciar sesión con un usuario existente o crear uno nuevo.
4. Usar el menú para:
   - (1) Agregar cuenta
   - (2) Editar cuenta
   - (3) Eliminar cuenta
   - (4) Mostrar cuentas
   - (0) Salir

MANEJO DE ERRORES
──────────────────
El sistema utiliza el módulo “excepciones.py” con clases específicas:
- UsuarioNoExisteError
- CredencialesInvalidasError
- ArchivoNoAccesibleError
- CuentaNoEncontradaError
- EntradaInvalidaError
- ContraseñaInvalidaError
- ArchivoModificado

Cada error es capturado por main.py y registrado automáticamente mediante log_event() 
en el archivo eventos_log.csv.

DESARROLLADOR
──────────────
Autor: FormidableTechnologies
Año: 2025
