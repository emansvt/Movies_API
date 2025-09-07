from django.contrib.auth.models import User #User objects: https://docs.djangoproject.com/en/5.0/topics/auth/default/
from rest_framework import serializers

class RegistrationSerializer(serializers.ModelSerializer):
    #style: el estilo 'password' que se usa en los formularios. Write_only: el usuario no puede leer el password, sólo escribir
    password2 = serializers.CharField(style={'input_type': 'password'}, write_only=True)
    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'password2']
        extra_kwargs = {
            'password': { 'write_only': True }
        }

#verificar si password y password2 son iguales y que el correo sea único y por lo tanto válido
    def save(self):
        #accedemos a los passwords
        password = self.validated_data['password']
        password2 = self.validated_data['password2']
        
        if password != password2:
            raise serializers.ValidationError({ 'Error' : 'Passwords does not match!'})
        
        if User.objects.filter(email=self.validated_data['email']).exists():
            raise serializers.ValidationError({'Error': 'La dirección de correo electrónico ya existe'})
            
        
        #si las condiciones de password y correo se cumplieron, creamos un nuevo usuario

        account = User(username=self.validated_data['username'], email=self.validated_data['email'] )
        #usamos set_password() para añadir el password - https://docs.djangoproject.com/en/5.0/topics/auth/default/#changing-passwords
        account.set_password(password)
        account.save()
        return account