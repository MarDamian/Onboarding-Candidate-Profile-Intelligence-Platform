# Documentación de la API - Candidate Profile Intelligence Platform

Bienvenido a la documentación de la API para la **Candidate Profile Intelligence Platform**. Esta API está construida con dos servicios:

- **FastAPI** (Puerto 8000): API pública para CRUD de candidatos
  - Crear, leer, actualizar y eliminar candidatos
  - Operaciones síncronas y rápidas
  - Documentación automática en `/docs`

- **Flask** (Puerto 5000): API administrativa para ETL, búsqueda semántica y mantenimiento
  - Procesos ETL para indexación
  - Búsqueda semántica con Qdrant
  - Operaciones de administración y mantenimiento

## FastAPI - Documentación

### URL Base

| Entorno | URL Base |
| :--- | :--- |
| **Desarrollo** | `http://localhost:8000/v1` |

### Endpoints de Candidatos

#### 1. Listar Candidatos
Recupera una lista de todos los candidatos registrados en el sistema.

- **URL:** `/candidate/`
- **Método:** `GET`
- **Respuesta Exitosa:**
  - **Código:** `200 OK`
  - **Contenido:** Lista de objetos `CandidateRead`.

#### 2. Obtener Detalle de Candidato
Recupera información detallada de un solo candidato mediante su ID.

- **URL:** `/candidate/{id}`
- **Método:** `GET`
- **Parámetros de URL:** `id=[int]`
- **Respuesta Exitosa:**
  - **Código:** `200 OK`
  - **Contenido:** Objeto `CandidateRead`.
- **Respuesta de Error:**
  - **Código:** `404 Not Found` (El candidato no existe).

#### 3. Crear Candidato
Crea un nuevo perfil de candidato.

- **URL:** `/candidate/`
- **Método:** `POST`
- **Parámetros de Datos:** Objeto `CandidateCreate`.
- **Respuesta Exitosa:**
  - **Código:** `201 Created`
  - **Contenido:** Objeto `CandidateCreate`.
- **Respuestas de Error:**
  - **Código:** `422 Unprocessable Entity` (Error de validación).
  - **Código:** `409 Conflict` (El correo electrónico o teléfono ya existen).

#### 4. Actualizar Candidato
Actualiza un perfil de candidato existente.

- **URL:** `/candidate/{id}`
- **Método:** `PUT`
- **Parámetros de URL:** `id=[int]`
- **Parámetros de Datos:** Objeto `CandidateUpdate`.
- **Respuesta Exitosa:**
  - **Código:** `200 OK`
  - **Contenido:** Objeto `CandidateRead` actualizado.
- **Respuestas de Error:**
  - **Código:** `404 Not Found` (El candidato no existe).
  - **Código:** `422 Unprocessable Entity` (Error de validación).

#### 5. Eliminar Candidato
Elimina un perfil de candidato del sistema.

- **URL:** `/candidate/{id}`
- **Método:** `DELETE`
- **Parámetros de URL:** `id=[int]`
- **Respuesta Exitosa:**
  - **Código:** `200 OK` (Devuelve el objeto del candidato eliminado).
- **Respuesta de Error:**
  - **Código:** `404 Not Found` (El candidato no existe).

#### 6. Búsqueda Semántica de Candidatos
Realiza una búsqueda semántica utilizando embeddings y filtros opcionales.

- **URL:** `/semantic_search/`
- **Método:** `POST`
- **Parámetros de Datos:** Objeto `SearchRequest`.
- **Respuesta Exitosa:**
  - **Código:** `200 OK`
  - **Contenido:** Objeto `SearchResponse` con lista de candidatos ordenados por relevancia.
- **Respuestas de Error:**
  - **Código:** `500 Internal Server Error` (Error consultando historial).

#### 7. Buscar Candidatos Similares
Encuentra candidatos similares a uno existente basándose en su perfil.

