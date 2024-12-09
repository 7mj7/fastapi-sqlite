# 1. Crear el entorno virtual
```console
python -m venv ENV --prompt=viuweb
```

# 2. Activar el entorno virtual según el sistema operativo
# En Windows:
```console
ENV\Scripts\activate
```
# En macOS/Linux:
```console
source ENV/Scripts/activate
```

# 3. Desactivar el entorno
```console
deactivate
```

# 4. Instalar dependencias
```console
pip install -r requirements.txt
```

#5. Ejecutar
```bash
fastapi dev app.py # desarrollo

fastapi run app.py # producción
```

https://www.youtube.com/watch?v=6eVj33l5e9M&t=2274s

MIN : 37