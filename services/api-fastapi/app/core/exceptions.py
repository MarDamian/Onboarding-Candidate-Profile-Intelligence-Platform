from fastapi import Request, status
from fastapi.responses import JSONResponse
from sqlalchemy.exc import IntegrityError
import logging

logger = logging.getLogger(__name__)


class DuplicateResourceError(Exception):
    """Excepción para recursos duplicados (email, phone, etc.)."""
    def __init__(self, field: str, value: str):
        self.field = field
        self.value = value
        self.message = f"El {field} '{value}' ya está registrado"
        super().__init__(self.message)


class ResourceNotFoundError(Exception):
    """Excepción para recursos no encontrados."""
    def __init__(self, resource: str, identifier: str):
        self.resource = resource
        self.identifier = identifier
        self.message = f"{resource} con ID {identifier} no encontrado"
        super().__init__(self.message)


async def integrity_error_handler(request: Request, exc: IntegrityError) -> JSONResponse:
    """
    Manejador global para errores de integridad de base de datos.
    
    Captura violaciones de constraints de unicidad (UNIQUE) y otros errores
    de integridad, retornando respuestas HTTP apropiadas.
    
    Args:
        request: Request de FastAPI
        exc: Excepción de IntegrityError de SQLAlchemy
        
    Returns:
        JSONResponse con status 409 y mensaje descriptivo
    """
    error_msg = str(exc.orig).lower()
    
    # Detectar violación de constraint de unicidad
    if "unique constraint" in error_msg or "duplicate" in error_msg:
        # Intentar extraer el campo duplicado
        if "email" in error_msg:
            detail = "El email ya está registrado en el sistema"
        elif "phone" in error_msg:
            detail = "El teléfono ya está registrado en el sistema"
        else:
            detail = "Ya existe un registro con estos datos"
        
        logger.warning(
            f"Integrity error - Duplicate entry",
            extra={
                "path": request.url.path,
                "method": request.method,
                "error": str(exc.orig)
            }
        )
        
        return JSONResponse(
            status_code=status.HTTP_409_CONFLICT,
            content={"detail": detail}
        )
    
    # Otros errores de integridad
    logger.error(
        f"Database integrity error",
        extra={
            "path": request.url.path,
            "method": request.method,
            "error": str(exc.orig)
        }
    )
    
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={"detail": "Error de validación en la base de datos"}
    )


async def duplicate_resource_error_handler(
    request: Request, 
    exc: DuplicateResourceError
) -> JSONResponse:
    """
    Manejador para errores de recursos duplicados.
    
    Args:
        request: Request de FastAPI
        exc: Excepción DuplicateResourceError
        
    Returns:
        JSONResponse con status 409 y mensaje descriptivo
    """
    logger.warning(
        f"Duplicate resource: {exc.field}",
        extra={
            "path": request.url.path,
            "method": request.method,
            "field": exc.field,
            "value": exc.value
        }
    )
    
    return JSONResponse(
        status_code=status.HTTP_409_CONFLICT,
        content={"detail": exc.message}
    )


async def resource_not_found_error_handler(
    request: Request,
    exc: ResourceNotFoundError
) -> JSONResponse:
    """
    Manejador para errores de recursos no encontrados.
    
    Args:
        request: Request de FastAPI
        exc: Excepción ResourceNotFoundError
        
    Returns:
        JSONResponse con status 404 y mensaje descriptivo
    """
    logger.info(
        f"Resource not found: {exc.resource}",
        extra={
            "path": request.url.path,
            "method": request.method,
            "resource": exc.resource,
            "identifier": exc.identifier
        }
    )
    
    return JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND,
        content={"detail": exc.message}
    )
