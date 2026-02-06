# Arquitectura del Sistema

Este documento describe la arquitectura general del proyecto **Candidate Profile Intelligence Platform**, incluyendo los componentes principales, sus responsabilidades y la forma en que se comunican entre sí.

La arquitectura se desarrolla de manera incremental y evoluciona a lo largo del onboarding técnico.

## Visión general

El sistema está diseñado como una arquitectura basada en servicios, con separación clara entre frontend, backend, procesamiento de datos e infraestructura.

En su estado actual (Semana 1), la arquitectura soporta un flujo CRUD end-to-end desde la interfaz de usuario hasta la base de datos.


## Componentes del sistema

### UI - Frontend

- **React App**
  - Interfaz principal construida con React y TypeScript.
  - **Gestión de Formularios**: Implementación de `react-hook-form` para validaciones eficientes y manejo de estado.
  - **Diseño y Estilo**: Sistema de estilos moderno con CSS optimizado, incluyendo tablas con zebra-striping, efectos de hover y diseño responsivo.
  - **Arquitectura de Red**: Capa de servicios centralizada (`CandidateService.ts`) con gestión de errores y estados de carga (`loading`) descentralizados directamente en los componentes de página para mayor precisión visual.
  - Consume la API pública expuesta por FastAPI.

> En fases posteriores se integrará un microfrontend en Svelte para vistas especializadas.


### Servicios - Backend

- **FastAPI**
  - API pública del sistema
  - Exposición de endpoints CRUD para la entidad principal (Candidate)
  - **Búsqueda semántica** con embeddings y filtros avanzados
  - Validaciones y documentación OpenAPI

- **Flask (Administración)**
  - API administrativa
  - Orquestación de procesos ETL
  - Gestión de colección Qdrant (reindex, stats, clear, rebuild)
  - Endpoints admin bajo `/v1/admin/etl` y `/v1/admin/qdrant`
  - No expuesta directamente al usuario final


### Pipelines - Procesamiento de Datos

- **ETL Pipeline**
  - **Extract**: Obtiene candidatos no indexados de PostgreSQL
  - **Transform**: Genera embeddings usando la API de Cohere
  - **Load**: Indexa en Qdrant y marca como procesados
  - Idempotencia garantizada con `last_indexed_at`

- **Embeddings Service**
  - Servicio centralizado para generación de vectores via API de Cohere
  - Modelo configurable via `EMBEDDING_MODEL` (default: embed-multilingual-v3.0)
  - Dimensión configurable via `EMBEDDING_DIMENSION` (default: 1024)
  - Distancia configurable via `EMBEDDING_DISTANCE` (default: Cosine)
  - Cloud API (sin carga local de modelos)

- **Search Service**
  - Búsqueda semántica en Qdrant
  - Filtros dinámicos (skills, nombre)
  - Score threshold configurable


### Data & Storage

- **PostgreSQL**
  - Base de datos relacional principal
  - Almacena información estructurada de candidatos
  - Campo `last_indexed_at` para control de indexación

- **Qdrant**
  - Motor de búsqueda vectorial
  - Colección `candidates` con configuración dinámica
  - Dimensión y distancia definidas por variables de entorno
  - Búsqueda por similitud con score threshold
  - Endpoints admin para mantenimiento (stats, clear, rebuild)

- **Redis**
  - Cache y soporte para procesamiento asíncrono
  - Tracking de jobs ETL

### Persistencia y Migraciones

- **Alembic**: Gestiona las migraciones de forma asíncrona al flujo de la aplicación.

- **Estrategia de Seeds**: Los datos de prueba se gestionan mediante scripts de Python para mantener la consistencia con los tipos de datos definidos en los modelos de SQLAlchemy.

### LLM y Embedding

- **LLM**: Implementado con langchain y cohere.
- **Embedding**: Para el embedding para no tener localmente por procesos pesados de espacio, se opto por api de cohere.

## Infraestructura

### Containerización
- Servicios containerizados con Docker
- Orquestación local mediante Docker Compose
- Volúmenes compartidos: 
  - `../pipelines:/app/pipelines` en FastAPI y Flask
  - `../prompts:/app/prompts` en FastAPI

### Imágenes Base
- **PostgreSQL**: `postgres:17.5-alpine`
- **Redis**: `redis:8.4.0-alpine`
- **Qdrant**: `qdrant/qdrant:v1.16.2`
- **Python**: `python:3.12-slim` (FastAPI y Flask)

### Startup Automático
- **FastAPI**: Ejecuta migraciones → seed → servidor
- **Flask**: Workers con timeout extendido para procesos ETL de larga duración