- **URL:** `/semantic_search/similar/{candidate_id}`
- **Método:** `GET`
- **Parámetros de URL:** `candidate_id=[int]`
- **Parámetros de Query:**
  - `limit`: Número de resultados (default: 5)
  - `score_threshold`: Umbral de similitud (default: 0.0)
- **Respuesta Exitosa:**
  - **Código:** `200 OK`
  - **Contenido:** Objeto `SearchResponse` con candidatos similares.
- **Respuestas de Error:**
  - **Código:** `404 Not Found` (El candidato no está indexado en Qdrant).
  - **Código:** `500 Internal Server Error` (Error en el servidor de búsqueda).

#### 8. Generar insights
Genera insight para un candidato correspondiente.

- **URL:** `/insights/{candidate_id}/`
- **Método:** `GET`
- **Parámetros de URL:** `candidate_id=[int]`
- **Respuesta Exitosa:**
  - **Código:** `200 OK`
  - **Contenido:** Objeto `InsightSchema` con campos respectivos para la UI.
- **Respuestas de Error:**
  - **Código:** `404 Not Found` (El candidato no está en la base de datos).
  - **Código:** `500 Internal Server Error` (Error en el servidor al generar el insight).

### Esquemas (Schemas)

#### CandidateBase
Campos básicos de identificación.
```json
{
  "name": "string",
  "email": "usuario@ejemplo.com",
  "phone": "string",
  "location": "string (opcional)",
  "education": "string (opcional)",
  "headline": "string (opcional)",
  "summary": "string (opcional)",
  "role": "string (opcional)",
  "experience": "string (opcional)",
  "skills": "string (opcional)"
}
```
#### CandidateUpdate
Todos los campos son opcionales para permitir actualizaciones parciales.

#### CandidateRead (Hereda de CandidateBase)
Retornado por los métodos de consulta. Incluye campos del sistema:
- `id`: `int`
- `is_active`: `bool`
- `created_at`: `datetime`
- `updated_at`: `datetime`

#### SearchRequest
Campos para búsqueda semántica:
- `query`: `str`
- `limit`: `int`
- `score_threshold`: `float`
- `skills_filter`: `Optional[list[str]]`
- `name_filter`: `Optional[str]`

#### InsightSchema
Retorna de la request para la generación de Insights
- `summary`: `str`
- `score`: `int`
- `strengths`: `List[str]`
- `weaknesses`: `List[str]`
- `suggested_role`: `str`

### Códigos de Error Comunes

| Código | Descripción |
| :--- | :--- |
| **400** | Bad Request (Estructura de entrada inválida) |
| **404** | Not Found (El recurso no existe) |
| **409** | Conflict (Conflicto por datos duplicados como el email) |
| **422** | Unprocessable Entity (Fallo de validación, ej. formato de email inválido) |

## Flask - Documentación de Api Administrativa

### URL Base

| Entorno | URL Base |
| :--- | :--- |
| **Desarrollo** | `http://localhost:5000/v1` |

### Endpoints de Administración ETL

#### 1. Ejecutar Pipeline ETL
Procesa candidatos pendientes de indexación en Qdrant.

- **URL:** `/admin/etl/sync`
- **Método:** `POST`
- **Respuesta Exitosa:**
  - **Código:** `200 OK`
  - **Contenido:** Objeto con status, mensaje y número de registros procesados.
- **Respuestas de Error:**
  - **Código:** `500 Internal Server Error` (Error durante ejecución del ETL).

#### 2. Consultar Status de Jobs ETL
Obtiene el historial de ejecuciones del pipeline ETL.

- **URL:** `/admin/etl/status`
- **Método:** `GET`
- **Respuesta Exitosa:**
  - **Código:** `200 OK`
  - **Contenido:** Lista de jobs con sus estados y resultados.
- **Respuestas de Error:**
  - **Código:** `500 Internal Server Error` (Error consultando historial).

