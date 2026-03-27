import json
from pathlib import Path
from typing import Union
from ..models.component import AircraftComponent


class JSONSerializer:
    """Handles JSON serialization for aircraft component data."""

    def __init__(self, filepath: Union[str, Path]):
        self.filepath = Path(filepath)

    def save(self, component: AircraftComponent) -> None:
        """Save component to JSON file."""
        self.filepath.parent.mkdir(parents=True, exist_ok=True)
        with open(self.filepath, 'w', encoding='utf-8') as f:
            json.dump(component.to_dict(), f, indent=2)

    def load(self) -> AircraftComponent:
        """Load component from JSON file."""
        with open(self.filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)
        return AircraftComponent.from_dict(data)

    def exists(self) -> bool:
        """Check if file exists."""
        return self.filepath.exists()
