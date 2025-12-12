# Secret Santa Frontend (Vite + React + Tailwind)

## Quick start

1. Install Node.js (v18+ recommended).
2. In the project directory run:
   ```bash
   npm install
   npm run dev
   ```
3. Open the app at the address shown by Vite (usually http://localhost:5173)

The frontend expects a FastAPI backend with endpoints:
- `GET /health`
- `POST /assign` (JSON)
- `POST /assign/csv` (multipart/form-data)
