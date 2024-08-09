from rest_framework import serializers
from .models import Book, Like, Recommendation,Comment

class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = '__all__'

class RecommendationSerializer(serializers.ModelSerializer):
    likes = serializers.SerializerMethodField()
    comments = serializers.SerializerMethodField()
    book=serializers.SerializerMethodField()
    is_liked_by_user = serializers.SerializerMethodField()

    class Meta:
        model = Recommendation
        fields = '__all__'

    def get_likes(self, instance):
        if instance:
            return instance.likes.filter(like=True).count()
        return 0
    
    def get_comments(self,instance):
        if instance:
            result=instance.comments.all()
            comment=[]
            for i in result:
                comment.append({'name':i.user.username,'comment':i.text})
            return comment
        return []
    
    def get_book(self,instance):
        if instance:
            return {'author':instance.book.author,'title':instance.book.title,'description':instance.book.description, 'book_id': instance.book.id,
                    'cover_image':instance.book.cover_image,'ratings':instance.book.ratings,'publishedDate':instance.book.publishedDate}
        return {}
    
    def get_is_liked_by_user(self, instance):
        user = self.context.get('request').user
        like_obj = Like.objects.filter(user=user,recommendation=instance).last()
        if like_obj:
            return like_obj.like
        return False
    
class LikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Like
        fields = '__all__'

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = '__all__'
