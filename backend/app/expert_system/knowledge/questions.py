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
    conditional_on: str | None = None,
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
        "conditional_logic": None if conditional_on is None else {
            "question_key": conditional_on,
            "operator": "equals",
            "value": True,
        },
        "image": None,
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
DISTRIBUTION_OPTIONS = [
    option("isolated", "Aisladas"),
    option("scattered", "Dispersas"),
    option("widespread", "Extendidas"),
]


QUESTIONS: tuple[dict[str, object], ...] = (
    question("leaf_lesions", "¿La hoja presenta manchas o lesiones?", "boolean", "leaf", 1),
    question("lesion_color", "¿Qué color tienen las manchas o lesiones?", "multiple_choice", "leaf", 2, COLOR_OPTIONS, "Selecciona todos los colores que observes.", "leaf_lesions"),
    question("lesion_shape", "¿Qué forma predomina en las lesiones?", "single_choice", "leaf", 3, SHAPE_OPTIONS, conditional_on="leaf_lesions"),
    question("lesion_size", "¿Cuál es el tamaño predominante de las lesiones?", "select", "leaf", 4, SIZE_OPTIONS, conditional_on="leaf_lesions"),
    question("lesion_center", "¿Cómo se observa el centro de la lesión?", "single_choice", "leaf", 5, [option("light", "Centro claro"), option("dark", "Centro oscuro"), option("uniform", "Color uniforme")], conditional_on="leaf_lesions"),
    question("lesion_border_halo", "¿Qué borde o halo presenta la lesión?", "multiple_choice", "leaf", 6, [option("yellow", "Halo amarillo"), option("reddish", "Halo rojizo"), option("dark", "Borde oscuro"), option("none", "Sin borde o halo definido")], "Selecciona todo lo que aplique.", "leaf_lesions"),
    question("leaf_side", "¿En qué cara de la hoja se observan los signos?", "multiple_choice", "leaf", 7, [option("upper", "Haz"), option("underside", "Envés"), option("both", "Ambas caras")], conditional_on="leaf_lesions"),
    question("lesion_distribution", "¿Cómo se distribuyen las lesiones en la hoja?", "single_choice", "leaf", 8, DISTRIBUTION_OPTIONS, conditional_on="leaf_lesions"),
    question("orange_powder_underside", "¿Observas polvo anaranjado en el envés, característico de roya?", "boolean", "leaf", 9, conditional_on="leaf_lesions"),
    question("eye_spot_compatible", "¿Las lesiones son compatibles con ojo de gallo o gotera?", "boolean", "leaf", 10, description="Considera lesiones en anillos o tipo diana con centro claro y borde oscuro.", conditional_on="leaf_lesions"),
    question("defoliation", "¿La planta presenta defoliación?", "boolean", "leaf", 11),
    question("necrosis", "¿Observas tejido necrosado en las hojas?", "boolean", "leaf", 12),
    question("humid_conditions", "¿El cultivo ha estado en condiciones de humedad alta?", "boolean", "leaf", 13),
    question("recent_rains", "¿Se han presentado lluvias recientes?", "boolean", "leaf", 14),
    question("nearby_plants_affected", "¿Los síntomas aparecen también en plantas cercanas?", "boolean", "leaf", 15),

    question("stem_lesions", "¿El tallo o la rama presenta lesiones visibles?", "boolean", "stem", 1),
    question("stem_lesion_color", "¿Qué color tienen las lesiones?", "multiple_choice", "stem", 2, COLOR_OPTIONS, conditional_on="stem_lesions"),
    question("stem_lesion_shape", "¿Qué forma tienen las lesiones?", "single_choice", "stem", 3, SHAPE_OPTIONS, conditional_on="stem_lesions"),
    question("stem_necrosis", "¿Observas necrosis en el tallo o la rama?", "boolean", "stem", 4),
    question("stem_drying", "¿Existe secamiento del tallo o de las ramas?", "boolean", "stem", 5),
    question("stem_distribution", "¿Cómo se distribuye el daño?", "single_choice", "stem", 6, DISTRIBUTION_OPTIONS),

    question("fruit_lesions", "¿El fruto presenta manchas o lesiones visibles?", "boolean", "fruit", 1),
    question("fruit_lesion_color", "¿Qué color tienen las manchas o lesiones?", "multiple_choice", "fruit", 2, COLOR_OPTIONS, conditional_on="fruit_lesions"),
    question("fruit_lesion_shape", "¿Qué forma predomina en las lesiones?", "single_choice", "fruit", 3, SHAPE_OPTIONS, conditional_on="fruit_lesions"),
    question("fruit_lesion_size", "¿Cuál es el tamaño predominante de las lesiones?", "select", "fruit", 4, SIZE_OPTIONS, conditional_on="fruit_lesions"),
    question("premature_fruit_drop", "¿Hay caída prematura de frutos?", "boolean", "fruit", 5),
    question("fruit_color_change", "¿Observas un cambio de color anormal en el fruto?", "boolean", "fruit", 6),
    question("abnormal_fruit_development", "¿El fruto presenta desarrollo anormal?", "boolean", "fruit", 7),
    question("fruit_insect_damage", "¿Observas perforaciones o presencia de insectos?", "boolean", "fruit", 8),
)


def questions_for(affected_part: str | None = None) -> tuple[dict[str, object], ...]:
    if affected_part is None:
        return QUESTIONS
    normalized_part = "stem" if affected_part == "stem_branch" else affected_part
    return tuple(question_item for question_item in QUESTIONS if question_item["affected_part"] == normalized_part)
