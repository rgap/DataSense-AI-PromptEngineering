from analyzer.dataset_analyzer import DatasetAnalyzer
from fastapi import APIRouter, File, UploadFile

router = APIRouter()


@router.post("/analyze_dataset/")
async def analyze_dataset(file=File(...)):
    """
    Analiza un dataset CSV usando la IA de Gemini.
    Retorna métricas, observaciones y sugerencias en formato JSON.

    Args:
        file: El archivo CSV del dataset a analizar.

    Returns:
        dict: Un objeto JSON con observaciones, métricas y sugerencias.
    """
    analyzer = DatasetAnalyzer()
    return await analyzer.analyze_file(file)
