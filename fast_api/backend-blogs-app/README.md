# Creacion de proyectos con fastapi con uv

1. Instalar uv
- [UV](https://docs.astral.sh/uv/getting-started/installation/)

2. Iniciar proyecto
- __uv init backend-blogs-app__

3. Instalar fastapi dentro de la carpeta del nombre del proyecto: ESTO YA LO INSTALA CON UN venv
- __uv add "fastapi[standard]"__

4. Ejecutar proyecto en desarrollo
- __uv run fastapi dev src/main.py__ | __uv run fastapi dev src/main.py --port 3500__

5. Instalar dependencias en caso de cambiar de computador
- __uv sync__

# Instalaciones variables por proyecto

- [Pydantic - Validacion de Datos Dtos](https://pydantic.dev/docs/validation/dev/get-started/install/)
- __uv add pydantic__

VIDEO: Seccion 5: Validaciones query parameters
