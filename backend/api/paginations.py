from rest_framework.pagination import PageNumberPagination


class PageNumberPaginationLimit(PageNumberPagination):
    page_size_query_param = 'limit'
