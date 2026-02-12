# ADR 004: Refactorización de Búsqueda Semántica - Migración de Flask a FastAPI

- **Estado:** Aceptado
- **Fecha:** 2026-02-03
- **Autor:** Oscar Osorio

## Contexto

El proyecto inicial tenía una arquitectura de dos APIs:
- **API Flask**: Gestión de ETL, Qdrant indexación y búsquedas semánticas
- **API FastAPI**: Gestión de candidatos

Esta división no era la especificada.

## Decisión

Se decidio que las búsquedas semánticas se **consolidarán en FastAPI**, migrando:

### Endpoints de Flask a FastAPI:

**Búsqueda Semántica (FastAPI `/v1/semantic_search`):**
- `POST /v1/semantic_search/` → Búsqueda semántica con filtros
- `GET /v1/semantic_search/similar/{candidate_id}` → Candidatos similares

### Arquitectura resultante:

```
FastAPI (Puerto 8000)
├── /v1/candidates (CRUD)
├── /v1/semantic_search (búsqueda)
```

## Implementación

### 1. Servicios necesarios

Reutilizar servicios existentes:
- `pipelines.utils.search_service.SearchService` (búsqueda semántica)
- `pipelines.etl.main.run_pipeline()` (ejecución ETL)
- Crear `EtlManager` equivalente si es necesario

### 2. Esquema

- SearchRequest

### 3. Integración en main.py

Registrar el nuevo router:
```python
from app.api.v1 import search
app.include_router(search.router, prefix="/v1")
```

## Consecuencias

### Positivas
- **Arquitectura Especifica en Onboarding**
- **Consistencia**: Mismos patrones de error, validación y respuesta

## Plan de Migración

1. Documentar cambios en rutas
2. Notificar sobre nuevas URLs
5. Deprecar endpoints de Flask gradualmente

## Referencia

- Ver [003-vector-search-with-qdrant.md](003-vector-search-with-qdrant.md)
- Ver [002-database-migrations-and-seeding.md](002-database-migrations-and-seeding.md)