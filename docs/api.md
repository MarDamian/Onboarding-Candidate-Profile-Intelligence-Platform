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

#### 3. Búsqueda Semántica de Candidatos
Realiza una búsqueda semántica utilizando embeddings y filtros opcionales.

- **URL:** `/search/`
- **Método:** `POST`
- **Parámetros de Datos:** Objeto `SearchRequest`.
- **Respuesta Exitosa:**
  - **Código:** `200 OK`
  - **Contenido:** Objeto `SearchResponse` con lista de candidatos ordenados por relevancia.
- **Respuestas de Error:**
  - **Código:** `500 Internal Server Error` (Error consultando historial).

#### 4. Buscar Candidatos Similares
Encuentra candidatos similares a uno existente basándose en su perfil.

- **URL:** `/search/similar/{candidate_id}`
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

#### 5. Re-indexar Todos los Candidatos
Fuerza la re-indexación completa de todos los candidatos en Qdrant.

- **URL:** `/admin/qdrant/reindex`
- **Método:** `POST`
- **Respuesta Exitosa:**
  - **Código:** `200 OK`
  - **Contenido:** Objeto con status, mensaje y número de candidatos re-indexados.
- **Respuestas de Error:**
  - **Código:** `500 Internal Server Error` (Error durante la re-indexación).

#### 6. Obtener Estadísticas de Qdrant
Obtiene información y métricas de la colección de candidatos.

- **URL:** `/admin/qdrant/stats`
- **Método:** `GET`
- **Respuesta Exitosa:**
  - **Código:** `200 OK`
  - **Contenido:** Objeto con estadísticas de la colección.
- **Respuestas de Error:**
  - **Código:** `500 Internal Server Error` (Error obteniendo estadísticas).

#### 7. Limpiar Colección de Qdrant
Elimina todos los puntos de la colección de candidatos en Qdrant.

- **URL:** `/admin/qdrant/clear`
- **Método:** `DELETE`
- **Respuesta Exitosa:**
  - **Código:** `200 OK`
  - **Contenido:** Objeto con status, mensaje y número de puntos eliminados.
- **Respuestas de Error:**
  - **Código:** `500 Internal Server Error` (Error limpiando colección).

#### 8. Reconstruir Colección desde Cero
Reconstruye completamente la colección limpiando Qdrant y re-indexando todos los candidatos.

- **URL:** `/admin/qdrant/rebuild`
- **Método:** `POST`
- **Respuesta Exitosa:**
  - **Código:** `200 OK`
  - **Contenido:** Objeto con status, mensaje y número de candidatos re-indexados.
- **Respuestas de Error:**
  - **Código:** `500 Internal Server Error` (Error reconstruyendo colección).
