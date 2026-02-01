# ADR 002: Gestión de Versicionamiento de Base de Datos y Datos Semilla

*   **Estado:** Aceptado
*   **Fecha:** 2026-02-01
*   **Autor:** Oscar Osorio, Damian Martinez

## Contexto
Se requería la inserción de datos de prueba (seeds). Inicialmente se consideró el uso de `init.sql`, pero esto generaba duplicidad de la lógica del esquema (Python vs SQL).

## Decisión
Hemos decidido implementar un **Script de Python** para la inserción de datos semilla.

1.  **init.sql**: Reservado exclusivamente para extensiones de PostgreSQL (como `uuid-ossp`) y tablas de infraestructura.
2.  **Seed Script**: Script en Python que utiliza los modelos de SQLAlchemy para garantizar que los datos de prueba cumplan con las restricciones de integridad.

## Consecuencias
*   **Positivas**: Facilidad para añadir cambios sin pérdida de datos, y entorno de desarrollo listo en segundos.
*   **Negativas**: Requiere un paso adicional (``docker compose exec api-fastapi python scripts/seed_db.py) durante el setup inicial.