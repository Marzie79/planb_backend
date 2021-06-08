from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response


# set last page number in header of response
# class Pagination(PageNumberPagination):
#     def get_paginated_response(self, data):
#         # add pages count to response header
#         return Response(data, headers={"Last-Page": self.page.paginator.num_pages})

class Pagination(PageNumberPagination):
    page_size = 6
    max_page_size = 1000

