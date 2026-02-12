# ADR 008 - Logs Estructurados

**Estado**: Aprobado  
**Fecha**: 2026-02-11  
**Autores**: Oscar Osorio, Damian Martinez

## Contexto

A medida que el ecosistema de microservicios de la plataforma crece (FastAPI, Flask, Rust Worker), la necesidad de una observabilidad robusta se vuelve crítica. Los logs en formato de texto plano son difíciles de analizar a escala y complican la integración con herramientas de monitoreo modernas.

### Requisitos Identificados

1.  **Observabilidad**: Facilitar el rastreo de errores y el monitoreo de flujos de datos.
2.  **Estandarización**: Todos los servicios (Python y Rust) deben emitir logs en un formato consistente.
3.  **Integración**: Los logs deben ser fácilmente procesables por sistemas como ELK (Elasticsearch, Logstash, Kibana) o Grafana Loki.
4.  **Bajo Impacto**: La implementación no debe comprometer el rendimiento de los servicios.

## Decisión

Se decidió implementar **Logs Estructurados en formato JSON** en todos los servicios del backend.

### Estrategia por Ecosistema

1.  **Python (FastAPI & Flask)**:
    - Se seleccionó la librería `python-json-logger` por su simplicidad y flexibilidad.
    - Se configuró un formateador JSON personalizado que incluye campos estándar como `asctime`, `levelname`, `name` y `message`.
    - En FastAPI, se centralizó la configuración en `app/core/logging_config.py`.
    - En Flask, la inicialización se integró en la función de fábrica de la aplicación (`create_app`).

2.  **Rust (Worker)**:
    - Se aprovechó el ecosistema de `tracing` ya existente.
    - Se habilitó la feature `json` en `tracing-subscriber`.
    - Se configuró el suscriptor global para emitir eventos en formato JSON hacia la salida estándar.

## Consecuencias

### Ventajas 

- **Análisis Automatizado**: Los logs pueden ser parseados directamente como objetos por herramientas de búsqueda y agregación.
- **Contexto Rico**: Es más sencillo añadir campos adicionales (ID de candidato, tipo de job, etc.) sin romper el formato de línea.
- **Consistencia**: Un formato único facilita la creación de dashboards de monitoreo unificados.

### Desventajas

- **Legibilidad Humana**: En la terminal de desarrollo, el JSON crudo es más difícil de leer que el texto plano (se recomienda el uso de herramientas como `jq`).
- **Dependencias Adicionales**: Se añadieron librerías de terceros en los servicios de Python.

## Verificación

Para verificar que el sistema está emitiendo logs correctos:
1.  **FastAPI/Flask**: Ejecutar el servicio y verificar que la primera línea de log sea un JSON válido (e.g., `"message": "FastAPI structured logging initialized"`).
2.  **Rust**: Observar la salida del worker; cada evento debe ser una línea JSON completa que incluya el nivel y el timestamp.
3.  **Docker**: Ejecutar `docker logs <container_id>` y confirmar que la salida es JSON estructurado.
