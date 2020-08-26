from rest_framework import viewsets

from .serializers import UserSerializer, HomeSerializer
from .models import User, Home


class UserViewSet(viewsets.ModelViewSet):
    model = User
    serializer_class = UserSerializer
    queryset = User.objects.all()
    allowed_methods = "GET", "POST", "PATCH", "DELETE"


class HomeViewSet(viewsets.ModelViewSet):
    model = Home
    serializer_class = HomeSerializer
    queryset = Home.objects.all()
    allowed_methods = "GET", "POST", "PATCH", "DELETE"