# Arquitectura del Sistema

Este documento describe la arquitectura general del proyecto **Candidate Profile Intelligence Platform**, incluyendo los componentes principales, sus responsabilidades y la forma en que se comunican entre sí.

La arquitectura se desarrolla de manera incremental y evoluciona a lo largo del onboarding técnico.

## Visión general

El sistema está diseñado como una arquitectura basada en servicios, con separación clara entre frontend, backend, procesamiento de datos e infraestructura.

En su estado actual (Semana 1), la arquitectura soporta un flujo CRUD end-to-end desde la interfaz de usuario hasta la base de datos.


## Componentes del sistema

### Frontend

- **React App**
  - Interfaz principal construida con React y TypeScript.
  - **Gestión de Formularios**: Implementación de `react-hook-form` para validaciones eficientes y manejo de estado.
  - **Diseño y Estilo**: Sistema de estilos moderno con CSS optimizado, incluyendo tablas con zebra-striping, efectos de hover y diseño responsivo.
  - **Arquitectura de Red**: Capa de servicios centralizada (`ApiCandidate.tsx`) con gestión de errores y estados de carga (`loading`) descentralizados directamente en los componentes de página para mayor precisión visual.
  - Consume la API pública expuesta por FastAPI.

> En fases posteriores se integrará un microfrontend en Svelte para vistas especializadas.


### Backend

- **FastAPI**
  - API pública del sistema
  - Exposición de endpoints CRUD para la entidad principal (Candidate)
  - Validaciones y documentación OpenAPI

- **Flask (Administración)**
  - API administrativa
  - Orquestación de procesos ETL y tareas de mantenimiento
  - No expuesta directamente al usuario final


### Data & Storage

- **PostgreSQL**
  - Base de datos relacional principal

- **Qdrant**
  - Motor de búsqueda vectorial

- **Redis**
  - Cache y soporte para procesamiento asíncrono

### Persistencia y Migraciones

- **Alembic**: Gestiona las migraciones de forma asíncrona al flujo de la aplicación.

- **Estrategia de Seeds**: Los datos de prueba se gestionan mediante scripts de Python para mantener la consistencia con los tipos de datos definidos en los modelos de SQLAlchemy.


## Flujo actual

```text
React → FastAPI → PostgreSQL
```

## Infraestructura
- Servicios containerizados con Docker
- Orquestación local mediante Docker Compose
