from rest_framework.pagination import LimitOffsetPagination, PageNumberPagination
from rest_framework.response import Response

class DefaultLimitOffsetPagination(LimitOffsetPagination):
    max_limit = 50


class SmallLimitOffsetPagination(LimitOffsetPagination):
    default_limit = 10
    max_limit = 20


class MediumLimitOffsetPagination(LimitOffsetPagination):
    default_limit = 20
    max_limit = 60


class LargeLimitOffsetPagination(LimitOffsetPagination):
    default_limit = 100
    max_limit = 100


class DefaultPageNumberPagination(PageNumberPagination):
    page_size = 50
    page_size_query_param = "page_size"
    max_page_size = 10000

    def get_paginated_response(self, data):
        return Response(
            {
                "count": self.page.paginator.count,
                "num_of_pages": self.page.paginator.num_pages,
                "links": {"next": self.get_next_link(), "previous": self.get_previous_link()},
                "results": data,
            }
        )