
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Movie
from .serializers import MovieSerializer


class IndexView(APIView):

    allowed_methods = ['GET']
    serializer_class = MovieSerializer

    def get(self, request, *args, **kwargs):
        queryset = Movie.objects.all()

        title = request.query_params.get('title', None)
        if title is not None:
            queryset = queryset.filter(title__icontains=title)

        year = request.query_params.get('year', None)
        if year is not None:
            queryset = queryset.filter(year__icontains=year)

        genre = request.query_params.get('genre', None)
        if genre is not None:
            queryset = queryset.filter(genre__name__icontains=genre)

        rating = request.query_params.get('rating', None)
        if rating is not None:
            queryset = queryset.filter(rating__icontains=rating)

        imdb_id = request.query_params.get('imdb_id', None)
        if imdb_id is not None:
            queryset = queryset.filter(imdb_id__icontains=imdb_id)

        serializer = self.serializer_class(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
