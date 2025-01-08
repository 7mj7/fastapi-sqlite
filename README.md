#  1. Crear el entorno virtual

```console
python -m venv ENV --prompt=viuweb
```

#  2. Activar el entorno virtual según el sistema operativo

##  En Windows:

```console
ENV\Scripts\activate
```

##  En macOS/Linux:

```console
source ENV/bin/activate
```

  

#  3. Desactivar el entorno

```console
deactivate
```

#  4. Instalar dependencias

```console
pip install -r requirements.txt
```

  

# 5. Ejecutar

```bash
fastapi  dev  app.py  # desarrollo
fastapi  run  app.py  # producción
```

# 6. Rellenar la base de datos con usuarios
En el archivo scripts/init_db.py hay un script con las instrucciones para volcar los datos a la base de datos.
Por defecto se crean los siguientes usuarios: 

 **Admin** (role = admin)  
 usuario : admin@example.com   
 contraseña : admin123  


 **Fotógrafo** (role = photographer)  
 usuario : fotografo@example.com  
 contraseña : foto123 

**Cliente** (role = client):  
usuario : cliente@example.com  
contraseña : cliente123  

  
 
# 99. Otras cosas
https://www.youtube.com/watch?v=6eVj33l5e9M&t=2274s
MIN : 37