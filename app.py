from fastapi import FastAPI
from api.routes import router

app = FastAPI(
    title="LitLens API",
    description="An AI-powered literature review assistant.",
    version="0.1.0",
    docs_url="/docs",              # 👈 explicitly enable Swagger UI
    redoc_url=None,                # optional: disables ReDoc
    openapi_url="/openapi.json"    # 👈 explicitly expose schema
)

# Include your routes
app.include_router(router)