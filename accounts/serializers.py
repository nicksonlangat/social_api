from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    following = serializers.SerializerMethodField(read_only=True)
    class Meta:
        model = get_user_model()
        fields = [
            "id", "email", "first_name",
            "last_name", "date_joined",
            "is_superuser", "is_staff",
            "is_active", "followers",
            "following",
        ]
    
    def get_following(self, obj):
        following_list = []
        all_users = get_user_model().objects.all()
        for user in all_users:
            followers_list = [i.id for i in user.followers.all()]
            if obj.id in followers_list:
                if user.email not in following_list:
                    following_list.append(user.email)
        return following_list
    
    def to_representation(self, instance):
        rep = super().to_representation(instance)
        rep["followers"] = [user.email for user in instance.followers.all()]
        return rep


class SignupSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ["email", "first_name", "last_name", "password"]
        extra_kwargs = {"password": {"write_only": True}}

    def validate_password(self, value):
        validate_password(value)
        return value

    def create(self, validated_data):
        user = get_user_model()(**validated_data)
        user.set_password(validated_data["password"])
        user.save()
        return user


