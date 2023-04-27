from uuid import UUID
from typing import NoReturn

from django.http import Http404
from django.db.models import QuerySet

from .models import Order


def get_user_order_from_(queryset: QuerySet, pk: UUID) -> Order | NoReturn:
    """Returns an order from the given queryset by the given pk (UUID)."""
    try:
        return queryset.get(pk=pk)
    except Order.DoesNotExist:
        raise Http404
