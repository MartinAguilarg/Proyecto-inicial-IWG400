# Proyecto Inicial IWG400 – Plataforma de fútbol amateur

Aplicación web desarrollada con **Python y Django** para conectar equipos de fútbol amateur, permitir el envío de desafíos, coordinar partidos y registrar sus resultados.

## Requisitos y dependencias

Para ejecutar el proyecto se necesita:

- **Python 3.14.3** o una versión compatible.
- **Django 6.1.2**, framework utilizado para desarrollar la aplicación.
- **SQLite**, sistema de base de datos utilizado por el proyecto, incluido en las instalaciones habituales de Python.

No es necesario instalar SQLite por separado.

## Instalación y ejecución local

Los siguientes pasos están pensados para Windows utilizando **Visual Studio Code**.

### 1. Descargar el repositorio

Descargar el repositorio en formato ZIP y extraer su contenido.

Luego, abrir en Visual Studio Code la carpeta `Proyecto-inicial-IWG400-main`, que contiene el archivo `manage.py`.

### 2. Abrir una terminal

En Visual Studio Code, seleccionar:

**Terminal → New Terminal**

Verificar que la terminal se encuentre en la carpeta donde está el archivo `manage.py`, ejecutando:

```powershell
dir
```

En la carpeta deben aparecer el archivo `manage.py` y las carpetas `proyecto`, `torneo` y `login`.

Si la terminal no está ubicada en esa carpeta, utilizar el comando `cd` para ingresar a ella. Por ejemplo:

```powershell
cd Proyecto-inicial-IWG400-main
```

### 3. Instalar Django

Ejecutar el siguiente comando en la terminal:

```powershell
python -m pip install Django==6.1.2
```

### 4. Crear la base de datos

Ejecutar las migraciones de Django para crear las tablas necesarias:

```powershell
python manage.py migrate
```

### 5. Iniciar el servidor

Ejecutar:

```powershell
python manage.py runserver
```

La terminal mostrará una dirección local similar a:

```text
http://127.0.0.1:8000/
```

Abrir esa dirección en un navegador para acceder a la aplicación.

Para detener el servidor, presionar `Ctrl + C` en la terminal.

## Datos para probar la funcionalidad corazón

El repositorio no incluye una base de datos con usuarios o equipos de demostración. Cada persona debe crear sus propios datos de prueba desde la aplicación.

### 1. Crear los equipos

Para probar el funcionamiento se necesitan al menos dos equipos, cada uno asociado a una cuenta de capitán.

1. Ingresar a la aplicación desde el navegador.
2. Seleccionar la opción de registro y crear una cuenta para el primer capitán.
3. Iniciar sesión y registrar el primer equipo.
4. Cerrar sesión y crear una segunda cuenta para el capitán del equipo rival.
5. Iniciar sesión con la segunda cuenta y registrar el segundo equipo.

Los equipos nuevos comienzan con una puntuación Elo de 1000.

Se recomienda crear al menos tres equipos con distintos puntajes Elo para observar las recomendaciones de rivales en el radar.

### 2. Probar el envío y aceptación de desafíos

1. Iniciar sesión con uno de los capitanes.
2. Ingresar al radar para consultar los equipos rivales recomendados según su nivel competitivo.
3. Seleccionar un equipo y enviarle un desafío.
4. Cerrar sesión e ingresar con la cuenta del capitán del equipo desafiado.
5. Revisar la bandeja de desafíos y aceptar la solicitud.
6. Ingresar a la sección de coordinación para proponer una fecha, hora y lugar para el partido.
7. El otro capitán debe responder a la propuesta para completar la coordinación.

La fecha, hora y lugar se acuerdan después de aceptar el desafío, y no forman parte de la solicitud inicial.

### 3. Probar el registro y validación de resultados

Una vez coordinado el partido, ambos capitanes pueden registrar el marcador desde la sección correspondiente.

Se pueden probar los siguientes escenarios:

**Caso 1: Resultados coincidentes**

- El capitán del equipo 1 registra un resultado de 1-2.
- El capitán del equipo 2 registra el mismo resultado: 1-2.
- El sistema compara ambos registros, confirma el partido y actualiza los puntajes Elo de los equipos.

**Caso 2: Resultados diferentes**

- El capitán del equipo 1 registra un resultado de 1-6.
- El capitán del equipo 2 registra un resultado diferente: 1-2.
- El sistema detecta la discrepancia, deja el partido en estado de disputa y no actualiza los puntajes Elo.

## Base de datos

El proyecto utiliza **SQLite** para almacenar la información de usuarios, equipos, desafíos y partidos.

El archivo `db.sqlite3` se genera localmente al ejecutar las migraciones y no está incluido en el repositorio.

Por lo tanto, cada persona que descargue el proyecto debe ejecutar:

```powershell
python manage.py migrate
```

Luego debe crear sus propias cuentas y equipos de prueba desde la aplicación.

## Tecnologías utilizadas

- Python
- Django
- SQLite
- HTML
- CSS
  
