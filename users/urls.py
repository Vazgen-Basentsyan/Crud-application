from django.urls import path
from django.conf.urls import url

from .views import UserView, HomeView, HomesView, UserDetailView, UserUpdateView

urlpatterns = [
    path('', HomeView.as_view(), name='index'),
    path('users', UserView.as_view(), name='users'),
    path('<slug:slug>', UserDetailView.as_view(), name='user-detail'),
    url(r'^update/(?P<pk>\d+)/$', UserUpdateView.as_view(), name='user-detail'),
    path('homes', HomesView.as_view(), name='homes'),
    path('homes/<int:user_id>', HomesView.as_view(), name='user_homes')
]