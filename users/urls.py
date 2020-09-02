from django.urls import path

from .views import UserView, HomeView, HomesView

urlpatterns = [
    path('', HomeView.as_view(), name='index'),
    path('users', UserView.as_view(), name='users'),
    path('homes', HomesView.as_view(), name='homes'),
    path('homes/<int:user_id>', HomesView.as_view(), name='user_homes')

]