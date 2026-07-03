# Evaluacion 2 - Ingenieria devops

## ¿Qué hace la API?

- Muestra el top 5 del ranking ATP
- Permite buscar jugadores por nombre

Stack: Python 3.12, FastAPI, SQLAlchemy, SQLite, Docker.


## Pipeline CI/CD

El pipeline corre automáticamente con cada push a main y tiene tres etapas en orden:

```
test → seguridad → despliegue
```

Si cualquier etapa falla, las siguientes no se ejecutan.

### Tests

Se usan pytest para correr los tests unitarios. Si alguno falla, el pipeline para ahí y no avanza.

```bash
pytest test_api.py -v
```

### Análisis de seguridad

Se usan dos herramientas:

- Dependabot: revisa las dependencias buscando vulnerabilidades conocidas
- Snyk: análisis más completo, con umbral en severidad alto. Si encuentra algo grave, bloquea el deploy

El repositorio también tiene Dependabot activado, que abre PRs automáticos cuando hay dependencias desactualizadas.

### Deploy en DigitalOcean

Cuando tests y seguridad pasan, el pipeline se conecta por SSH a un Droplet y despliega la app. El proceso es:

1. Si ya existe el proyecto en el servidor, hace git pull
2. Si no existe, lo clona
3. Levanta todo con docker compose up -d --build
4. Verifica que la API responda (/api/rankings/top)
5. Si no responde en 10 intentos, imprime los logs y falla



## Docker

El proyecto tiene un Dockerfile basado en python:3.12-slim. Por seguridad, la app corre con un usuario sin privilegios de root.

Para correrlo local:

```bash
docker compose up --build
```



## Docker Compose

Se usa Docker Compose para orquestar el servicio. El puerto y otras variables se configuran en un archivo .env que no se sube al repo.

```yaml
services:
  tennis-api:
    build: .
    ports:
      - "${APP_PORT:-8000}:8000"
    env_file:
      - .env
```



## Trazabilidad y calidad

Cada push genera una ejecución en GitHub Actions con logs completos. Desde ahí se puede ver exactamente qué commit disparó el deploy, qué tests corrieron y qué analizó Snyk.

El deploy solo llega al servidor si los tests pasan y si no hay vulnerabilidades graves en las dependencias. Las credenciales del servidor están guardadas como secrets en GitHub y nunca se exponen en el código.



## Secrets necesarios

| Nombre | Para qué sirve                  |
|--------|---------------------------------|
| `DO_HOST` | IP del servidor en DigitalOcean |
| `DO_SSH_KEY` | Clave SSH para conectarse al servidor |
| `SNYK_TOKEN` | Token de autenticación de Snyk  |



## Correr el proyecto local-

```bash
git clone https://github.com/DanielBeltranl/Entrega-2-ingenieria-devops.git
cd Entrega-2-ingenieria-devops

echo "APP_PORT=8000" > .env

docker compose up --build
```

La pagina queda disponible en `http://104.248.234.200:8000/`.
