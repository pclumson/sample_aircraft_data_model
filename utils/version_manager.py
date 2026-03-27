from pathlib import Path
from datetime import datetime
from typing import List
import shutil


class VersionManager:
    """Manages version history for component data files."""

    def __init__(self, base_dir: Path):
        self.base_dir = Path(base_dir)
        self.base_dir.mkdir(parents=True, exist_ok=True)

    def create_backup(self, filepath: Path) -> Path:
        """Create timestamped backup of file."""
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        backup_path = self.base_dir / f"{filepath.stem}_{timestamp}{filepath.suffix}"
        shutil.copy2(filepath, backup_path)
        return backup_path

    def list_versions(self, filepath: Path) -> List[Path]:
        """List all version backups for a file."""
        prefix = filepath.stem
        return sorted(self.base_dir.glob(f"{prefix}_*.json"))

    def restore_version(self, backup_path: Path, target_path: Path) -> None:
        """Restore a specific version."""
        shutil.copy2(backup_path, target_path)
