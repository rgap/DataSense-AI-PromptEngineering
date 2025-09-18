import io
import json
import re

import google.generativeai as genai
import pandas as pd
from fastapi import HTTPException
from utils.helpers import clean_json_keys

from .metrics_calculator import MetricsCalculator


class DatasetAnalyzer:
    """Simple dataset analyzer using Gemini AI with pre-computed metrics."""

    def __init__(self):
        self.model = genai.GenerativeModel("gemini-2.0-flash")

    async def analyze_file(self, file):
        """
        Analyze a dataset file and return structured analysis results.
        """
        # Validate file type
        if not file.filename.endswith(".csv"):
            raise HTTPException(
                status_code=400,
                detail="Tipo de archivo no soportado. Sube un archivo .csv",
            )

        try:
            # Read and process file
            contents = await file.read()
            df = self._read_file(contents, file.filename)

            # Calculate metrics locally
            metrics = MetricsCalculator(df).calculate_all_metrics()

            # Get AI analysis
            return await self._get_ai_analysis(metrics)

        except pd.errors.EmptyDataError:
            raise HTTPException(
                status_code=400, detail="El archivo está vacío o no contiene datos."
            )
        except Exception as e:
            print(f"ERROR: {e}")
            raise HTTPException(
                status_code=500, detail=f"Error interno del servidor: {e}"
            )

    def _read_file(self, contents, filename):
        """Read CSV file contents into DataFrame."""
        try:
            return pd.read_csv(io.StringIO(contents.decode("utf-8")))
        except UnicodeDecodeError:
            return pd.read_csv(io.StringIO(contents.decode("latin1")))

    async def _get_ai_analysis(self, metrics):
        """Get AI analysis from computed metrics."""
        # Create prompt
        prompt = self._create_prompt(metrics)

        # Call Gemini API
        response = self.model.generate_content(
            prompt,
            generation_config=genai.types.GenerationConfig(
                response_mime_type="application/json"
            ),
        )

        # Process response
        if not response.text:
            raise HTTPException(
                status_code=500, detail="No se recibió respuesta de Gemini"
            )

        return self._parse_response(response.text)

    def _create_prompt(self, metrics):
        """Create analysis prompt with structured framework tags."""
        metrics_json = json.dumps(metrics, ensure_ascii=False, indent=2)

        return f"""
# Context
You are analyzing a CSV dataset. The user has uploaded a CSV file and needs insights about data quality, patterns, and actionable recommendations.

# Role
You are an expert data analyst specializing in data quality assessment and providing actionable business insights.

# Instructions
- Analyze the provided metrics from the CSV dataset
- Generate between 5-8 specific observations about data quality issues
- Provide 3-4 actionable suggestions for improvement
- Focus on the most critical findings that impact data reliability
- Keep titles under 50 characters and messages under 100 characters
- Base your analysis only on the provided metrics

# Structure
Return your analysis as a JSON object with exactly this structure:
{{
    "observaciones": [
        {{
            "tipo_de_reporte": "observacion",
            "titulo": "Brief title (max 50 chars)",
            "mensaje": "Clear explanation (max 100 chars)"
        }}
    ],
    "metricas": {{
        "porcentaje_valores_faltantes": integer_0_to_100,
        "porcentaje_filas_duplicadas": integer_0_to_100,
        "salud_del_dataset": integer_0_to_100
    }},
    "sugerencias": [
        {{
            "tipo_de_reporte": "sugerencia",
            "titulo": "Action title (max 50 chars)",
            "mensaje": "Specific recommendation (max 100 chars)"
        }}
    ]
}}

# Parameters
Dataset metrics to analyze:
{metrics_json}
"""

    def _parse_response(self, response_text):
        """Parse and validate AI response."""
        try:
            # Extract JSON
            json_match = re.search(r"\{.*\}", response_text, re.DOTALL)
            if not json_match:
                raise ValueError("No se encontró JSON en la respuesta")

            # Parse and clean JSON
            parsed_json = json.loads(json_match.group(0))
            cleaned_json = clean_json_keys(parsed_json)

            # Return cleaned JSON
            return cleaned_json

        except (json.JSONDecodeError, ValueError) as e:
            raise HTTPException(
                status_code=500, detail=f"Error procesando respuesta: {e}"
            )
        except Exception:
            raise HTTPException(
                status_code=500, detail="La respuesta no cumple con el formato esperado"
            )
