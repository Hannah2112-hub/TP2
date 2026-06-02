import time
import json
from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import StreamingResponse
from src.repositories.metrics_repository import MetricsRepository

# Sustainable Web Design (SWD) model constants
# 1 GB = 0.81 kWh. 1 kWh = 442g CO2 (Global grid average roughly)
# According to co2.js SWD model:
# Energy per byte = 0.81 kWh / 10^9 = 0.81e-9 kWh/byte
# Carbon intensity = 442 g/kWh
# gCO2 per byte = (0.81e-9) * 442 = 3.5802e-7 gCO2/byte

CO2_PER_BYTE = 3.5802e-7

class SustainabilityMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        start_time = time.time()
        
        # Call the next middleware/endpoint
        response = await call_next(request)
        
        # Calculate response time
        process_time_ms = (time.time() - start_time) * 1000
        
        # Estimate bytes transfered
        # First try Content-Length header
        content_length = response.headers.get("Content-Length")
        bytes_transferred = 0
        
        if content_length:
            bytes_transferred = int(content_length)
        else:
            # Fallback estimation based on common response types
            # Note: This is an estimation for streaming/chunked responses without Content-Length
            bytes_transferred = 500 # Default estimation if missing
            
        # Calculate CO2
        co2_estimated = bytes_transferred * CO2_PER_BYTE
        
        # Async logging using background execution or simple synchronous insert
        # For simplicity with psycopg2, we'll insert directly (blocking slightly)
        MetricsRepository.insert_metric(
            method=request.method,
            path=request.url.path,
            status_code=response.status_code,
            bytes_transferred=bytes_transferred,
            co2_estimated=co2_estimated,
            response_time_ms=process_time_ms
        )
        
        return response
