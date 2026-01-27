# Onboarding-Candidate-Profile-Intelligence-Platforme

##Features
- CRUD completo de perfiles (crear, editar, eliminar y listar)
- Ingesta masiva de perfiles mediante ETL
- Indexación semántica en Qdrant
- Búsqueda avanzada desde la interfaz de usuario
- Generación de insights mediante LLM (resúmenes, extracción de información y scoring)
- Microfrontend especializado en Svelte para vistas específicas

##Stack Tecnológico:
- FastAPI - CRUD completo de perfiles - Búsqueda semántica - Generación de insights con LLM
- Flask - Administración del sistema: ejecución de ETL, reindexación en Qdrant y visualización de ejecuciones
- Rust Worker - Procesamiento de jobs pesados (ETL batch y generación de embeddings)
- PostgreSQL - Almacenamiento de datos principales
- Redis - Cache - Gestión de jobs y colas
- Qdrant - Motor de búsqueda vectorial
- React App - Interfaz principal (CRUD y búsqueda)
- Svelte Microfrontend - Vista especializada embebida

##Estructura del proyecto:
    docs/
    ├─adr/
        ├─onboarding.md
        ├─architecture.md
        ├─api.md
        ├─runbook.md

    services/
    ├─api-fastapi/
    ├─api-flask/
    ├─worker-rust/

    ui/
    ├─react-app/
    ├─/svelte-mf

    pipelines/
    ├─/etl

    infra/
    ├─docker-compose.yml
    ├─Dockerfile.*
    ├─/db