from rest_framework.pagination import PageNumberPagination

class UserPagination(PageNumberPagination):
    def get_paginated_response(self, data):

        print(data)

        return super().get_paginated_response(data)
    


class PostPagination(PageNumberPagination):
    page_query_param = 'page'
