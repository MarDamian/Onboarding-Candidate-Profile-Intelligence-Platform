# ADR 007 - Timeouts y Reintentos

**Estado**: Aprobado  
**Fecha**: 2026-02-11  
**Autores**: Oscar Osorio, Damian Martinez

## Contexto

El sistema interactúa con diversas APIs externas (Cohere, LLMs) y bases de datos (PostgreSQL, Qdrant). Las fallas transitorias de red o la latencia excesiva en estos servicios externos afectaban la estabilidad de la plataforma, causando bloqueos en los hilos de ejecución o fallas críticas en los pipelines de datos (ETL).

### Requisitos Identificados

1.  **Resiliencia**: El sistema debe reintentar automáticamente operaciones fallidas por problemas temporales.
2.  **Límites de Tiempo**: Ninguna petición debe quedar colgada indefinidamente (Timeouts).
3.  **Reintentos Exponenciales**: Los reintentos deben espaciarse progresivamente para evitar saturar servicios en recuperación.
4.  **Omnipresencia**: La solución debe cubrir Python (FastAPI/ETL), Rust (Worker) y Frontend (React/Svelte).

## Decisión

Se decidió implementar mecanismos robustos de reintentos y timeouts utilizando las mejores prácticas de cada ecosistema.

### Componentes Implementados

1.  **Python (Tenacity)**:
    - Se integró la librería `tenacity` para manejar reintentos mediante decoradores.
    - Se creó `@external_api_retry` para llamadas a APIs y `@db_retry` para operaciones de base de datos.
    - Se configuró el timeout de las llamadas al LLM dinámicamente desde el `.env`.

2.  **Rust (Reqwest Middleware)**:
    - Se añadieron `reqwest-middleware` y `reqwest-retry`.
    - Se configuró una política de `ExponentialBackoff` para las llamadas al servicio de embeddings.
    - Se aplicaron `tokio::time::timeout` a las consultas de PostgreSQL y Qdrant.

3.  **Frontend (React/Svelte)**:
    - **React**: Se implementó un interceptor en un `apiClient` de Axios personalizado que maneja el conteo de reintentos y el delay.
    - **Svelte**: Se creó una función `fetchWithRetry` que encapsula la lógica de reintentos sobre el `fetch` nativo.

## Consecuencias

### Ventajas 

- **Mayor Disponibilidad**: Los cortes de red momentáneos ya no son visibles para el usuario final.
- **Eficiencia de Recursos**: Los hilos del servidor se liberan rápidamente gracias a los timeouts, evitando el agotamiento de recursos.
- **Idempotencia**: Se reforzó la seguridad en el pipeline de datos al asegurar que las operaciones críticas se completen exitosamente.

### Desventajas

- **Complejidad del Código**: Se añade una capa adicional de lógica en los servicios de API.
- **Latencia en Fallas Reales**: Una falla permanente ahora tarda unos segundos más en reportarse debido a los reintentos (ej. 3 intentos x 1-4s de espera en teoria).

## Guía de Pruebas Funcionales

Para verificar esta implementación en Docker:
1.  **Frontend**: Detener el servicio `api-fastapi` y observar los reintentos en la consola del navegador.
2.  **IA**: Establecer `LLM_TIMEOUT=1` en el `.env` y observar cómo el sistema intenta la llamada 3 veces antes de fallar.
3.  **ETL**: Detener `qdrant` durante una sincronización y verificar que el worker reintenta la conexión en lugar de morir.
