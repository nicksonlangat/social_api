from django.db import models
from accounts.models import User

# Create your models here.
class Post(models.Model):
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="post_author"
    )
    title = models.CharField(max_length=255)
    content = models.TextField()
    image = models.ImageField(upload_to="posts", null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return str(self.title)
