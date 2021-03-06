import requests
from rest_framework import status
from rest_framework.response import Response
from .models import Movie, Genre
from .serializers import MovieSerializer
from rest_framework.decorators import api_view

def setQuery(dic):
    x = ''
    if dic['title']:
        x += "{}={}&".format('t', dic['title'])
    if dic['year']:
        x += "{}={}&".format('r', dic['year'])
    if dic['rating']:
        x += "{}={}&".format('y', dic['rating'])
    if dic['imdb_id']:
        x += "{}={}&".format('i', dic['imdb_id'])
    # if dic['genre']:
    #     x += "{}={}&".format('i', dic['genre'])
    return x

@api_view(['GET'])
def getList(request):
    print(request.data)
    serializer_class = MovieSerializer

    if bool(request.data) is False:
        data = setQuery(
            {'title':request.query_params.get('title') or "",
             'year':request.query_params.get('year') or "",
             'rating':request.query_params.get('rating') or "",
             'imdb_id':request.query_params.get('imdb_id') or ""
             # 'genre':request.query_params.get('genre') or ""
             }
        )
        a = "http://www.omdbapi.com/?{}apikey=5992d630".format(data)
        print(a)
        res = requests.get(a)
        movie_item = res.json()
        k = {}

        k['title'] = movie_item.get('Title')
        k['year'] = movie_item.get('Year')
        k['rating'] = movie_item.get('imdbRating')
        k['imdb_id'] = movie_item.get('imdbID')
        # k['genre'] = movie_item.get('Genre')
        movie, created = Movie.objects.get_or_create(**k)

        genre_list = movie_item.get('Genre')
        # create genre for each genre in list and attach to current movie
        for name in genre_list.split(','):
            name = name.strip()
            genre, created = Genre.objects.get_or_create(title=name)
            movie.genre.add(genre)
        movie.save()


    # rest of the code
    queryset = Movie.objects.all()

    title = request.query_params.get('title', None)
    if title is not None:
        queryset = queryset.get(title__icontains=title)

    year = request.query_params.get('year', None)
    if year is not None:
        queryset = queryset.get(year__icontains=year)

    genre = request.query_params.get('genre', None)
    if genre is not None:
        queryset = queryset.get(genre__icontains=genre)

    rating = request.query_params.get('rating', None)
    if rating is not None:
        queryset = queryset.get(rating__icontains=rating)

    imdb_id = request.query_params.get('imdb_id', None)
    if imdb_id is not None:
        queryset = queryset.get(imdb_id__icontains=imdb_id)

    serializer = serializer_class(queryset)
    return Response(serializer.data, status=status.HTTP_200_OK)
