from fastapi import FastAPI

from backend.api.endpoints.components import router as components_router

app = FastAPI(title="Component Prices API")
app.include_router(components_router)
