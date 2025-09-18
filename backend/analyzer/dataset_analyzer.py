import io
import json
import re

import google.generativeai as genai
import pandas as pd
from fastapi import HTTPException
from models.schemas import ValidatedAnalysisResult
from utils.helpers import clean_json_keys

from .metrics_calculator import MetricsCalculator


class DatasetAnalyzer:
    """
    Dataset analyzer that uses Google's Gemini AI to analyze CSV and Excel
    files.
    """

    def __init__(self):
        self.model = genai.GenerativeModel('gemini-2.0-flash')
        self.analysis_prompt_template = self._get_analysis_prompt_template()

    async def analyze_file(self, file) -> ValidatedAnalysisResult:
        """
        Analyze a dataset file and return structured analysis results.
        """
        # Validate file type
        if not file.filename.endswith(('.csv', '.xlsx')):
            raise HTTPException(
                status_code=400,
                detail="Tipo de archivo no soportado. Por favor, sube un "
                       "archivo .csv o .xlsx"
            )

        try:
            # Read file content
            contents = await file.read()
            df = self._read_dataframe(contents, file.filename)

            # Calculate metrics locally instead of sending raw data
            metrics_calculator = MetricsCalculator(df)
            computed_metrics = metrics_calculator.calculate_all_metrics()

            # Generate analysis using Gemini AI with computed metrics
            analysis_result = await self._generate_ai_analysis(
                computed_metrics
            )

            return analysis_result

        except pd.errors.EmptyDataError:
            raise HTTPException(
                status_code=400,
                detail="El archivo está vacío o no contiene datos."
            )
        except Exception as e:
            print(f"ERROR: Error inesperado en analyze_file: {e}")
            print(f"ERROR: Tipo de excepción: {type(e)}")
            print(f"ERROR: Representación completa: {repr(e)}")
            raise HTTPException(
                status_code=500,
                detail=f"Error interno del servidor: {e}"
            )

    def _read_dataframe(self, contents: bytes, filename: str) -> pd.DataFrame:
        """
        Read file contents into a pandas DataFrame.
        """
        if filename.endswith('.csv'):
            try:
                return pd.read_csv(io.StringIO(contents.decode('utf-8')))
            except UnicodeDecodeError:
                return pd.read_csv(io.StringIO(contents.decode('latin1')))
        elif filename.endswith('.xlsx'):
            return pd.read_excel(io.BytesIO(contents))

    async def _generate_ai_analysis(self, computed_metrics: dict) -> \
            ValidatedAnalysisResult:
        """
        Generate AI analysis using Gemini model with computed metrics.
        """
        metrics_json = json.dumps(
            computed_metrics, ensure_ascii=False, indent=2
        )
        formatted_prompt = self.analysis_prompt_template.format(
            metrics_data=metrics_json
        )

        # Debug logging
        print(f"DEBUG: Prompt formateado (primeros 500 caracteres): "
              f"{formatted_prompt[:500]}...")
        print(f"DEBUG: Longitud total del prompt: {len(formatted_prompt)} "
              "caracteres.")

        # Call Gemini API
        response = await self._call_gemini_api(formatted_prompt)

        # Process and validate response
        return self._process_gemini_response(response)

    async def _call_gemini_api(self, prompt: str):
        """
        Call Gemini API with the formatted prompt.
        """
        try:
            print("DEBUG: Intentando llamar a model.generate_content()...")
            response = self.model.generate_content(
                prompt,
                generation_config=genai.types.GenerationConfig(
                    response_mime_type="application/json"
                )
            )
            print(f"DEBUG: Llamada completada. Objeto de respuesta: "
                  f"{response}")

            if not hasattr(response, 'text') or not response.text:
                print(f"ADVERTENCIA: Respuesta sin texto. Objeto completo: "
                      f"{response}")
                if (response.candidates and
                        response.candidates[0].finish_reason):
                    reason = response.candidates[0].finish_reason
                    raise ValueError(f"Gemini API no retornó texto. "
                                     f"Razón: {reason}")
                else:
                    raise ValueError(f"Gemini API no retornó texto. "
                                     f"Objeto: {response}")

            return response

        except Exception as e:
            print(f"ERROR: Fallo en la llamada a Gemini API: {e}")
            print(f"ERROR: Tipo de excepción: {type(e)}")
            print(f"ERROR: Representación completa: {repr(e)}")
            raise HTTPException(
                status_code=500,
                detail=f"Error en la comunicación con Gemini API: {e}"
            )

    def _process_gemini_response(self, response) -> ValidatedAnalysisResult:
        """
        Process and validate Gemini API response.
        """
        try:
            raw_gemini_response = response.text
            print(f"DEBUG: Respuesta cruda de Gemini: "
                  f"{raw_gemini_response[:1000]}")

            # Extract JSON from response
            json_match = re.search(r'\{.*\}', raw_gemini_response,
                                   re.DOTALL | re.MULTILINE)

            if not json_match:
                print(f"ERROR: No JSON encontrado. Respuesta completa: "
                      f"{raw_gemini_response}")
                raise ValueError("No se encontró un bloque JSON válido en la "
                                 "respuesta de Gemini.")

            json_str = json_match.group(0)
            parsed_json = json.loads(json_str)
            cleaned_json = clean_json_keys(parsed_json)

            print("DEBUG: JSON limpio final:")
            print(json.dumps(cleaned_json, indent=2, ensure_ascii=False))

            # Validate with Pydantic
            try:
                validated = ValidatedAnalysisResult(**cleaned_json)
                return validated
            except Exception as validation_error:
                print(f"ERROR: Validación fallida: {validation_error}")
                raise HTTPException(
                    status_code=500,
                    detail="El JSON recibido no cumple con la estructura "
                           "esperada."
                )

        except (json.JSONDecodeError, ValueError) as e:
            print(f"ERROR: Fallo al procesar JSON: {e}")
            print(f"ERROR: Tipo de excepción: {type(e)}")
            print(f"ERROR: Respuesta cruda: {response.text}")
            raise HTTPException(
                status_code=500,
                detail=f"Error al procesar la respuesta de Gemini: {e}. "
                f"Respuesta recibida: {response.text[:500]}..."
            )

    def _get_analysis_prompt_template(self) -> str:
        """
        Get the analysis prompt template for Gemini AI.
        """
        return """
Eres un analista de datos experto que debe producir un reporte ejecutivo \
claro basado en métricas pre-calculadas de un dataset.

Tu objetivo es analizar las métricas proporcionadas y generar observaciones \
y sugerencias accionables sobre la calidad, estructura y patrones del dataset.

INSTRUCCIONES:
- Usa ÚNICAMENTE las métricas proporcionadas, no inventes datos
- Identifica problemas de calidad de datos basándote en las métricas
- Detecta patrones relevantes (correlaciones, outliers, distribuciones)
- Proporciona sugerencias accionables y específicas
- Mantén un tono neutral y objetivo
- No hagas suposiciones sobre el contexto de negocio

CONCEPTOS A DETECTAR:
1. Calidad de datos: valores faltantes, duplicados, outliers
2. Estructura: dimensiones, tipos de variables
3. Patrones: correlaciones fuertes, distribuciones anómalas
4. Problemas: inconsistencias, columnas problemáticas

RESTRICCIONES:
- Responde SOLO con JSON válido, sin texto adicional
- Máximo 10 observaciones (prioriza las más importantes)
- Máximo 4 sugerencias accionables
- Cada observación/sugerencia: máximo 100 caracteres
- Las métricas deben ser números enteros entre 0 y 100

FORMATO DE SALIDA REQUERIDO:
```json
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
MÉTRICAS DEL DATASET:
{metrics_data}
"""
