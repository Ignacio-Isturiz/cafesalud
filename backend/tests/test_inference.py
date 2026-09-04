from app.expert_system.engine.inference import InferenceEngine


def test_accumulates_score_and_ranks_primary_hypothesis() -> None:
    result = InferenceEngine().evaluate({
        "affected_part": "leaf",
        "leaf_lesions": True,
        "yellow_spots": True,
        "orange_powder_underside": True,
        "humid_conditions": True,
        "recent_rains": True,
        "dense_shade": True,
        "poor_air_circulation": True,
        "nearby_plants_affected": True,
    })
    assert result["primary_hypothesis"]["disease"] == "coffee_rust"
    assert result["primary_hypothesis"]["score"] == 100
    assert result["alternative_hypotheses"] == []


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
    assert result["primary_hypothesis"]["score"] >= 75


def test_cultivation_conditions_adjust_confidence_without_changing_hypothesis() -> None:
    base_answers = {
        "affected_part": "leaf",
        "leaf_lesions": True,
        "iron_spot_compatible": False,
        "orange_powder_underside": True,
    }
    low_support = InferenceEngine().evaluate(base_answers)
    high_support = InferenceEngine().evaluate({
        **base_answers,
        "humid_conditions": True,
        "recent_rains": True,
        "dense_shade": True,
        "poor_air_circulation": True,
        "nearby_plants_affected": True,
    })

    assert low_support["primary_hypothesis"]["disease"] == "coffee_rust"
    assert high_support["primary_hypothesis"]["disease"] == "coffee_rust"
    assert high_support["primary_hypothesis"]["score"] > low_support["primary_hypothesis"]["score"]


def test_leaf_hypotheses_follow_diagram_priority() -> None:
    engine = InferenceEngine()

    iron_spot = engine.evaluate({
        "affected_part": "leaf",
        "leaf_lesions": True,
        "iron_spot_compatible": True,
    })
    rust = engine.evaluate({
        "affected_part": "leaf",
        "leaf_lesions": True,
        "iron_spot_compatible": False,
        "orange_powder_underside": True,
    })
    eye_spot = engine.evaluate({
        "affected_part": "leaf",
        "leaf_lesions": True,
        "iron_spot_compatible": False,
        "orange_powder_underside": False,
        "eye_spot_compatible": True,
    })

    assert iron_spot["primary_hypothesis"]["disease"] == "iron_spot"
    assert rust["primary_hypothesis"]["disease"] == "coffee_rust"
    assert eye_spot["primary_hypothesis"]["disease"] == "american_leaf_spot"
    assert all(not result["alternative_hypotheses"] for result in (iron_spot, rust, eye_spot))


def test_no_match_returns_preliminary_guidance() -> None:
    result = InferenceEngine().evaluate({
        "affected_part": "stem",
        "stem_lesions": False,
        "stem_progressive_drying": False,
    })

    assert result["primary_hypothesis"] is None
    assert result["alternative_hypotheses"] == []
    assert result["explanation"] == []
    assert result["recommendations"]
    assert "preliminar" in result["disclaimer"]


def test_stem_hypotheses_follow_diagram_branches() -> None:
    engine = InferenceEngine()
    common = {"affected_part": "stem", "stem_lesions": True}

    necrosis = engine.evaluate({**common, "stem_necrosis": True})
    fungal = engine.evaluate({
        **common,
        "stem_necrosis": False,
        "stem_fungal_structures": True,
    })
    pest = engine.evaluate({
        **common,
        "stem_necrosis": False,
        "stem_fungal_structures": False,
        "stem_insect_damage": True,
    })
    unspecified = engine.evaluate({
        **common,
        "stem_necrosis": False,
        "stem_fungal_structures": False,
        "stem_insect_damage": False,
    })

    assert necrosis["primary_hypothesis"]["disease"] == "stem_necrotic_disorder"
    assert fungal["primary_hypothesis"]["disease"] == "stem_fungal_disorder"
    assert pest["primary_hypothesis"]["disease"] == "stem_associated_pest"
    assert unspecified["primary_hypothesis"]["disease"] == "stem_unspecified_disorder"
    assert all(not result["alternative_hypotheses"] for result in (necrosis, fungal, pest, unspecified))


def test_stem_conditions_adjust_confidence_without_changing_hypothesis() -> None:
    base_answers = {
        "affected_part": "stem",
        "stem_lesions": False,
        "stem_progressive_drying": True,
        "stem_necrosis": False,
        "stem_fungal_structures": False,
        "stem_insect_damage": True,
    }
    low_support = InferenceEngine().evaluate(base_answers)
    high_support = InferenceEngine().evaluate({
        **base_answers,
        "stem_humid_conditions": True,
        "stem_recent_rains": True,
        "stem_dense_shade": True,
        "stem_poor_air_circulation": True,
        "stem_damage_distribution": "widespread",
    })

    assert low_support["primary_hypothesis"]["disease"] == "stem_associated_pest"
    assert high_support["primary_hypothesis"]["disease"] == "stem_associated_pest"
    assert high_support["primary_hypothesis"]["score"] > low_support["primary_hypothesis"]["score"]
    assert high_support["primary_hypothesis"]["score"] == 100


def test_fruit_hypotheses_follow_diagram_branches() -> None:
    engine = InferenceEngine()
    common = {"affected_part": "fruit", "fruit_lesions": True}

    disease = engine.evaluate({**common, "fruit_necrosis_or_rot": True})
    pest = engine.evaluate({
        **common,
        "fruit_necrosis_or_rot": False,
        "fruit_insect_damage": True,
    })
    unspecified = engine.evaluate({
        **common,
        "fruit_necrosis_or_rot": False,
        "fruit_insect_damage": False,
    })

    assert disease["primary_hypothesis"]["disease"] == "fruit_associated_disease"
    assert pest["primary_hypothesis"]["disease"] == "fruit_associated_pest"
    assert unspecified["primary_hypothesis"]["disease"] == "fruit_unspecified_disorder"
    assert all(not result["alternative_hypotheses"] for result in (disease, pest, unspecified))


def test_fruit_conditions_adjust_confidence_without_changing_hypothesis() -> None:
    base_answers = {
        "affected_part": "fruit",
        "fruit_lesions": False,
        "fruit_abnormal_change": True,
        "fruit_necrosis_or_rot": False,
        "fruit_insect_damage": True,
    }
    low_support = InferenceEngine().evaluate(base_answers)
    high_support = InferenceEngine().evaluate({
        **base_answers,
        "fruit_development_stage": "ripening",
        "fruit_humid_conditions": True,
        "fruit_recent_rains": True,
        "fruit_dense_shade": True,
        "fruit_damage_distribution": "widespread",
    })

    assert low_support["primary_hypothesis"]["disease"] == "fruit_associated_pest"
    assert high_support["primary_hypothesis"]["disease"] == "fruit_associated_pest"
    assert high_support["primary_hypothesis"]["score"] > low_support["primary_hypothesis"]["score"]
    assert high_support["primary_hypothesis"]["score"] == 100


def test_legacy_fruit_alteration_answers_activate_the_new_flow() -> None:
    result = InferenceEngine().evaluate({
        "affected_part": "fruit",
        "fruit_lesions": False,
        "premature_fruit_drop": True,
        "fruit_necrosis_or_rot": False,
        "fruit_insect_damage": False,
    })

    assert result["primary_hypothesis"]["disease"] == "fruit_unspecified_disorder"
