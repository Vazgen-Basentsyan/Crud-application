from rest_framework import viewsets

from .serializers import UserSerializer, HomeSerializer
from .models import User, Home
from django.views.generic import ListView, TemplateView
import django_filters


class HomeView(TemplateView):
    template_name = 'users/home.html'
    model = User
    queryset = User.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["users"] = User.objects.all()
        context["homes"] = Home.objects.all()
        return context

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


class UserView(ListView):
    model = User
    paginate_by =  2
    template_name = 'users/users_list.html'
    queryset = User.objects.all()


class HomesView(ListView):
    model = Home
    paginate_by =  10
    template_name = 'users/homes_list.html'
    queryset = Home.objects.all()

    def get_queryset(self):
        user_id = self.kwargs.get("user_id")
        queryset = super().get_queryset().filter()
        if user_id:
            queryset = queryset.filter(user_id=user_id)
        return queryset

