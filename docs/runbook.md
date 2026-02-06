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

**Nota:** Si tienes problemas dedependencias en `package.json` (u otro servicio), usá el flag `-V` para recrear los volúmenes anónimos y evitar que Docker reutilice un `node_modules` desactualizado:

```bash
docker compose -f infra/docker-compose.yml up  -V --build 

docker compose -f infra/docker-compose.yml --env-file .env up -d
```

Esto levantará los siguientes servicios en segundo plano:
- PostgreSQL (Base de datos relacional)
- Redis (Cache y tracking de jobs ETL)
- Qdrant (Motor de búsqueda vectorial)
- FastAPI (API pública - CRUD y búsqueda semántica)
- Flask (API administrativa - ETL y gestión Qdrant)
- React (Interfaz de usuario)

**Configuración automática:**
Al iniciar, FastAPI ejecuta automáticamente:
1. `alembic upgrade head` - Aplica todas las migraciones pendientes
2. `python scripts/seed_db.py` - Inserta candidatos de prueba
3. `uvicorn app.main:app` - Inicia el servidor

Esto garantiza que la base de datos esté siempre actualizada y con datos de prueba disponibles.

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
- Para re-indexar Qdrant manualmente: `POST http://localhost:5000/v1/admin/qdrant/reindex`
- Configuración de embeddings se gestiona en `.env`
