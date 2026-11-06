## Proyecto Inicial IWG400 – Plataforma de fútbol amateur

Aplicación web desarrollada con Python y Django para conectar equipos de fútbol amateur, permitir el envío de desafíos, coordinar partidos y registrar sus resultados.

## Requisitos

Para ejecutar el proyecto se necesita:

Python 3.14.3 o una versión compatible.

Django 6.1.2.

## Instalación y ejecución local

Los siguientes pasos están pensados para Windows utilizando Visual Studio Code.

## 1. Descargar el repositorio

Descargue el código del repositorio en formato ZIP y extraiga su contenido. Luego, abra la carpeta del proyecto en Visual Studio Code mediante File → Open Folder.

## 2. Abrir una terminal

En Visual Studio Code, abra una terminal desde Terminal → New Terminal.

Verifique que la terminal se encuentre en la carpeta que contiene el archivo manage.py. Si el archivo se encuentra dentro de una subcarpeta, utilice el comando cd para ingresar a ella.

Por ejemplo:

cd Proyecto-inicial-IWG400-main

Puede utilizar el comando:

dir

para verificar que en la carpeta se encuentren archivos como manage.py y las carpetas del proyecto.

## 3. Instalar Django

Ejecute el siguiente comando en la terminal:

python -m pip install Django==6.1.2

## 4. Crear las tablas necesarias

Ejecute:

python manage.py migrate

## 5. Iniciar el servidor de Django

Ejecute:

python manage.py runserver

La terminal mostrará una dirección similar a:

http://127.0.0.1:8000/

Abra esta dirección en un navegador para utilizar la aplicación.

Para detener el servidor, presione Ctrl + C en la terminal.

## Datos para probar la funcionalidad principal

El repositorio no incluye una base de datos con usuarios o equipos de demostración. Al ejecutar las migraciones se crea la estructura de la base de datos; para probar la aplicación hay que registrar usuarios y equipos desde la interfaz.

1. Ingresar a la aplicación y registrar una cuenta para el capitán del primer equipo.
2. Iniciar sesión y crear un equipo.
3. Cerrar sesión y registrar una segunda cuenta para el capitán del equipo rival.
4. Iniciar sesión con la segunda cuenta y crear otro equipo.
5. Volver a iniciar sesión con el primer capitán y entrar al radar para consultar los equipos rivales y enviar un desafío.
6. Iniciar sesión con el capitán del equipo desafiado, revisar la bandeja de desafíos y aceptar la solicitud.
7. Desde la sección de coordinación, proponer una fecha, hora y lugar para el partido. El otro capitán debe responder a la propuesta para acordar la coordinación.
8. Una vez realizado el partido, cada capitán debe registrar el marcador desde la sección correspondiente.

**Para probar la validación de resultados:**

- Caso 1: ambos capitanes registran el mismo marcador. El sistema confirma el partido y actualiza los puntajes Elo.
- Caso 2: los capitanes registran marcadores diferentes. El partido queda en estado de disputa y los puntajes Elo no se actualizan automáticamente.

Se recomienda crear al menos tres equipos con distintos puntajes Elo para observar diferentes alternativas de rivales en el radar. Los equipos nuevos comienzan con un puntaje Elo de 1000.

## Base de datos

El proyecto utiliza SQLite. El archivo `db.sqlite3` se genera localmente al ejecutar las migraciones y no se incluye en el repositorio. Si se descarga el proyecto en otro computador, se debe ejecutar nuevamente `python manage.py migrate` y crear usuarios y equipos de prueba.

## Tecnologías

- Python
- Django
- HTML y CSS
- SQLite
