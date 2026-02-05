# ADR 005: Integración de LLM Cohere y Embedding API - Insights Avanzados

- **Estado:** Aceptado
- **Fecha:** 2026-02-04
- **Autor:** Oscar Osorio

## Contexto

En la fase de desarrollo de Semana 2 (Día 9-10), el sistema requiere capacidades avanzadas de inteligencia artificial para generar insights automáticos sobre candidatos. Esto incluye:

1. **Generación de resúmenes técnicos** - Análisis profundo del perfil del candidato
2. **Scoring de compatibilidad** - Evaluación entre candidato y descripción de vacante
3. **Análisis comparativo** - Posicionamiento del candidato vs similares en el mercado
4. **Extracción de habilidades** - Identificación y evaluación estructurada de skills

### Desafíos Identificados

- **Calidad de análisis:** Los prompts versionados requieren un LLM potente para generar insights de calidad
- **Multilingüismo:** El sistema debe soportar candidatos con perfiles en múltiples idiomas
- **Latencia:** Las respuestas deben ser rápidas para una experiencia de usuario fluida
- **Costo:** Necesidad de balancear calidad vs costo de tokens consumidos
- **Embeddings históricos:** La migración de embeddings locales a API requiere sincronización

## Decisión

Se decidió implementar una arquitectura híbrida de LLM y Embeddings usando **Cohere** como proveedor principal:

### 1. LLM - Cohere Command A

**Modelo:** `command-a-03-2025`

**Características:**

- Modelo más poderoso de Cohere, optimizado para reasoning y tareas complejas
- Soporte multilingüe nativo (incluido español)
- Contexto extendido (4096 tokens)
- Mejor rendimiento en tareas estructuradas y JSON output
- Pricing competitivo con ~2-3x mejora en calidad vs modelos anteriores

**Configuración:**

```python
llm = ChatCohere(
    model="command-a-03-2025",
    cohere_api_key=settings.COHERE_API_KEY,
    temperature=0,
)
```

**Casos de Uso:**

- Generación de resúmenes técnicos con análisis profundo
- Scoring de compatibilidad con justificación detallada
- Análisis comparativo y recomendaciones estratégicas
- Extracción y evaluación estructurada de skills

### 2. Embedding - Cohere Multilingual Light

**Modelo:** `embed-multilingual-light-v3.0`

**Características:**

- Optimizado para múltiples idiomas (incluyendo español)
- Ligero y rápido (768 dimensiones vs 1536 de modelos más grandes)
- Excelente balance entre calidad y performance
- Soporta búsqueda semántica multilingüe
- Mejor rendimiento que local `all-MiniLM-L6-v2` en contexto multilíngue

**Configuración:**

```python
class CoherEmbeddings:
    model_name = "embed-multilingual-light-v3.0"
    input_type = "search_document"  # o "search_query"
```

**Migración de Local a API:**

- Mantener `all-MiniLM-L6-v2` para candidatos existentes inicialmente
- Re-indexar gradualmente con `embed-multilingual-light-v3.0`
- Scripts de migración para transición sin downtime

### 3. Arquitectura Integrada

```
Generación de Insights (LLM)
├── Prompts - v1, v2
├── Context Compress

Búsqueda Semántica (Embeddings)
Model: embed-multilingual-light
├── Candidates
├── Qdrant, Search
```

## Consecuencias

### Positivas

**Calidad Superior de Insights**

- El modelo `command-a-03-2025` proporciona análisis más profundos y contextuales
- Mejor comprensión de lenguaje técnico y requerimientos complejos
- Justificaciones más convincentes en scoring

**Soporte Multilingüe Robusto**

- Embeddings multilingües nativos de Cohere
- Candidatos con perfiles en español, inglés, etc.
- Búsqueda semántica cross-lingüe

**Performance Mejorado**

- Embeddings API más rápidos que modelos locales
- Caching de embeddings en Qdrant
- Búsqueda más precisa en Qdrant

**Consistency en Stack**

- Mismo proveedor (Cohere) para LLM y Embeddings
- Mejores integraciones y compatibilidad
- Soporte unified desde un único proveedor

**Escalabilidad**

- API manejada por Cohere, no requiere GPUs locales
- Fácil de escalar sin infraestructura adicional
- Facturación por uso

### Negativas

**Dependencia de API Externa**

- Requerimiento de conectividad a Cohere API
- Posible latencia de red
- Fallback requerido si Cohere API está no disponible

**Costo Recurrente**

- Pricing por tokens consumidos en LLM
- Pricing por embeddings generados
- Requiere monitoreo de gastos

**Migración de Embeddings Históricos**

- Los embeddings existentes (local all-MiniLM) no son compatibles con API Cohere
- Requiere re-indexación de candidatos históricos
- Necesita script de migración y validación

**Rate Limiting y Quotas**

- Límites de llamadas por minuto/mes según plan
- Requiere manejo de rate limiting en código
- Posibles rechazos si se excede límite

### Estrategia de migración


#### Fase 1: Coexistencia
- Mantener embeddings locales existentes
- Nuevos candidatos con Cohere embeddings
- Qdrant con índices paralelos

#### Fase 2: Validación
- Validar calidad de búsqueda
- Comparar resultados
- Feedback de usuarios

#### Fase 3: Migración Gradual
- Re-indexar lotes de candidatos históricos
- Validar en cada lote
- Rollback plan

#### Fase 4: Finalización
- Eliminar índices de embeddings locales
- Usar únicamente Cohere embeddings
- Documentación de proceso


## Referencias

- [Cohere API Documentation](https://docs.cohere.com/)
- [Command A Model](https://docs.cohere.com/v1/docs/cohere-embed)
- [Embeddings API](https://docs.cohere.com/reference/embed)
- [Pricing](https://cohere.com/pricing)
- [ADR 003: Qdrant Search](./003-vector-search-with-qdrant.md)
