import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from ..models.database import Base, get_database_engine, init_db
from ..models.component import AircraftComponent, Dimension, LoadData, LoadCase, MaterialType


@pytest.fixture(scope="session")
def engine():
    """Create test database engine."""
    engine = create_engine("sqlite:///:memory:", echo=False)
    Base.metadata.create_all(engine)
    return engine


@pytest.fixture
def session(engine):
    """Create test database session."""
    Session = sessionmaker(bind=engine)
    return Session()


@pytest.fixture
def sample_component():
    """Create a sample aircraft component for testing."""
    return AircraftComponent(
        component_id="TEST-001",
        name="Test Wing Splice",
        material=MaterialType.ALUMINUM,
        dimensions=Dimension(length=2.5, width=0.3, height=0.15, tolerance=0.0005),
        mass=45.7,
        version="1.0.0"
    )


@pytest.fixture
def sample_load_data():
    """Create sample load data for testing."""
    return LoadData(
        case_type=LoadCase.STATIC,
        force_vector=[15000.0, 5000.0, -2000.0],
        moment_vector=[500.0, 200.0, 100.0],
        temperature=293.15
    )
