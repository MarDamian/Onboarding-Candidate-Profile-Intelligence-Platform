# Documentación de la API - Candidate Profile Intelligence Platform

Bienvenido a la documentación de la API para la **Candidate Profile Intelligence Platform**. Esta API está construida con dos servicios:

- FastAPI: Permite gestionar perfiles de candidatos, incluyendo su creación, recuperación, actualización y eliminación.

- Flask: Permite gestionar procesos ETL y tareas de mantenimiento.

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

#### CandidateCreate (Hereda de CandidateBase)
Requerido para la creación. `name`, `email`, y `phone` son obligatorios.

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

## Flask - Documentación

### URL Base

| Entorno | URL Base |
| :--- | :--- |
| **Desarrollo** | `http://localhost:5000/v1` |

### Endpoints de Candidatos

#### 1. Procesar ETL y records procesados

- **URL:** `admin/etl/sync/`
- **Método:** `POST`
- **Respuesta Exitosa:**
  - **Código:** `200 OK`
  - **Contenido:** status, mensaje y records procesados.

#### 2. Status de jobs

- **URL:** `admin/etl/status/`
- **Método:** `GET`
- **Respuesta Exitosa:**
  - **Código:** `200 OK`
  - **Contenido:** Jobs encontrados y status.