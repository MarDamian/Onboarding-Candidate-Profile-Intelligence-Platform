from pathlib import Path
from functools import lru_cache

class PromptLoader:
    """Carga prompts desde el sistema de archivos para permitir versionamiento.
    """
    PROMPTS_BASE_PATH = Path(__file__).resolve().parents[2] / "prompts"
    
    @classmethod
    @lru_cache(maxsize=10)
    def get_prompt(cls, category: str, version: str) -> str:
        
        file_path = cls.PROMPTS_BASE_PATH / category / f"{version}.txt"
        if not file_path.exists():
            raise FileNotFoundError(f"Prompt no encontrado: {file_path}")
        return file_path.read_text(encoding="utf-8")