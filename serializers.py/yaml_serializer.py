import yaml
from pathlib import Path
from typing import Union
from ..models.component import AircraftComponent


class YAMLSerializer:
    """Handles YAML serialization for aircraft component data."""

    def __init__(self, filepath: Union[str, Path]):
        self.filepath = Path(filepath)

    def save(self, component: AircraftComponent) -> None:
        """Save component to YAML file."""
        self.filepath.parent.mkdir(parents=True, exist_ok=True)
        with open(self.filepath, 'w', encoding='utf-8') as f:
            yaml.dump(component.to_dict(), f, default_flow_style=False)

    def load(self) -> AircraftComponent:
        """Load component from YAML file."""
        with open(self.filepath, 'r', encoding='utf-8') as f:
            data = yaml.safe_load(f)
        return AircraftComponent.from_dict(data)
