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

## Frontend

Vue.js is available for building interactive components. The home page shows a
minimal example component mounted from `stats/static/stats/app.js` and loaded
from the Vue CDN. Additional Vue components can be created in that directory
and referenced from Django templates using the `{% static %}` tag.
