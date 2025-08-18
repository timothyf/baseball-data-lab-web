# baseball-data-lab-web

A Django based web interface for exploring data from the `baseball-data-lab` library.

## Development

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
2. Run database migrations and start the development server:
   ```bash
   python manage.py migrate
   python manage.py runserver
   ```
3. Visit `http://localhost:8000/` to see the home page displaying information from `baseball-data-lab`.

This project is a minimal scaffold and is intended to grow with additional views and data presentations over time.
