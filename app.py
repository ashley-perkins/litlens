from fastapi import FastAPI
from api.routes import router

app = FastAPI(
    title="LitLens API",
    description="An AI-powered literature review assistant.",
    version="0.1.0"
)

# Include your routes
app.include_router(router)
