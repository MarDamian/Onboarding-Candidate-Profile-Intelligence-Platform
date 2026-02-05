# Colección de Qdrant - Documentación

## Información General

- **Nombre de la colección**: `candidates`
- **Dimensión de vectores**: Configurable via `EMBEDDING_DIMENSION` (default: 384)
- **Función de distancia**: Configurable via `EMBEDDING_DISTANCE` (default: Cosine)
- **Modelo de embeddings**: Configurable via `EMBEDDING_MODEL` (default: all-MiniLM-L6-v2)

### Variables de Entorno

Todas las configuraciones de embeddings se gestionan mediante variables de entorno definidas en `infra/.env`:

```bash
EMBEDDING_MODEL=all-MiniLM-L6-v2
EMBEDDING_DIMENSION=384
EMBEDDING_DISTANCE=Cosine
```

**Opciones disponibles:**
- **EMBEDDING_MODEL**: Cualquier modelo de sentence-transformers
  - `all-MiniLM-L6-v2` (384 dims, rápido, CPU)
  - `paraphrase-multilingual-MiniLM-L12-v2` (384 dims, multilenguaje)
  - `all-mpnet-base-v2` (768 dims, mejor calidad)
  
- **EMBEDDING_DISTANCE**: Métrica de similitud
  - `Cosine` - Similitud coseno (recomendado)
  - `Euclid` - Distancia euclidiana
  - `Dot` - Producto punto

- **EMBEDDING_DIMENSION**: Tamaño del vector (debe coincidir con el modelo)

---

## Estructura de la Colección

### Vector

Cada candidato se representa como un vector de 384 dimensiones generado por `sentence-transformers` a partir del texto contextual:

```
{candidate.name} | {candidate.summary} | Skills: {candidate.skills} | Experience: {candidate.experience}
```

### Payload

Cada punto en la colección contiene los siguientes campos:

| Campo | Tipo | Descripción | Ejemplo |
|-------|------|-------------|---------|
| `name` | string | Nombre completo del candidato | "Juan Pérez" |
| `text_content` | string | Texto concatenado usado para generar el embedding | "Juan Pérez \| Senior Developer..." |
| `update_at` | string | Timestamp de última actualización | "2026-02-01 10:30:00" |

---

## Proceso de Indexación

### 1. Extracción (extract.py)
```sql
SELECT id, name, summary, skills, experience, updated_at
FROM candidates
WHERE last_indexed_at IS NULL OR updated_at > last_indexed_at
```
- Obtiene candidatos **no indexados** o **modificados** desde última indexación
- Garantiza **idempotencia** del proceso ETL

### 2. Transformación (transform.py)
```python
# Construir contexto textual rico
context_text = f"{name} | {summary} | Skills: {skills} | Experience: {experience}"

# Generar embedding usando el modelo configurado en EMBEDDING_MODEL
vector = embeddings_service.generate_embedding(context_text)
```
- Concatena información relevante del candidato
- Genera vector usando el modelo especificado en `.env`
- La dimensión del vector coincide con `EMBEDDING_DIMENSION`

### 3. Carga (load.py)
```python
# Leer configuración desde variables de entorno
dimension = int(os.getenv("EMBEDDING_DIMENSION", "384"))
distance = os.getenv("EMBEDDING_DISTANCE", "Cosine")

# Crear/verificar colección con configuración dinámica
q_client.create_collection(
    collection_name="candidates",
    vectors_config=VectorParams(size=dimension, distance=distance)
)

# Insertar/actualizar puntos
q_client.upsert(collection_name="candidates", points=points)

# Marcar como indexado en PostgreSQL
UPDATE candidates SET last_indexed_at = NOW() WHERE id IN (...)
```
- Garantiza que la colección exista
- Usa `upsert` para evitar duplicados
- Actualiza `last_indexed_at` para idempotencia

## Búsqueda Semántica

### Endpoint: POST /v1/search/

**Request Body:**
```json
{
  "query": "desarrollador python con experiencia en machine learning",
  "limit": 10,
  "score_threshold": 0.5,
  "skills_filter": ["Python", "TensorFlow"],
  "name_filter": "Juan"
}
```

**Response:**
```json
{
  "query": "desarrollador python con experiencia en machine learning",
  "total_results": 3,
  "results": [
    {
      "id": 1,
      "score": 0.87,
      "name": "Juan Pérez",
      "text_content": "Juan Pérez | Senior ML Engineer...",
      "updated_at": "2026-02-01"
    }
  ]
}
```

### Parámetros de Búsqueda

| Parámetro | Tipo | Default | Descripción |
|-----------|------|---------|-------------|
| `query` | string | **requerido** | Texto de búsqueda en lenguaje natural |
| `limit` | int | 10 | Número máximo de resultados (1-50) |
| `score_threshold` | float | 0.5 | Umbral mínimo de similitud (0.0-1.0) |
| `skills_filter` | list[string] | null | Filtrar por skills específicas |
| `name_filter` | string | null | Filtrar por nombre del candidato |

### Score de Similitud

- **0.0 - 0.4**: Poca relevancia
- **0.5 - 0.7**: Relevancia moderada
- **0.7 - 0.9**: Alta relevancia
- **0.9 - 1.0**: Muy alta relevancia (casi idéntico)

---

## Endpoint Adicional: Buscar Similares

### Endpoint: GET /v1/search/similar/{candidate_id}

Encuentra candidatos similares a uno existente.

**Request:**
```
GET /v1/search/similar/5?limit=5&score_threshold=0.6
```

**Response:**
```json
{
  "query": "Similares al candidato ID 5",
  "total_results": 5,
  "results": [
    {
      "id": 12,
      "score": 0.82,
      "name": "María García",
      "text_content": "María García | Backend Developer..."
    }
  ]
}
```

**Casos de uso:**
- Recomendaciones de candidatos relacionados
- Encontrar perfiles complementarios
- Detección de duplicados

---

## Mantenimiento

### Endpoints Administrativos (Flask API - Puerto 5000)

#### 1. Ejecutar Pipeline ETL

**Endpoint:** `POST /v1/admin/etl/sync`

Ejecuta el pipeline completo de ETL para sincronizar candidatos desde PostgreSQL a Qdrant.

#### 2. Consultar Estado del ETL

**Endpoint:** `GET /v1/admin/etl/status`

Obtiene el historial de ejecuciones del ETL almacenado en Redis.

### Re-indexación Completa

**Endpoint:** `POST /v1/admin/qdrant/reindex`

Para re-indexar todos los candidatos (forzar sincronización completa):

## Optimizaciones

### Modelo de Embeddings

**Actual:** `all-MiniLM-L6-v2`
- Dimensiones: 384
- Tamaño: ~80MB
- Velocidad: ~2000 sentencias/segundo (CPU)

**Alternativas:**

| Modelo | Dimensiones | Tamaño | Uso |
|--------|-------------|--------|-----|
| `paraphrase-MiniLM-L3-v2` | 384 | ~60MB | Más rápido, menor calidad |
| `all-mpnet-base-v2` | 768 | ~420MB | Mejor calidad, más lento |

### Indexación Incremental

El sistema ya implementa indexación incremental mediante `last_indexed_at`:
- Solo procesa candidatos nuevos o modificados
- Evita re-procesamiento innecesario
- Optimiza recursos de cómputo


