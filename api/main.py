from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .routes import components, loads
from ..models.database import get_database_engine, init_db
from ..utils.config import settings

app = FastAPI(
    title="Aircraft Component Data API",
    description="RESTful API for managing aircraft component data models",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(components.router, prefix="/api/v1")
app.include_router(loads.router, prefix="/api/v1")

# Database initialization
@app.on_event("startup")
async def startup_event():
    engine = get_database_engine(settings.database_url)
    init_db(engine)
    app.state.engine = engine
    app.state.session = lambda: engine.connect()

@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "aircraft-component-api"}

@app.get("/")
async def root():
    return {
        "message": "Welcome to Aircraft Component Data API",
        "docs": "/docs",
        "health": "/health"
    }
