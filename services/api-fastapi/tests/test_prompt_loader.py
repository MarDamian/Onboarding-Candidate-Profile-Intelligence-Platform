"""
Tests unitarios para PromptLoader.

¿Por qué testear el cargador de prompts?
- Los prompts son la "programación" del LLM — un prompt roto = insights rotos
- Verificamos que el sistema de versionamiento (v1, v2) funciona
- Garantizamos que prompts inexistentes lanzan errores claros
- El cache (lru_cache) debe funcionar correctamente para evitar I/O repetido
"""

import pytest
import sys, os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from app.llm.prompt_loader import PromptLoader


class TestPromptLoader:
    """Tests para carga de prompts versionados desde filesystem."""

    def test_load_existing_prompt(self):
        """Debe cargar prompt existente (candidate_summary/v1)."""
        prompt = PromptLoader.get_prompt("candidate_summary", "v1")
        assert isinstance(prompt, str)
        assert len(prompt) > 0

    def test_load_v2_prompt(self):
        """Debe cargar versión 2 del prompt."""
        prompt = PromptLoader.get_prompt("candidate_summary", "v2")
        assert isinstance(prompt, str)
        assert len(prompt) > 0

    def test_load_skill_extraction_prompt(self):
        """Debe cargar prompt de extracción de skills."""
        prompt = PromptLoader.get_prompt("skill_extraction", "v1")
        assert isinstance(prompt, str)
        assert len(prompt) > 0

    def test_nonexistent_prompt_raises(self):
        """Debe lanzar FileNotFoundError para prompt inexistente."""
        # Limpiar cache para forzar lectura
        PromptLoader.get_prompt.cache_clear()
        with pytest.raises(FileNotFoundError):
            PromptLoader.get_prompt("nonexistent_category", "v99")

    def test_prompts_are_cached(self):
        """Llamadas repetidas deben usar cache (lru_cache)."""
        PromptLoader.get_prompt.cache_clear()
        
        prompt1 = PromptLoader.get_prompt("candidate_summary", "v1")
        prompt2 = PromptLoader.get_prompt("candidate_summary", "v1")
        
        assert prompt1 == prompt2
        # Verificar que el cache tiene al menos 1 hit
        cache_info = PromptLoader.get_prompt.cache_info()
        assert cache_info.hits >= 1
