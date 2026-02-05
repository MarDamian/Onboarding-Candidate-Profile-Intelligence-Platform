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
- Refactorización del servicio **FastAPI** hacia una estructura anidada (`app/`)
  - Separación clara de `api`, `core`, `db`, `schemas` y `models`
- Implementacion de Validaciones en schemas y models
- Rutas de GET POST PUT DELETE para la gestion de candidatos
- Documentacion de rutas openapi
- Documentación del flujo de migraciones en el onboarding
- Ajustes de configuración:
  - Variables de entorno
  - Carga de settings
  - Reglas de ignore actualizadas
- Integracion a a Docker
  - Dockerfile.fastapi
  - docker-compose.yml(api-fastapi service)
- Especificacion de variables de entorno y requirements.txt

Las funcionalidades de negocio (ETL, búsqueda semántica, LLM) se implementarán progresivamente en las siguientes fases.

**Semana 1 – Día 5**

Durante este día se implementa:

- Inicialización de **Alembic** para manejo de migraciones
  - Configuración de conexión a base de datos
  - Definición de `Base` unificada
  - Creación de migraciones iniciales
- Manejo de estados de la aplicación:
  - Estados de carga
  - Manejo centralizado de errores
- Mejora de experiencia de usuario:
  - Formularios con `react-hook-form`
  - Validaciones en frontend
  - Componentes reutilizables
- Dockerización de la aplicación React
  - Integración del frontend dentro de la orquestación existente
  - Configuración de variables de entorno
- Ajustes de CORS en FastAPI para permitir comunicación UI ↔ API
- Actualización de documentación técnica y arquitectónica

**Cierre Semana 1:**

- Implementación exitosa de **Alembic**.
- CRUD funcional y verificado con datos semilla automatizados.
- Documentación de arquitectura de persistencia completada.

**Semana 2 - Día 6-7**

- Implementación pipeline del ETL
  - ETL idempotente (usando `last_indexed_at`) mediante migración con alembic
  - ETL con Redis y PostgreSQL
- Endpoint administrativo en Flask y Dockerización del servicio Flask
- Ajustes de CORS en Flask para permitir comunicación UI ↔ API
- Actualización de documentación técnica y arquitectónica

**Semana 2 - Día 8**

- **Implementación de embeddings reales con sentence-transformers**
  - Servicio de embeddings centralizado (`pipelines/utils/embeddings_service.py`)
  - Modelo `all-MiniLM-L6-v2` optimizado para CPU (384 dimensiones)
  - Integración con el pipeline ETL para generación automática de vectores
- **Colección de Qdrant completamente documentada**
  - Estructura de vectores y payload
  - Proceso de indexación incremental
  - Documentación de mantenimiento y troubleshooting
- **Búsqueda semántica funcional en Flask**
  - Endpoint `/v1/search/` con búsqueda por texto en lenguaje natural
  - Filtros por skills y nombre del candidato
  - Score threshold configurable
  - Endpoint `/v1/search/similar/{id}` para encontrar candidatos similares
- **Separación de responsabilidades**
  - FastAPI dedicado exclusivamente a CRUD de candidatos
  - Flask con ETL y búsqueda semántica
  - Eliminación de redundancia de torch en FastAPI
- **Optimizaciones de infraestructura**
  - Actualización de Dockerfiles y docker-compose
  - Volúmenes compartidos para pipelines entre servicios
  - Variables de entorno para Qdrant configuradas
- Actualización completa de documentación de API y arquitectura

**Semana 2 - Día 9-10 LLM (Nivel Avanzado)**

- **LLM orchestration**
  - `PromptManager`: Carga y caching de prompts con versionado (v1, v2)
  - `ContextManager`: Compresión inteligente de contexto
  - `ErrorHandler`: Manejo centralizado de errores y fallbacks
  - `Agent`: Orquestador principal completa