#### 3. Re-indexar Todos los Candidatos
Fuerza la re-indexación completa de todos los candidatos en Qdrant.

- **URL:** `/admin/qdrant/reindex`
- **Método:** `POST`
- **Respuesta Exitosa:**
  - **Código:** `200 OK`
  - **Contenido:** Objeto con status, mensaje y número de candidatos re-indexados.
- **Respuestas de Error:**
  - **Código:** `500 Internal Server Error` (Error durante la re-indexación).

#### 4. Obtener Estadísticas de Qdrant
Obtiene información y métricas de la colección de candidatos.

- **URL:** `/admin/qdrant/stats`
- **Método:** `GET`
- **Respuesta Exitosa:**
  - **Código:** `200 OK`
  - **Contenido:** Objeto con estadísticas de la colección.
- **Respuestas de Error:**
  - **Código:** `500 Internal Server Error` (Error obteniendo estadísticas).

#### 5. Limpiar Colección de Qdrant
Elimina todos los puntos de la colección de candidatos en Qdrant.

- **URL:** `/admin/qdrant/clear`
- **Método:** `DELETE`
- **Respuesta Exitosa:**
  - **Código:** `200 OK`
  - **Contenido:** Objeto con status, mensaje y número de puntos eliminados.
- **Respuestas de Error:**
  - **Código:** `500 Internal Server Error` (Error limpiando colección).

#### 6. Reconstruir Colección desde Cero
Reconstruye completamente la colección limpiando Qdrant y re-indexando todos los candidatos.

- **URL:** `/admin/qdrant/rebuild`
- **Método:** `POST`
- **Respuesta Exitosa:**
  - **Código:** `200 OK`
  - **Contenido:** Objeto con status, mensaje y número de candidatos re-indexados.
- **Respuestas de Error:**
  - **Código:** `500 Internal Server Error` (Error reconstruyendo colección).

---

## FastAPI - Endpoints de LLM Insights (Día 9-10)

### Introducción

Los endpoints de LLM proporcionan generación automática de insights sobre candidatos utilizando inteligencia artificial. Incluyen:

- **Resúmenes técnicos** - Análisis profundo del perfil
- **Scoring de compatibilidad** - Evaluación contra vacantes
- **Análisis comparativo** - Posicionamiento vs otros candidatos

**URL Base para Insights:** `http://localhost:8000/v1/insights`

### 1. Obtener Insights Generales de Candidato

Genera un resumen completo con análisis técnico, fortalezas, áreas de mejora y análisis comparativo.

- **URL:** `/insights/{candidate_id}`
- **Método:** `GET`
- **Parámetros de URL:**
  - `candidate_id`: ID del candidato (int, requerido)
- **Parámetros de Query:**
  - `include_comparison`: Incluir análisis comparativo (boolean, default: true)

**Respuesta Exitosa:**
```json
{
  "candidate_id": 1,
  "insight_type": "summary",
  "success": true,
  "summary": {
    "candidate_id": 1,
    "candidate_name": "Juan Pérez",
    "headline": "Senior Python Developer",
    "technical_summary": "Juan es un desarrollador Python con 5 años de experiencia...",
    "years_of_experience": 5.0,
    "key_skills": [
      {
        "skill": "Python",
        "proficiency_level": "Advanced",
        "years_of_experience": 5.0,
        "confidence_score": 0.95
      }
    ],
    "comparison_metrics": {
      "percentile_rank": 85.0,
      "similar_candidates_count": 5,
      "avg_experience_years": 4.2,
      "skill_alignment": 0.75
    },
    "strengths": ["Technical skills well-developed", "Domain expertise demonstrated"],
    "areas_for_improvement": ["Continuous learning opportunities"],
    "recommendations": ["Invest in cloud technologies", "Develop leadership skills"],
    "generated_at": "2026-02-04T10:30:00",
    "model_version": "v1"
  },
  "score": null,
  "error": null
}
```

