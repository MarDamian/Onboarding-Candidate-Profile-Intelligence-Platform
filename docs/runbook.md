# Onboarding Técnico

Este documento describe los pasos necesarios para configurar el entorno de desarrollo local y comenzar a trabajar en el proyecto **Candidate Profile Intelligence Platform**.

El onboarding está orientado a desarrolladores y se centra en levantar la infraestructura base del sistema.

## Requisitos

Asegúrate de tener instalado:

- Docker
- Docker Compose
- Git

## Set up del entorno

### 1. Clonar el repositorio

```bash
git clone https://github.com/MarDamian/Onboarding-Candidate-Profile-Intelligence-Platform.git

cd Onboarding-Candidate-Profile-Intelligence-Platform
```

### 2. Configurar las variables de entorno:
El proyecto utiliza variables de entorno para configuración de servicios y embeddings.
```bash
cp .env.example .env
```
Modifica el archivo `.env` si necesitas cambiar:
- Credenciales de base de datos
- Configuración de embeddings (modelo, dimensión, distancia)
- URLs de servicios

### 3. Levantar servicios con Docker
Para iniciar todos los servicios del proyecto:
```bash
docker compose -f infra/docker-compose.yml --env-file .env build

docker compose -f infra/docker-compose.yml --env-file .env up 
```

**Nota:** Si tienes problemas de dependencias en `package.json` (u otro servicio), usá el flag `-V` para recrear los volúmenes anónimos y evitar que Docker reutilice un `node_modules` desactualizado:

```bash
docker compose -f infra/docker-compose.yml up  -V --build 

docker compose -f infra/docker-compose.yml --env-file .env up -d
```

Esto levantará los siguientes servicios en segundo plano:
- PostgreSQL (Base de datos relacional)
- Redis (Cache, tracking de jobs ETL y cola de procesamiento asíncrono)
- Qdrant (Motor de búsqueda vectorial)
- FastAPI (API pública - CRUD y búsqueda semántica)
- Flask (API administrativa - ETL y gestión Qdrant)
- React (Interfaz de usuario)
- Worker Rust (Procesador asíncrono de jobs desde Redis)

**Configuración automática:**
Al iniciar, FastAPI ejecuta automáticamente:
1. `alembic upgrade head` - Aplica todas las migraciones pendientes
2. `python scripts/seed_db.py` - Inserta candidatos de prueba y encola un job `etl_sync` a Redis
3. `uvicorn app.main:app` - Inicia el servidor

Esto garantiza que la base de datos esté siempre actualizada y con datos de prueba disponibles.
El Worker Rust procesará el job encolado automáticamente, indexando los seeds en Qdrant sin intervención manual.

### 4. Verificar servicios
Una vez levantados los contenedores, verifica que los servicios estén respondiendo:

**Servicios de API:**
- FastAPI: http://localhost:8000
- FastAPI Docs (Swagger): http://localhost:8000/docs
- Flask Admin: http://localhost:5000
- Flask Health: http://localhost:5000/health

**Frontend:**
- React App: http://localhost:5173

Verifica el estado de los contenedores:
```bash
docker compose ps
```
Todos deben estar en estado `running`.

**Verificar Worker Rust:**
Para confirmar que el Worker Rust está consumiendo jobs desde Redis correctamente:
```bash
docker compose -f infra/docker-compose.yml logs worker_rust
```
Deberías ver logs indicando que el worker está conectado a Redis y esperando jobs:
```
INFO worker_rust: Starting Worker Rust...
INFO worker_rust: Redis connected successfully at redis://redis:6379
INFO worker_rust: Waiting for jobs from queue: candidate_jobs
```

Para probar el flujo completo de procesamiento asíncrono:
```bash
# 1. Encolar un job ETL desde Flask
curl -X POST http://localhost:5000/v1/admin/etl/sync

# 2. Verificar los logs del Worker Rust
docker compose -f infra/docker-compose.yml logs worker_rust --tail 20
```

## Pruebas Automatizadas

El proyecto cuenta con **116 tests** distribuidos en 4 suites. Los tests se ejecutan dentro de los contenedores Docker activos.

### Ejecutar todos los tests
```bash
# FastAPI 
docker exec fastapi_app python -m pytest tests/ -v

# Flask 
docker exec flask_admin python -m pytest tests/ -v

# React 
docker exec react_app npm run test

# Pipelines ETL 
docker exec fastapi_app python -m pytest pipelines/tests/ -v
```

### CI
El proyecto incluye un workflow de GitHub Actions (`.github/workflows/ci.yml`) que ejecuta automáticamente todos los tests en cada push y pull request. Los jobs corren en paralelo:
- `test-fastapi`, `test-flask`, `test-pipelines` (Python + pytest)
- `test-react` (Vitest)
- `check-rust` (cargo check)
- `docker-build` (validación de build)

## Flujo de PR (IMPORTANTE)

### Flujo de trabajo
- `main`: rama estable
- `features`: integración de features
- `feature/*`: desarrollo de funcionalidades específicas

### Gitflow ejemplo
Siempre las ramas feature/* se integran en features mediante Pull Request. Nunca se hace merge directo
```bash
git checkout features
git pull
git checkout -b feature/{feature-name}
```
### Notas

- No hacer merge directo a `main`
- No ejecutar Alembic fuera de Docker
- Todas las modificaciones de modelos deben incluir migración
- Las migraciones y seeds se ejecutan automáticamente en `docker compose up`
- La indexación en Qdrant es automática: los candidatos se indexan al crear/actualizar y se eliminan de Qdrant al borrar
- Para forzar un re-index completo asíncrono: `POST http://localhost:5000/v1/admin/qdrant/reindex` (202 Accepted, procesado por Worker Rust)
- Para re-index síncrono legacy: `POST http://localhost:5000/v1/admin/qdrant/reindex/sync`
- Configuración de embeddings se gestiona en `.env`
- Los jobs ETL se procesan de forma asíncrona: Flask/FastAPI encolan → Redis → Worker Rust procesa
- Para ejecución síncrona legacy usa: `POST http://localhost:5000/v1/admin/etl/sync/direct`
