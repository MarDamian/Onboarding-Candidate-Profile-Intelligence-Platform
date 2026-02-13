"""
Tests de integración para los endpoints CRUD de candidatos.

¿Por qué tests de integración para endpoints?
- Validan el flujo completo: HTTP request → router → DB → response
- Detectan errores de serialización entre Pydantic schemas y SQLAlchemy models
- Verifican status codes, headers y estructura de respuesta
- Son más confiables que tests unitarios aislados para APIs REST

Cobertura:
- GET /v1/candidate/ → lista vacía y con datos
- GET /v1/candidate/{id} → encontrado y 404
- POST /v1/candidate/ → creación exitosa y validación
- PUT /v1/candidate/{id} → actualización parcial y 404
- DELETE /v1/candidate/{id} → eliminación exitosa y 404
"""


class TestListCandidates:
    """Tests para GET /v1/candidate/"""

    def test_list_empty(self, client):
        """Debe retornar lista vacía cuando no hay candidatos."""
        response = client.get("/v1/candidate/")
        assert response.status_code == 200
        assert response.json() == []

    def test_list_with_candidates(self, client, sample_candidate):
        """Debe retornar todos los candidatos creados."""
        client.post("/v1/candidate/", json=sample_candidate)
        response = client.get("/v1/candidate/")
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 1
        assert data[0]["name"] == sample_candidate["name"]
        assert data[0]["email"] == sample_candidate["email"]

    def test_list_multiple_candidates(self, client, sample_candidate):
        """Debe retornar múltiples candidatos."""
        client.post("/v1/candidate/", json=sample_candidate)
        
        second = sample_candidate.copy()
        second["email"] = "otro@example.com"
        second["phone"] = "+5491199998888"
        client.post("/v1/candidate/", json=second)
        
        response = client.get("/v1/candidate/")
        assert response.status_code == 200
        assert len(response.json()) == 2


class TestGetCandidate:
    """Tests para GET /v1/candidate/{id}"""

    def test_get_existing(self, client, sample_candidate):
        """Debe retornar candidato por ID."""
        create_resp = client.post("/v1/candidate/", json=sample_candidate)
        candidate_id = create_resp.json()["id"] if "id" in create_resp.json() else 1
        
        response = client.get(f"/v1/candidate/{candidate_id}")
        assert response.status_code == 200
        assert response.json()["name"] == sample_candidate["name"]

    def test_get_not_found(self, client):
        """Debe retornar 404 para ID inexistente."""
        response = client.get("/v1/candidate/9999")
        assert response.status_code == 404
        assert "not found" in response.json()["detail"].lower()


class TestCreateCandidate:
    """Tests para POST /v1/candidate/"""

    def test_create_success(self, client, sample_candidate):
        """Debe crear candidato y retornar 201."""
        response = client.post("/v1/candidate/", json=sample_candidate)
        assert response.status_code == 201
        data = response.json()
        assert data["name"] == sample_candidate["name"]
        assert data["email"] == sample_candidate["email"]
        assert data["phone"] == sample_candidate["phone"]

    def test_create_missing_required_fields(self, client):
        """Debe retornar 422 cuando faltan campos obligatorios."""
        response = client.post("/v1/candidate/", json={"name": "Solo nombre"})
        assert response.status_code == 422

    def test_create_invalid_email(self, client, sample_candidate):
        """Debe retornar 422 para email inválido."""
        sample_candidate["email"] = "no-es-un-email"
        response = client.post("/v1/candidate/", json=sample_candidate)
        assert response.status_code == 422

    def test_create_minimal_fields(self, client):
        """Debe crear candidato con campos requeridos y opcionales como string vacío.
        
        Nota: El modelo SQLAlchemy define todos los campos como Mapped[str] (NOT NULL),
        por lo que Pydantic los acepta como Optional pero la DB requiere al menos string vacío.
        """
        minimal = {
            "name": "Test User",
            "email": "test@example.com",
            "phone": "+5491100001111",
            "location": "",
            "headline": "",
            "summary": "",
            "role": "",
            "experience": "",
            "skills": "",
            "education": ""
        }
        response = client.post("/v1/candidate/", json=minimal)
        assert response.status_code == 201


class TestUpdateCandidate:
    """Tests para PUT /v1/candidate/{id}"""

    def test_update_partial(self, client, sample_candidate, sample_candidate_update):
        """Debe actualizar solo los campos enviados."""
        create_resp = client.post("/v1/candidate/", json=sample_candidate)
        candidate_id = create_resp.json().get("id", 1)
        
        response = client.put(f"/v1/candidate/{candidate_id}", json=sample_candidate_update)
        assert response.status_code == 200
        data = response.json()
        assert data["name"] == sample_candidate_update["name"]
        assert data["role"] == sample_candidate_update["role"]

    def test_update_not_found(self, client, sample_candidate_update):
        """Debe retornar 404 para candidato inexistente."""
        response = client.put("/v1/candidate/9999", json=sample_candidate_update)
        assert response.status_code == 404


class TestDeleteCandidate:
    """Tests para DELETE /v1/candidate/{id}"""

    def test_delete_success(self, client, sample_candidate):
        """Debe eliminar candidato y retornar sus datos."""
        client.post("/v1/candidate/", json=sample_candidate)
        
        response = client.delete("/v1/candidate/1")
        assert response.status_code == 200
        assert response.json()["name"] == sample_candidate["name"]

        # Verificar que ya no existe
        get_response = client.get("/v1/candidate/1")
        assert get_response.status_code == 404

    def test_delete_not_found(self, client):
        """Debe retornar 404 para candidato inexistente."""
        response = client.delete("/v1/candidate/9999")
        assert response.status_code == 404


class TestRootEndpoint:
    """Tests para GET /"""

    def test_root(self, client):
        """Debe retornar respuesta de salud."""
        response = client.get("/")
        assert response.status_code == 200
        assert response.json() == {"Hello": "World"}
