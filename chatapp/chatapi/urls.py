from django.urls import path
from . import views


urlpatterns = [
    path("login", views.loginRes),
    path("signup", views.signupRes),
    path("users", views.usersRes),
    path("chat/<int:id>", views.chatRes),
    path("chats", views.chatsRes),
    path("sendchat", views.sendchatRes)
]