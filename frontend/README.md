# 🎨 DataSense-AI Frontend

Modern and responsive user interface for CSV file analysis, built with **React**, **TypeScript**, and **TailwindCSS**.

---

## 🔐 Requirements

- Node.js **18+**
- npm or yarn
- DataSense-AI backend running on port 8000

---

## ⚙️ Installation & Setup

### 1. Navigate to the frontend directory

```bash
cd frontend
```

### 2. Install dependencies

```bash
npm install
# or
yarn install
```

### 3. Configure environment variables (optional)

Create a `.env` file in the `frontend` directory to customize the backend URL:

```env
VITE_API_BASE_URL=http://localhost:8000
```

### 4. Run the development server

```bash
npm run dev
# or
yarn dev
```

### 5. Access the application

Once the server is running, open:

```
http://localhost:5173
```

---

## 🚀 Available Scripts

- `npm run dev` - Runs the development server
- `npm run build` - Builds the application for production
- `npm run preview` - Previews the production build
- `npm run lint` - Runs ESLint to check the code

---

## 📁 Project Structure

```
frontend/
├── public/
│   └── img/
│       ├── iconos/          # SVG and PNG icons
│       └── logo.svg         # Application logo
├── src/
│   ├── api/
│   │   └── datasetAnalysisApi.ts    # API client for backend
│   ├── components/
│   │   ├── Metrics/              # Metrics components
│   │   │   ├── AnalysisHeader.tsx
│   │   │   ├── MetricsCard.tsx
│   │   │   ├── ObservationsCarousel.tsx
│   │   │   └── SuggestionsCard.tsx
│   │   ├── Characteristics.tsx   # Characteristics component
│   │   ├── SidebarDrc.tsx       # Right sidebar
│   │   ├── SidebarIzq.tsx       # Left sidebar
│   │   └── Title.tsx            # Title component
│   ├── layouts/
│   │   └── AppLayout.tsx        # Main application layout
│   ├── types/
│   │   └── index.ts             # TypeScript type definitions
│   ├── utils/
│   │   └── index.ts             # Helper functions
│   ├── views/
│   │   ├── DashboardView.tsx    # Analysis results view
│   │   ├── HomeView.tsx         # Main view/file upload
│   │   └── LoadingView.tsx      # Loading view during analysis
│   ├── main.tsx                 # Application entry point
│   ├── router.tsx               # Route configuration
│   └── index.css                # Global styles
├── package.json
├── vite.config.ts               # Vite configuration
└── tsconfig.json                # TypeScript configuration
```

---

## 🛠️ Technologies Used

### **Core**

- **React 19**: User interface library
- **TypeScript**: Static typing for JavaScript
- **Vite**: Fast build tool

### **Routing & State Management**

- **React Router DOM**: Client-side routing
- **TanStack Query**: Server state management and caching
- **Zustand**: Lightweight global state management

### **UI & Styling**

- **TailwindCSS 4**: Utility-first CSS framework
- **Headless UI**: Unstyled accessible components
- **Heroicons**: SVG icons
- **Framer Motion**: Smooth animations
- **React Icons**: Icon library

### **Data & Validation**

- **Zod**: Schema validation and parsing
- **Recharts**: React charting library

### **UX Enhancements**

- **React Dropzone**: File upload with drag & drop
- **React Toastify**: Toast notifications
- **React Intersection Observer**: Intersection observer for animations

---

## 🌐 Application Routes

- **`/`** - Main view (CSV file upload)
- **`/analizando`** - Loading view during analysis
- **`/resultados`** - Dashboard with analysis results

---

## 📊 Main Features

### 🔄 **File Upload**

- Intuitive drag & drop interface
- CSV format validation
- File preview before analysis

### 📈 **Results Dashboard**

- Key dataset metrics
- Observations categorized by type
- Actionable suggestions
- Interactive visualizations

### 🎯 **User Experience**

- Responsive design for all devices
- Smooth animations and transitions
- Informative loading states
- Elegant error handling

---

## 🔌 Backend Integration

The application communicates with the backend through:

- **Endpoint**: `POST /analyze_dataset/`
- **Format**: Multipart/form-data
- **Response**: JSON with metrics, observations, and suggestions

---

## 🎨 Style Customization

The project uses TailwindCSS 4 with custom configuration. Styles can be modified in:

- `src/index.css` - Global styles and CSS variables
- `tailwind.config.js` - TailwindCSS configuration (if required)

---

## 🚀 Deployment

### For Vercel (recommended)

```bash
npm run build
# Upload the dist/ folder to Vercel
```

### For other providers

```bash
npm run build
# Serve the dist/ folder with any static server
```

---

## 🔧 Development Configuration

### Environment Variables

- `VITE_API_BASE_URL`: Backend base URL (default: `http://localhost:8000`)

### Import Aliases

The project is configured with `@/` alias pointing to `src/` for cleaner imports:

```typescript
import { Component } from "@/components/Component";
```
