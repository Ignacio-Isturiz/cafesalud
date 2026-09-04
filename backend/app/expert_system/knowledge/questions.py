YES_NO = [
    {"value": True, "label": "Sí"},
    {"value": False, "label": "No"},
]


def option(value: str, label: str, description: str | None = None) -> dict[str, object]:
    item: dict[str, object] = {"value": value, "label": label}
    if description:
        item["description"] = description
    return item


def question(
    key: str,
    label: str,
    question_type: str,
    affected_part: str,
    order: int,
    options: list[dict[str, object]] | None = None,
    description: str | None = None,
    conditional_logic: dict[str, object] | None = None,
    image_key: str | None = "default",
) -> dict[str, object]:
    return {
        "id": f"{affected_part}-{order}",
        "key": key,
        "label": label,
        "description": description,
        "type": question_type,
        "options": YES_NO if question_type == "boolean" else (options or []),
        "required": True,
        "order": order,
        "affected_part": affected_part,
        "conditional_logic": conditional_logic,
        "image": None if image_key is None else f"/images/questions/{(key if image_key == 'default' else image_key).replace('_', '-')}.webp",
    }


def when(question_key: str, value: str | bool = True, operator: str = "equals") -> dict[str, object]:
    return {"question_key": question_key, "operator": operator, "value": value}


LEAF_HYPOTHESIS_IDENTIFIED = {
    "any": [
        {"question_key": "iron_spot_compatible", "operator": "equals", "value": True},
        {"question_key": "orange_powder_underside", "operator": "equals", "value": True},
        {"question_key": "eye_spot_compatible", "operator": "equals", "value": True},
    ]
}

STEM_ANALYSIS_ACTIVE = {
    "any": [
        {"question_key": "stem_lesions", "operator": "equals", "value": True},
        {"question_key": "stem_progressive_drying", "operator": "equals", "value": True},
    ]
}

STEM_HYPOTHESIS_IDENTIFIED = {
    "any": [
        {"question_key": "stem_necrosis", "operator": "equals", "value": True},
        {"question_key": "stem_fungal_structures", "operator": "equals", "value": True},
        {"question_key": "stem_insect_damage", "operator": "equals", "value": True},
        {"question_key": "stem_insect_damage", "operator": "equals", "value": False},
    ]
}

FRUIT_ANALYSIS_ACTIVE = {
    "any": [
        {"question_key": "fruit_lesions", "operator": "equals", "value": True},
        {"question_key": "fruit_abnormal_change", "operator": "equals", "value": True},
    ]
}

FRUIT_HYPOTHESIS_IDENTIFIED = {
    "any": [
        {"question_key": "fruit_necrosis_or_rot", "operator": "equals", "value": True},
        {"question_key": "fruit_insect_damage", "operator": "equals", "value": True},
        {"question_key": "fruit_insect_damage", "operator": "equals", "value": False},
    ]
}


COLOR_OPTIONS = [
    option("yellow", "Amarillo"),
    option("orange", "Anaranjado"),
    option("brown", "Café o pardo"),
    option("reddish", "Rojizo"),
    option("gray", "Grisáceo"),
    option("other", "Otro color"),
]
SHAPE_OPTIONS = [
    option("circular", "Circular"),
    option("irregular", "Irregular"),
    option("target_like", "En anillos o tipo diana"),
    option("elongated", "Alargada"),
    option("other", "Otra forma"),
]
SIZE_OPTIONS = [option("small", "Pequeña"), option("medium", "Mediana"), option("large", "Grande")]
FRUIT_STAGE_OPTIONS = [
    option("green", "Verde"),
    option("growing", "En crecimiento"),
    option("ripening", "En maduración"),
    option("ripe", "Maduro"),
    option("dry", "Seco"),
]
DISTRIBUTION_OPTIONS = [
    option("isolated", "Aisladas"),
    option("scattered", "Dispersas"),
    option("widespread", "Extendidas"),
]


