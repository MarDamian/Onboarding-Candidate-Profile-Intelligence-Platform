# Onboarding Técnico

Este documento describe los pasos necesarios para configurar el entorno de desarrollo local y comenzar a trabajar en el proyecto **Candidate Profile Intelligence Platform**.

El onboarding está orientado a desarrolladores y se centra en levantar la infraestructura base del sistema.

## Requisitos

Asegúrate de tener instalado:

- Docker
- Docker Compose
- Git

## Setup del entorno

### 1. Clonar el repositorio

```bash
git clone https://github.com/wTreeData/Onboarding-Candidate-Profile-Intelligence-Platform.git

cd Onboarding-Candidate-Profile-Intelligence-Platform
```

### 2. Configurar las variables de entorno:
El proyecto actual utiliza variables de entorno para la configuración de servicios.
```bash
cp .env.example .env
```
Deberás modificar el archivo .env si es necesario, según el entorno local.

### 3. Levantar servicios con Docker
Para iniciar los servicios base del proyecto, tiene que ejecutar:
```bash
cd ./infra/

docker compose up
```
Esto levantará los siguientes servicios:
- PostgreSQL
- Redis
- Qdrant
- FastAPI

### 4. Verificar
Una vez levantados los contenedores, verifica que los servicios estén corriendo:
- PostgreSQL disponible en localhost:5433
- Redis disponible en localhost:6379
- Qdrant accesible en http://localhost:6333
- FastAPI accesible en http://localhost:8000
Si ves que todos los contenedores están en estado running, el entorno está correctamente configurado.
