from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from ..schemas import ComponentCreate, ComponentUpdate, ComponentResponse, APIResponse
from ...models.database import get_session, Component, Dimension, LoadCase, init_db
from ...validators.schema_validator import SchemaValidator
import uuid

router = APIRouter(prefix="/components", tags=["Components"])


@router.get("/", response_model=List[ComponentResponse])
async def list_components(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_session)
):
    """List all aircraft components."""
    components = db.query(Component).offset(skip).limit(limit).all()
    return [ComponentResponse(**comp.to_dict()) for comp in components]


@router.get("/{component_id}", response_model=ComponentResponse)
async def get_component(
    component_id: str,
    db: Session = Depends(get_session)
):
    """Get a specific component by ID."""
    component = db.query(Component).filter(Component.component_id == component_id).first()
    if not component:
        raise HTTPException(status_code=404, detail="Component not found")
    return ComponentResponse(**component.to_dict())


@router.post("/", response_model=APIResponse)
async def create_component(
    component_data: ComponentCreate,
    db: Session = Depends(get_session)
):
    """Create a new aircraft component."""
    try:
        # Generate component ID
        component_id = str(uuid.uuid4())

        # Create component
        component = Component(
            component_id=component_id,
            name=component_data.name,
            material=component_data.material.value,
            mass=component_data.mass,
            version=component_data.version,
            metadata=str(component_data.metadata)
        )

        # Create dimensions
        dimension = Dimension(
            component_id=None,  # Will be set after component is added
            length=component_data.dimensions.length,
            width=component_data.dimensions.width,
            height=component_data.dimensions.height,
            tolerance=component_data.dimensions.tolerance
        )
        component.dimensions = dimension

        db.add(component)
        db.commit()
        db.refresh(component)

        # Update dimension's component_id
        dimension.component_id = component.id
        db.commit()

        return APIResponse(success=True, message="Component created successfully", data=component.to_dict())
    except Exception as e:
        db.rollback()
        return APIResponse(success=False, message=f"Error creating component: {str(e)}", errors=[str(e)])


@router.put("/{component_id}", response_model=APIResponse)
async def update_component(
    component_id: str,
    component_data: ComponentUpdate,
    db: Session = Depends(get_session)
):
    """Update an existing component."""
    component = db.query(Component).filter(Component.component_id == component_id).first()
    if not component:
        raise HTTPException(status_code=404, detail="Component not found")

    try:
        update_data = component_data.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            if value is not None:
                setattr(component, field, value)

        db.commit()
        db.refresh(component)

        return APIResponse(success=True, message="Component updated successfully", data=component.to_dict())
    except Exception as e:
        db.rollback()
        return APIResponse(success=False, message=f"Error updating component: {str(e)}", errors=[str(e)])


@router.delete("/{component_id}", response_model=APIResponse)
async def delete_component(
    component_id: str,
    db: Session = Depends(get_session)
):
    """Delete a component."""
    component = db.query(Component).filter(Component.component_id == component_id).first()
    if not component:
        raise HTTPException(status_code=404, detail="Component not found")

    try:
        db.delete(component)
        db.commit()
        return APIResponse(success=True, message="Component deleted successfully")
    except Exception as e:
        db.rollback()
        return APIResponse(success=False, message=f"Error deleting component: {str(e)}", errors=[str(e)])
