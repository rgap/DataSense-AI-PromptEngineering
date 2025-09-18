# 🚀 DataSense-AI Service

Automatic dataset analysis service powered by **Gemini (Google Generative AI)**.

---

## 🔐 Requirements

- Python **3.9+**
- A valid Gemini account and API Key

---

## ⚙️ Installation & Setup

### 1. Clone the repository

```bash
git clone https://github.com/DataSense-AI/DataSense-AI.git
cd DataSense-AI/ai_service/ai_service
```

### 2. Create a virtual environment and install dependencies

```bash
python -m venv venv
source venv/bin/activate    # On Windows: .\venv\Scripts\activate
pip install -r requirements.txt
```

### 3. Configure your environment file

Create a `.env` file and add your Gemini API key:

```env
GEMINI_API_KEY=your_api_key_here
```

### 4. Run the server

```bash
uvicorn service:app --reload
```

### 5. Access API docs

Once the server is running, open:

```
http://localhost:8000/docs
```

---

## 📡 Main Endpoint

**POST** `/analyze_dataset/`

### Example Response

```json
{
  "observations": [
    {
      "report_type": "observation",
      "title": "Skewed Distribution",
      "message": "Variable X contains extreme values that affect the overall mean."
    }
    // Up to 10 observations
  ],
  "metrics": {
    "missing_values_percentage": 12,
    "duplicate_rows_percentage": 3,
    "dataset_health": 82
  },
  "suggestions": [
    {
      "report_type": "suggestion",
      "title": "Remove duplicates to avoid distortions."
    }
    // Up to 4 suggestions
  ]
}
```

---

## ⚠️ Strict Analysis Rules (enforced by Gemini)

- No external inferences.
- No automatic data cleaning.
- No imputation or automatic removal of outliers/duplicates.
- Maximum **10 observations** and **4 suggestions**.
- Neutral, objective, and actionable focus.
