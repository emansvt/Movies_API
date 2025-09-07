from django.urls import path, include
#usando urls con function based views
#from list_app.api.views import movie_list, movie_details
from rest_framework.routers import DefaultRouter

#usando class based views urls
from list_app.api.views import WatchListAV, WatchListDetailsAV, ReviewList, ReviewDetail, ReviewCreate, StreamPlatformMVS, UserReview, WatchListGV

# urlpatterns = [
#     path('list/', movie_list, name='movie-list'),
#     path('<int:pk>', movie_details, name='movie-detail')
# ]

#usando routers para stream
router = DefaultRouter()
router.register('stream', StreamPlatformMVS, basename='streaming-platform')

urlpatterns = [
    path('list/', WatchListAV.as_view(), name='watch-list'),
    #con el generic model
    path('list2/', WatchListGV.as_view(), name='movie-list'),
    path('<int:pk>/', WatchListDetailsAV.as_view(), name='title-detail'),
    # path('stream/', StreamPlatformAV.as_view(), name='streaming-platform'),
    # path('stream/<int:pk>', StreamPlatformDetailAV.as_view(), name='streaming-detail'),
    #usando routers (include)
    path('', include(router.urls)),
    # path('review/', ReviewList.as_view(), name='review-list'),
    # path('review/<int:pk>', ReviewDetail.as_view(), name='review-detail'),
    path('<int:pk>/review-create/', ReviewCreate.as_view(), name='review-create'),
    path('<int:pk>/review/', ReviewList.as_view(), name='review-list'),
    path('review/<int:pk>/', ReviewDetail.as_view(), name='review-detail'),#también es para editar con PUT
    #filtro mapeando por valor
    # path('review/<str:username>/', UserReview.as_view(), name='user-review-detail'),
    #filtro mapeando por parámetro (url/?parameter=value)
    path('review/', UserReview.as_view(), name='user-review-detail')
]