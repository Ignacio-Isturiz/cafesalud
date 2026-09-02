from app.expert_system.engine.models import Condition, Rule


# Pesos iniciales de demostración. TODO: validar pesos con experto agrónomo.
RULES: tuple[Rule, ...] = (
    Rule(
        id="rust-foliar-pattern",
        disease_id="coffee_rust",
        conditions=(
            Condition("affected_part", "leaf", "Parte afectada: hoja", 2, required=True),
            Condition("leaf_lesions", True, "Manchas o lesiones foliares", 1),
            Condition("yellow_spots", True, "Manchas amarillas", 2),
            Condition("orange_powder_underside", True, "Polvo anaranjado en el envés", 4),
            Condition("humid_conditions", True, "Condiciones húmedas", 1),
        ),
    ),
    Rule(
        id="iron-spot-foliar-pattern",
        disease_id="iron_spot",
        conditions=(
            Condition("affected_part", "leaf", "Parte afectada: hoja", 2, required=True),
            Condition("leaf_lesions", True, "Manchas o lesiones foliares", 1),
            Condition("circular_brown_lesions", True, "Lesiones circulares pardas", 3),
            Condition("light_center", True, "Centro claro", 2),
            Condition("yellow_halo", True, "Halo amarillento o rojizo", 2),
        ),
    ),
    Rule(
        id="american-leaf-spot-pattern",
        disease_id="american_leaf_spot",
        conditions=(
            Condition("affected_part", "leaf", "Parte afectada: hoja", 2, required=True),
            Condition("leaf_lesions", True, "Manchas o lesiones foliares", 1),
            Condition("target_like_lesions", True, "Lesiones tipo diana", 3),
            Condition("light_center", True, "Centro claro", 2),
            Condition("dark_margin", True, "Borde oscuro", 2),
        ),
    ),
)