**Códigos de Respuesta:**
- `200 OK`: Insight generado exitosamente
- `404 Not Found`: Candidato no existe
- `500 Internal Server Error`: Error generando insight

---

### 2. Generar Score de Compatibilidad

Evalúa la compatibilidad técnica y cultural entre un candidato y una descripción de vacante.

- **URL:** `/insights/score`
- **Método:** `POST`
- **Content-Type:** `application/json`

**Request Body:**
```json
{
  "candidate_id": 1,
  "job_description": "Buscamos Senior Python Developer con 5+ años de experiencia en Django/FastAPI...",
  "required_skills": ["Python", "FastAPI", "PostgreSQL", "Docker"],
  "nice_to_have_skills": ["Kubernetes", "Redis", "AWS"],
  "weight_technical": 0.7,
  "weight_cultural_fit": 0.3
}
```

**Respuesta Exitosa:**
```json
{
  "candidate_id": 1,
  "insight_type": "score",
  "success": true,
  "summary": null,
  "score": {
    "overall_score": 0.85,
    "technical_score": 0.90,
    "cultural_fit_score": 0.75,
    "justification": "Excelente alineación técnica. El candidato cubre todas las skills requeridas...",
    "matching_skills": ["Python", "FastAPI", "PostgreSQL", "Docker"],
    "missing_skills": ["Kubernetes"],
    "growth_potential": "High"
  },
  "error": null
}
```

**Códigos de Respuesta:**
- `200 OK`: Score calculado exitosamente
- `404 Not Found`: Candidato no existe
- `422 Unprocessable Entity`: Validación fallida (job_description muy corta)
- `500 Internal Server Error`: Error calculando score

**Validaciones:**
- `job_description`: Mínimo 10 caracteres
- `candidate_id`: Mayor a 0
- Pesos: entre 0.0 y 1.0

---

### 3. Generar Resumen Detallado

Genera un análisis profundo del candidato con evaluación de skills, potencial y recomendaciones.

- **URL:** `/insights/summary`
- **Método:** `POST`
- **Content-Type:** `application/json`

**Request Body:**
```json
{
  "candidate_id": 1,
  "include_comparison": true,
  "include_skills_assessment": true,
  "comparison_limit": 5
}
```

**Respuesta Exitosa:**
- Estructura idéntica al endpoint GET `/insights/{candidate_id}`
- Incluye análisis más detallado de skills

**Códigos de Respuesta:**
- `200 OK`: Resumen generado
- `404 Not Found`: Candidato no existe
- `500 Internal Server Error`: Error generando resumen

---

### 4. Obtener Análisis Comparativo

Compara el candidato con otros perfiles similares en la base de datos.

- **URL:** `/insights/{candidate_id}/comparison`
- **Método:** `GET`
- **Parámetros de URL:**
  - `candidate_id`: ID del candidato (int, requerido)
- **Parámetros de Query:**
  - `limit`: Cantidad de similares (int, default: 5, rango: 1-20)
  - `score_threshold`: Umbral mínimo de similitud (float, default: 0.3, rango: 0.0-1.0)

**Respuesta Exitosa:**
```json
{
  "reference_candidate_id": 1,
  "reference_candidate_name": "Juan Pérez",
  "comparison_metrics": {
    "percentile_rank": 85.0,
    "similar_candidates_count": 5,
    "avg_experience_years": 4.2,
    "skill_alignment": 0.75
  },
  "similar_profiles": [
    {
      "id": 2,
      "name": "María García",
      "score": 0.92
    },
    {
      "id": 3,
      "name": "Carlos López",
      "score": 0.88
    }
  ],
  "insights": "Juan se posiciona en el percentil 85, por encima del promedio...",
  "generated_at": "2026-02-04T10:30:00"
}
```

**Códigos de Respuesta:**
- `200 OK`: Comparación generada
- `404 Not Found`: Candidato no existe
- `500 Internal Server Error`: Error generando comparación

