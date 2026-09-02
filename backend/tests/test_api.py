from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_diseases_and_diagnosis_endpoints() -> None:
    diseases = client.get("/api/v1/diseases")
    assert diseases.status_code == 200
    assert len(diseases.json()) == 3

    diagnosis = client.post(
        "/api/v1/diagnosis/evaluate",
        json={"answers": {"affected_part": "hoja", "leaf_lesions": "sí", "yellow_spots": True, "orange_powder_underside": True}},
    )
    assert diagnosis.status_code == 200
    assert diagnosis.json()["primary_hypothesis"]["disease"] == "coffee_rust"


def test_questions_are_filtered_and_structured_by_affected_part() -> None:
    response = client.get("/api/v1/diagnosis/questions", params={"affected_part": "leaf"})

    assert response.status_code == 200
    questions = response.json()
    assert len(questions) == 15
    assert [question["order"] for question in questions] == list(range(1, 16))
    assert all(question["affected_part"] == "leaf" for question in questions)
    assert set(questions[0]) == {
        "id",
        "key",
        "label",
        "description",
        "type",
        "options",
        "required",
        "order",
        "affected_part",
        "conditional_logic",
        "image",
    }


def test_question_catalog_exposes_conditional_logic() -> None:
    response = client.get("/api/v1/diagnosis/questions", params={"affected_part": "fruit"})

    assert response.status_code == 200
    questions = {question["key"]: question for question in response.json()}
    assert len(questions) == 8
    assert questions["fruit_lesion_color"]["conditional_logic"] == {
        "question_key": "fruit_lesions",
        "operator": "equals",
        "value": True,
    }
    assert questions["premature_fruit_drop"]["conditional_logic"] is None


def test_stem_alias_is_supported() -> None:
    response = client.get("/api/v1/diagnosis/questions", params={"affected_part": "stem_branch"})

    assert response.status_code == 200
    assert len(response.json()) == 6
    assert all(question["affected_part"] == "stem" for question in response.json())


def test_invalid_affected_part_is_rejected() -> None:
    response = client.get("/api/v1/diagnosis/questions", params={"affected_part": "root"})

    assert response.status_code == 422
