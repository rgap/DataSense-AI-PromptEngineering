import os

import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()


def get_gemini_config():
    """
    Configure and return Gemini API settings.
    """
    try:
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            raise ValueError(
                "La variable de entorno GEMINI_API_KEY no está configurada. "
                "Por favor, configúrala antes de ejecutar el servicio."
            )
        genai.configure(api_key=api_key)
        return api_key
    except Exception as e:
        raise RuntimeError(
            f"Error al configurar la API de Gemini: {e}. "
            "Asegúrate de que GEMINI_API_KEY esté configurada correctamente."
        )
