from prometheus_client import Counter, Histogram, Gauge, generate_latest, CONTENT_TYPE_LATEST
from fastapi import Request
import time

# Metrics definitions
REQUEST_COUNT = Counter('api_requests_total', 'Total API requests', ['method', 'endpoint', 'status'])
REQUEST_DURATION = Histogram('api_request_duration_seconds', 'API request duration', ['method', 'endpoint'])
ACTIVE_COMPONENTS = Gauge('active_components_count', 'Number of active components in DB')
SERIALIZATION_TIME = Histogram('serialization_duration_seconds', 'Time taken to serialize data', ['format'])

def measure_request(request: Request, start_time: float, status_code: int):
    duration = time.time() - start_time
    REQUEST_COUNT.labels(method=request.method, endpoint=request.url.path, status=status_code).inc()
    REQUEST_DURATION.labels(method=request.method, endpoint=request.url.path).observe(duration)

def get_metrics():
    return generate_latest()
