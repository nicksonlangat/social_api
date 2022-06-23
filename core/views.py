from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from core.serializers import PostSerializer
from .models import Post
import datetime
import logging

logger = logging.getLogger(__name__)

# Create your views here.
class PostsViewset(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = Post.objects.all()
    serializer_class = PostSerializer

    def get_queryset(self):
        user = self.request.user
        followed_authors = []
        followed_authors.append(user.id)
        for post in self.queryset:
            try:
                author_followers = post.author.followers.get(id=user.id)
                if author_followers is not None:
                    followed_authors.append(post.author.id)
            except Exception as e:
                logger.warning(str(e) + 'at - ' + str(datetime.datetime.now())+' hours!')
        qs = self.queryset.filter(author_id__in=followed_authors)
        return qs
