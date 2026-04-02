from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .routes import components, loads
from ..models.database import get_database_engine, init_db
from ..utils.config import settings

from fastapi import FastAPI, Request
from fastapi.responses import Response
import time
from .metrics import measure_request, get_metrics



app = FastAPI(
    title="Aircraft Component Data API",
    description="RESTful API for managing aircraft component data models",
    version="1.0.0"
)



#app = FastAPI(...)

@app.middleware("http")
async def metrics_middleware(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    measure_request(request, start_time, response.status_code)
    return response

@app.get("/metrics")
async def metrics():
    return Response(content=get_metrics(), media_type=CONTENT_TYPE_LATEST)



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





