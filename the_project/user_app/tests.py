from django.contrib.auth.models import User
#para usar el nombre dentro de las urls i.e name=login
from django.urls import reverse
#para el HTTP response status
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token

class RegisterTestCase(APITestCase):

#las clases deben empezar con test_ i.e test_mi_test
    def test_register(self):
        data = {
            "username": "testuser",
            "email": "user@test.com",
            "password": "123password@",
            "password2": "123password@"
        }
        
        response = self.client.post(reverse('register'), data)
        #hacemos un match entre la respuesta y el status con el método assetEqual para ver si los valores coinciden
        #assertEqual(first, second, msg=None), If the first value does not equal the second value, the test will fail. The msg is optional
        self.assertEqual(response.status_code, status.HTTP_201_CREATED, msg='Test realizado')

class LoginLogoutTest(APITestCase):
    #usamos el método setUp que se ejecuta antes del bloqie de test
    def setUp(self):
        self.user = User.objects.create_user(username='sometestuser', password='@user123')

    def test_login(self):
        data = {
            "username" : "sometestuser",
            "password" : "@user123"
        }
        response = self.client.post(reverse('login'), data)
        self.assertEqual(response.status_code, status.HTTP_200_OK, msg="Hay un error en el test login!")

    def test_logout(self):
        self.token = Token.objects.get(user__username="sometestuser")
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        response = self.client.post(reverse('logout'))
        self.assertEqual(response.status_code, status.HTTP_202_ACCEPTED)