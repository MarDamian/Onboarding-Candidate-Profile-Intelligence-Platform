# ADR 003: Motor de Búsqueda Vectorial con Qdrant y Sentence Transformers

*   **Estado:** Aceptado
*   **Fecha:** 2026-02-03
*   **Autor:** Damian Martinez

## Contexto

El sistema requiere capacidades de búsqueda semántica para permitir a los usuarios encontrar candidatos basándose en descripciones en lenguaje natural, más allá de coincidencias exactas de palabras clave. Esto requiere:

1. Generación de embeddings (vectores) a partir de texto
2. Almacenamiento eficiente de vectores de alta dimensión
4. Capacidad de combinar búsqueda vectorial con filtros.

## Decisión

Hemos decidido implementar **Qdrant v1.16.2** como motor de búsqueda vectorial y **Sentence Transformers** con el modelo `all-MiniLM-L6-v2` para la generación de embeddings.

### Componentes clave:

1. **Qdrant**:
   - Colección `candidates` con vectores de 384 dimensiones
   - Soporte para filtros combinados.
   - Persistencia en volúmenes Docker

2. **Sentence Transformers**:
   - Modelo `all-MiniLM-L6-v2` (optimizado para CPU)
   - Embeddings de 384 dimensiones
   - Balance entre calidad y rendimiento

3. **Configuración dinámica**:
   - Variables de entorno para modelo, dimensión y métrica de distancia
   - Permite cambiar de modelo sin modificar código
   - Facilita experimentación con diferentes modelos

## Consecuencias

**Positivas**

- **Búsqueda semántica efectiva**: Los usuarios pueden buscar con lenguaje natural ("desarrollador Python con 5 años de experiencia")
- **Performance optimizado**: Qdrant está diseñado específicamente para búsqueda vectorial
- **Bajo consumo de recursos**: El modelo all-MiniLM-L6-v2 funciona eficientemente en CPU
- **Flexibilidad**: Configuración dinámica permite cambiar modelos según necesidades
- **Filtros combinados**: Se puede buscar semánticamente y filtrar por skills específicas
- **Búsqueda de similares**: Endpoint para encontrar candidatos similares a uno dado

**Negativas**

- **Tiempo de procesamiento**: La generación de embeddings añade latencia al pipeline ETL


