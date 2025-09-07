from django.contrib.auth.models import User
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token

from list_app import models


class StreamPlatformTestCase(APITestCase):
    def setUp(self):
    #generamos un usuario, password y token
        self.user = User.objects.create_user(username='userTest', password='user123')
        self.token = Token.objects.get(user__username=self.user)
        #creamos un user manualmente para probar list y detail
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        self.stream = models.StreamPlatform.objects.create(name='Netflix', about='Streaming', website='https://netflix.com')
    
    def test_streamplatform_create(self):
        data = {
            "name": "Netflix",
            "about": "Straming",
            "website": "https://www.netflix.com"
        }
        response = self.client.post(reverse('streaming-platform-list'), data)
        #solo el administrador tiene permisos para crear streaming, entonces lanzamos un HTTP 403
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_streamplatform_list(self):
        response = self.client.get(reverse('streaming-platform-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_streamplatform_detail(self):
        #accedemos al id, usando un tuple (self.stream.id,) iterable en lugar de un entero
        response = self.client.get(reverse('streaming-platform-detail', args=(self.stream.id,)))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

class WatchlistTestCase(APITestCase):
    #creau usuario, autenticarlo y crear un stream
    def setUp(self):
        self.user = User.objects.create_user(username='userTest', password='user123')
        self.token = Token.objects.get(user__username=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        self.stream = models.StreamPlatform.objects.create(name='Netflix', about='Streaming', website='https://netflix.com')
        #creamos un movie para acceder a ella en el test_get
        self.watchlist = models.WatchList.objects.create(platform=self.stream, title='The test', storyline= 'The test storyline', active=True)

    def test_watchlist_create(self):
        data = {
            "platform": self.stream,
            "title": "Test example movie",
            "storyline" : "Some test history",
            "active": True 
        }
        response = self.client.post(reverse('watch-list'), data)
        #Un usuario diferente al administrador no puede crear, actualizar o borrar un elemento
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_watchlist_delete(self):
        response = self.client.delete(reverse('title-detail', args=(self.watchlist.id,)))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_watchlist_put(self):
        data = {
            "platform": self.stream,
            "title": "Test put",
            "storyline" : "Some test put method history",
            "active": True 
        }
        response = self.client.put(reverse('title-detail', args=(self.watchlist.id,)), data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_watchlist_list(self):
        response = self.client.get(reverse('watch-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_watchlist_detail(self):
        #el url nos pide un id, entonces pasamos el id como argumento (tuple)
        response = self.client.get(reverse('title-detail', args=(self.watchlist.id,)))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        #accedemos al elemento creado y verificamos si coincide con la response
        self.assertEqual(models.WatchList.objects.get().title, 'The test')
        #también podemos verificar el count
        self.assertEqual(models.WatchList.objects.count(), 1)

class ReviewTestCase(APITestCase):
    def setUp(self):
        #segun el modelo Review nacesitaremos crear usuario, streamplatform y peli
        #crear usuario
        self.user = User.objects.create_user(username='userTest', password='user123')
        self.token = Token.objects.get(user__username=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        #crear srteam platform y dos pelis
        self.stream = models.StreamPlatform.objects.create(name='Netflix', about='Streaming', website='https://netflix.com')
        self.watchlist = models.WatchList.objects.create(platform=self.stream, title='The test', storyline= 'The test storyline', active=True)
        self.watchlist2 = models.WatchList.objects.create(platform=self.stream, title='The test', storyline= 'The test storyline', active=True)
        #creamos un review para test_review_update, ya que no hay id
        self.review = models.Review.objects.create(review_user=self.user, rating=2, description='Review description', watchlist=self.watchlist2, active=True)

    def test_review_create(self):
        data = {
            "review_user": self.user,
            "rating": 3,
            "description": 'Test description',
            "watchlist": self.watchlist,
            "active": True
        }
        response = self.client.post(reverse('review-create', args=(self.watchlist.id,)), data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(models.Review.objects.count(), 2)
        #repetimos el test para comprobar que no se puede crear un review 2 veces por usuario, esta vez con 400 bad request
        response = self.client.post(reverse('review-create', args=(self.watchlist.id,)), data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
    #add un review como utilizador no autenticado
    def test_review_create_unauth(self):
        data = {
            "review_user": self.user,
            "rating": 3,
            "description": 'Test description',
            "watchlist": self.watchlist,
            "active": True
        }
        self.client.force_authenticate(user=None)
        response = self.client.post(reverse('review-create', args=(self.watchlist.id,)), data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_review_update(self):
        data = {
            "review_user": self.user,
            "rating": 5,
            "description": 'Test description - Updated',
            "watchlist": self.watchlist,
            "active": False
        }
        response = self.client.put(reverse('review-detail', args=(self.review.id,)), data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_review_list(self):
        response = self.client.get(reverse('review-list', args=(self.watchlist.id,)))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_review_detail(self):
        response = self.client.get(reverse('review-detail', args=(self.review.id,)))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_review_delete(self):
        response = self.client.delete(reverse('review-detail', args=(self.review.id,)))
        #HTTP_204_NO_CONTENT
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_review_user(self):
        response = self.client.get('/watch/review/?username' + self.user.username)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        