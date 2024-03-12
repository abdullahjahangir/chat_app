from django.contrib import admin
from django.urls import path

from .views import home, about, login_user, logout_user, register_user, chat
from .views import HomeView, AboutView, LoginView, LogoutView, RegisterView, ChatView

urlpatterns = [
    path("home/", HomeView.as_view(), name="home"),
    path("chat/<int:pk>/", ChatView.as_view(), name="chat"),
    path("about/", AboutView.as_view(), name="about"),
    path("login/", LoginView.as_view(), name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("register/", RegisterView.as_view(), name="register"),
    # Function Base Views
    # path("home/", home, name="home"),
    # path("chat/<int:pk>/", chat, name="chat"),
    # path("about/", about, name="about"),
    # path("login/", login_user, name="login"),
    # path("logout/", logout_user, name="logout"),
    # path("register/", register_user, name="register"),
]
