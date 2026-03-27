from typing import Dict, Any, List
from ..models.component import AircraftComponent, MaterialType, LoadCase


class SchemaValidator:
    """Validates component data against defined schema rules."""

    REQUIRED_FIELDS = ['component_id', 'name', 'material', 'dimensions', 'mass']

    @staticmethod
    def validate_component(component: AircraftComponent) -> List[str]:
        """Validate component and return list of errors."""
        errors = []

        # Validate mass
        if component.mass <= 0:
            errors.append("Mass must be positive")

        # Validate dimensions
        if component.dimensions.length <= 0:
            errors.append("Length must be positive")
        if component.dimensions.width <= 0:
            errors.append("Width must be positive")
        if component.dimensions.height <= 0:
            errors.append("Height must be positive")

        # Validate load cases
        for i, load in enumerate(component.load_cases):
            if len(load.force_vector) != 3:
                errors.append(f"Load case {i}: Force vector must have 3 components")
            if len(load.moment_vector) != 3:
                errors.append(f"Load case {i}: Moment vector must have 3 components")

        return errors

    @staticmethod
    def is_valid(data: Dict[str, Any]) -> tuple[bool, List[str]]:
        """Check if raw data conforms to schema."""
        errors = []

        for field in SchemaValidator.REQUIRED_FIELDS:
            if field not in data:
                errors.append(f"Missing required field: {field}")

        if 'material' in data and data['material'] not in [m.value for m in MaterialType]:
            errors.append(f"Invalid material type: {data['material']}")

        if 'dimensions' in data:
            dim = data['dimensions']
            for d in ['length', 'width', 'height']:
                if d not in dim or dim[d] <= 0:
                    errors.append(f"Invalid dimension: {d}")

        return len(errors) == 0, errors
