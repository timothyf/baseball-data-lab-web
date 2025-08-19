import os

def vite_dev_mode(request):
    return {
        "DJANGO_USE_VITE_DEV": os.environ.get("DJANGO_USE_VITE_DEV") == "1"
    }
