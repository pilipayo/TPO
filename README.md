# 🔐 Gestor de Contraseñas con Encriptación y Manejo de Usuarios

## 📘 Descripción General
Este proyecto implementa un **gestor de contraseñas seguro** que permite crear, editar, eliminar y mostrar contraseñas de diferentes aplicaciones, protegidas por un **usuario administrador**.  
Las contraseñas se validan según su robustez y se pueden generar de forma aleatoria.

El programa está dividido en tres módulos principales:

- **`main.py`** → Control principal del flujo del programa.  
- **`funciones.py`** → Lógica del sistema, validaciones, encriptación, manejo de archivos y menú.  
- **`excepciones.py`** → Excepciones personalizadas que facilitan el control de errores.

---

## ⚙️ Características Principales
- Login seguro con encriptación de credenciales.  
- Generación de contraseñas aleatorias seguras.  
- Validación con nivel de robustez (Débil, Intermedia, Fuerte).  
- Gestión de cuentas personales (agregar, editar, eliminar, mostrar).  
- Registro de eventos en `eventos_log.csv`.  
- Interfaz con colores (usando **Colorama**).  
- Manejo de errores mediante excepciones propias.

---

## 🧱 Requisitos del Sistema
- **Python** 3.8 o superior  
- **Dependencias externas**:
  ```bash
  pip install colorama
  ```

---

## 📂 Estructura del Proyecto
```
📁 GestorContraseñas/
│
├── main.py              # Punto de entrada del programa
├── funciones.py         # Lógica, encriptación, validación y menú
├── excepciones.py       # Excepciones personalizadas
│
├── eventos_log.csv      # Registro automático de eventos
├── [usuario].csv        # Archivo cifrado del usuario administrador
├── [usuario]claves.csv  # Contraseñas almacenadas
└── [usuario]claves2.csv # Archivo temporal para edición
```

---

## 🚀 Ejecución
1. Abrir la terminal en la carpeta del proyecto.  
2. Ejecutar:
   ```bash
   python main.py
   ```
3. Iniciar sesión o crear un usuario nuevo.  
4. Usar el menú para seleccionar una opción:
   - `1` → Agregar cuenta  
   - `2` → Editar cuenta  
   - `3` → Eliminar cuenta  
   - `4` → Mostrar cuentas  
   - `0` → Salir  

---

## ⚡ Manejo de Errores
El módulo `excepciones.py` contiene las siguientes clases:

- `UsuarioNoExisteError`
- `CredencialesInvalidasError`
- `ArchivoNoAccesibleError`
- `CuentaNoEncontradaError`
- `EntradaInvalidaError`
- `ContraseñaInvalidaError`
- `ArchivoModificado`

Cada excepción es registrada mediante `log_event()` en el archivo `eventos_log.csv`.

---

## 👨‍💻 Autor: FormidableTech
Integrantes del equipo 4:
-IGNACIO STAMATI
-PAYO MARIA DEL PILAR
-PLUT JUAN IGNACIO
-SCIOLETTI BRERO NICOLAS
Versión **1.0 — 2025**  

