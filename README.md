# API BarrioSeguro
Este proyecto es una API para la gestión de una aplicación de Barrio Seguro, desarrollada con FastAPI y SQLAlchemy.

## Prerrequisitos
**Python**: Asegúrate de tener Python instalado en tu sistema. Puedes descargarlo desde [python.org](https://www.python.org/downloads/).

**Git**: Asegúrate de tener Git instalado para clonar el repositorio. Puedes descargarlo desde [git-scm.com](https://git-scm.com/downloads).

## Instalación

### Paso 1: Clonar el Repositorio

Primero, clona tu repositorio desde GitHub.
```bash
git clone <https://github.com/NunezIvan/Backend-BarrioSeguro>
```

### Paso 2: Crear y Activar un Entorno Virtual
#### En Windows:
```bash
python -m venv env
 cd .\env\Scripts\activate
```
#### En Linux:
```bash
python3 -m venv env
source env/bin/activate
```


### Paso 3: Crear y Activar un Entorno Virtual
Instala todas las dependencias necesarias que están listadas en el archivo requirements.txt.
```bash
pip install -r requirements.txt
```


### Paso 4: Configurar Variables de Entorno
Crea un archivo .env en la raíz del proyecto y define las variables de entorno necesarias. Por ejemplo, para la URL de la base de datos:
```bash
DATABASE_URL=mysql+pymysql://usuario:contraseña@localhost/nombre_base_datos
SECRET_KEY=TuClaveSecretaSuperSecreta
```


### Paso 5: Crear la Base de Datos
Asegúrate de que tu servidor de base de datos esté configurado y funcionando. Luego, crea la base de datos necesaria si aún no existe.

Accede a tu servidor de base de datos y ejecuta:
```bash
CREATE DATABASE nombre_base_datos;
```


### Paso 6: Ejecutar Migraciones
Si estás utilizando migraciones para gestionar tu esquema de base de datos, ejecuta las migraciones necesarias.



### Paso 7: Ejecutar Migraciones
Inicia tu aplicación FastAPI.
```bash
uvicorn src.main:app --reload
```


### Paso 8: Acceder a la Documentación de la API
FastAPI proporciona automáticamente documentación interactiva de la API. Puedes acceder a ella navegando a las siguientes URLs en tu navegador web:
. Swagger UI: http://127.0.0.1:8000/docs
. Redoc: http://127.0.0.1:8000/redoc



## Estructura del proyecto
```bash
<RAIZ_DEL_PROYECTO>/
│
├── .env
├── requirements.txt
├── README.md
├── env/
├── src/
│   ├── main.py
│   ├── config/
│   │   ├── db.py
│   │   ├── utils.py
│   ├── models/
│   │   ├── BarrioSeguro_model.py
│   ├── routers/
│   │   ├── vecinos_routers1.py
│   ├── schema/
│   │   ├── vecinos_schema.py
```

## Diagrama de la Base de Datos

![Diagrama de la Base de Datos](DB_BarrioSeguro_Image.png)