---

### 5. Health Check del Servicio de LLM

Verifica la disponibilidad y configuración del servicio de LLM.

- **URL:** `/insights/health`
- **Método:** `GET`

**Respuesta Exitosa:**
```json
{
  "status": "healthy",
  "service": "LLM Insights",
  "version": "1.0.0"
}
```

**Respuesta de Error:**
```json
{
  "detail": "LLM service unavailable: COHERE_API_KEY not configured"
}
```

**Códigos de Respuesta:**
- `200 OK`: Servicio disponible
- `503 Service Unavailable`: Servicio no configurado o no disponible

---

## Esquemas Principales

### InsightResponse

```typescript
{
  candidate_id: number;
  insight_type: "summary" | "score" | "comparison";
  summary?: CandidateSummary;
  score?: ScoreResult;
  error?: string;
  success: boolean;
}
```

### CandidateSummary

```typescript
{
  candidate_id: number;
  candidate_name: string;
  headline: string;
  technical_summary: string;
  years_of_experience: number;
  key_skills: SkillAssessment[];
  comparison_metrics?: ComparisonMetrics;
  strengths: string[];
  areas_for_improvement: string[];
  recommendations: string[];
  generated_at: datetime;
  model_version: string;
}
```

### ScoreResult

```typescript
{
  overall_score: number; // 0-1
  technical_score: number; // 0-1
  cultural_fit_score: number; // 0-1
  justification: string;
  matching_skills: string[];
  missing_skills: string[];
  growth_potential: "Low" | "Medium" | "High";
}
```

### SkillAssessment

```typescript
{
  skill: string;
  proficiency_level: "Beginner" | "Intermediate" | "Advanced" | "Expert";
  years_of_experience: number;
  confidence_score: number; // 0-1
}
```

---

## Manejo de Errores

Todos los endpoints retornan errores estructurados:

```json
{
  "detail": "Descripción del error"
}
```

**Errores Comunes:**

| Status | Descripción | Causa |
|--------|-------------|-------|
| 404 | Candidato no encontrado | El ID del candidato no existe |
| 422 | Validación fallida | Datos inválidos en request |
| 500 | Error del servidor | Fallo interno (LLM, DB, etc) |
| 503 | Servicio no disponible | LLM no configurado o API key inválida |

---

## Ejemplos de Uso

### Ejemplo 1: Obtener Insights Completos

```bash
curl -X GET "http://localhost:8000/v1/insights/1?include_comparison=true" \
  -H "accept: application/json"
```

### Ejemplo 2: Evaluar Candidato contra Vacante

```bash
curl -X POST "http://localhost:8000/v1/insights/score" \
  -H "Content-Type: application/json" \
  -d '{
    "candidate_id": 1,
    "job_description": "Buscamos Senior Python Developer con experiencia en FastAPI y PostgreSQL...",
    "required_skills": ["Python", "FastAPI", "PostgreSQL"],
    "weight_technical": 0.75,
    "weight_cultural_fit": 0.25
  }'
```

### Ejemplo 3: Comparar con Candidatos Similares

```bash
curl -X GET "http://localhost:8000/v1/insights/1/comparison?limit=10&score_threshold=0.5" \
  -H "accept: application/json"
```

---

## Consideraciones de Performance

- **Latencia**: Cada llamada a LLM toma 2-5 segundos aproximadamente
- **Caching**: Los prompts se cachean en memoria para mejor performance
- **Compresión**: El contexto se comprime automáticamente para ahorrar tokens
- **Async**: Todos los endpoints son asíncronos para máxima concurrencia

---

## Próximos Pasos

1. **Frontend Integration**: Integrar endpoints en React UI
2. **Caching**: Implementar Redis para cachear insights generados
3. **A/B Testing**: Soportar múltiples versiones de prompts
4. **Feedback Loop**: Recolectar feedback de insights para mejora continua
