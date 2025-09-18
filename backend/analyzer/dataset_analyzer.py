import io
import json
import re

import google.generativeai as genai
import pandas as pd
from fastapi import HTTPException
from models.schemas import ValidatedAnalysisResult
from utils.helpers import clean_json_keys


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

        Args:
            file: UploadFile object containing the dataset

        Returns:
            ValidatedAnalysisResult: Structured analysis with observations,
            metrics, and suggestions

        Raises:
            HTTPException: For various error conditions during analysis
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
            dataset_string = df.to_csv(index=False)

            # Generate analysis using Gemini AI
            analysis_result = await self._generate_ai_analysis(dataset_string)

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

        Args:
            contents: File contents as bytes
            filename: Name of the file to determine format

        Returns:
            pd.DataFrame: The loaded dataset
        """
        if filename.endswith('.csv'):
            try:
                return pd.read_csv(io.StringIO(contents.decode('utf-8')))
            except UnicodeDecodeError:
                return pd.read_csv(io.StringIO(contents.decode('latin1')))
        elif filename.endswith('.xlsx'):
            return pd.read_excel(io.BytesIO(contents))

    async def _generate_ai_analysis(self, dataset_string: str) -> \
            ValidatedAnalysisResult:
        """
        Generate AI analysis using Gemini model.

        Args:
            dataset_string: CSV string representation of the dataset

        Returns:
            ValidatedAnalysisResult: Validated and structured analysis results
        """
        formatted_prompt = self.analysis_prompt_template.format(
            dataset_content=dataset_string
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

        Args:
            prompt: The formatted analysis prompt

        Returns:
            The response object from Gemini API

        Raises:
            HTTPException: If API call fails
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

        Args:
            response: Raw response from Gemini API

        Returns:
            ValidatedAnalysisResult: Validated analysis results

        Raises:
            HTTPException: If response processing fails
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

        Returns:
            str: The formatted prompt template
        """
        return """
Eres un servicio de IA Gemini altamente especializado en el análisis de \
datasets. Tu objetivo es analizar el dataset suministrado, proporcionar \
métricas, observaciones y sugerencias accionables para ofrecer un panorama \
completo sobre la estructura, patrones, anomalías y sesgos del dataset, \
guiando al usuario en su interpretación y en futuras acciones.

Conceptos a detectar:
1. Características:
    - Estructura:
        - Dimensión del dataset (nº de filas y columnas)
    - Patrón de variables:
        - Correlación Positiva/Negativa
        - Tendencias temporales
        - General (comportamiento general de las variables)
        - Estación (estacionalidad en datos temporales)
        - Clustering (agrupaciones naturales)
        - Asociación (reglas de asociación)
    - Anomalías de datos:
        - Valores atípicos (outliers)
        - Valores faltantes (NaN/null)
        - Inconsistencia
        - Mal formato
        - Duplicados
    - Distribución:
        - Importancia de características

2. Sesgos:
    - Sesgos de datos:
        - Histórico
        - Representación
        - Medida
    - Sesgos de estructura:
        - Asociación
        - Confirmación (complaciente)
    - Sesgos de instrucción:
        - Contexto de Instrucción

3. Tipos de observaciones decision making:
    - Data-Driven
    - Hypothesis-Driven
    - Exploratory-Driven

Restricciones:
- No infieras información de fuentes externas o no proporcionadas en el \
dataset.
- No realices imputación automática de valores faltantes (NaN/null). Solo \
identifícalos y sugiere acciones.
- No elimines automáticamente valores atípicos (outliers). Solo detéctalos y \
señala su impacto potencial.
- No corrijas automáticamente inconsistencias o datos mal formateados. \
Reporta los hallazgos y sugiere correcciones manuales.
- No elimines filas duplicadas automáticamente. Informa sobre su presencia y \
deja la decisión al usuario.
- Al identificar correlaciones, 'correlación no implica causalidad'.
- No intentes 'corregir' sesgos detectados en los datos; en su lugar, ofrece \
estrategias de mitigación para que el usuario las implemente.
- Mantén un tono neutral y objetivo al reportar sobre sesgos, especialmente \
en datos sensibles; evita juicios de valor.
- Todas las sugerencias y observaciones deben estar directamente respaldadas \
por la evidencia encontrada en el dataset analizado y debe entenderse \
facilmente para el usuario.
- Las sugerencias deben ser accionables y específicas, evitando \
recomendaciones vagas o genéricas.
- Reconoce explícitamente la limitación del servicio al no tener conocimiento \
intrínseco del contexto de negocio del usuario.
- La salida debe ser clara, concisa y fácil de entender, priorizando la \
visualización sobre la jerga técnica excesiva.
- No inventes información.
- No des opiniones.
- Arrays vacíos deben ser [].
- No uses saltos de línea innecesarios dentro del JSON.
- Responde SOLO con el JSON, sin texto adicional.
- El análisis debe generar un máximo de 4 'sugerencias'.
- Cada 'sugerencia' debe tener un límite de 100 caracteres.
- Cada 'observacion' debe tener un límite de 100 caracteres.
- No exceder el límite de entrega de 10 observaciones (Priorizar las más \
relevantes del análisis).
- Las 'metricas' deben ser exclusivamente un valor numérico entre 0 y 100.
- No hacer observaciones sobre los nombres de las columnas.
- No hacer observaciones sobre los formatos de datos de las columnas.

Formato de Salida Requerido:
- Las claves principales de la salida JSON deben ser "observaciones", \
"metricas" y "sugerencias".
- El contenido de "observaciones" contiene un límite de 100 caracteres y \
debe plantear el contenido de manera natural, legible y de fácil \
entendimiento para el usuario.
- Las "observaciones" deben describir un porqué de la observación realizada, \
explicando su impacto o implicación. Deben usar los 'Conceptos a detectar' y \
'Sesgos' para categorizar y dar contexto.
- La estructura para cada elemento dentro de "observaciones" debe ser la \
siguiente:
```json
{{
    "tipo_de_reporte": "string",
    "titulo": "string",
    "mensaje": "string"
}}
```
- Las 'metricas' deben ser exclusivamente un valor numérico entre 0 y 100.
- La estructura para cada elemento dentro de "sugerencias" debe ser la \
siguiente:
```json
{{
    "tipo_de_reporte": "string",
    "titulo": "string",
    "mensaje": "string"
}}
```
- Responde SOLO con el JSON, sin texto adicional.
- Las "observaciones" deben describir un porqué de la observación realizada, \
explicando su impacto o implicación. Deben usar los 'Conceptos a detectar' y \
'Sesgos' para categorizar y dar contexto.
- Las "sugerencias" deben describir un porqué de la observación realizada, \
explicando su impacto o implicación. Deben usar los 'Conceptos a detectar' y \
'Sesgos' para categorizar y dar contexto.
- El formato del JSON DEBE ser el siguiente:
```json
{{
    "observaciones": [
        {{"tipo_de_reporte": "observacion", "titulo": "string"}},
        {{"tipo_de_reporte": "observacion", "titulo": "string"}},
        {{"tipo_de_reporte": "observacion", "titulo": "string"}},
        {{"tipo_de_reporte": "observacion", "titulo": "string"}},
        {{"tipo_de_reporte": "observacion", "titulo": "string"}},
        {{"tipo_de_reporte": "observacion", "titulo": "string"}}
        // ... (hasta 10 objetos de observación, priorizando las más \
relevantes y con el porqué/impacto)
    ],
    "metricas": {{
        "porcentaje_valores_faltantes": int, // Ejemplo: 15
        "porcentaje_filas_duplicadas": int, // Ejemplo: 5
        "salud_del_dataset": int // Ejemplo: 75
    }},
    "sugerencias": [
        {{"tipo_de_reporte": "sugerencia", "titulo": "string"}},
        {{"tipo_de_reporte": "sugerencia", "titulo": "string"}},
        {{"tipo_de_reporte": "sugerencia", "titulo": "string"}},
        {{"tipo_de_reporte": "sugerencia", "titulo": "string"}}
        // ... (hasta 4 objetos de sugerencia, accionables y específicas)
    ]
}}
```
Dataset a analizar (en formato CSV):
```csv
{dataset_content}
```
        """
