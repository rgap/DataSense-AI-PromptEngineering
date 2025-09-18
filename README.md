# 📌 DataSense-AI

An intelligent CSV dataset analysis platform powered by **Gemini AI**. The goal is to analyze datasets and provide suggestions, alerts, and observations that help in data-driven decision making.
Designed for teams, companies, or users who work with large volumes of data and need quick insights for decision making.

> **Note**: The backend has been significantly improved through advanced **prompt engineering** techniques to enhance the AI analysis.

---

## 📖 Table of Contents

- [About the Project](#-about-the-project)
- [Features](#-features)
- [Technologies Used](#️-technologies-used)
- [Project Structure](#-project-structure)
- [Quick Start](#-quick-start)
- [Installation](#️-installation)
- [Usage](#️-usage)

---

## 📝 About the Project

> DataSense-AI allows users to upload CSV files and get comprehensive analysis including metrics, observations, and actionable suggestions through an intuitive web interface powered by Google's Gemini AI.

The platform provides:

- **Automated Analysis**: AI-powered insights from your CSV data
- **Visual Dashboard**: Interactive metrics and observations
- **Actionable Suggestions**: Data-driven recommendations
- **Modern UI**: Responsive design with smooth animations

---

## ✨ Features

- ✅ **Smart CSV Analysis** with Gemini AI
- ✅ **Interactive Dashboard** with key metrics
- ✅ **Drag & Drop File Upload** interface
- ✅ **Real-time Processing** with loading states
- ✅ **Responsive Design** for all devices
- ✅ **Type-safe Development** with TypeScript
- ✅ **Modern Tech Stack** (React 19, FastAPI, TailwindCSS)

---

## 🛠️ Technologies Used

### **Frontend**

- **React 19** with TypeScript
- **Vite** for fast development
- **TailwindCSS 4** for styling
- **TanStack Query** for state management
- **Framer Motion** for animations
- **Recharts** for data visualization

### **Backend**

- **FastAPI** for high-performance API
- **Google Generative AI** (Gemini) for analysis
- **Pandas** for data processing
- **Uvicorn** for ASGI server
- **Python 3.9+**

### **Tools & Development**

- **TypeScript** for type safety
- **ESLint** for code quality
- **Git** for version control
- **Zod** for data validation

---

## 📁 Project Structure

```
DataSense-AI-PromptEngineering/
├── frontend/                 # React TypeScript frontend
│   ├── src/
│   │   ├── components/       # Reusable UI components
│   │   ├── views/           # Page components
│   │   ├── api/             # API client
│   │   └── types/           # TypeScript definitions
│   └── README.md            # Frontend documentation
├── backend/                  # FastAPI Python backend
│   ├── analyzer/            # Dataset analysis logic
│   ├── api/                 # API routes
│   ├── config/              # Configuration
│   └── README.md            # Backend documentation
├── _data/                   # Sample data files
└── README.md               # This file
```

---

## 🚀 Quick Start

### Prerequisites

- **Node.js 18+** and npm/yarn
- **Python 3.9+**
- **Gemini API Key** from Google AI Studio

### 1. Clone the repository

```bash
git clone <your-repo-url>
cd DataSense-AI-PromptEngineering
```

### 2. Setup Backend

```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: .\venv\Scripts\activate
pip install -r requirements.txt

# Create .env file
echo "GEMINI_API_KEY=your_api_key_here" > .env

# Start backend server
uvicorn service:app --reload
```

### 3. Setup Frontend

```bash
cd ../frontend
npm install
npm run dev
```

### 4. Access the Application

Open your browser and navigate to:

```
http://localhost:5173
```

The backend API will be running on:

```
http://localhost:8000
```

---

## ⚙️ Installation

For detailed installation instructions, please refer to the individual README files:

- **Backend Setup**: See [`backend/README.md`](./backend/README.md)
- **Frontend Setup**: See [`frontend/README.md`](./frontend/README.md)

---

## ▶️ Usage

1. **Start the backend server** (in `backend/` directory):

   ```bash
   uvicorn service:app --reload
   ```

2. **Start the frontend development server** (in `frontend/` directory):

   ```bash
   npm run dev
   ```

3. **Upload your CSV file** through the web interface at `http://localhost:5173`

4. **View the analysis results** including:
   - Dataset health metrics
   - Missing values analysis
   - Data quality observations
   - Actionable improvement suggestions

---

## 📊 API Documentation

Once the backend is running, you can access the interactive API documentation at:

```
http://localhost:8000/docs
```
