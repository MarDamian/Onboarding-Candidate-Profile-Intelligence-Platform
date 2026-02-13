"""
Tests unitarios para ContextCompressor (LLM prompt compression).

¿Por qué testear la compresión?
- El compresor afecta directamente la calidad y costo de las respuestas del LLM
- Un bug en compresión puede enviar datos truncados/corruptos al modelo
- Validar que el truncado respeta el límite de 1500 caracteres
- Verificar que la deduplicación de skills funciona correctamente
- El compresor es lógica pura sin dependencias externas → ideal para unit testing
"""

import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from app.llm.compression import ContextCompressor


class TestCompress:
    """Tests para el método compress() de limpieza de texto."""

    def test_removes_multiple_spaces(self):
        """Debe colapsar múltiples espacios en uno."""
        result = ContextCompressor.compress("hello    world")
        assert "    " not in result
        assert "hello world" in result

    def test_removes_newlines(self):
        """Debe reemplazar saltos de línea por espacio."""
        result = ContextCompressor.compress("hello\n\nworld")
        assert "\n" not in result

    def test_removes_special_characters(self):
        """Debe eliminar caracteres especiales no alfanuméricos."""
        result = ContextCompressor.compress("hello @#$ world!")
        assert "@" not in result
        assert "#" not in result
        assert "$" not in result

    def test_truncates_long_text(self):
        """Debe truncar texto a 1500 caracteres máximo."""
        long_text = "a" * 3000
        result = ContextCompressor.compress(long_text)
        assert len(result) == 1500

    def test_preserves_short_text(self):
        """No debe truncar texto corto."""
        short_text = "hello world"
        result = ContextCompressor.compress(short_text)
        assert result == "hello world"

    def test_empty_string(self):
        """Debe manejar string vacío."""
        result = ContextCompressor.compress("")
        assert result == ""


class TestCompressCandidate:
    """Tests para compress_candidate()."""

    def test_basic_compression(self):
        """Debe extraer profile, skills y experience."""
        candidate = {
            "summary": "Desarrollador Python",
            "skills": ["Python", "FastAPI", "Docker"],
            "experience": []
        }
        result = ContextCompressor.compress_candidate(candidate)
        assert "profile" in result
        assert "skills" in result
        assert "experience" in result
        assert result["profile"] == "Desarrollador Python"

    def test_skills_deduplication(self):
        """Debe eliminar skills duplicadas."""
        candidate = {
            "summary": "Dev",
            "skills": ["Python", "Python", "Docker", "Docker"],
            "experience": []
        }
        result = ContextCompressor.compress_candidate(candidate)
        assert len(result["skills"]) == 2

    def test_skills_limit_to_12(self):
        """Debe limitar skills a máximo 12."""
        candidate = {
            "summary": "Dev",
            "skills": [f"skill_{i}" for i in range(20)],
            "experience": []
        }
        result = ContextCompressor.compress_candidate(candidate)
        assert len(result["skills"]) <= 12

    def test_experience_limit_to_4(self):
        """Debe limitar experiencia a máximo 4 entradas."""
        candidate = {
            "summary": "Dev",
            "skills": [],
            "experience": [
                {"role": f"Role {i}", "years": i, "achievements": ["a", "b"]}
                for i in range(10)
            ]
        }
        result = ContextCompressor.compress_candidate(candidate)
        assert len(result["experience"]) <= 4

    def test_experience_highlights_limited(self):
        """Debe limitar highlights a 3 por experiencia."""
        candidate = {
            "summary": "Dev",
            "skills": [],
            "experience": [
                {"role": "Dev", "years": 5, "achievements": ["a", "b", "c", "d", "e"]}
            ]
        }
        result = ContextCompressor.compress_candidate(candidate)
        assert len(result["experience"][0]["highlights"]) <= 3


class TestToPromptContext:
    """Tests para to_prompt_context() (formato de salida para LLM)."""

    def test_generates_string_output(self):
        """Debe generar string para inyectar en prompt."""
        candidate = {
            "summary": "Desarrollador Python senior",
            "skills": ["Python", "FastAPI"],
            "experience": []
        }
        result = ContextCompressor.to_prompt_context(candidate)
        assert isinstance(result, str)
        assert "Perfil:" in result
        assert "Habilidades clave:" in result

    def test_includes_experience_when_present(self):
        """Debe incluir experiencia cuando hay datos."""
        candidate = {
            "summary": "Dev",
            "skills": ["Python"],
            "experience": [
                {"role": "Backend Dev", "years": 3, "achievements": ["API REST"]}
            ]
        }
        result = ContextCompressor.to_prompt_context(candidate)
        assert "Experiencia relevante:" in result
        assert "Backend Dev" in result


class TestPreprocessContext:
    """Tests para preprocess_context()."""

    def test_deduplicates_skills_list(self):
        """Debe eliminar skills duplicadas en contexto."""
        context = {"skills": ["Python", "Python", "React", "React"]}
        result = ContextCompressor.preprocess_context(context)
        assert len(result["skills"]) == 2

    def test_truncates_long_summary(self):
        """Debe truncar summary a 1000 caracteres."""
        context = {"summary": "x" * 2000}
        result = ContextCompressor.preprocess_context(context)
        assert len(result["summary"]) == 1003  # 1000 + "..."

    def test_preserves_short_summary(self):
        """No debe truncar summary corto."""
        context = {"summary": "Breve resumen"}
        result = ContextCompressor.preprocess_context(context)
        assert result["summary"] == "Breve resumen"
