from api.routes import router
from config.settings import get_gemini_config
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Configure Gemini API
get_gemini_config()

# Initialize FastAPI application
app = FastAPI(
    title="API de Análisis de CSV con Gemini",
    description="Servicio de IA para análisis de archivos CSV, proporcionando "
                "métricas, observaciones y sugerencias accionables.",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

# Include API routes
app.include_router(router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("service", host="0.0.0.0", port=8000, reload=True)
