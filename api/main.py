import asyncio
from contextlib import asynccontextmanager
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware

from api.auth import router as auth_router
from api.routers import executive, machine, production, quality, inventory, tool, maintenance, sensors, reports
from api.ws_manager import manager, check_alerts_background


@asynccontextmanager
async def lifespan(app: FastAPI):
    task = asyncio.create_task(check_alerts_background())
    yield
    task.cancel()
    try:
        await task
    except asyncio.CancelledError:
        pass


app = FastAPI(
    title="AMIP - AMM Manufacturing Intelligence Platform",
    description="API de support a la decision pour atelier CNC",
    version="1.1.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router, prefix="/api/auth", tags=["Authentication"])
app.include_router(executive.router, prefix="/api/executive", tags=["Vue Executive"])
app.include_router(machine.router, prefix="/api/machine", tags=["Machine"])
app.include_router(production.router, prefix="/api/production", tags=["Ordre Fabrication"])
app.include_router(quality.router, prefix="/api/quality", tags=["Qualite"])
app.include_router(inventory.router, prefix="/api/inventory", tags=["Inventaire"])
app.include_router(tool.router, prefix="/api/tool", tags=["Outil"])
app.include_router(maintenance.router, prefix="/api/maintenance", tags=["Maintenance"])
app.include_router(sensors.router, prefix="/api/sensors", tags=["Capteurs"])
app.include_router(reports.router, tags=["Export Rapports"])


@app.websocket("/ws/notifications")
async def websocket_endpoint(ws: WebSocket):
    await manager.connect(ws)
    try:
        while True:
            await ws.receive_text()
    except WebSocketDisconnect:
        manager.disconnect(ws)


@app.get("/")
def root():
    return {
        "name": "AMIP API",
        "version": "1.0.0",
        "description": "AMM Manufacturing Intelligence Platform",
        "modules": [
            "/api/executive",
            "/api/machine",
            "/api/production",
            "/api/quality",
            "/api/inventory",
            "/api/tool",
            "/api/maintenance",
            "/api/sensors",
        ],
    }


@app.get("/health")
def health():
    from api.database import fetch_one
    try:
        result = fetch_one("SELECT 1 AS ok")
        return {"status": "healthy", "database": "connected" if result else "error"}
    except Exception as e:
        return {"status": "unhealthy", "database": str(e)}
