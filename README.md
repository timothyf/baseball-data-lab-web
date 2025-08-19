# baseball-data-lab-web

A Django based web interface for exploring data from the `baseball-data-lab` library.

## Development

1. Install Python dependencies:
   ```bash
   pip install -r backend/requirements.txt
   ```
2. Install frontend dependencies:
   ```bash
   cd frontend
   npm install
   cd ..
   ```
3. Run database migrations:
   ```bash
   cd backend
   python manage.py migrate
   cd ..
   ```
4. Start the frontend and backend development servers together:
   ```bash
   foreman start -j Procfile.dev
   ```
5. Visit `http://localhost:8000/` to see the home page displaying information from `baseball-data-lab`.

This project is a minimal scaffold and is intended to grow with additional views and data presentations over time.

## Frontend

Vue components live in the `frontend/` directory and are bundled with Vite into
`backend/static/frontend/main.js` for production. During development you can run:

```bash
npm run dev
```

to start a development server with hot-reloading. When `DEBUG` is enabled,
the Django template pulls scripts from `http://localhost:5173` automatically.
In production, the prebuilt asset is referenced using the `{% static %}` tag.
