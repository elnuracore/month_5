from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Film, Genre, Director
from django.db import transaction
from .serializers import (FilmDetailSerializers, 
                          FilmListSerializers,
                          FilmValidateSerializers, 
                          GenreSerializers,
                          DirectorSerializers
                          )
from common.permissions import IsModerator
from rest_framework.generics import ListAPIView, ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.pagination import PageNumberPagination
from rest_framework.viewsets import ModelViewSet

class GenreListAPIView(ListCreateAPIView):
    serializer_class = GenreSerializers
    queryset = Genre.objects.all()
    pagination_class = PageNumberPagination
    permission_classes = [IsModerator]

class GenreDetailAPIView(RetrieveUpdateDestroyAPIView):
    serializer_class = GenreSerializers
    queryset = Genre.objects.all()
    lookup_field = "id"
    permission_classes = [IsModerator]


class DirectorViewSet(ModelViewSet):
    serializer_class = DirectorSerializers
    queryset = Director.objects.all()
    pagination_class = PageNumberPagination
    lookup_field = "id"



@api_view(['GET', 'PUT', 'DELETE'])
def film_detail_api_view(request, id):
    try:
        film = Film.objects.get(id=id)
    except:
        return Response(status=status.HTTP_404_NOT_FOUND,
                        data={'error' : 'film not found!'})
    
    if request.method == "GET":
        data = FilmDetailSerializers(film, many=False).data
        return Response(data=data)
    
    elif request.method == "PUT":

        film.title = request.data.get('title')
        film.text = request.data.get('text')
        film.release_year = request.data.get('release_year')
        film.is_hit = request.data.get('is_hit')
        film.rating = request.data.get('rating')
        film.director_id = request.data.get('director_id')  # Foreign Key field
        film.genres.set(request.data.get('genres'))  # ManyToMany field
        film.save()
        return Response(status=status.HTTP_201_CREATED, 
                        data=FilmDetailSerializers(film).data)
    
    elif request.method == "DELETE":
        film.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)






@api_view(['GET', 'POST'])
def film_list_api_view(request):
    if request.method == "GET":
        films = Film.objects.select_related('director').prefetch_related('genres', 'reviews').all()
        data = FilmListSerializers(films, many=True).data

        return Response(
            data = data
    )
    elif request.method == "POST":
        serializer = FilmValidateSerializers(data=request.data)
        # if not serializer.is_valid():
        #     return Response(status=status.HTTP_400_BAD_REQUEST, data=serializer.errors)
        serializer.is_valid(raise_exception=True)

        title = serializer.validated_data.get('title')
        text = serializer.validated_data.get('text')
        release_year = serializer.validated_data.get('release_year')
        is_hit = serializer.validated_data.get('is_hit')
        rating= serializer.validated_data.get('rating')
        director_id = serializer.validated_data.get('director_id')
        genres = serializer.validated_data.get('genres')
        print(title, text, release_year, is_hit, rating, genres)

        with transaction.atomic():
            film  = Film.objects.create(
                title=title,
                text=text,
                release_year=release_year,
                is_hit=is_hit,
                rating=rating,
                director_id=director_id
                )
            film.genres.set(genres)
            film.save()

        return Response(status=status.HTTP_201_CREATED, data=FilmDetailSerializers(film).data)
    
    


    