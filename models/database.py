from sqlalchemy import Column, Integer, String, Float, DateTime, Text, ForeignKey, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy.dialects.postgresql import UUID
from datetime import datetime
import uuid

Base = declarative_base()


class Component(Base):
    """SQLAlchemy model for aircraft component."""
    __tablename__ = 'components'

    id = Column(Integer, primary_key=True, autoincrement=True)
    component_id = Column(String(36), unique=True, nullable=False, index=True)
    name = Column(String(255), nullable=False)
    material = Column(String(50), nullable=False)
    mass = Column(Float, nullable=False)
    version = Column(String(20), default='1.0.0')
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    metadata = Column(Text)  # JSON stored as text

    # Relationships
    dimensions = relationship('Dimension', back_populates='component', uselist=False, cascade='all, delete-orphan')
    load_cases = relationship('LoadCase', back_populates='component', cascade='all, delete-orphan')

    def to_dict(self):
        return {
            'id': self.id,
            'component_id': self.component_id,
            'name': self.name,
            'material': self.material,
            'mass': self.mass,
            'version': self.version,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
            'dimensions': self.dimensions.to_dict() if self.dimensions else None,
            'load_cases': [lc.to_dict() for lc in self.load_cases]
        }


class Dimension(Base):
    """SQLAlchemy model for component dimensions."""
    __tablename__ = 'dimensions'

    id = Column(Integer, primary_key=True, autoincrement=True)
    component_id = Column(Integer, ForeignKey('components.id'), nullable=False)
    length = Column(Float, nullable=False)
    width = Column(Float, nullable=False)
    height = Column(Float, nullable=False)
    tolerance = Column(Float, default=0.001)

    component = relationship('Component', back_populates='dimensions')

    def to_dict(self):
        return {
            'length': self.length,
            'width': self.width,
            'height': self.height,
            'tolerance': self.tolerance
        }


class LoadCase(Base):
    """SQLAlchemy model for load case data."""
    __tablename__ = 'load_cases'

    id = Column(Integer, primary_key=True, autoincrement=True)
    component_id = Column(Integer, ForeignKey('components.id'), nullable=False)
    case_type = Column(String(50), nullable=False)
    force_x = Column(Float, nullable=False)
    force_y = Column(Float, nullable=False)
    force_z = Column(Float, nullable=False)
    moment_x = Column(Float, nullable=False)
    moment_y = Column(Float, nullable=False)
    moment_z = Column(Float, nullable=False)
    temperature = Column(Float, default=293.15)
    timestamp = Column(DateTime, default=datetime.utcnow)

    component = relationship('Component', back_populates='load_cases')

    def to_dict(self):
        return {
            'case_type': self.case_type,
            'force_vector': [self.force_x, self.force_y, self.force_z],
            'moment_vector': [self.moment_x, self.moment_y, self.moment_z],
            'temperature': self.temperature,
            'timestamp': self.timestamp.isoformat() if self.timestamp else None
        }


# Database connection factory
def get_database_engine(db_url='sqlite:///aircraft_data.db'):
    """Create database engine."""
    engine = create_engine(db_url, echo=False)
    return engine


def init_db(engine):
    """Initialize database tables."""
    Base.metadata.create_all(engine)


def get_session(engine):
    """Create database session."""
    Session = sessionmaker(bind=engine)
    return Session()
