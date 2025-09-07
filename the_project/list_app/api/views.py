from list_app.models import WatchList, StreamPlatform, Review
from django.shortcuts import get_object_or_404
from list_app.api.pagination import WatchListPagination, WatchListLimitOffsetPagination, WatchListCursorPagination

#Para class based views
# from rest_framework.authentication import BasicAuthentication
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from rest_framework import status
from rest_framework import generics
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.throttling import UserRateThrottle, AnonRateThrottle
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
#custom throttling
from list_app.api.throttling import ReviewListThrottling, ReviewCreateThrotling
# from rest_framework import mixins
from list_app.api.serializers import WatchListSerializer, StreamPlatformSerializer, ReviewSerializer
#custom permissions
from list_app.api.permissions import IsReviewUserOrReadOnly, IsAdminOrReadOnly

#USANDO GENERIC VIEWS y concrete generic views https://www.django-rest-framework.org/api-guide/generic-views/

class ReviewCreate(generics.CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ReviewSerializer
    throttle_classes = [ReviewCreateThrotling]

    def get_queryset(self):
        return Review.objects.all()
    
    #usamos el hook 'perform_create'
    def perform_create(self, serializer):
        pk = self.kwargs.get('pk')
        watchlist = WatchList.objects.get(pk=pk)
        #VERIFICAR QUE NO HAYA MAS DE 1 REVIEW POR USUARIO
        #acceder al nombre del usuario
        reviewer = self.request.user
        #buscar si el usuario 'reviewer' ya ha hecho algún review (watchlist y review_user vienen del modelo)
        review_queryset = Review.objects.filter(watchlist=watchlist, review_user=reviewer)
        if review_queryset.exists():
            raise ValidationError('You have already reviewed this title!')
        #usamos el atributo 'watchlist' del modelo Review
        #verificamos si ya hay algún rating 
        if watchlist.number_ratings == 0:
            # si todavía no hay rating serializer.validated_data['rating'] es el nuevo rating
            watchlist.avg_rating = serializer.validated_data['rating'] 
        else:
            #si ya hay ratings calculamos el promedio entre el anterior y el nuevo
            watchlist.avg_rating = (watchlist.avg_rating + serializer.validated_data['rating'])/2 

        watchlist.number_ratings = watchlist.number_ratings + 1
        watchlist.save()
        serializer.save(watchlist=watchlist, review_user=reviewer)


class ReviewList(generics.ListAPIView):
    serializer_class = ReviewSerializer
    #define permission class
    # permission_classes = [IsAuthenticated]
    #activar throttling para este view
    throttle_classes = [ReviewListThrottling]
    #usando django-filter package, funciona con generics
    filter_backends = [DjangoFilterBackend]
    #elejimos los campos que queremos filtrar i.e. ?review_user__username=admin&active=true
    filterset_fields = ['review_user__username', 'active']

    def get_queryset(self):
        #usamos el atributo 'watchlist' del modelo Review como primary key(pk)
        pk = self.kwargs['pk']
        return Review.objects.filter(watchlist=pk) 
           

class ReviewDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    #solo el administrador tiene permisos para editar, los demás usuarios tienen 'read only permissions'
    #permission_classes = [AdminOrReadOnly]
    permission_classes= [IsReviewUserOrReadOnly]
    # throttle_classes = [UserRateThrottle, AnonRateThrottle]
    throttle_scope = 'review-detail'

#USANDO GENERIC VIEWS y mixins https://www.django-rest-framework.org/api-guide/generic-views/#examples

# class ReviewList(mixins.ListModelMixin, mixins.CreateModelMixin, generics.GenericAPIView):
    #al usar los atributos propios de generic views, usamos sus nombres (como queryset, serializer_class). https://www.django-rest-framework.org/api-guide/generic-views/#attributes
#     queryset = Review.objects.all()
#     serializer_class = ReviewSerializer

#     def get(self, request, *args, **kwargs):
#         return self.list(request, *args, **kwargs)

#     def post(self, request, *args, **kwargs):
#         return self.create(request, *args, **kwargs)
    
# class ReviewDetail(mixins.RetrieveModelMixin, generics.GenericAPIView):
#     queryset = Review.objects.all()
#     serializer_class = ReviewSerializer    

#     def get(self, request, *args, **kwargs):
#         return self.retrieve(request, *args, **kwargs)

##### Streaming Platform views

#usando Model View Sets (más potente). Con ReadOnlyModelViewSet no hay post ni delete requests

class StreamPlatformMVS(viewsets.ModelViewSet):
    permission_classes = [IsAdminOrReadOnly] #si no es SAFE_METHOD (GET) sólo el administrador puede editar
    queryset = StreamPlatform.objects.all()
    serializer_class = StreamPlatformSerializer

##usando ViewSet y routers (en urls.py)

# class StreamPlatformVS(viewsets.ViewSet):
#     def list(self, request):
#         queryset = StreamPlatform.objects.all()
#         serializer = StreamPlatformSerializer(queryset, many=True)
#         return Response(serializer.data)
    
#     def retrieve(self, request, pk=None):
#         queryset = StreamPlatform.objects.all()
#         user = get_object_or_404(queryset, pk=pk)
#         serializer = StreamPlatformSerializer(user)
#         return Response(serializer.data)
    
#usando API View
# class StreamPlatformAV(APIView):
#     def get(self, request):
#         platform = StreamPlatform.objects.all()
        # Si usamos HyperlinkedRelatedField en el serializer añadimos contexto para evitar un error:
        #`HyperlinkedRelatedField` requires the request in the serializer context. Add `context={'request': request}` when instantiating the serializer.
        # serializer = StreamPlatformSerializer(platform, many=True, context={'request': request})
    #     serializer = StreamPlatformSerializer(platform, many=True)
    #     return Response(serializer.data)

    # def post(self, request):
    #     serializer = StreamPlatformSerializer(data=request.data)
    #     if serializer.is_valid():
    #         serializer.save()
    #         return Response(serializer.data)
    #     else: 
    #         return Response(serializer.errors)
        
class StreamPlatformDetailAV(APIView):
    permission_classes = [IsAdminOrReadOnly] #si no es SAFE_METHOD (GET) sólo el administrador puede editar
    def get(self, request, pk):
        try:
            streaming = StreamPlatform.objects.get(pk=pk)
        except StreamPlatform.DoesNotExist:
            return Response({'error': 'Element not found :('}, status=status.HTTP_404_NOT_FOUND)
        serializer = StreamPlatformSerializer(streaming)
        return Response(serializer.data)
    
    def put(self, request, pk):
        streaming = StreamPlatform.objects.get(pk=pk)
        serializer = StreamPlatformSerializer(streaming, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
    def delete(self, request, pk):
        streaming = StreamPlatform.objects.get(pk=pk)
        streaming.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
##### WATCHLIST VIEWS
class WatchListGV(generics.ListAPIView):
    queryset = WatchList.objects.all()
    serializer_class = WatchListSerializer
    # pagination_class = WatchListPagination
    #pagination_class = WatchListLimitOffsetPagination
    pagination_class = WatchListCursorPagination

    #los 3 tipos de filtros, ver: https://www.django-rest-framework.org/api-guide/filtering/#djangofilterbackend

    # filter_backends = [DjangoFilterBackend]
    # filterset_fields = ['title', 'platfotm__name']

    # filter_backends = [filters.SearchFilters]
    # ^ = Starts-with search.
    # search_fields = ['title', '^platform']

    filter_backends = [filters.OrderingFilter]
    ordering_fields = ['avg_rating']

class WatchListAV(APIView):
    permission_classes = [IsAdminOrReadOnly] #si no es SAFE_METHOD (GET) sólo el administrador puede editar
    def get(self, request):
        movies = WatchList.objects.all()
        serializer = WatchListSerializer(movies, many=True)
        return Response(serializer.data)
    
    def post(self, request):
        serializer = WatchListSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors)
        
    def put(self, request, pk):
        streaming = WatchList.objects.get(pk=pk)
        serializer = WatchListSerializer(streaming, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
    def delete(self, request, pk):
        streaming = WatchList.objects.get(pk=pk)
        streaming.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
        
class WatchListDetailsAV(APIView):
    permission_classes = [IsAdminOrReadOnly] #si no es SAFE_METHOD (GET) sólo el administrador puede editar
    def get(self, request, pk):
        try:
            movie = WatchList.objects.get(pk=pk)
        except WatchList.DoesNotExist:
            return Response({'error': 'Element not found :('}, status=status.HTTP_404_NOT_FOUND)
        serializer = WatchListSerializer(movie)
        return Response(serializer.data)

    def put(self, request, pk):
        movie = WatchList.objects.get(pk=pk)
        serializer = WatchListSerializer(movie, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
    def delete(self, request, pk):
        movie = WatchList.objects.get(pk=pk)
        movie.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
        
#######FILTRADO POR USUARIO
class UserReview(generics.ListAPIView):
    serializer_class = ReviewSerializer
    #define permission class
    # permission_classes = [IsAuthenticated]
    #activar throttling para este view
    # throttle_classes = [ReviewListThrottling]
    

    def get_queryset(self):
        #mapeamos por el valor username:
        #username = self.kwargs['username']#nos regresa el nombre de usuario

        #o mapeando por parámetro:
        username = self.request.query_params.get('username')

        # accedemos al campo review_user del modelo Review y usamos la notación de doble guión bajo para acceder a la Foreign key username
        # del modelo User (ver models.py)
        return Review.objects.filter(review_user__username=username)    