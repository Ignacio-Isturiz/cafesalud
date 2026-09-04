from app.domain.disease import DiseaseDefinition


DISEASES: tuple[DiseaseDefinition, ...] = (
    DiseaseDefinition(
        id="coffee_rust",
        name="Roya del café",
        description="Patrón foliar asociado a manchas amarillas y signos anaranjados, especialmente en el envés.",
        affected_part="leaf",
        symptoms=("leaf_lesions", "yellow_spots", "orange_powder_underside"),
        recommendations=(
            "Consulta a un profesional agrónomo para confirmar la causa.",
            "Registra humedad, lluvias recientes y distribución del problema.",
            "Evita trasladar material vegetal afectado sin orientación técnica.",
        ),
    ),
    DiseaseDefinition(
        id="iron_spot",
        name="Mancha de hierro",
        description="Patrón foliar de lesiones circulares pardas, con centro claro y halo rojizo o amarillento.",
        affected_part="leaf",
        symptoms=("leaf_lesions", "circular_brown_lesions", "light_center", "yellow_halo"),
        recommendations=(
            "Solicita confirmación técnica antes de aplicar tratamientos.",
            "Revisa el estado nutricional y las condiciones de humedad del lote.",
            "Documenta la evolución y presencia en plantas cercanas.",
        ),
    ),
    DiseaseDefinition(
        id="american_leaf_spot",
        name="Ojo de gallo / Gotera",
        description="Patrón foliar de lesiones circulares con centro claro y borde oscuro.",
        affected_part="leaf",
        symptoms=("leaf_lesions", "target_like_lesions", "light_center", "dark_margin"),
        recommendations=(
            "Confirma la hipótesis con asistencia agronómica local.",
            "Evalúa humedad, sombra, aireación y distribución de las lesiones.",
            "Separa la observación de hojas afectadas del resto del manejo del cultivo.",
        ),
    ),
    DiseaseDefinition(
        id="stem_necrotic_disorder",
        name="Afección con necrosis en tallo o rama",
        description="Patrón de tejido muerto, necrosis o secamiento localizado en tallos o ramas.",
        affected_part="stem_branch",
        symptoms=("stem_necrosis", "stem_progressive_drying"),
        recommendations=(
            "Solicita una evaluación agronómica para identificar la causa de la necrosis.",
            "Registra el avance del secamiento y retira material únicamente con orientación técnica.",
            "Revisa humedad, lluvias, sombra, aireación y distribución del daño.",
        ),
    ),
    DiseaseDefinition(
        id="stem_fungal_disorder",
        name="Posible enfermedad fúngica de tallo o rama",
        description="Patrón asociado con hilos, micelio u otras estructuras visibles sobre el tallo o las ramas.",
        affected_part="stem_branch",
        symptoms=("stem_fungal_structures",),
        recommendations=(
            "Confirma la presencia de estructuras fúngicas con asistencia agronómica.",
            "Evita trasladar o podar material afectado sin medidas de higiene adecuadas.",
            "Documenta las condiciones ambientales y la distribución del problema.",
        ),
    ),
    DiseaseDefinition(
        id="stem_associated_pest",
        name="Posible plaga asociada en tallo o rama",
        description="Patrón de perforaciones o insectos visibles en tallos o ramas.",
        affected_part="stem_branch",
        symptoms=("stem_insect_damage",),
        recommendations=(
            "Registra fotografías de las perforaciones o insectos para facilitar su identificación.",
            "Consulta a un profesional antes de aplicar controles físicos, biológicos o químicos.",
            "Revisa otras plantas para determinar la distribución del daño.",
        ),
    ),
    DiseaseDefinition(
        id="stem_unspecified_disorder",
        name="Posible afección de tallo o rama",
        description="El daño observado mantiene una hipótesis de enfermedad, sin signos visibles de hongos o insectos.",
        affected_part="stem_branch",
        symptoms=("stem_lesions", "stem_progressive_drying"),
        recommendations=(
            "Solicita una inspección agronómica para diferenciar enfermedad, daño físico u otra causa.",
            "Registra la evolución y distribución del daño en el lote.",
            "Evita aplicar tratamientos hasta contar con una identificación más precisa.",
        ),
    ),
    DiseaseDefinition(
        id="fruit_associated_disease",
        name="Posible afección asociada al fruto",
        description="Patrón de necrosis, pudrición o hundimiento del tejido del fruto.",
        affected_part="fruit",
        symptoms=("fruit_lesions", "fruit_necrosis_or_rot"),
        recommendations=(
            "Solicita una evaluación agronómica para identificar la causa del daño en el fruto.",
            "Registra la etapa del fruto y la evolución de la necrosis o pudrición.",
            "Evita trasladar frutos afectados sin orientación técnica.",
        ),
    ),
    DiseaseDefinition(
        id="fruit_associated_pest",
        name="Posible plaga asociada al fruto",
        description="Patrón de perforaciones o signos visibles de alimentación de insectos en el fruto.",
        affected_part="fruit",
        symptoms=("fruit_insect_damage",),
        recommendations=(
            "Registra fotografías de las perforaciones o insectos para facilitar su identificación.",
            "Consulta a un profesional antes de aplicar medidas de control.",
            "Revisa otros frutos y plantas para determinar la distribución del daño.",
        ),
    ),
    DiseaseDefinition(
        id="fruit_unspecified_disorder",
        name="Posible alteración fisiológica o fitopatológica del fruto",
        description="Alteración del fruto sin necrosis, pudrición, perforaciones ni insectos visibles.",
        affected_part="fruit",
        symptoms=("fruit_abnormal_change", "fruit_lesions"),
        recommendations=(
            "Solicita una inspección agronómica para diferenciar una alteración fisiológica de una enfermedad.",
            "Registra la etapa de desarrollo, el cambio de color y la caída de frutos.",
            "Documenta las condiciones ambientales y la distribución del problema.",
        ),
    ),
)

DISEASE_BY_ID = {disease.id: disease for disease in DISEASES}
