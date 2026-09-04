from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_diseases_and_diagnosis_endpoints() -> None:
    diseases = client.get("/api/v1/diseases")
    assert diseases.status_code == 200
    assert len(diseases.json()) == 10

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
    assert len(questions) == 18
    assert [question["order"] for question in questions] == list(range(1, 19))
    assert all(question["affected_part"] == "leaf" for question in questions)
    assert questions[0]["image"] == "/images/questions/leaf-lesions.webp"
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
    assert len(questions) == 12
    assert questions["fruit_lesion_color"]["conditional_logic"] == {
        "question_key": "fruit_lesions",
        "operator": "equals",
        "value": True,
    }
    assert questions["fruit_abnormal_change"]["conditional_logic"] == {
        "question_key": "fruit_lesions",
        "operator": "equals",
        "value": False,
    }


def test_fruit_catalog_follows_the_decision_tree() -> None:
    response = client.get("/api/v1/diagnosis/questions", params={"affected_part": "fruit"})

    assert response.status_code == 200
    questions = {question["key"]: question for question in response.json()}
    assert {
        condition["question_key"]
        for condition in questions["fruit_necrosis_or_rot"]["conditional_logic"]["any"]
    } == {"fruit_lesions", "fruit_abnormal_change"}
    assert questions["fruit_insect_damage"]["conditional_logic"] == {
        "question_key": "fruit_necrosis_or_rot",
        "operator": "equals",
        "value": False,
    }
    assert {
        (condition["question_key"], condition["value"])
        for condition in questions["fruit_development_stage"]["conditional_logic"]["any"]
    } == {
        ("fruit_necrosis_or_rot", True),
        ("fruit_insect_damage", True),
        ("fruit_insect_damage", False),
    }


def test_leaf_catalog_follows_the_decision_tree() -> None:
    response = client.get("/api/v1/diagnosis/questions", params={"affected_part": "leaf"})

    assert response.status_code == 200
    questions = {question["key"]: question for question in response.json()}
    assert questions["foliar_decline"]["conditional_logic"] == {
        "question_key": "leaf_lesions",
        "operator": "equals",
        "value": False,
    }
    assert questions["orange_powder_underside"]["conditional_logic"]["question_key"] == "iron_spot_compatible"
    assert questions["eye_spot_compatible"]["conditional_logic"]["question_key"] == "orange_powder_underside"
    assert {
        condition["question_key"]
        for condition in questions["humid_conditions"]["conditional_logic"]["any"]
    } == {"iron_spot_compatible", "orange_powder_underside", "eye_spot_compatible"}


def test_stem_alias_is_supported() -> None:
    response = client.get("/api/v1/diagnosis/questions", params={"affected_part": "stem_branch"})

    assert response.status_code == 200
    questions = response.json()
    assert len(questions) == 12
    assert [question["order"] for question in questions] == list(range(1, 13))
    assert all(question["affected_part"] == "stem" for question in questions)


def test_stem_catalog_follows_the_decision_tree() -> None:
    response = client.get("/api/v1/diagnosis/questions", params={"affected_part": "stem"})

    assert response.status_code == 200
    questions = {question["key"]: question for question in response.json()}
    assert questions["stem_progressive_drying"]["conditional_logic"] == {
        "question_key": "stem_lesions",
        "operator": "equals",
        "value": False,
    }
    assert {
        condition["question_key"]
        for condition in questions["stem_necrosis"]["conditional_logic"]["any"]
    } == {"stem_lesions", "stem_progressive_drying"}
    assert questions["stem_fungal_structures"]["conditional_logic"]["question_key"] == "stem_necrosis"
    assert questions["stem_insect_damage"]["conditional_logic"]["question_key"] == "stem_fungal_structures"
    assert {
        (condition["question_key"], condition["value"])
        for condition in questions["stem_humid_conditions"]["conditional_logic"]["any"]
    } == {
        ("stem_necrosis", True),
        ("stem_fungal_structures", True),
        ("stem_insect_damage", True),
        ("stem_insect_damage", False),
    }


def test_invalid_affected_part_is_rejected() -> None:
    response = client.get("/api/v1/diagnosis/questions", params={"affected_part": "root"})

    assert response.status_code == 422
