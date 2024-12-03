from rest_framework import serializers
from .models import *


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = '__all__'


class CountrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Country
        fields = ['country_name']


class DirectorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Director
        fields = ['director_name']


class ActorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Actor
        fields = ['actor_name',]


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = ['genre_name']


class MovieLanguagesSerializer(serializers.ModelSerializer):
    class Meta:
        model = MovieLanguages
        fields = ['language', 'video']


class MomentsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Moments
        fields = ['movie_moments']


class RatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rating
        fields = '__all__'


class FavoriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Favorite
        fields = '__all__'


class FavoriteMovieSerializer(serializers.ModelSerializer):
    class Meta:
        model = FavoriteMovie
        fields = '__all__'


class HistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = History
        fields = '__all__'


class MovieListSerializer(serializers.ModelSerializer):
    country = CountrySerializer(many=True)
    genre = GenreSerializer(many=True )
    year = serializers.DateField(format('%d-%m-%Y'))
    avg_rating = serializers.SerializerMethodField()

    class Meta:
        model = Movie
        fields = ['id', 'movie_name', 'movie_image', 'year', 'country', 'genre', 'status_movie', 'avg_rating']

    def get_avg_rating(self,obj):
        return obj.get_avg_rating()


class MovieDetailSerializer(serializers.ModelSerializer):
    country = CountrySerializer(many=True)
    genre = GenreSerializer(many=True )
    year = serializers.DateField(format('%d-%m-%Y'))
    director = DirectorSerializer(many=True)
    actor = ActorSerializer(many=True)
    videos = MovieLanguagesSerializer(many=True, read_only=True)
    moments = MomentsSerializer(many=True, read_only=True)

    class Meta:
        model = Movie
        fields = ['movie_name', 'movie_image', 'year', 'country', 'genre', 'director',
                  'actor', 'types', 'movie_time', 'description', 'movie_trailer', 'status_movie', 'videos', 'moments']

class ActorDetailSerializer(serializers.ModelSerializer):
    actor_films = MovieListSerializer(many=True, read_only=True)

    class Meta:
        model = Actor
        fields = ['actor_name','actor_image', 'bio', 'age', 'actor_films']
