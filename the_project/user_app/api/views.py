#usamos function based view: https://www.django-rest-framework.org/api-guide/views/#function-based-views
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework import status

from user_app.api.serializers import RegistrationSerializer
from user_app import models

@api_view(['POST'])
def logout_view(request):
    if request.method == 'POST':
        request.user.auth_token.delete()
        return Response(status=status.HTTP_202_ACCEPTED)

@api_view(['POST'])
def registration_view(request):
    if request.method == 'POST':
        serializer = RegistrationSerializer(data=request.data)
        #creamos un diccionario para almacenar los datos del usuario registrado
        data: dict
        data = {}

        if serializer.is_valid():
            #usamos el método save() creado en el serializador RegistrationSerializer
            account = serializer.save()
            data['response'] = "User created successfuly!"
            data['username'] = account.username
            data['email'] = account.email
            token = Token.objects.get(user=account).key
            data['token'] = token

        else:
            data = serializer.errors

        return Response(data, status.HTTP_201_CREATED)