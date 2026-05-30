# Tennis API — Pipeline CI/CD con GitHub Actions

Microservicio desarrollado en FastAPI que expone estadísticas de tenis (ranking ATP y búsqueda de jugadores). Este documento describe el pipeline de integración y despliegue continuo implementado para la Entrega 2 de Ingeniería DevOps.

---

## Descripción del microservicio

La API permite:
- Consultar el top 5 del ranking ATP
- Buscar jugadores por nombre

Tecnologías usadas: Python 3.12, FastAPI, SQLAlchemy, SQLite, Docker.

---

## Estructura del pipeline (GitHub Actions)

El pipeline se dispara automáticamente en cada push a `main` y tiene tres etapas que corren en orden:

```
test → security → deploy
```

### 1. Unit Tests (IE2)

Se ejecutan con **pytest** usando el archivo `test_api.py`. Si algún test falla, el pipeline se detiene y no avanza a las siguientes etapas.

```yaml
- name: Run pytest
  run: pytest test_api.py -v
```

### 2. Análisis de seguridad (IE3)

Esta etapa incluye dos herramientas:

**pip-audit** — revisa las dependencias del proyecto buscando CVEs conocidos:
```yaml
- name: Dependency audit (pip-audit)
  run: pip-audit -r requirements.txt
```

**Snyk** — análisis más profundo de dependencias con umbral de severidad `high`. Si encuentra vulnerabilidades de severidad alta o crítica, el pipeline falla y bloquea el despliegue:
```yaml
- name: Snyk dependency scan
  run: snyk test --severity-threshold=high --file=requirements.txt --package-manager=pip
```

Además, el repositorio tiene **Dependabot** configurado para abrir Pull Requests automáticamente cuando hay actualizaciones de dependencias disponibles.

> Si la etapa de seguridad falla, el job de deploy no se ejecuta porque tiene `needs: security` definido en el pipeline.

### 3. Deploy automático en DigitalOcean (IE4)

Una vez que tests y seguridad pasan, el pipeline se conecta por SSH a un Droplet en DigitalOcean y ejecuta el despliegue. El script:

1. Clona el repositorio si no existe, o hace `git pull` si ya estaba
2. Levanta el servicio con `docker compose up -d --build`
3. Verifica que la API responda correctamente (health check con `curl`)
4. Si el health check falla después de 10 intentos, imprime los logs y retorna error

```yaml
- name: Deploy via SSH
  uses: appleboy/ssh-action@v1.2.0
  with:
    host: ${{ secrets.DO_HOST }}
    username: root
    key: ${{ secrets.DO_SSH_KEY }}
```

---

## Contenerización (IE1)

El microservicio está contenerizado con Docker. El `Dockerfile` usa una imagen base `python:3.12-slim` y corre la aplicación con un usuario sin privilegios de root por seguridad.

La imagen se construye automáticamente durante el deploy con `docker compose up --build`, lo que garantiza que siempre se despliega la versión más reciente del código.

---

## Orquestación con Docker Compose (IE5)

Se usa **Docker Compose** para orquestar el servicio. Permite definir el puerto expuesto y las variables de entorno desde un archivo `.env`:

```yaml
services:
  tennis-api:
    build: .
    ports:
      - "${APP_PORT:-8000}:8000"
    env_file:
      - .env
```

El archivo `.env` no se sube al repositorio (está en `.gitignore`) y se crea manualmente en el servidor con las variables necesarias.

---

## Trazabilidad y calidad

- **Trazabilidad**: cada push genera una ejecución del pipeline en GitHub Actions con logs completos de cada etapa. Se puede ver exactamente qué commit disparó el deploy, qué tests corrieron y qué analizó Snyk.
- **Calidad**: el pipeline bloquea el deploy si los tests fallan o si hay vulnerabilidades de seguridad altas. No es posible llegar a producción sin pasar ambas validaciones.
- **Secrets**: las credenciales del servidor (IP, clave SSH) se almacenan como secrets en GitHub y nunca quedan expuestos en el código.

---

## Variables de entorno y secrets necesarios

| Nombre | Descripción |
|--------|-------------|
| `DO_HOST` | IP del Droplet en DigitalOcean |
| `DO_SSH_KEY` | Clave privada SSH para conectarse al servidor |
| `SNYK_TOKEN` | Token de autenticación de Snyk |

---

## Cómo correr el proyecto localmente

```bash
# Clonar el repositorio
git clone https://github.com/DanielBeltranl/Entrega-2-ingenieria-devops.git
cd Entrega-2-ingenieria-devops

# Crear archivo .env
echo "APP_PORT=8000" > .env

# Levantar con Docker Compose
docker compose up --build
```

La API queda disponible en `http://localhost:8000`.
