# Metropol
Sistema de gestión para un despacho de abogados, incluyendo: gestión de personas, vencimientos (juicios), pagos, expedientes y otros. 

# Prerrequisitos
* Debe haber un fichero con la estructura que se indica en el ejemplo (doc/metropol_settings.ini) en la ruta /etc/secrets del sistema (C:\etc\secrets) en Windows. Este fichero contiene la configuración del proyecto y la base de datos.
* Debe existir una base de datos vacía con UTF-8 como juego de caracteres y un usuario con permisos en la misma. Estos datos son los correspondientes al fichero anterior.

# Requisitos
* Python 3.X

1.Instalación de dependencias para Python (se recomienda usar virtualenv)
```
pip install -r requirements.txt
```

2.Creación de tablas
```
python manage.py makemigrations
python manage.py migrate
```

3.Generación de usuario de prueba
```
python manage.py populate_db
```

# Ejecución (Servidor de desarrollo)
```
python manage.py runserver
```

Puede acceder en localhost:8000 con (usuario:contraseña) -> carborgar:metropol
