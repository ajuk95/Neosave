from django.conf import urls
from Users.views import get_all_users, get_user, post_user
from django.urls import path
from django.conf.urls import include

urlpatterns = [
    path('user/create/', post_user),
    path('user/<id>', get_user),
    path('users/', get_all_users),
]
