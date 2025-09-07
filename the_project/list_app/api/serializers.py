from rest_framework import serializers
from list_app.models import WatchList, StreamPlatform, Review

####### USANDO MODEL SERIALIZERS (más corto)

class ReviewSerializer(serializers.ModelSerializer):
    review_user = serializers.StringRelatedField(read_only=True)
    class Meta:
        model = Review
        # fields = '__all__'
        exclude = ['watchlist']

class WatchListSerializer(serializers.ModelSerializer):
    #usar el related_name en el modelo, muestra el modelo Review dentro de WatchList
    # reviews = ReviewSerializer(many=True, read_only=True)
    #mostrar el nombre de la plataforma y no el número. platform es la ForeignKey del modelo Watchlist y name es un campo del model Stream Platform
    platform = serializers.CharField(source='platform.name')

    class Meta:
        model = WatchList
        fields = '__all__'
        # exclude = ['name']
        # fields = ['id', 'name', 'description']

class StreamPlatformSerializer(serializers.ModelSerializer):
    #Tomamos el nombre en 'related_field=watchlist' el modelo WatchList (platform = models.ForeignKey(StreamPlatform, on_delete=models.CASCADE, related_name="watchlist"))

    #SERIALIZER RELATIONS https://www.django-rest-framework.org/api-guide/relations/#stringrelatedfield

    #watchlist = serializers.StringRelatedField(many=True)
    #tomamos el nombre del path en urls.py (en este caso 'title-detail')
    #watchlist = serializers.HyperlinkedRelatedField(many=True, read_only=True, view_name='title-detail')
    watchlist = WatchListSerializer(many=True, read_only=True)
    class Meta:
        model = StreamPlatform
        fields = '__all__'
    
   


###### USANDO SERIALIZERS

#validación por validators
# def description_length(value):
#     if len(value) < 5:
#         raise serializers.ValidationError('Description must have 5 characters minimum!')
#     return value

# class MovieSerializer(serializers.Serializer):
#     id = serializers.IntegerField(read_only=True)
#     name = serializers.CharField()
#     description = serializers.CharField(validators=[description_length])
#     active = serializers.BooleanField(default=True)

#     #usamos los métodos create() y update() de la clase serializers
#     def create(self, validated_data):
#         return Movie.objects.create(**validated_data)
    
#     # instance contiene los valores viejos y validated_data los nuevos
#     def update(self, instance, validated_data):
#         instance.name = validated_data.get('name', instance.name)
#         instance.description = validated_data.get('description', instance.name)
#         instance.active = validated_data.get('active', instance.active)
#         instance.save()
#         return instance
    
#     def validate_name(self, value):
#         if len(value) < 2:
#             raise serializers.ValidationError('The name is too short!')
#         return value
    
#     def validate(self, data):
#         if data['name'] == data['description']:
#             raise serializers.ValidationError('Name and description fields must be different!')
#         return data
     