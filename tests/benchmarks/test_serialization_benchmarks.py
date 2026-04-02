import pytest
import json
import yaml
import h5py
import numpy as np
from pathlib import Path
from models.component import AircraftComponent, Dimension, LoadData, LoadCase, MaterialType
from serializers.json_serializer import JSONSerializer
from serializers.yaml_serializer import YAMLSerializer
from serializers.hdf5_serializer import HDF5Serializer

@pytest.fixture
def large_component(benchmark):
    """Generate a component with 10,000 load cases for benchmarking."""
    comp = AircraftComponent(
        component_id="BENCH-001",
        name="Large Wing Assembly",
        material=MaterialType.CARBON_FIBER,
        dimensions=Dimension(length=15.0, width=2.0, height=0.5),
        mass=1200.0
    )
    # Generate 10,000 random load cases
    for _ in range(10000):
        comp.add_load_case(LoadData(
            case_type=LoadCase.STATIC,
            force_vector=np.random.uniform(-20000, 20000, 3).tolist(),
            moment_vector=np.random.uniform(-5000, 5000, 3).tolist(),
            temperature=np.random.uniform(200, 400)
        ))
    return comp

def test_json_serialization_speed(benchmark, large_component):
    """Benchmark JSON serialization speed."""
    serializer = JSONSerializer("bench_output.json")
    result = benchmark(serializer.save, large_component)
    assert result is None

def test_yaml_serialization_speed(benchmark, large_component):
    """Benchmark YAML serialization speed."""
    serializer = YAMLSerializer("bench_output.yaml")
    result = benchmark(serializer.save, large_component)
    assert result is None

def test_hdf5_serialization_speed(benchmark, large_component):
    """Benchmark HDF5 serialization speed (should be fastest for large data)."""
    serializer = HDF5Serializer("bench_output.h5")
    result = benchmark(serializer.save, large_component)
    assert result is None

def test_hdf5_compression_ratio(benchmark, large_component):
    """Benchmark compression ratio of HDF5 vs JSON."""
    # Save JSON
    json_ser = JSONSerializer("bench_comp.json")
    json_ser.save(large_component)
    json_size = Path("bench_comp.json").stat().st_size

    # Save HDF5
    hdf5_ser = HDF5Serializer("bench_comp.h5")
    hdf5_ser.save(large_component)
    hdf5_size = Path("bench_comp.h5").stat().st_size

    ratio = json_size / hdf5_size
    print(f"\nCompression Ratio (JSON/HDF5): {ratio:.2f}x")
    assert ratio > 5.0, "HDF5 should compress significantly better than JSON for this data"
