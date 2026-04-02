import pytest
from ..models.component import AircraftComponent, Dimension, LoadData, LoadCase, MaterialType


class TestDimension:
    def test_volume_calculation(self, sample_component):
        dim = sample_component.dimensions
        expected_volume = dim.length * dim.width * dim.height
        assert dim.volume() == expected_volume

    def test_to_dict(self, sample_component):
        dim_dict = sample_component.dimensions.to_dict()
        assert dim_dict['length'] == 2.5
        assert dim_dict['width'] == 0.3
        assert dim_dict['height'] == 0.15

    def test_from_dict(self):
        data = {'length': 2.5, 'width': 0.3, 'height': 0.15, 'tolerance': 0.0005}
        dim = Dimension.from_dict(data)
        assert dim.length == 2.5
        assert dim.width == 0.3


class TestLoadData:
    def test_magnitude_calculation(self, sample_load_data):
        expected_mag = (15000**2 + 5000**2 + (-2000)**2) ** 0.5
        assert abs(sample_load_data.magnitude() - expected_mag) < 0.01

    def test_to_dict(self, sample_load_data):
        load_dict = sample_load_data.to_dict()
        assert load_dict['case_type'] == 'static'
        assert len(load_dict['force_vector']) == 3


class TestAircraftComponent:
    def test_auto_generate_id(self):
        comp = AircraftComponent(
            component_id="",
            name="Auto ID Test",
            material=MaterialType.ALUMINUM,
            dimensions=Dimension(length=1.0, width=1.0, height=1.0),
            mass=10.0
        )
        assert comp.component_id != ""
        assert len(comp.component_id) == 36  # UUID length

    def test_add_load_case(self, sample_component, sample_load_data):
        initial_count = len(sample_component.load_cases)
        sample_component.add_load_case(sample_load_data)
        assert len(sample_component.load_cases) == initial_count + 1

    def test_total_force_magnitude(self, sample_component, sample_load_data):
        sample_component.add_load_case(sample_load_data)
        total_mag = sample_component.get_total_force_magnitude()
        assert total_mag > 0

    def test_version_increment(self, sample_component):
        old_version = sample_component.version
        new_version = sample_component.increment_version()
        assert new_version != old_version
        assert new_version == "1.0.1"

    def test_serialization_roundtrip(self, sample_component):
        comp_dict = sample_component.to_dict()
        restored = AircraftComponent.from_dict(comp_dict)
        assert restored.component_id == sample_component.component_id
        assert restored.name == sample_component.name
        assert restored.mass == sample_component.mass
