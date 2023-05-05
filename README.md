# PruebaTecnica
Hola a todos traté de abarcar la mayor parte del contenido de la prueba

Preparé la propuesta conforme al ejercicio, separé el proyecto en dos partes, una donde se manejan los modelos, con sus respectivas operaciones CRUD con sus respectivos tests, llamada "presupuesto" y otra llamada "interfaces" donde se consume esta otra aplicación, las interfaces tienen un front sencillo debido al tiempo.

- La base de datos que se está manejando es postgresql en su versión mas reciente, la conexión se hace mediante psycopg2.
- Se desactivó temporalmente la autenticación "CSRF" para evitar el manejo de usuarios o tokens debido al tiempo, sin embargo se creó un método para la creación de usuarios que puede ser utilizado posteriormente.


## Para ejecutar el proyecto 
### 1.- Entorno de ejecución
Debe descargarse, posicionarse en la rama "main"

En caso de utilizar un entorno virtual deberá crearlo primero, desde la terminal (linux) ejecutar:
```
python3 -m venv nombre_del_entorno

```
y posteriormente activarlo
```
source nombre_del_entorno/bin/activate

```

Una vez dentro del entorno virtual verificamos que exista la variable "PYTHONPATH"
Desde la terminal
```
echo $PYTHONPATH
```
en caso de que esté vacía o no devuelva la ruta de "site-packages", ejecutar el siguiente comando:
```
python -m site
```
devolverá las rutas de python, tomaremos la ruta de "site-packages" que debe verse como:
```
'/home/user/nombre_del_entorno/lib/python3.9/site-packages'
```
copiamos la ruta a la variable local:
```
export PYTHONPATH="${PYTHONPATH}:/home/user/nombre_del_entorno/lib/python3.9/site-packages"
```
igual ejecutamos en caso de no tener instalado los paquetes de desarrollo de python:
```
sudo apt-get install libpq-dev python-dev
```
Esto evitará futuros percances con la base de datos de postgresql



En caso de no tener una base de datos postgres, recomiendo crear una en docker por comodidad, para este caso la vamos a llamar prueba para que pueda ejecutarse como en el ejercicio

```
docker run --name prueba -e POSTGRES_PASSWORD=contraseña --publish 5432:5432 -d postgres
```

### 2.- Ejecución

una vez localizados dentro de la carpeta del proyecto:
Instalamos los requerimientos del proyecto con:
```
pip install -r requirements.txt
```
para la primera ejecución, se recomienda correr las migraciones:
```
python manage.py migrate
```
Y posteriormente ejecutamos:
```
python manage.py runserver
```
Que iniciará el proyecto


Se adjunta carpeta de pruebas...