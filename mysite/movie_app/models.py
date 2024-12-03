from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MaxValueValidator, MinValueValidator
from phonenumber_field.modelfields import PhoneNumberField
from multiselectfield import MultiSelectField


class Profile(AbstractUser):
    password = models.CharField(max_length=255, default='default_password')
    age = models.PositiveSmallIntegerField(null=True, blank=True,
                                           validators=[MinValueValidator(15), MaxValueValidator(70)])
    phone_number = PhoneNumberField(null=True, blank=True)

    STATUS_CHOICES = (
        ('Pro', 'Pro'),
        ('Simple', 'Simple'),
    )
    status = models.CharField(max_length=16, choices=STATUS_CHOICES, default='Simple')

    def __str__(self):
        return f'{self.first_name} {self.last_name}'


class Country(models.Model):
    country_name = models.CharField(max_length=32, unique=True)

    def __str__(self):
        return self.country_name


class Director(models.Model):
    director_name = models.CharField(max_length=32)
    bio = models.TextField()
    age = models.PositiveSmallIntegerField(validators=[MaxValueValidator(100)])
    director_image = models.ImageField(upload_to='director_images/')

    def __str__(self):
        return self.director_name


class Actor(models.Model):
    actor_name = models.CharField(max_length=32)
    bio = models.TextField()
    age = models.PositiveSmallIntegerField(validators=[MaxValueValidator(100)])
    actor_image = models.ImageField(upload_to='actor_images/')

    def __str__(self):
        return self.actor_name


class Genre(models.Model):
    genre_name = models.CharField(max_length=16, unique=True)

    def __str__(self):
        return self.genre_name


class Movie(models.Model):
    MOVIE_TYPES = [
        ('144', '144p'),
        ('360', '360p'),
        ('480', '480p'),
        ('720', '720p'),
        ('1080', '1080p'),
    ]

    STATUS_CHOICES = [
        ('pro', 'Pro'),
        ('simple', 'Simple'),
    ]

    movie_name = models.CharField(max_length=64)
    year = models.DateField()
    country = models.ManyToManyField(Country)
    director = models.ManyToManyField(Director)
    actor = models.ManyToManyField(Actor, related_name='actor_films')
    genre = models.ManyToManyField(Genre)
    types = MultiSelectField(max_length=16, choices=MOVIE_TYPES, max_choices=5)
    movie_time = models.PositiveIntegerField()
    description = models.TextField()
    movie_trailer = models.FileField(upload_to="movie_trailer/")
    movie_image = models.ImageField(upload_to="movie_poster/")
    status_movie = models.CharField(max_length=16, choices=STATUS_CHOICES)

    def __str__(self):
        return self.movie_name


    def get_avg_rating(self):
        ratings = self.reviews.all()
        if ratings.exists():
            return round(sum(i.stars for i in ratings) / ratings.count(), 1)
        return 0


class MovieLanguages(models.Model):
    language = models.CharField(max_length=32)
    video = models.FileField(upload_to='videos/')
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name='videos')

    def __str__(self):
        return self.language


class Moments(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name='moments')
    movie_moments = models.ImageField(upload_to='movie_moments/')

    def __str__(self):
        return str(self.movie_moments)


class Rating(models.Model):
    user = models.ForeignKey(Profile, on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name='reviews')
    stars = models.IntegerField(choices=[(i, str(i)) for i in range(1, 11)], null=True, blank=True)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True)
    text = models.TextField()
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user}, {self.movie}'


class Favorite(models.Model):
    user = models.OneToOneField(Profile, on_delete=models.CASCADE)


class FavoriteMovie(models.Model):
    user = models.ForeignKey(Favorite, on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)


class History(models.Model):
    user = models.ForeignKey(Profile, on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    viewed_at = models.DateTimeField(auto_now_add=True)
