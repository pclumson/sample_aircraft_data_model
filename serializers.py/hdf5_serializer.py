import h5py
import numpy as np
from pathlib import Path
from typing import Union
from ..models.component import AircraftComponent


class HDF5Serializer:
    """Handles HDF5 serialization for large-scale simulation data."""

    def __init__(self, filepath: Union[str, Path]):
        self.filepath = Path(filepath)

    def save(self, component: AircraftComponent) -> None:
        """Save component to HDF5 file with compression."""
        self.filepath.parent.mkdir(parents=True, exist_ok=True)

        with h5py.File(self.filepath, 'w') as f:
            # Metadata group
            meta = f.create_group('metadata')
            meta.attrs['component_id'] = component.component_id
            meta.attrs['name'] = component.name
            meta.attrs['material'] = component.material.value
            meta.attrs['version'] = component.version
            meta.attrs['mass'] = component.mass
            meta.attrs['created_at'] = component.created_at.isoformat()

            # Dimensions dataset
            dims = f.create_group('dimensions')
            dims.attrs['length'] = component.dimensions.length
            dims.attrs['width'] = component.dimensions.width
            dims.attrs['height'] = component.dimensions.height
            dims.attrs['tolerance'] = component.dimensions.tolerance

            # Load cases dataset
            if component.load_cases:
                loads = f.create_group('load_cases')
                forces = np.array([lc.force_vector for lc in component.load_cases])
                moments = np.array([lc.moment_vector for lc in component.load_cases])

                loads.create_dataset('forces', data=forces, compression='gzip', chunks=True)
                loads.create_dataset('moments', data=moments, compression='gzip', chunks=True)

                # Store case types as strings
                case_types = np.array([lc.case_type.value for lc in component.load_cases])
                loads.create_dataset('case_types', data=case_types)

    def load(self) -> AircraftComponent:
        """Load component from HDF5 file."""
        with h5py.File(self.filepath, 'r') as f:
            meta = f['metadata']
            dims = f['dimensions']

            component = AircraftComponent(
                component_id=meta.attrs['component_id'],
                name=meta.attrs['name'],
                material=meta.attrs['material'],
                dimensions=Dimension(
                    length=dims.attrs['length'],
                    width=dims.attrs['width'],
                    height=dims.attrs['height'],
                    tolerance=dims.attrs['tolerance']
                ),
                mass=meta.attrs['mass'],
                version=meta.attrs['version'],
                created_at=datetime.fromisoformat(meta.attrs['created_at'])
            )

            # Load load cases if they exist
            if 'load_cases' in f:
                loads = f['load_cases']
                forces = loads['forces'][:]
                moments = loads['moments'][:]
                case_types = loads['case_types'][:]

                for i, (force, moment, case_type) in enumerate(zip(forces, moments, case_types)):
                    component.add_load_case(LoadData(
                        case_type=LoadCase(case_type.decode() if isinstance(case_type, bytes) else case_type),
                        force_vector=force.tolist(),
                        moment_vector=moment.tolist(),
                        temperature=293.15  # Default temperature
                    ))

            return component
