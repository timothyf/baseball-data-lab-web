from rest_framework.decorators import api_view

from ..models import HallOfFameVote


@api_view(['GET'])
def hall_of_fame_players(request):
    pass  # pragma: no cover - to be implemented in future