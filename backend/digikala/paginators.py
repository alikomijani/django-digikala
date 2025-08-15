from rest_framework.pagination import PageNumberPagination
from rest_framework import viewsets


class BasePageNumberPagination(PageNumberPagination):
    page_size = 20  # default items per page
    page_size_query_param = "page_size"
    max_page_size = 50


class BasePaginatedViewSet(viewsets.ModelViewSet):
    """Base ViewSet with Base pagination helper."""

    pagination_class = BasePageNumberPagination

    def paginate_queryset_and_respond(self, queryset, serializer_class):
        page = self.paginate_queryset(queryset)
        serializer = serializer_class(page, many=True)
        return self.get_paginated_response(serializer.data)
