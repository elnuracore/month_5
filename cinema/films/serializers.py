from rest_framework import serializers
from .models import Film, Director, Genre
from rest_framework.exceptions import ValidationError


class GenreSerializers(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = "__all__"
    
class DirectorSerializers(serializers.ModelSerializer):
    class Meta:
        model = Director
        fields = "id fio".split()

class FilmDetailSerializers(serializers.ModelSerializer):
    class Meta:
        model = Film
        fields = '__all__'

class FilmListSerializers(serializers.ModelSerializer):
    director = DirectorSerializers()
    genres = serializers.SerializerMethodField()
    class Meta:
        model = Film
        fields = 'id director genres title is_hit rating created reviews'.split()
        depth = 1

    def get_genres(self, films):
        return films.genre_names[0:2]

class FilmValidateSerializers(serializers.Serializer):
    title = serializers.CharField(min_length=1, max_length=255)
    text = serializers.CharField(required=False)
    release_year = serializers.IntegerField()
    is_hit = serializers.BooleanField(default=True)
    rating = serializers.FloatField(min_value=1, max_value=10)
    director_id = serializers.IntegerField()
    genres = serializers.ListField(child=serializers.IntegerField())

    def validate_director_id(self, director_id):
        try:
            Director.objects.get(id=director_id)
        except Director.DoesNotExist:
            raise ValidationError("Director does not exist")
        return director_id




