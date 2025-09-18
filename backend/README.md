# 🚀 DataSense-AI Backend Service

Servicio de análisis automático de archivos CSV potenciado por **Gemini (Google Generative AI)**.

---

## 🔐 Requisitos

- Python **3.9+**
- Una cuenta válida de Gemini y clave API

---

## ⚙️ Instalación y Configuración

### 1. Navegar al directorio del backend

```bash
cd backend
```

### 2. Crear un entorno virtual e instalar dependencias

```bash
python -m venv venv
source venv/bin/activate    # En Windows: .\venv\Scripts\activate
pip install -r requirements.txt
```

### 3. Configurar el archivo de entorno

Crear un archivo `.env` en el directorio `backend` y agregar tu clave API de Gemini:

```env
GEMINI_API_KEY=tu_clave_api_aqui
```

### 4. Ejecutar el servidor

```bash
uvicorn service:app --reload
```

### 5. Acceder a la documentación de la API

Una vez que el servidor esté ejecutándose, abrir:

```
http://localhost:8000/docs
```

---

## 📡 Estructura de la API

### Endpoint Principal

**POST** `/analyze_dataset/`

Analiza un dataset CSV usando la IA de Gemini y retorna métricas, observaciones y sugerencias en formato JSON.

**Parámetros:**

- `file`: Archivo CSV del dataset a analizar (form-data)

**Respuesta:**

- Objeto JSON con observaciones, métricas y sugerencias del dataset

---

## 📁 Estructura del Proyecto

```
backend/
├── analyzer/
│   ├── dataset_analyzer.py    # Analizador principal de datasets
│   └── metrics_calculator.py  # Calculadora de métricas
├── api/
│   └── routes.py              # Rutas de la API
├── config/
│   └── settings.py            # Configuración de Gemini API
├── prompts/
│   └── prompt.md              # Prompts para Gemini
├── utils/
│   └── helpers.py             # Funciones auxiliares
├── service.py                 # Aplicación FastAPI principal
└── requirements.txt           # Dependencias Python
```

---

## 🛠️ Tecnologías Utilizadas

- **FastAPI**: Framework web moderno y rápido
- **Uvicorn**: Servidor ASGI de alto rendimiento
- **Pandas**: Manipulación y análisis de datos
- **Google Generative AI**: API de Gemini para análisis con IA
- **Python-dotenv**: Gestión de variables de entorno

---

## ⚠️ Reglas de Análisis Estrictas (aplicadas por Gemini)

- Sin inferencias externas
- Sin limpieza automática de datos
- Sin imputación o eliminación automática de valores atípicos/duplicados
- Máximo **10 observaciones** y **4 sugerencias**
- Enfoque neutral, objetivo y accionable

---

## 🔧 Configuración CORS

El servidor está configurado para permitir solicitudes desde cualquier origen durante el desarrollo. Para producción, se recomienda configurar orígenes específicos.