- **Insights**
  - Generación de resúmenes técnicos detallados (`generate_summary`)
  - Scoring de compatibilidad candidato-vacante (`generate_score`)
  - Análisis comparativo y posicionamiento en mercado (`generate_comparison`)
  - Métodos auxiliares para extracción de datos (años exp, skills, percentiles)
- **Schemas de Validación Pydantic**
  - `InsightResponse`: respuesta unificada para todos los endpoints
- **Endpoints REST Insights**
  - `GET /v1/insights/{candidate_id}` - Insights generales con comparación opcional
- **Prompts Versionados Avanzados**
  - `prompts/candidate_summary/v1.txt` - Prompt base refinado
  - `prompts/candidate_summary/v2.txt` - Prompt avanzado con análisis estratégico profundo
  - `prompts/skill_extraction/v1.txt` - Extracción estructurada de skills (JSON)
- **Integración Cohere LLM**
  - Decisión por `command-a-03-2025` para superior reasoning
  - Decisión por `embed-multilingual-light-v3.0` para embeddings multilingües
  - ADR 005 documentando todas las decisiones arquitectónicas
  - Migración planeada de embeddings locales a API Cohere (4 fases)
- **Documentación Arquitectónica Completa**
  - ADR 005: Decisiones sobre LLM y Embeddings API
  - Actualización de `docs/api.md`

**Semana 2 - Día 11-12 React UI Insights**

- **Componentes React para Insights**
  - `Insight.tsx` - Visualización de resumen técnico
  - `Card.tsx` - Componente Card para uso
- **Integración Frontend-Backend**
  - Servicio `InsightService.ts` - Cliente TypeScript para endpoints
  - Estados de carga, error y éxito
  - Refresh automático
- **UI/UX Mejorada**
  - navbar mejorado y estilizado, se agrego buscador para la lista

**Pendiente:**

- Semana 3 — Microfrontend y Robustez

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
- **Sentence Transformers**: Generación de embeddings
  - Modelo: `all-MiniLM-L6-v2` (optimizado para CPU)
  - Servicio centralizado de embeddings
  - Configuración dinámica vía variables de entorno
- **LLMs - Cohere**: Generación de insights avanzados
  - Modelo: `command-a-03-2025` para superior reasoning y tareas complejas
  - Embeddings API: `embed-multilingual-light-v3.0` para búsqueda multilingüe
  - Arquitectura SOLID con 6 componentes especializados
  - Servicio de Insights con 3 tipos de análisis (summary, score, comparison)
  - Prompts versionados para A/B testing

### Frontend

- **React + TypeScript**: Interfaz principal
  - Vite como bundler y dev server
  - React Router para navegación
  - Gestión de estado con hooks
  - Componentes para CRUD completo
  - Componentes de Insights (ScoringCard, ComparisonChart, SkillsAssessment)
  - Hooks personalizados (useInsights, useScoring, useComparison)
- **Svelte**: Microfrontend especializado integrado en React (pendiente)

### Infraestructura

- **Docker & Docker Compose**: Orquestación de servicios
  - Postgres, Redis, Qdrant, FastAPI, Flask, React
  - Volúmenes para persistencia de datos
  - Red compartida entre servicios
  - Hot reload en desarrollo
- **Git**: Control de versiones

## Servicios y puertos

| Servicio   | Puerto | Descripción                                   |
| ---------- | ------ | --------------------------------------------- |
| FastAPI    | 8000   | API REST para CRUD de candidatos              |
| Flask      | 5000   | API administrativa (ETL + búsqueda semántica) |
| React      | 5173   | Interfaz de usuario web                       |
| PostgreSQL | 5433   | Base de datos relacional                      |
| Redis      | 6379   | Cache y cola de jobs                          |
| Qdrant     | 6333   | Motor de búsqueda vectorial                   |

## Endpoints principales

### FastAPI (Puerto 8000)

