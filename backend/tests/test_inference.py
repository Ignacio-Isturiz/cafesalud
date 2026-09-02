from app.expert_system.engine.inference import InferenceEngine


def test_accumulates_score_and_ranks_primary_hypothesis() -> None:
    result = InferenceEngine().evaluate({
        "affected_part": "leaf",
        "leaf_lesions": True,
        "yellow_spots": True,
        "orange_powder_underside": True,
        "humid_conditions": True,
    })
    assert result["primary_hypothesis"]["disease"] == "coffee_rust"
    assert result["primary_hypothesis"]["score"] == 100


def test_returns_no_hypothesis_below_threshold() -> None:
    result = InferenceEngine().evaluate({"affected_part": "fruit", "fruit_lesions": False})
    assert result["primary_hypothesis"] is None
    assert result["alternative_hypotheses"] == []


def test_explains_matched_evidence() -> None:
    result = InferenceEngine().evaluate({
        "affected_part": "leaf",
        "leaf_lesions": True,
        "circular_brown_lesions": True,
        "light_center": True,
        "yellow_halo": True,
    })
    assert result["primary_hypothesis"]["disease"] == "iron_spot"
    assert any("lesiones circulares pardas" in text for text in result["explanation"])
    assert any(item["symptom"] == "light_center" for item in result["matched_evidence"])


def test_normalizes_questionnaire_answers_before_evaluation() -> None:
    result = InferenceEngine().evaluate({
        "affected_part": "leaf",
        "leaf_lesions": True,
        "lesion_color": ["yellow", "orange"],
        "orange_powder_underside": True,
        "humid_conditions": False,
        "recent_rains": True,
    })

    assert result["primary_hypothesis"]["disease"] == "coffee_rust"
    assert result["primary_hypothesis"]["score"] == 100


def test_no_match_returns_preliminary_guidance() -> None:
    result = InferenceEngine().evaluate({
        "affected_part": "stem",
        "stem_lesions": True,
        "stem_necrosis": True,
    })

    assert result["primary_hypothesis"] is None
    assert result["alternative_hypotheses"] == []
    assert result["explanation"] == []
    assert result["recommendations"]
    assert "preliminar" in result["disclaimer"]
