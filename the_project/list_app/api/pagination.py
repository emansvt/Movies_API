from rest_framework.pagination import PageNumberPagination
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.pagination import CursorPagination

# más info: https://www.django-rest-framework.org/api-guide/pagination/

class WatchListPagination(PageNumberPagination):
    page_size = 3
    #el parámetro que aparece en la url del reques, i.e. http://127.0.0.1:8000/watch/list2/?p=2
    page_query_param = 'p'
    #se puede personalizar el número de resultados, i.e. http://127.0.0.1:8000/watch/list2/?p=2&size=3
    page_size_query_param = 'size'
    #se puede restringir el numer máximo de resultados
    max_page_size = 10
    #se puede personalizar la última página para acceder al resultado directamente (default= 'last') i.e http://127.0.0.1:8000/watch/list2/?p=end
    #last_page_strings = 'end'

class WatchListLimitOffsetPagination(LimitOffsetPagination):
    #i.e. GET https://api.example.org/accounts/?limit=100&offset=400
    default_limit = 4
    max_limit = 10
    limit_query_param = 'limit'
    offset_query_param = 'start'

class WatchListCursorPagination(CursorPagination):
    page_size = 3
    #elegimos un campo del modelo para ordenar en función de él. i.e. el campo 'created' del modelo WatchList. '-created' cambia el orden de nuevo a viejo
    ordering = '-created'