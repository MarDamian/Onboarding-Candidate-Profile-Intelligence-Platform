# ADR 009 - LLM Fallback y Estrategia de Redundancia

**Estado**: Aprobado  
**Fecha**: 2026-02-12  
**Autores**: Oscar Osorio, Damian Martinez

## Contexto

El servicio de generación de insights depende críticamente de APIs externas (Cohere). Fallos en la red, latencia excesiva, límites de tokens o caídas del servicio del proveedor pueden interrumpir la experiencia del usuario y el flujo de los pipelines de datos.

### Requisitos Identificados

1.  **Resiliencia**: El sistema debe ser capaz de recuperarse automáticamente ante fallos del proveedor principal.
2.  **Baja Latencia**: En caso de fallo, la transición al modelo de respaldo debe ser rápida.
3.  **Costeo y Cuotas**: El fallback debe ser económicamente viable y no exceder límites de tokens secundarios.
4.  **Consistencia**: La respuesta del modelo de respaldo debe mantener el mismo esquema de datos definido en `InsightSchema`.

## Decisión

Se decidió implementar un mecanismo de **Fallback en Cascada** utilizando LangChain y el ecosistema de integraciones de `langchain-cohere` y `langchain-groq`.

### Detalles de la Implementación

1.  **Proveedor Principal (Cohere)**:
    - Se mantiene a Cohere (`command-a-03-2025`) como el modelo base debido a su capacidad de razonamiento y manejo de herramientas (tool calling).
    - Se configuró con reintentos exponenciales mediante `@external_api_retry`.

2.  **Proveedor de Fallback (Groq)**:
    - Se seleccionó Groq (`llama-3.3-70b-versatile`) como respaldo debido a su extrema velocidad y compatibilidad con el esquema de herramientas de LangChain.
    - Acceso mediante la librería `langchain-groq`.

3.  **Encadenamiento con `.with_fallbacks()`**:
    - En lugar de manejar excepciones manuales pesadas, se utilizó el método nativo de LangChain para encadenar los objetos `ChatCohere` y `ChatGroq`.
    - Esto permite que cualquier error de ejecución (timeout, 429, 500) en el principal dispare automáticamente la llamada al secundario.

4.  **Guardrails Reforzados**:
    - Se integró `request_timeout` en ambos modelos para asegurar que el fallback ocurra antes de que el timeout global mate la petición.
    - Se actualizó el esquema `score` en `InsightSchema` para aceptar tipos `Union[float, int]`, permitiendo flexibilidad entre diferentes modelos que retornan puntajes en escalas distintas (0-1 vs 0-100).

## Consecuencias

### Ventajas 

- **Alta Disponibilidad**: El servicio de insights es ahora mucho más robusto frente a interrupciones externas.
- **Flexibilidad de Proveedores**: La arquitectura permite añadir más modelos a la cascada (ej. Anthropic u OpenAI) con cambios mínimos.
- **Separación de Responsabilidades**: El `Agent` se encarga de la lógica de redundancia, mientras que el pipeline solo consume el resultado final.

### Desventajas

- **Complejidad de Configuración**: Requiere gestionar múltiples API Keys y configuraciones en el entorno (`.env`).
- **Variabilidad en Resultados**: Aunque el esquema es el mismo, la calidad o tono del resumen puede variar ligeramente entre Cohere y Groq.

## Verificación

1.  **Simulación de Error**: Cambiar la `COHERE_API_KEY` por una inválida y verificar que el sistema entrega insights utilizando la llave de Groq.
2.  **Manejo de Timeouts**: Configurar un `LLM_TIMEOUT` muy bajo (ej. 1s) para forzar el salto al fallback.
3.  **Validación de Esquema**: Asegurar que las respuestas de ambos proveedores sean parseadas correctamente por Pydantic y guardadas en el caché de Redis.