QUESTIONS: tuple[dict[str, object], ...] = (
    question("leaf_lesions", "¿La hoja presenta manchas o lesiones?", "boolean", "leaf", 1),
    question("foliar_decline", "¿Presenta amarillamiento, marchitez o caída anormal de hojas?", "boolean", "leaf", 2, conditional_logic=when("leaf_lesions", False), image_key="defoliation"),
    question("lesion_color", "¿Qué color tienen las manchas o lesiones?", "multiple_choice", "leaf", 3, COLOR_OPTIONS, "Selecciona todos los colores que observes.", when("leaf_lesions")),
    question("lesion_shape", "¿Qué forma predomina en las lesiones?", "single_choice", "leaf", 4, SHAPE_OPTIONS, conditional_logic=when("leaf_lesions")),
    question("lesion_size", "¿Cuál es el tamaño predominante de las lesiones?", "select", "leaf", 5, SIZE_OPTIONS, conditional_logic=when("leaf_lesions")),
    question("lesion_center", "¿Cómo se observa el centro de la lesión?", "single_choice", "leaf", 6, [option("light", "Centro claro"), option("dark", "Centro oscuro"), option("uniform", "Color uniforme")], conditional_logic=when("leaf_lesions")),
    question("lesion_border_halo", "¿Qué borde o halo presenta la lesión?", "multiple_choice", "leaf", 7, [option("yellow", "Halo amarillo"), option("reddish", "Halo rojizo"), option("dark", "Borde oscuro"), option("none", "Sin borde o halo definido")], "Selecciona todo lo que aplique.", when("leaf_lesions")),
    question("leaf_side", "¿En qué cara de la hoja se observan los signos?", "multiple_choice", "leaf", 8, [option("upper", "Haz"), option("underside", "Envés"), option("both", "Ambas caras")], conditional_logic=when("leaf_lesions")),
    question("lesion_distribution", "¿Cómo se distribuyen las lesiones en la hoja?", "single_choice", "leaf", 9, DISTRIBUTION_OPTIONS, conditional_logic=when("leaf_lesions")),
    question("iron_spot_compatible", "¿La lesión es circular, parda o marrón rojiza, con centro claro y halo rojizo o amarillento?", "boolean", "leaf", 10, description="Este patrón orienta la hipótesis hacia mancha de hierro.", conditional_logic=when("leaf_lesions"), image_key="lesion_border_halo"),
    question("orange_powder_underside", "¿Presenta signos foliares característicos de roya, especialmente polvo anaranjado en el envés?", "boolean", "leaf", 11, conditional_logic=when("iron_spot_compatible", False)),
    question("eye_spot_compatible", "¿Las lesiones son compatibles con ojo de gallo o gotera?", "boolean", "leaf", 12, description="Considera lesiones circulares o tipo diana, con centro claro y borde oscuro.", conditional_logic=when("orange_powder_underside", False)),
    question("humid_conditions", "¿El cultivo ha estado en condiciones de humedad alta?", "boolean", "leaf", 13, conditional_logic=LEAF_HYPOTHESIS_IDENTIFIED),
    question("recent_rains", "¿Se han presentado lluvias recientes?", "boolean", "leaf", 14, conditional_logic=LEAF_HYPOTHESIS_IDENTIFIED),
    question("dense_shade", "¿El cultivo presenta sombra densa?", "boolean", "leaf", 15, conditional_logic=LEAF_HYPOTHESIS_IDENTIFIED, image_key="humid_conditions"),
    question("poor_air_circulation", "¿Hay poca aireación entre las plantas?", "boolean", "leaf", 16, conditional_logic=LEAF_HYPOTHESIS_IDENTIFIED, image_key=None),
    question("nutritional_stress", "¿La planta muestra señales de deficiencia o estrés nutricional?", "boolean", "leaf", 17, conditional_logic=LEAF_HYPOTHESIS_IDENTIFIED, image_key=None),
    question("nearby_plants_affected", "¿Los síntomas aparecen también en plantas cercanas?", "boolean", "leaf", 18, conditional_logic=LEAF_HYPOTHESIS_IDENTIFIED),

    question("stem_lesions", "¿El tallo o la rama presenta lesiones visibles?", "boolean", "stem", 1),
    question("stem_progressive_drying", "¿Existe secamiento o muerte progresiva de ramas?", "boolean", "stem", 2, conditional_logic=when("stem_lesions", False), image_key="stem_drying"),
    question("stem_lesion_color", "¿Qué color tienen las lesiones?", "multiple_choice", "stem", 3, COLOR_OPTIONS, "Selecciona todos los colores que observes.", when("stem_lesions")),
    question("stem_lesion_shape", "¿Qué forma tienen las lesiones?", "single_choice", "stem", 4, SHAPE_OPTIONS, conditional_logic=when("stem_lesions")),
    question("stem_necrosis", "¿Hay tejido muerto, necrosis o secamiento localizado?", "boolean", "stem", 5, conditional_logic=STEM_ANALYSIS_ACTIVE),
    question("stem_fungal_structures", "¿Hay hilos, micelio u otra estructura visible sobre el tallo o la rama?", "boolean", "stem", 6, description="Estos signos orientan hacia una posible enfermedad fúngica.", conditional_logic=when("stem_necrosis", False), image_key=None),
    question("stem_insect_damage", "¿Hay perforaciones o insectos visibles en el tallo o la rama?", "boolean", "stem", 7, conditional_logic=when("stem_fungal_structures", False), image_key=None),
    question("stem_humid_conditions", "¿El cultivo ha estado en condiciones de humedad alta?", "boolean", "stem", 8, conditional_logic=STEM_HYPOTHESIS_IDENTIFIED, image_key="humid_conditions"),
    question("stem_recent_rains", "¿Se han presentado lluvias recientes?", "boolean", "stem", 9, conditional_logic=STEM_HYPOTHESIS_IDENTIFIED, image_key="recent_rains"),
    question("stem_dense_shade", "¿El cultivo presenta sombra densa?", "boolean", "stem", 10, conditional_logic=STEM_HYPOTHESIS_IDENTIFIED, image_key="humid_conditions"),
    question("stem_poor_air_circulation", "¿Hay poca aireación entre las plantas?", "boolean", "stem", 11, conditional_logic=STEM_HYPOTHESIS_IDENTIFIED, image_key=None),
    question("stem_damage_distribution", "¿Cómo se distribuye el daño en el tallo o las ramas?", "single_choice", "stem", 12, DISTRIBUTION_OPTIONS, conditional_logic=STEM_HYPOTHESIS_IDENTIFIED, image_key="stem_distribution"),

    question("fruit_lesions", "¿El fruto presenta manchas o lesiones visibles?", "boolean", "fruit", 1),
    question("fruit_abnormal_change", "¿Presenta caída prematura, cambio de color o desarrollo anormal?", "boolean", "fruit", 2, conditional_logic=when("fruit_lesions", False), image_key="abnormal_fruit_development"),
    question("fruit_lesion_color", "¿Qué color tienen las manchas o lesiones?", "multiple_choice", "fruit", 3, COLOR_OPTIONS, "Selecciona todos los colores que observes.", when("fruit_lesions")),
    question("fruit_lesion_shape", "¿Qué forma predomina en las lesiones?", "single_choice", "fruit", 4, SHAPE_OPTIONS, conditional_logic=when("fruit_lesions")),
    question("fruit_lesion_size", "¿Cuál es el tamaño predominante de las lesiones?", "select", "fruit", 5, SIZE_OPTIONS, conditional_logic=when("fruit_lesions")),
    question("fruit_necrosis_or_rot", "¿La lesión presenta necrosis o hundimiento del tejido?", "boolean", "fruit", 6, description="Incluye tejido muerto, pudrición o zonas hundidas.", conditional_logic=FRUIT_ANALYSIS_ACTIVE, image_key="fruit_lesions"),
    question("fruit_insect_damage", "¿Hay perforaciones o signos de alimentación de insectos?", "boolean", "fruit", 7, conditional_logic=when("fruit_necrosis_or_rot", False)),
    question("fruit_development_stage", "¿En qué etapa de desarrollo se encuentra el fruto?", "single_choice", "fruit", 8, FRUIT_STAGE_OPTIONS, conditional_logic=FRUIT_HYPOTHESIS_IDENTIFIED, image_key=None),
    question("fruit_humid_conditions", "¿El cultivo ha estado en condiciones de humedad alta?", "boolean", "fruit", 9, conditional_logic=FRUIT_HYPOTHESIS_IDENTIFIED, image_key="humid_conditions"),
    question("fruit_recent_rains", "¿Se han presentado lluvias recientes?", "boolean", "fruit", 10, conditional_logic=FRUIT_HYPOTHESIS_IDENTIFIED, image_key="recent_rains"),
    question("fruit_dense_shade", "¿El cultivo presenta sombra densa?", "boolean", "fruit", 11, conditional_logic=FRUIT_HYPOTHESIS_IDENTIFIED, image_key="humid_conditions"),
    question("fruit_damage_distribution", "¿Cómo se distribuye el daño en los frutos?", "single_choice", "fruit", 12, DISTRIBUTION_OPTIONS, conditional_logic=FRUIT_HYPOTHESIS_IDENTIFIED, image_key=None),
)


def questions_for(affected_part: str | None = None) -> tuple[dict[str, object], ...]:
    if affected_part is None:
        return QUESTIONS
    normalized_part = "stem" if affected_part == "stem_branch" else affected_part
    return tuple(question_item for question_item in QUESTIONS if question_item["affected_part"] == normalized_part)
