# Candidate Profile Intelligence Platform

Plataforma de inteligencia para la gestión y análisis de perfiles de candidatos, diseñada para cubrir un flujo completo end-to-end: desde la creación y administración de datos hasta la búsqueda semántica y generación de insights mediante LLMs.

El proyecto forma parte de un plan de onboarding técnico enfocado en la construcción progresiva de un sistema moderno, escalable y bien documentado.

## Objetivo del proyecto

Construir un sistema completamente funcional que permita:

- Gestionar perfiles de candidatos mediante un CRUD completo
- Ingestar datos de forma masiva a través de procesos ETL
- Indexar perfiles de forma semántica en un motor vectorial
- Realizar búsquedas avanzadas desde una interfaz web
- Generar insights automáticos utilizando LLMs
- Integrar un microfrontend especializado dentro de la aplicación principal


## Estado actual

**Semana 1 – Día 1–2**

Actualmente el proyecto se encuentra en una fase inicial e incluye:

- Configuración del repositorio y estructura base
- Infraestructura levantada mediante Docker Compose
- Servicios base disponibles:
  - PostgreSQL
  - Redis
  - Qdrant
- Documentación inicial del proyecto

Las funcionalidades de negocio (CRUD, ETL, búsqueda semántica, LLM) se implementarán progresivamente en las siguientes fases.

**Semana 1 – Día 3–4**

Ya con las bases establecidas, se procede a la implementación de los servicios principales:

- Implementación de fastapi con CRUD completo de candidatos
- Estructuracion de archivos y carpetas
- Implementacion de Validaciones en schemas y models
- Rutas de GET POST PUT DELETE para la gestion de candidatos
- Documentacion de rutas openapi
- Integracion a a Docker
    - Dockerfile.fastapi
    - docker-compose.yml(api-fastapi service)
- Especificacion de variables de entorno y requirements.txt

Las funcionalidades de negocio (ETL, búsqueda semántica, LLM) se implementarán progresivamente en las siguientes fases.

## Features (objetivo final)

- CRUD completo de perfiles (crear, editar, eliminar y listar)
- Ingesta masiva de perfiles mediante ETL
- Indexación semántica en Qdrant
- Búsqueda avanzada desde la interfaz de usuario
- Generación de insights mediante LLM (resúmenes, extracción de información y scoring)
- Microfrontend especializado en Svelte para vistas específicas


## Stack tecnológico

### Backend
- **FastAPI**: API pública para CRUD de perfiles, búsqueda semántica e insights
- **Flask**: API administrativa para ETL, reindexación y monitoreo
- **Rust**: Workers para procesamiento batch y tareas pesadas

### Data
- **PostgreSQL**: Base de datos principal
- **Redis**: Cache y gestión de jobs
- **Procesos ETL**: Ingesta y transformación de datos

### Vector & AI
- **Qdrant**: Motor de búsqueda vectorial
- **LLMs**: Prompts versionados, tool calling y compresión de contexto

### Frontend
- **React**: Interfaz principal (CRUD y búsqueda)
- **Svelte**: Microfrontend especializado integrado en React

### Infraestructura
- **Docker & Docker Compose**
- **Git**


## Estructura del proyecto

```text
docs/
├─ adr/
├─ onboarding.md
├─ architecture.md
├─ api.md
├─ runbook.md

infra/
    ├─ .env.example
    ├─ docker-compose.yml
    ├─ Dockerfile.fastapi
    ├─ db/

services/
├─ api-fastapi/
    ├── api/
    ├── v1/
        ├── candidate.py
    ├── core/
        ├── config.py
    ├── db/
        ├── models/
            ├── candidate.py
        ├── database.py
    ├── schemas/
        ├── candidate.py
    ├── main.py
    ├── requirements.txt       
├─ api-flask/
├─ worker-rust/

ui/
├─ react-app/
├─ svelte-mf/

pipelines/
├─ etl/


```