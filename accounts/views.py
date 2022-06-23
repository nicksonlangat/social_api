from django.contrib.auth import get_user_model
from rest_framework import mixins, viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.views import APIView
from rest_framework import exceptions
from accounts.utils import get_tokens_for_user
from . import serializers

class UserListView(mixins.ListModelMixin, viewsets.GenericViewSet):
    permission_classes = [AllowAny]
    queryset = get_user_model().objects.all()
    serializer_class = serializers.UserSerializer


class SignUpUserView(mixins.CreateModelMixin, viewsets.GenericViewSet):
    permission_classes = [AllowAny]
    queryset = get_user_model().objects.all()
    serializer_class = serializers.SignupSerializer

    def post(self, request):
        serializer = serializers.SignupSerializer(request.DATA)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {
                    "success": True,
                },
                status=status.HTTP_201_CREATED,
            )
        else:
            return Response(serializer._errors, status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        User = get_user_model()
        email = request.data.get("email")
        password = request.data.get("password")
        response = Response()
        if (email is None) or (password is None):
            raise exceptions.AuthenticationFailed("email and password required")
        user = User.objects.filter(email=email).first()
        if user is None:
            raise exceptions.AuthenticationFailed("user not found")
        if not user.check_password(password):
            raise exceptions.AuthenticationFailed("wrong password")

        token = get_tokens_for_user(user)
        response.data = token
        return response


class FollowView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        response = Response()
        action = request.data.get("action")
        user = request.user
        user_to_follow = get_user_model().objects.get(
            id=request.data.get("user_to_follow")
        )
        user_followers = [user.id for user in user_to_follow.followers.all()]
         
        if action == "follow":
            if user.id not in user_followers:
                user_to_follow.followers.add(user)
                response.data = {
                    "message": f"You are now following {user_to_follow.first_name}"
                }
            else:
                response.data = {
                    "message": f"You are already following {user_to_follow.first_name}"
                }

        elif action == "unfollow":
            if user.id in user_followers:
                user_to_follow.followers.remove(user)
                response.data = {
                    "message": f"You have unfollowed {user_to_follow.first_name}"
                }
            else:
                response.data = {
                    "message": f"You are not following {user_to_follow.first_name}"
                }
        return response

