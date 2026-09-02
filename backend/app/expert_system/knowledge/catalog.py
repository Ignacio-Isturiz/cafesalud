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
)

DISEASE_BY_ID = {disease.id: disease for disease in DISEASES}

