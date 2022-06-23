from rest_framework import serializers

from core.models import Post


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ["id", "author", "title", "content", "image", "created_at"]

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        rep["author"] = instance.author.email
        return rep
