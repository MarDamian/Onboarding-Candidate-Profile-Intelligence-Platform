# ADR 001: Descentralización del Manejo de Errores y Estados de Carga

*   **Estado:** Aceptado
*   **Fecha:** 2026-01-30
*   **Autor:** Oscar Osorio, Damian Martinez

## Contexto
Originalmente, los estados de carga (`loading`) y la captura de errores (`try/catch`) se gestionaban dentro de la capa de servicios (`ApiCandidate.tsx`). Esto provocaba:
1.  Falta de precisión visual: El componente no sabía exactamente cuándo terminaba la operación de red si el servicio manejaba el `finally`.
2.  Feedback genérico: Todos los errores se manejaban de la misma forma, dificultando mostrar alertas personalizadas según el contexto de la página (ej: "Error al borrar" vs "Error al listar").
3.  Servicios pesados: Los servicios contenían lógica de UI que no les correspondía.

## Decisión
Hemos decidido mover todos los bloques `try/catch/finally` desde la capa de servicios directamente a los componentes de React (Pages). 

Los servicios ahora son funciones asíncronas puras que:
1.  Retornan el resultado de la promesa de Axios.
2.  Permiten que los errores se propaguen hacia arriba.

Los componentes ahora:
1.  Envuelven las llamadas en `try/catch`.
2.  Utilizan el bloque `finally` para asegurar que `setLoading(false)` se ejecute siempre, garantizando la consistencia de la UI.

## Consecuencias
### Positivas
*   **Consistencia de UI**: Los estados de carga se limpian siempre, evitando que los botones se queden bloqueados.
*   **Detección de Errores Granular**: Cada página puede decidir cómo notificar al usuario (alertas, redirecciones o mensajes en pantalla).
*   **Código más Limpio**: La capa de servicios es ahora una interfaz de comunicación pura.

### Negativas
*   **Repetición de Código**: Hay un poco más de estructura de `try/catch` en los componentes, pero se compensa con la claridad del flujo de datos.
