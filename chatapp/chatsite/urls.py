from django.urls import path
from . import views


urlpatterns = [
    path("", views.IndexView.as_view(), name="index"),
    path("index", views.IndexView.as_view(), name="index"),
    path("login", views.LoginView.as_view(), name="login"),
    path("signup", views.SignupView.as_view(), name="signup"),
    path("logout", views.LogoutView.as_view(), name="logout"),
    path("newchat", views.NewChatView.as_view(), name="newchat"),
    path("chat/<int:id>", views.ChatView.as_view(), name="chat"),
]