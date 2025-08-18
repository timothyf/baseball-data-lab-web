from django.shortcuts import render

try:
    import baseball_data_lab as bdl
    _bdl_error = None
except Exception as exc:  # pragma: no cover - handles missing dependency
    bdl = None
    _bdl_error = str(exc)

def home(request):
    """Simple view that demonstrates integration with baseball-data-lab."""
    message = "baseball-data-lab library is not installed."
    data = None
    if bdl is not None:
        message = f"Using baseball-data-lab version {getattr(bdl, '__version__', 'unknown')}"
        try:
            sample = getattr(bdl, 'get_sample_data', lambda: [])()
            data = sample
        except Exception as exc:  # pragma: no cover - defensive
            data = [f"Error fetching data: {exc}"]
    elif _bdl_error:
        message = f"baseball-data-lab import error: {_bdl_error}"
    return render(request, 'stats/home.html', {'message': message, 'data': data})
