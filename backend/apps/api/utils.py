"""Utility helpers for API views."""

import logging
from functools import wraps
from django.http import JsonResponse

logger = logging.getLogger(__name__)


def require_unified_client(view_func):
    """Ensure ``UnifiedDataClient`` is available and provide an instance.

    The decorated view must accept a ``client`` positional argument which will
    be an instance of ``UnifiedDataClient``. If the client library is missing or
    the client fails to instantiate, a standardized JSON error response is
    returned.
    """

    @wraps(view_func)
    def _wrapped(request, *args, **kwargs):
        from . import views as api_views  # Local import to avoid circular deps

        client_cls = getattr(api_views, "UnifiedDataClient", None)
        if client_cls is None:
            return JsonResponse(
                {"error": "baseball-data-lab library is not installed"}, status=500
            )
        try:
            client = client_cls()
        except Exception as exc:  # pragma: no cover - defensive
            logger.error("Failed to instantiate UnifiedDataClient: %s", exc)
            return JsonResponse({"error": str(exc)}, status=500)
        return view_func(request, client, *args, **kwargs)

    return _wrapped

