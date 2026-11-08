# Agenda de Contactos con Acceso Aleatorio
---

## Requisitos Mínimos del Sistema

### Hardware
* **Procesador:** x86_64 o ARM de 1 GHz o superior.
* **Memoria RAM:** 512 MB disponibles (2 GB recomendados).
* **Almacenamiento:** 50 MB de espacio libre en disco para el entorno, dependencias, archivos de datos y respaldos.

### Software y Entorno
* **Sistema Operativo:** Windows 10/11, Linux (Ubuntu/Debian/Fedora) o macOS.
* **Intérprete:** Python 3.8 o superior.
* **Módulos nativos incluidos:** `os`, `json`, `hashlib`, `zipfile`, `datetime`, `tkinter`.
* **Librerías externas:** `fpdf` / `fpdf2` (para la generación de reportes en PDF).

> **Nota para usuarios de Linux (Ubuntu/Debian):** Si `tkinter` no viene preinstalado con tu distribución de Python, instálalo ejecutando:
> ```bash
> sudo apt-get update && sudo apt-get install python3-tk
> ```

---

## Proceso de Ejecución

Sigue estos pasos desde la terminal para clonar y ejecutar el proyecto localmente:

### 1. Clonar el repositorio
```bash
git clone <https://github.com/JaviRexUITU25/ArchivosP2.git>
