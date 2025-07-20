from fastapi import FastAPI
from routes import router as api_router

app = FastAPI(
    title="E-commerce API",
    description="A sample backend application for an e-commerce platform.",
    version="1.0.0"
)

# Include the API router from routes.py
app.include_router(api_router)

@app.get("/", tags=["Root"])
def read_root():
    """A simple health check endpoint."""
    return {"message": "Welcome to the E-commerce API!"}