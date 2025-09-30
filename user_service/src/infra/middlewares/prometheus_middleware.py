from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
from prometheus_client import Counter, Histogram
import time

REQUEST_COUNT = Counter(
    "app_requests_total",
    "Total number of HTTP requests",
    ["method", "endpoint", "http_status"]
)

REQUEST_LATENCY = Histogram(
    "app_request_latency_seconds",
    "Latency of HTTP requests in seconds",
    ["endpoint"],
)

ERROR_COUNT = Counter(
    "app_errors_total",
    "Total number of server errors (5xx)",
    ["endpoint"],
)

class PrometheusMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        start_time = time.time()
        response = await call_next(request)
        latency = time.time() - start_time

        endpoint = request.url.path
        method = request.method
        status_code = str(response.status_code)

        REQUEST_COUNT.labels(method=method, endpoint=endpoint, http_status=status_code).inc()
        REQUEST_LATENCY.labels(endpoint=endpoint).observe(latency)

        if status_code.startswith("5"):
            ERROR_COUNT.labels(endpoint=endpoint).inc()        

        return response