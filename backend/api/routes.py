from analyzer.dataset_analyzer import DatasetAnalyzer
from fastapi import APIRouter, File, UploadFile
from models.schemas import ValidatedAnalysisResult

router = APIRouter()


@router.post("/analyze_dataset/", response_model=ValidatedAnalysisResult)
async def analyze_dataset(file: UploadFile = File(...)):
    """
    Analiza un dataset CSV o Excel usando la IA de Gemini.
    Retorna métricas, observaciones y sugerencias en formato JSON.

    Args:
        file (UploadFile): El archivo del dataset (CSV) a analizar.

    Returns:
        AnalysisResult: Un objeto JSON con observaciones, métricas y
        sugerencias.

    Raises:
        HTTPException: Si el tipo de archivo no es soportado, el archivo
        está vacío, o si ocurre un error durante el procesamiento o la
        comunicación con Gemini.
    """
    analyzer = DatasetAnalyzer()
    return await analyzer.analyze_file(file)
