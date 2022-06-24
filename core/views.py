from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from core.serializers import PostSerializer
from .models import Post
import datetime
import logging

from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.views.decorators.vary import vary_on_cookie

logger = logging.getLogger(__name__)

# Create your views here.
class PostsViewset(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    
    @method_decorator(vary_on_cookie)
    @method_decorator(cache_page(60*60))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

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
