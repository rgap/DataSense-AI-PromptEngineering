# 📌 DataSense-AI

Es una plataforma de análisis de datasets en formato csv ( en un principio ). Su objetivo es analizar y dar sugerencias, alertas y observaciones que ayuden en la toma de decisiones en base al proposito del dataset.
Está pensado para equipos, empresas, o usuarios que cuenten con grandes volumenes de datos y quieren una respuesta pronta para la toma de decisiones.

[Figma](https://www.figma.com/design/GJgPDmHTE44pZ5B41Xgffe/DataSense-AI---No-Country?node-id=2-432&t=mhd70IRg6kSjXHL0-1)

---

## 📖 Índice
- [Acerca del proyecto](#-acerca-del-proyecto)
- [Características](#-características)
- [Tecnologías utilizadas](#-tecnologías-utilizadas)
- [Instalación](#-instalación)
- [Uso](#-uso)
- [Estructura del proyecto](#-estructura-del-proyecto)
- [Contribuciones](#-contribuciones)
- [Licencia](#-licencia)
- [Equipo](#-equipo)

---

## 📝 Acerca del proyecto

> Este proyecto permite a los usuarios cargar un archivo CSV y obtener un análisis visual de los datos mediante gráficos interactivos.

---

## ✨ Características
- ✅ Análisis de archivo CSV  
- ✅ Soporte para [React - Gemini API - TypeScript]  
- ✅ Fácil de instalar y usar  

---

## 🛠️ Tecnologías utilizadas
- **Lenguajes:** TypeScript, Python.
- **Frameworks/Librerías:** React, Zod, React Router, React Query DOM, TailwindCSS, FastAPI, Pydantic, google.generativeai, pandas, uvicorn.
- **Herramientas:** Git, Figma.

---

## ⚙️ Instalación

1. Clonar el repositorio:
   ```bash
   git clone https://github.com/DataSense-AI/DataSense-AI.git
   ```

2. Entrar al directorio del proyecto:

   ```bash
   cd DataSense-AI
   ```
   
3. Entrar al directorio de la API y seguir los pasos del README.md:

   ```bash
   cd ai_service
   ```

4. Entrar al directorio del frontend y seguir los pasos del README.md:

   ```bash
   cd frontend
   ```

## ▶️ Uso

```bash
npm run dev
```

Abrir otra terminal para el uso de la API:

```bash
uvicorn service:app --reload 
```

Luego abrir en el navegador:

```bash
http://localhost:5173
```

## 📂 Estructura del proyecto

```bash
DataSense-AI/
│── ai_service/             # Código fuente del servicio de la API
│   ├── service.py  # Python services
│   ├── venv/      # Entorno Virtual
│   ├── .env       # Configuaciones de entorno
│── frontend/            # Código fuente del frontend
│   ├── src/  # Directorio con código fuente
│       ├── api/  # Endpoints hacía la api
│       ├── components/  # Componentes utilizados
│       ├── layouts/  # Layouts base utilizados
│       ├── utils/  # Funciones Utilizadas
│       ├── types/  # Tipos de los objetos utilizados
│       ├── views/  # Vistas utilizados
│       ├── index.css  # Estilos utilizados
│       ├── main.tsx  # Archivo main base
│       ├── router.tsx  # Rutas utilizadas
│   ├── public/  # Directorio con cosas utilizadas en el desarrollo
│       ├── iconos/  # Iconos utilizados
│           ├── png/  # Iconos en formato png
│           ├── svg/  # Iconos en formato svg
│── clientes_data.csv        # Archivo de prueba 1
│── Restaurant reviews.csv        # Archivo de prueba 2
│── README.md        # Documentación
```

## 🤝 Contribuciones
¡Las contribuciones son bienvenidas!
Si quieres colaborar:

1. Haz un fork del proyecto

2. Crea una nueva rama (git checkout -b feature/nueva-funcionalidad)

3. Haz commit de tus cambios (git commit -m 'Agrega nueva funcionalidad')

4. Haz push a la rama (git push origin feature/nueva-funcionalidad)

5. Crea un Pull Request

## 📜 Licencia
Este proyecto está bajo la licencia MIT.
Consulta el archivo LICENSE para más información.

## 📬 Equipo

- Matias Ron Ares 💼 [LinkedIn](https://www.linkedin.com/in/mat%C3%ADas-ron-ares-a4b09819a?utm_source=share&utm_campaign=share_via&utm_content=profile&utm_medium=android_app)
- Salvador Martínez 💼 [LinkedIn](https://www.linkedin.com/in/salvador-mart%C3%ADnez-2bb28135a/)
- Kevin Agustin Ruiz 💼 [LinkedIn](https://www.linkedin.com/in/kevinagustin/)
- Rel Guzman 💼 [LinkedIn](https://www.linkedin.com/in/relguzman/)
- Natalia Silva 💼 [LinkedIn](https://www.linkedin.com/in/natalia-silva-b1577527a?utm_source=share&utm_campaign=share_via&utm_content=profile&utm_medium=android_app)
