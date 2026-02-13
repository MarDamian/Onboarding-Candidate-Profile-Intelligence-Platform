# Candidate Profile Intelligence Platform

![alt text](https://img.shields.io/badge/react-313131?style=flat&logo=react)
![alt text](https://img.shields.io/badge/svelte-313131?style=flat&logo=svelte)
![alt text](https://img.shields.io/badge/fastapi-313131?style=flat&logo=fastapi)
![alt text](https://img.shields.io/badge/flask-313131?style=flat&logo=flask)
![alt text](https://img.shields.io/badge/qdrant-313131?style=flat&logo=qdrant)
![alt text](https://img.shields.io/badge/cohere-313131?style=flat&logo=cohere)
![alt text](https://img.shields.io/badge/rust-313131?style=flat&logo=rust)
![alt text](https://img.shields.io/badge/postgres-313131?style=flat&logo=postgresql)
![alt text](https://img.shields.io/badge/redis-313131?style=flat&logo=redis)
![alt text](https://img.shields.io/badge/postman-313131?style=flat&logo=postman)
![alt text](https://img.shields.io/badge/Status-Finished-success)

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

## Checklist

**Backend CRUD**
- [x] Modelo de dominio definido
- [x] CRUD completo en FastAPI
- [x] Validaciones con Pydantic
- [x] Manejo estándar de errores 
- [x] OpenAPI documentado

**Frontend React**
- [x] Listado de entidades
- [x] Creación, edición y eliminación
- [x] Manejo de errores
- [x] Variables de entorno

**ETL**
- [x] Idempotencia
- [x] Validaciones
- [x] Tracking de ejecuciones
- [x] Endpoint administrativo

**Qdrant**
- [x] Colección documentada
- [x] Definición de payloads
- [x] Operaciones de upsert
- [x] Reindexación soportada

**LLM Avanzado**
- [x] Prompts versionados
- [x] Tool calling implementado
- [x] Prompt compression aplicada
- [x] Guardrails (tokens y timeouts)
- [x] Fallback seguro

**Microfrontend (Svelte)**
- [x] Aplicación Svelte creada
- [x] Funcionalidad clara y aislada
- [x] Integración con React
- [x] Build y despliegue mediante Docker

**Infraestructura y Calidad**
- [x] Docker Compose
- [x] Logs estructurados
- [x] Pruebas mínimas
- [x] CI activo

**Documentación**
- [x] README (por terminar)
- [x] Arquitectura
- [x] API
- [x] Runbook
- [x] ADRs

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
  - Documentación automática con OpenAPI/Swagger
  - Validación de datos con Pydantic
  - Alembic para migraciones de base de datos
- **Flask**: API administrativa para ETL, reindexación y monitoreo
  - Gestión de procesos ETL con Redis como cola
  - Endpoints administrativos para operaciones batch
  - Gunicorn como servidor WSGI
- **Rust Worker**: Procesador asíncrono de jobs batch
  - Consumo eficiente de jobs desde Redis con BLPOP bloqueante
  - Arquitectura modular con separación de responsabilidades
  - Tokio para runtime asíncrono de alto rendimiento
  - Logging estructurado con tracing
  - Escalabilidad horizontal con múltiples workers

### Data

- **PostgreSQL 17.5**: Base de datos relacional principal
  - Almacenamiento de perfiles de candidatos
  - Gestión de timestamps para indexación incremental
  - Scripts de inicialización y seeding automáticos
- **Redis 8.4.0**: Cache y gestión de jobs
  - Tracking de estado de procesos ETL
  - Sistema de jobs para operaciones asíncronas
- **Procesos ETL**: Ingesta y transformación de datos
  - Pipeline modular (Extract → Transform → Load)
  - Procesamiento idempotente con `last_indexed_at`
  - Generación automática de embeddings

### Vector & AI

- **Qdrant v1.16.2**: Motor de búsqueda vectorial
  - Almacenamiento y búsqueda de embeddings de 384 dimensiones
  - Soporte para filtros combinados (skills, nombre)
  - Persistencia de datos en volúmenes Docker
- **Cohere Embeddings**: Generación de vectores para búsqueda semántica
  - Modelo: `embed-multilingual-v3.0` (1024 dimensiones)
  - API cloud (sin procesamiento local)
  - Integrado en Worker Rust para procesamiento batch
  - Configuración dinámica vía variables de entorno
- **LLMs - Cohere**: Generación de insights avanzados
  - Modelo: `command-a-03-2025` para superior reasoning y tareas complejas
  - Arquitectura SOLID con 6 componentes especializados
  - Servicio de Insights con 3 tipos de análisis (summary, score, comparison)
  - Prompts versionados para A/B testing

### Testing

- **pytest 8.3.5 + pytest-cov**: Tests unitarios e integración para Python
  - SQLite in-memory para aislamiento de DB
  - Mocks de servicios externos (Qdrant, Cohere, Redis)
  - Cobertura de código con reportes XML
- **Vitest 3.2 + @testing-library/react**: Tests de frontend
  - jsdom como entorno de ejecución
  - Testing Library para interacción con componentes
  - Mocks de axios para servicios API
- **GitHub Actions CI/CD**: Pipeline automatizado
  - 6 jobs paralelos (FastAPI, Flask, Pipelines, React, Rust, Docker)
  - Cache de dependencias para builds rápidos
  - Artefactos de cobertura por servicio

### Frontend

- **React + TypeScript**: Interfaz principal
  - Vite como bundler y dev server
  - React Router para navegación
  - Gestión de estado con hooks
  - Componentes para CRUD completo
  - Componentes de Insights (ScoringCard, ComparisonChart, SkillsAssessment)
  - Hooks personalizados (useInsights, useScoring, useComparison)
- **Svelte**: Microfrontend especializado integrado en React
  - Vista de "Candidatos Similares"
  - Arquitectura basada en componentes ligeros
  - Integración vía Iframe con paso de parámetros por URL

### Infraestructura

- **Docker & Docker Compose**: Orquestación de servicios
  - Postgres, Redis, Qdrant, FastAPI, Flask, React
  - Volúmenes para persistencia de datos
  - Red compartida entre servicios
  - Hot reload en desarrollo
- **Git**: Control de versiones
- **GitHub Actions**: CI con tests automatizados en cada push/PR

## Servicios y puertos

| Servicio    | Puerto | Descripción                                   |
| ----------- | ------ | --------------------------------------------- |
| FastAPI     | 8000   | API REST para CRUD de candidatos              |
| Flask       | 5000   | API administrativa (ETL + búsqueda semántica) |
| React       | 5173   | Interfaz de usuario web                       |
| Svelte      | 5174   | Microfrontend de candidatos similares         |
| Worker Rust | -      | Procesamiento asíncrono de jobs desde Redis   |
| PostgreSQL  | 5433   | Base de datos relacional                      |
| Redis       | 6379   | Cache y cola de jobs                          |
| Qdrant      | 6333   | Motor de búsqueda vectorial                   |

## Estructura del proyecto

```text
docs/
├── adr/                           # Architecture Decision Records
├── runbook.md                     # Guía de ejecucion y uso
├── arquitecture.md                # Documentación de arquitectura
├── api.md                         # Documentación de endpoints
└── qdrant-collection.mb           # Documentacion de qdrant

infra/
├── docker-compose.yml             # Orquestación de servicios
├── Dockerfile.fastapi             # Imagen para FastAPI
├── Dockerfile.flask               # Imagen para Flask
├── Dockerfile.react               # Imagen para React
├── Dockerfile.worker_rust         # Imagen para Worker Rust
├── Dockerfile.svelte              # Imagen para Svelte
├── Dockerfile.pipeline            # Imagen para Pipeline
└── db/
    └── init.sql                   # Script de inicialización de DB

.github/
└── workflows/
    └── ci.yml                     # Pipeline CI (jobs paralelos)

services/
├── api-fastapi/                   # API principal (CRUD + búsqueda)
│   ├── alembic/                   # Migraciones de base de datos
│   ├── app/
│   │   ├── api/v1/                # Endpoints versioned
│   │   ├── core/                  # Configuración
│   │   ├── db/                    # Modelos y conexión
│   │   │   └── models/            # Modelos de base de datos
│   │   ├── schemas/               # Validación con Pydantic
│   │   └──  llm/
│   ├── tests/                     # tests (pytest)
│   ├── scripts/
│   ├── requirements.txt
│   └── alembic.ini
│
├── api-flask/                     # API administrativa (ETL)
│   ├── app/
│   │   ├── api/                   # Rutas de ETL
│   │   ├── core/                  # Configuración
│   │   ├── services/              # Lógica de ETL
│   │   └── __init__.py
│   ├── tests/                     # tests (pytest)
│   ├── requirements.txt
│   └── run.py
│
├── worker-rust/                   # Worker batch asíncrono
│   ├── src/
│   │   └── jobs/                  # Procesadores de jobs
│   └── Cargo.toml

ui/
└── react-app/                     # Interfaz de usuario
│    ├── src/
│    │   ├── __tests__/             # tests (Vitest)
│    │   ├── components/            # Componentes reutilizables
│    │   ├── pages/                 # Páginas de la aplicación
│    │   ├── services/              # Cliente API
│    │   └── types/                 # Tipos TypeScript
│    ├── package.json
│    └── vite.config.ts
│
└── svelte-mf/                     # Microfrontend en Svelte
    ├── src/
    │   ├── assets/
    │   ├── lib/
    │   │     ├── components/
    │   │     └── services/
    │   └── routes/
    ├── package.json
    └── vite.config.ts

pipelines/
├── etl/                           # Pipeline ETL modular
├── tests/                         # tests (pytest)
└── utils/                         # Servicios de Embedding y busqueda Semantica

prompts/
├── candidate_summary/             # Prompts versionados para resúmenes
└── skill_extraction/              # Prompts para extracción de skills
```

## Documentación adicional

- **[Ejecucion Inicial](docs/runbook.md)**: Guía paso a paso para nuevos desarrolladores
- **[Arquitectura](docs/arquitecture.md)**: Decisiones de diseño y patrones utilizados
- **[API Reference](docs/api.md)**: Documentación completa de endpoints
- **[ADRs](docs/adrs/)**: Decisiones arquitectónicas registradas
  - **ADR 009**: LLM Fallback y Estrategia de Redundancia
  - **ADR 008**: Logs Estructurados en formato JSON
  - **ADR 007**: Manejo de Timeouts y Reintentos
  - **ADR 006**: Worker Batch en Rust para Procesamiento Asíncrono
  - **ADR 005**: Integración de LLM Cohere y Embeddings API
  - **ADR 004**: Vector Search con Qdrant
  - **ADR 003**: Refactor de búsqueda semántica
  - **ADR 002**: Migraciones de base de datos
  - **ADR 001**: Manejo descentralizado de errores

## Contribuciones

Este proyecto forma parte de un plan de onboarding. Para contribuir:

1. Revisar la [documentación de arquitectura](docs/arquitecture.md)
2. Consultar los [ADRs](docs/adrs/) para entender decisiones de diseño
3. Seguir la [guía de ejecucion](docs/runbook.md) para configurar el entorno
