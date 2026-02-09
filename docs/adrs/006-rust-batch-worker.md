# ADR 006 - Worker Batch en Rust para Procesamiento Asíncrono

**Estado**: Aprobado  
**Fecha**: 2026-02-09  
**Autores**: Oscar Osorio, Damian Martinez

## Contexto

El sistema **Candidate Profile Intelligence Platform** requiere procesamiento batch para dos operaciones principales:

1. **ETL de sincronización completa**: Extraer candidatos no indexados de PostgreSQL, generar embeddings mediante Cohere API, e indexarlos en Qdrant
2. **Generación de embeddings por lotes**: Procesar grupos específicos de candidatos bajo demanda

### Requisitos Identificados

- Procesamiento asíncrono que no bloquee las APIs principales (FastAPI/Flask)
- Alta eficiencia en el consumo de recursos para procesamiento de largo plazo
- Capacidad de escalar horizontalmente con múltiples workers
- Manejo robusto de errores y reintentos
- Logging detallado para monitoreo y debugging
- Integración con sistema de colas (Redis)

### Limitaciones del Enfoque Anterior

El procesamiento ETL inicial estaba implementado directamente en Flask con ejecución síncrona:
- **Bloqueo de API**: Los requests ETL bloqueaban el servidor Flask durante todo el procesamiento
- **Timeout de requests**: Procesos largos excedían los timeouts de HTTP
- **Consumo de recursos**: Python consume significativamente más memoria en operaciones de larga duración
- **Escalabilidad limitada**: Difícil escalar horizontalmente sin infraestructura adicional (Celery)

## Decisión

Implementar un **Worker dedicado en Rust** que consuma jobs de una cola Redis y ejecute el procesamiento batch de forma asíncrona.

### Componentes Implementados

1. **Flask Admin API** (`/v1/admin/etl/sync`):
   - Recibe solicitudes de procesamiento ETL
   - Encola jobs en formato JSON a Redis
   - Retorna inmediatamente con job ID (HTTP 202 Accepted)

2. **Redis Queue** (`jobs:etl`):
   - Cola FIFO para jobs pendientes
   - Almacena estado de jobs procesados (`job:{id}`)
   - Soporte para múltiples consumidores (workers)

3. **Rust Worker**:
   - Consume jobs con `BLPOP` (bloqueante, eficiente)
   - Arquitectura modular:
     - `config.rs`: Gestión de configuración desde variables de entorno
     - `queue.rs`: Conexión y operaciones con Redis
     - `jobs/`: Procesadores especializados por tipo de job
   - Runtime asíncrono con **Tokio**
   - Logging detallado con **tracing**

## Consecuencias

### Ventajas

**Alto rendimiento**: Procesamiento eficiente de grandes volúmenes de datos  
**Bajo consumo de recursos**: Menor footprint de memoria y CPU  
**Type safety**: Detección temprana de errores en compilación  
**Escalabilidad**: Fácil agregar más workers según demanda  
**Desacoplamiento**: APIs no bloqueadas por procesamiento pesado  
**Logging robusto**: Tracing estructurado con niveles de log configurables  

### Desventajas

**Curva de aprendizaje**: Equipo necesita familiarizarse con Rust y ownership model  
**Debugging más complejo**: Menos herramientas de profiling que Python  
**Dependencias compiladas**: Cambios requieren rebuild completo

- [Redis Lists como Job Queue](https://redis.io/topics/data-types#lists)
- [Tokio - Async Runtime para Rust](https://tokio.rs/)
- [Cohere Embed API](https://docs.cohere.com/reference/embed)
- [Qdrant Client Rust](https://docs.qdrant.tech/documentation/quick-start/)