- `GET /v1/candidates/` - Listar candidatos
- `POST /v1/candidates/` - Crear candidato
- `GET /v1/candidates/{candidate_id}` - Obtener candidato
- `PUT /v1/candidates/{candidate_id}` - Actualizar candidato
- `DELETE /v1/candidates/{candidate_id}` - Eliminar candidato
- `GET /docs` - Documentación Swagger/OpenAPI
- `POST /v1/semantic_search/` - Busqueda semantica para encontrar candidatos
- `GET /v1/semantic_search/similar/{candidate_id}` - Busqueda por similitud de varios candidatos del candidato elegido
- `GET /v1/insights/{candidate_id}` - Insights generales del candidato
- `POST /v1/insights/score` - Scoring de compatibilidad candidato-vacante
- `POST /v1/insights/summary` - Resumen técnico comprensivo
- `GET /v1/insights/{candidate_id}/comparison` - Análisis comparativo vs mercado
- `GET /v1/insights/health` - Estado del servicio de insights

### Flask (Puerto 5000)

- `POST /v1/admin/etl/sync` - Ejecutar pipeline ETL completo
- `GET /v1/admin/etl/status` - Consultar estado de job ETL
- `POST /v1/admin/qdrant/reindex` - Re-indexar todos los candidatos
- `GET /v1/admin/qdrant/stats` - Estadísticas de Qdrant

## Inicio rápido

### Prerrequisitos

- Docker y Docker Compose instalados
- Git para clonar el repositorio

### Pasos para levantar el proyecto

1. **Clonar el repositorio**

```bash
git clone <repository-url>
cd Onboarding-Candidate-Profile-Intelligence-Platform
```

2. **Configurar variables de entorno**

```bash
cd infra
cp .env.example .env
# Editar .env con tus configuraciones
```

3. **Levantar todos los servicios**

```bash
docker compose up
```

4. **Acceder a los servicios**

- UI React: http://localhost:5173
- API FastAPI: http://localhost:8000/docs
- API Flask: http://localhost:5000
- Qdrant Dashboard: http://localhost:6333/dashboard

### Inicialización automática

Al levantar los servicios, se ejecutan automáticamente:

- **Migraciones de Alembic**: Crean/actualizan la estructura de la base de datos
- **Seed de datos**: Insertan candidatos de ejemplo para pruebas
- **Colección Qdrant**: Se crea automáticamente al ejecutar el primer ETL

## Estructura del proyecto

