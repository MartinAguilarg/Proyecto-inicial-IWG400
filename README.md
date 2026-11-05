# Proyecto Inicial IWG400 – Plataforma de fútbol amateur

Aplicación web desarrollada con **Python y Django** para conectar equipos de fútbol amateur, gestionar desafíos, coordinar partidos y registrar sus resultados.

## Requisitos

- Python 3.15.2
- pip (administrador de paquetes de Python).
- Git (opcional, para clonar el repositorio).

## Instalación y ejecución local

Los siguientes pasos están pensados para Windows utilizando la terminal de Visual Studio Code.

1. **Descargar o clonar el repositorio** y abrir la carpeta del proyecto en Visual Studio Code.

2. **Abrir una terminal** desde el menú Terminal → New Terminal.

3. 3. **Ubicarse en la carpeta principal del proyecto**, donde se encuentra el archivo `manage.py`.

   Primero, ejecutar el siguiente comando para visualizar los archivos y carpetas del directorio actual:

   ```powershell
   dir
   ```

   Si la carpeta del proyecto se encuentra dentro de otra carpeta, utilizar el comando `cd` seguido de su nombre para ingresar a ella. Por ejemplo:

   ```powershell
   cd Proyecto-inicial-IWG400
   ```

   Si se necesita regresar a la carpeta anterior, utilizar:

   ```powershell
   cd ..
   ```

   Una vez dentro de la carpeta principal, ejecutar nuevamente `dir` y comprobar que aparezca el archivo `manage.py`.
4. **Crear un entorno virtual** para instalar las dependencias del proyecto:

   ```powershell
   python -m venv venv
   ```

   Activarlo con:

   ```powershell
   .\venv\Scripts\Activate.ps1
   ```

5. **Instalar Django**:

   ```powershell
   python -m pip install --upgrade pip
   python -m pip install Django==6.1.1
   ```

6. **Aplicar las migraciones** para crear las tablas de la base de datos:

   ```powershell
   python manage.py migrate
   ```

7. **Iniciar el servidor de desarrollo**:

   ```powershell
   python manage.py runserver
   ```

8. **Abrir la aplicación** en el navegador mediante la siguiente dirección:

   http://127.0.0.1:8000/

Para detener el servidor, volver a la terminal y presionar `Ctrl + C`.

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
