from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import BookViewSet, RecommendationViewSet, LikeViewSet, CommentViewSet, search_books,index,register,login_view,logout_view,submit_recommendation,recommendations_view

router = DefaultRouter()
router.register(r'books', BookViewSet)
router.register(r'recommendations', RecommendationViewSet)
router.register(r'likes', LikeViewSet)
router.register(r'comments', CommentViewSet)

urlpatterns = [
    path('register/', register, name='register'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('index/', index, name='index'),
    path('', include(router.urls)),
    path('search/', search_books, name='search-books'),
    path('submit_recommendation/',submit_recommendation,name='submit-recommendation'),
    path('recommendationsList/', recommendations_view, name='recommendations_view'),
]
