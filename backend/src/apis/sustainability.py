import os
import json
import aiofiles
from fastapi import APIRouter
from fastapi.responses import HTMLResponse, JSONResponse
from src.repositories.metrics_repository import MetricsRepository

router = APIRouter()

@router.get("/environmental-impact", response_class=HTMLResponse, tags=["Sostenibilidad"])
def get_environmental_impact():
    global_metrics = MetricsRepository.get_global_metrics()
    recent_metrics = MetricsRepository.get_recent_metrics(100)
    ranking = MetricsRepository.get_endpoints_ranking()
    
    total_requests = global_metrics.get("total_requests", 0)
    total_co2 = global_metrics.get("total_co2", 0.0)
    avg_co2 = global_metrics.get("avg_co2", 0.0)
    
    most_polluting = ranking[0] if ranking else None
    
    html_content = f"""
    <!DOCTYPE html>
    <html lang="es">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Dashboard de Impacto Ambiental</title>
        <style>
            body {{ font-family: 'Inter', sans-serif; background-color: #1a1a1a; color: #f0f0f0; margin: 0; padding: 20px; }}
            h1, h2 {{ color: #4ade80; }}
            .card-container {{ display: flex; gap: 20px; flex-wrap: wrap; margin-bottom: 30px; }}
            .card {{ background-color: #2d2d2d; border-radius: 8px; padding: 20px; flex: 1; min-width: 200px; box-shadow: 0 4px 6px rgba(0,0,0,0.3); border-left: 4px solid #4ade80; }}
            .card h3 {{ margin-top: 0; font-size: 0.9em; color: #a0a0a0; text-transform: uppercase; }}
            .card p {{ font-size: 1.8em; margin: 0; font-weight: bold; }}
            table {{ width: 100%; border-collapse: collapse; margin-top: 20px; background-color: #2d2d2d; border-radius: 8px; overflow: hidden; }}
            th, td {{ padding: 12px 15px; text-align: left; border-bottom: 1px solid #404040; }}
            th {{ background-color: #3d3d3d; color: #4ade80; font-weight: 600; }}
            tr:hover {{ background-color: #363636; }}
            .table-container {{ overflow-x: auto; max-height: 500px; overflow-y: auto; border-radius: 8px; }}
            .status-200 {{ color: #4ade80; }}
            .status-400 {{ color: #fbbf24; }}
            .status-500 {{ color: #f87171; }}
        </style>
    </head>
    <body>
        <h1>🌱 Monitoreo de Impacto Ambiental (Green Software)</h1>
        
        <div class="card-container">
            <div class="card">
                <h3>Total Solicitudes</h3>
                <p>{total_requests}</p>
            </div>
            <div class="card">
                <h3>CO2 Total Estimado</h3>
                <p>{total_co2:.6f} g</p>
            </div>
            <div class="card">
                <h3>Promedio CO2 / Solicitud</h3>
                <p>{avg_co2:.6f} g</p>
            </div>
            <div class="card">
                <h3>Endpoint Más Contaminante</h3>
                <p style="font-size: 1.2em">{f"{most_polluting['method']} {most_polluting['path']}" if most_polluting else "N/A"}</p>
            </div>
        </div>

        <h2>Registro de Solicitudes (Últimas 100)</h2>
        <div class="table-container">
            <table>
                <thead>
                    <tr>
                        <th>Fecha y Hora</th>
                        <th>Método</th>
                        <th>Ruta</th>
                        <th>Estado HTTP</th>
                        <th>Tiempo (ms)</th>
                        <th>Bytes Transferidos</th>
                        <th>CO2 Estimado (g)</th>
                    </tr>
                </thead>
                <tbody>
    """
    
    for row in recent_metrics:
        if row["status_code"] < 400:
            status_class = "status-200"
        elif row["status_code"] < 500:
            status_class = "status-400"
        else:
            status_class = "status-500"
        html_content += f"""
                    <tr>
                        <td>{row["timestamp"]}</td>
                        <td>{row["method"]}</td>
                        <td>{row["path"]}</td>
                        <td class="{status_class}">{row["status_code"]}</td>
                        <td>{row["response_time_ms"]:.2f}</td>
                        <td>{row["bytes_transferred"]}</td>
                        <td>{row["co2_estimated"]:.8f}</td>
                    </tr>
        """
        
    html_content += """
                </tbody>
            </table>
        </div>
    </body>
    </html>
    """
    
    return HTMLResponse(content=html_content)


@router.get("/api/sustainability", tags=["Sostenibilidad"])
async def get_greenframe_report():
    report_path = os.path.join(os.getcwd(), "backend", "public", "assets", "greenframe-latest.json")
    if not os.path.exists(report_path):
        report_path = os.path.join(os.getcwd(), "public", "assets", "greenframe-latest.json")
        
    if os.path.exists(report_path):
        try:
            async with aiofiles.open(report_path, "r", encoding="utf-8") as f:
                content = await f.read()
            data = json.loads(content)
            return JSONResponse(content=data)
        except Exception as e:
            return JSONResponse(status_code=500, content={"error": f"Error parsing report: {str(e)}"})
    else:
        return JSONResponse(
            status_code=404,
            content={"message": "El análisis de GreenFrame aún no se ha ejecutado. Ejecute 'greenframe analyze' primero."}
        )
