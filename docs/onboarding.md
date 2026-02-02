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
El proyecto actual utiliza variables de entorno para la configuración de servicios.
```bash
cp infra/.env.example infra/.env
```
Deberás modificar el archivo .env si es necesario, según el entorno local.

### 3. Levantar servicios con Docker
Para iniciar los servicios base del proyecto, tiene que ejecutar:
```bash
cd ./infra/

docker compose up -d
```
Esto levantará los siguientes servicios en segundo plano:
- PostgreSQL
- Redis
- Qdrant
- FastAPI
- React

### 4. Aplicar migraciones y Seeds
Una vez esten los contenedores levantados, debes preparar la base de datos:

- Aplicar la estructura ded tablas:
```bash
docker compose run api-fastapi alembic upgrade head
```
- Ahora también deberías ver la versión actual:
```bash
docker compose run api-fastapi alembic current
``` 
Tener en cuenta no ejecutar migraciones directamente contra la base de datos.

- Insertar candidatos de prueba
```bash
docker compose exec api-fastapi python scripts/seed_db.py
```

### 5. Verificar
Una vez levantados los contenedores, verifica que los servicios estén corriendo:
- PostgreSQL disponible en http://localhost:5433
- Redis disponible en http://localhost:6379
- Qdrant accesible en http://localhost:6333
- FastAPI accesible en http://localhost:8000
- React App accesible en http://localhost:5173
- Flask accesible en http://localhost:5000
Si ves que todos los contenedores están en estado running, el entorno está correctamente configurado.

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
