from rest_framework import routers
from .views import *
from django.urls import path, include
from .views import MovieListApiView
from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView


router = routers.SimpleRouter()
router.register(r'user', ProfileViewSet, basename='user')
router.register(r'director', DirectorViewSet, basename='director')
router.register(r'actor', ActorViewSet, basename='actor')
router.register(r'favorite', FavoriteViewSet, basename='favorite')
router.register(r'favorite_movie', FavoriteMovieViewSet, basename='favorite_movie')
router.register(r'history', HistoryViewSet, basename='history')
router.register(r'rating', RatingViewSet, basename='rating')

urlpatterns = [
    path('', include(router.urls)),
    path('movie', MovieListApiView.as_view(), name='movie_list'),
    path('movies/', MovieListApiView.as_view(), name='movie-list'),
    path('movie/<int:pk>/', MovieDetailApiView.as_view(), name='movie_detail'),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]