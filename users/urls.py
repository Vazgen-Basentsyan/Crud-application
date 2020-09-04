from django.urls import path

from .views import UserView, HomeView, HomesView, UserDetailView, UserUpdateView, HomeUpdateView, ImageListView


urlpatterns = [
    path('', HomeView.as_view(), name='index'),
    path('users', UserView.as_view(), name='users'),
    path('users/<int:pk>', UserUpdateView.as_view(), name='users-update'),
    path('homes/<int:pk>', HomeUpdateView.as_view(), name='homes-update'),
    path('homes', HomesView.as_view(), name='homes'),
    path('homes/<int:user_id>', HomesView.as_view(), name='user_homes'),
    path('images/<int:home_id>', ImageListView.as_view(), name='home_images'),
    path('<slug:slug>', UserDetailView.as_view(), name='user-detail'),
]