# from django.shortcuts import render
# from list_app.models import Movie
# from django.http import JsonResponse

# # Create your views here.
# def movie_list(request):
#     movies = Movie.objects.all()
#     # creamos una variable iterable 'data' y usamos values() para obtener un QuerySet en forma de diccionario
#     data = {
#         'movies': list(movies.values())
#     }
#     # enviamos data como una respuesta JSON
#     return JsonResponse(data)

# def movie_details(request, pk):
#     movie = Movie.objects.get(pk=pk)
#     data = {
#         'name': movie.name,
#         'description': movie.description,
#         'active': movie.active
#     }
#     return JsonResponse(data)