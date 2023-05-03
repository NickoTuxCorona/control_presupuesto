# PruebaTecnica
Hola a todos traté de abarcar la mayor parte del contenido de la prueba

Preparé la propuesta conforme al ejercicio, separé el proyecto en dos partes, una donde se manejan los modelos, con sus respectivas operaciones CRUD con sus respectivos tests, llamada "presupuesto" y otra llamada "interfaces" donde se consume esta otra aplicación, las interfaces tienen un front sencillo debido al tiempo.

- La base de datos que se está manejando es postgresql en su versión mas reciente, la conexión se hace mediante psycopg2.
- Se desactivó temporalmente la autenticación "CSRF" para evitar el manejo de usuarios o tokens debido al tiempo, sin embargo se creó un método para la creación de usuarios que puede ser utilizado posteriormente.