from models.component import AircraftComponent, Dimension, LoadData, LoadCase, MaterialType
from serializers.json_serializer import JSONSerializer
from serializers.yaml_serializer import YAMLSerializer
from serializers.hdf5_serializer import HDF5Serializer
from validators.schema_validator import SchemaValidator
from utils.version_manager import VersionManager
from pathlib import Path


def main():
    # Create a sample aircraft component
    wing_splice = AircraftComponent(
        component_id="WING-SPLICE-001",
        name="Left Wing Splice Assembly",
        material=MaterialType.ALUMINUM,
        dimensions=Dimension(length=2.5, width=0.3, height=0.15, tolerance=0.0005),
        mass=45.7,
        version="1.0.0"
    )
    
    # Add load cases
    wing_splice.add_load_case(LoadData(
        case_type=LoadCase.STATIC,
        force_vector=[15000.0, 5000.0, -2000.0],
        moment_vector=[500.0, 200.0, 100.0],
        temperature=293.15
    ))
    
    wing_splice.add_load_case(LoadData(
        case_type=LoadCase.FATIGUE,
        force_vector=[12000.0, 4000.0, -1500.0],
        moment_vector=[400.0, 150.0, 80.0],
        temperature=293.15
    ))
    
    # Validate component
    errors = SchemaValidator.validate_component(wing_splice)
    if errors:
        print(f"Validation errors: {errors}")
        return
    
    print(f"✓ Component validated successfully")
    print(f"  Total force magnitude: {wing_splice.get_total_force_magnitude():.2f} N")
    
    # Save to different formats
    output_dir = Path("output")
    
    # JSON
    json_ser = JSONSerializer(output_dir / "wing_splice.json")
    json_ser.save(wing_splice)
    print(f"✓ Saved to JSON: {json_ser.filepath}")
    
    # YAML
    yaml_ser = YAMLSerializer(output_dir / "wing_splice.yaml")
    yaml_ser.save(wing_splice)
    print(f"✓ Saved to YAML: {yaml_ser.filepath}")
    
    # HDF5 (for large datasets)
    hdf5_ser = HDF5Serializer(output_dir / "wing_splice.h5")
    hdf5_ser.save(wing_splice)
    print(f"✓ Saved to HDF5: {hdf5_ser.filepath}")
    
    # Version management
    version_mgr = VersionManager(Path("backups"))
    backup = version_mgr.create_backup(json_ser.filepath)
    print(f"✓ Backup created: {backup}")
    
    # Increment version and save
    new_version = wing_splice.increment_version()
    print(f"✓ Version incremented to: {new_version}")
    
    json_ser.save(wing_splice)
    print("✓ Updated component saved")


if __name__ == "__main__":
    main()