```text
docs/
├── adr/                           # Architecture Decision Records
├── onboarding.md                  # Guía de onboarding técnico
├── arquitecture.md                # Documentación de arquitectura
├── api.md                         # Documentación de endpoints
└── qdrant-collection.mb           # Documentacion de qdrant

infra/
├── docker-compose.yml             # Orquestación de servicios
├── Dockerfile.fastapi             # Imagen para FastAPI
├── Dockerfile.flask               # Imagen para Flask
├── Dockerfile.react               # Imagen para React
└── db/
    └── init.sql                   # Script de inicialización de DB

services/
├── api-fastapi/                   # API principal (CRUD + búsqueda)
│   ├── alembic/                   # Migraciones de base de datos
│   ├── app/
│   │   ├── api/v1/                # Endpoints versioned
│   │   ├── core/                  # Configuración
│   │   ├── db/                    # Modelos y conexión
│   │   ├── schemas/               # Validación con Pydantic
│   │   ├── candidate.py           # Schemas de candidatos
│   │   ├── search.py              # Schemas de búsqueda
│   │   └── insights.py            # Schemas de insights (9 modelos Pydantic)
│   │   ├── llm/
│   │   │   ├── agent.py                   # Orquestador LLM con SOLID
│   │   │   ├── insight_service.py         # Lógica de generación de insights
│   │   │   ├── compression.py             # Compresión de contexto
│   │   │   ├── prompt_loader.py           # Carga de prompts
│   │   │   └── tools.py                   # Herramientas para LLM
│   │   └── main.py
│   ├── scripts/
│   │   └── seed_db.py             # Script de datos semilla
│   ├── requirements.txt
│   └── alembic.ini
│
├── api-flask/                     # API administrativa (ETL)
│   ├── app/
│   │   ├── api/                   # Rutas de ETL
│   │   ├── core/                  # Configuración
│   │   ├──services/              # Lógica de ETL
│   │   └── __init__.py
│   ├── requirements.txt
│   └── run.py

ui/
└── react-app/                     # Interfaz de usuario
    ├── src/
    │   ├── components/            # Componentes reutilizables
    │   │   ├── CandidateCRUD.tsx
    │   │   ├── SearchResults.tsx
    │   │   ├── InsightsSummary.tsx
    │   │   ├── ScoringCard.tsx
    │   │   ├── ComparisonChart.tsx
    │   │   └── SkillsAssessment.tsx
    │   ├── pages/                 # Páginas de la aplicación
    │   │   ├── Create.tsx
    │   │   ├── Edit.tsx
    │   │   ├── List.tsx
    │   │   ├── Show.tsx
    │   │   └── InsightsPage.tsx
    │   ├── services/              # Cliente API
    │   │   ├── ApiCandidate.ts
    │   │   └── InsightsApiService.ts
    │   ├── hooks/                 # Hooks personalizados
    │   │   ├── useInsights.ts
    │   │   ├── useScoring.ts
    │   │   └── useComparison.ts
    │   └── types/                 # Tipos TypeScript
    │       └── candidate.ts
    ├── package.json
    └── vite.config.ts

pipelines/
├── etl/                           # Pipeline ETL modular
│   ├── extract.py                 # Extracción de datos
│   ├── transform.py               # Transformación y embeddings
│   ├── load.py                    # Carga a Qdrant
│   └── main.py                    # Orquestador del pipeline
└── utils/
    ├── embeddings_service.py      # Servicio de generación de embeddings
    └── search_service.py          # Serrvicio de busqueda con qdrant

prompts/
├── candidate_summary/             # Prompts versionados para resúmenes
└── skill_extraction/              # Prompts para extracción de skills
```

## Documentación adicional

- **[Onboarding técnico](docs/onboarding.md)**: Guía paso a paso para nuevos desarrolladores
- **[Arquitectura](docs/arquitecture.md)**: Decisiones de diseño y patrones utilizados
- **[API Reference](docs/api.md)**: Documentación completa de endpoints
- **[ADRs](docs/adrs/)**: Decisiones arquitectónicas registradas
  - **ADR 005**: [Integración de LLM Cohere y Embeddings API](docs/adrs/005-llm-embedding-decision.md)
  - **ADR 004**: Vector Search con Qdrant
  - **ADR 003**: Refactor de búsqueda semántica
  - **ADR 002**: Migraciones de base de datos
  - **ADR 001**: Manejo descentralizado de errores
- **[SOLID Validation](docs/SOLID-validation.md)**: Prueba de cumplimiento de principios SOLID
- **[Implementation Checklist](docs/IMPLEMENTATION-CHECKLIST.md)**: Verificación de requisitos implementados

## Próximos pasos

Para continuar con el desarrollo del proyecto:

1. **Testing & Optimizaciones (Semana 3)**
   - Suite completa de unit tests para componentes LLM
   - Tests de integración para endpoints de insights
   - Implementación de caching con Redis
   - Rate limiting y quota management

2. **Monitoreo y Observabilidad**
   - Dashboards Grafana para métricas de insights
   - Alertas para latencia y costo de tokens
   - Logging centralizado con ELK

3. **Microfrontend en Svelte**
   - Vista especializada de análisis de candidatos
   - Integración con la aplicación React principal
   - Module Federation para carga lazy

4. **Optimizaciones de Cohere API**
   - Migración de embeddings locales a Cohere (4 fases)
   - Fine-tuning de prompts con feedback
   - A/B testing de modelos y temperaturas

## Contribuciones

Este proyecto forma parte de un plan de onboarding. Para contribuir:

1. Revisar la [documentación de arquitectura](docs/arquitecture.md)
2. Consultar los [ADRs](docs/adrs/) para entender decisiones de diseño
3. Seguir la [guía de onboarding](docs/onboarding.md) para configurar el entorno
