# Seguridad de Base de Datos - Servidor HTTP

Este proyecto consiste en un servidor HTTP simple desarrollado con FastAPI para la clase de **Seguridad de Base de Datos**. El servidor permite realizar consultas a una base de datos MySQL y está diseñado para demostrar conceptos de seguridad como la Inyección de SQL y el Principio de Menor Privilegio.

## Requisitos Previos

* Python 3.7+
* Una instancia de base de datos MySQL activa (con las tablas `country` y `city`).

## Instalación

Para instalar las dependencias necesarias, ejecuta el siguiente comando en tu terminal:

```bash
pip install fastapi uvicorn sqlalchemy pymysql cryptography python-dotenv
```

## Configuración

Creen un archivo llamado `.env` en la raíz del proyecto con las credenciales especificadas en la tarea:

```env
DB_USER=usuario
DB_PASSWORD=contraseña
DB_HOST=direccion
DB_NAME=world
```

## Ejecución

Para iniciar el servidor, utiliza `uvicorn`:

```bash
uvicorn server:app --reload
```

El servidor estará disponible en `http://127.0.0.1:8000`.

## Endpoints

El servidor expone las siguientes rutas:

* **GET `/countries`**: Obtiene la lista de países utilizando el ORM de SQLAlchemy (Consulta segura).
* **GET `/cities`**: Obtiene la lista de ciudades. Este endpoint se utiliza para demostrar el **Principio de Menor Privilegio** (fallará si el usuario de la DB no tiene permisos de lectura sobre la tabla `city`).
* **GET `/buscar?nombre=Nombre`**: Busca una ciudad por su nombre. 
    * **⚠️ Advertencia:** Este endpoint es vulnerable a **SQL Injection** de forma intencional para fines educativos, ya que utiliza concatenación directa de strings en la consulta.
