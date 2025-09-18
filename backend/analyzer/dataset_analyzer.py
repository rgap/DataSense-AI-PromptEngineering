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
<role>
Eres un analista de datos experto especializado en evaluación de calidad de datos CSV.
</role>

<task>
Analiza los datos CSV y encuentra problemas. Da observaciones y sugerencias.
</task>

<context>
Tienes métricas de un archivo CSV:
- Datos básicos
- Números
- Categorías
- Correlaciones
- Problemas encontrados
</context>

<instructions>
- Analiza las métricas proporcionadas
- Encuentra problemas de datos
- Da sugerencias útiles
- Títulos cortos
- Mensajes claros
- Enfócate en lo importante
</instructions>

<output_format>
Responde solo con JSON:
{{
    "observaciones": [
        {{
            "tipo_de_reporte": "observacion",
            "titulo": "string (máx 50 caracteres)",
            "mensaje": "string (máx 100 caracteres)"
        }}
    ],
    "metricas": {{
        "porcentaje_valores_faltantes": int,
        "porcentaje_filas_duplicadas": int,
        "salud_del_dataset": int
    }},
    "sugerencias": [
        {{
            "tipo_de_reporte": "sugerencia",
            "titulo": "string (máx 50 caracteres)",
            "mensaje": "string (máx 100 caracteres)"
        }}
    ]
}}
</output_format>

<constraints>
- Genera entre 5 y 8 observaciones
- Genera 3 o 4 sugerencias
- Métricas: números 0-100
</constraints>

<data>
{metrics_json}
</data>
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
