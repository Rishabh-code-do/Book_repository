from rest_framework import viewsets
from rest_framework.decorators import api_view,action,permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.conf import settings
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.exceptions import ValidationError,NotFound
from rest_framework import filters
import requests
from django.shortcuts import render,redirect
from .models import Book, Recommendation, Like, Comment
from .serializers import BookSerializer, RecommendationSerializer, LikeSerializer, CommentSerializer
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required

@api_view(['GET'])
def search_books(request):
    query = request.query_params.get('q', '')
    if not query:
        return Response({'error': 'Query parameter is required'}, status=400)

    api_key = settings.GOOGLE_BOOKS_API_KEY
    url = f'https://www.googleapis.com/books/v1/volumes?q={query}&maxResults=20&key={api_key}'
    response = requests.get(url)

    if response.status_code != 200:
        return Response({'error': 'Failed to fetch data from Google Books API'}, status=response.status_code)

    data = response.json().get('items', [])
    books = []
    for item in data:
        volume_info = item.get('volumeInfo', {})
        book = {
            'google_books_id': item.get('id', ''),
            'title': volume_info.get('title', 'No Title'),
            'author': ', '.join(volume_info.get('authors', [])),
            'description': volume_info.get('description', 'No Description'),
            'cover_image': volume_info.get('imageLinks', {}).get('thumbnail', ''),
            'ratings': volume_info.get('averageRating', 0),
            'publishedDate':volume_info.get('publishedDate', '')
        }
        books.append(book)

    return Response(books)

class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer

class RecommendationViewSet(viewsets.ModelViewSet):
    queryset = Recommendation.objects.all()
    serializer_class = RecommendationSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['book__ratings','book__publishedDate']
    ordering_fields = ['book__ratings','book__publishedDate']

    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated])
    def my_recommendations(self, request):
        recommendations = self.queryset.filter(user=request.user)
        serializer = self.get_serializer(recommendations, many=True)
        return Response(serializer.data)

class LikeViewSet(viewsets.ModelViewSet):
    queryset = Like.objects.all()
    serializer_class = LikeSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        user = request.user
        bookId = request.data.get('bookId')

        if not user:
            return Response({'error': 'User is not logged in '}, status=500)
        
        if not bookId:
            return Response({'error': 'Book ID Not Found'})
        
        book_recommendation = Recommendation.objects.filter(book_id=bookId).last()

        if not book_recommendation:
            return Response({ 'error': 'Book Recommendation not found' })
        
        like_obj, is_created = Like.objects.get_or_create(recommendation=book_recommendation, user=user)
        if is_created:
            like_obj.like = True
        else:
            like_obj.like = False if like_obj.like == True else True
        like_obj.save()
        
        response_data = {
            'message': 'Liked!' if like_obj.like == True else 'Unliked!',
            'like': like_obj.like,
            'book_id': bookId,
            'user': user.username
        }
        
        return Response(response_data, status=201)

    

class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        user = request.user
        bookId = request.data.get('bookId')
        text = request.data.get('comment')

        if not user:
            return Response({'error': 'User is not logged in '}, status=500)
        
        if not bookId:
            return Response({'error': 'Book ID Not Found'})
        
        book_recommendation = Recommendation.objects.filter(book_id=bookId).last()

        if book_recommendation:
            Comment.objects.create(recommendation=book_recommendation,user=user, text=text)

        return Response({'success': 'Comment Added'}, status=201)

def index(request):
    return render(request, 'index.html')

@permission_classes([IsAuthenticated])
def recommendations_view(request):
    return render(request, 'recommendations.html')

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def submit_recommendation(request):
    user = request.user
    book_id = request.data.get('book_id')
    try:
        book = Book.objects.get(google_books_id=book_id)
    except Book.DoesNotExist:
        url = f'https://www.googleapis.com/books/v1/volumes/{book_id}?key={settings.GOOGLE_BOOKS_API_KEY}'
        response = requests.get(url)

        if response.status_code != 200:
            return Response({'error': 'Failed to fetch book data from Google Books API'}, status=response.status_code)

        book_data = response.json().get('volumeInfo', {})

        book = Book.objects.create(
            google_books_id=book_id,
            title=book_data.get('title', 'No Title'),
            author=', '.join(book_data.get('authors', [])),
            description=book_data.get('description', 'No Description'),
            cover_image=book_data.get('imageLinks', {}).get('thumbnail', ''),
            ratings=book_data.get('averageRating', 0),
            publishedDate=book_data.get('publishedDate', ''),
        )

    recommendation, created = Recommendation.objects.get_or_create(book=book)

    if not created:
        if not recommendation.user.filter(id=user.id).exists():
            recommendation.user.add(user)
        return Response({"message": "Recommendation updated successfully"})
    else:
        recommendation.user.add(user)
        return Response({"message": "Recommendation submitted successfully"})


def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('index')  
    else:
        form = UserCreationForm()
    return render(request, 'register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('index')  
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})

@login_required
def logout_view(request):
    logout(request)
    return redirect('login')  