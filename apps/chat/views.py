from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib.auth import login, logout, mixins
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views import View
from .decorators import unauthenticated_user
from .models import ChatRoom, Message
from .forms import MessageForm


class HomeView(mixins.LoginRequiredMixin, View):
    login_url = "login"

    def get(self, request):
        chat_rooms = ChatRoom.objects.filter(users=request.user).prefetch_related(
            "users"
        )
        return render(request, "chat/home.html", context={"chat_rooms": chat_rooms})


class ChatView(mixins.LoginRequiredMixin, View):
    login_url = "login"

    def get(self, request, pk):
        form = MessageForm()
        chat_room = (
            ChatRoom.objects.get(id=pk)
            if ChatRoom.objects.filter(id=pk).exists()
            else None
        )
        if chat_room:
            messages = Message.objects.filter(chat_room=chat_room).order_by("timestamp")
            return render(
                request,
                "chat/chat.html",
                context={"room": chat_room, "messages": messages, "form": form},
            )
        else:
            return HttpResponseRedirect(reverse("home"))

    def post(self, request, pk):
        chat_room = (
            ChatRoom.objects.get(id=pk)
            if ChatRoom.objects.filter(id=pk).exists()
            else None
        )
        form = MessageForm(data=request.POST)
        if chat_room and form.is_valid():
            content = form.cleaned_data["content"]
            Message.objects.create(
                sender=request.user, chat_room=chat_room, content=content
            )
            return redirect("chat", pk=pk)
        else:
            return HttpResponseRedirect(reverse("home"))


class AboutView(View):
    @method_decorator(login_required(login_url="login"))
    def get(self, request):
        return render(request, "chat/about.html")


class LoginView(View):
    @method_decorator(unauthenticated_user)
    def get(self, request):
        form = AuthenticationForm()
        return render(request, "chat/login.html", context={"form": form})

    @method_decorator(unauthenticated_user)
    def post(self, request):
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect("home")
        return render(request, "chat/login.html", context={"form": form})


class RegisterView(View):
    @method_decorator(unauthenticated_user)
    def get(self, request):
        form = UserCreationForm()
        return render(request, "chat/register.html", context={"form": form})

    @method_decorator(unauthenticated_user)
    def post(self, request):
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("login")
        return render(request, "chat/register.html", context={"form": form})


class LogoutView(View):
    def get(self, request):
        logout(request)
        return redirect("login")


""" Function Base Views """


@login_required(login_url="login")
def home(request):
    chat_rooms = ChatRoom.objects.filter(users=request.user).prefetch_related("users")
    return render(request, "chat/home.html", context={"chat_rooms": chat_rooms})


@login_required(login_url="login")
def chat(request, pk):
    if request.method == "GET":
        form = MessageForm()
        chat_room = (
            ChatRoom.objects.get(id=pk)
            if ChatRoom.objects.filter(id=pk).exists()
            else None
        )
        if chat_room:
            messages = Message.objects.filter(chat_room=chat_room).order_by("timestamp")
            return render(
                request,
                "chat/chat.html",
                context={"room": chat_room, "messages": messages, "form": form},
            )
        else:
            return HttpResponseRedirect(reverse("home"))
    elif request.method == "POST":
        chat_room = (
            ChatRoom.objects.get(id=pk)
            if ChatRoom.objects.filter(id=pk).exists()
            else None
        )
        form = MessageForm(data=request.POST)
        if chat_room and form.is_valid():
            content = form.cleaned_data["content"]
            Message.objects.create(
                sender=request.user, chat_room=chat_room, content=content
            )
            return redirect("chat", pk=pk)
        else:
            return HttpResponseRedirect(reverse("home"))


@login_required(login_url="login")
def about(request):
    return render(request, "chat/about.html")


@unauthenticated_user
def login_user(request):
    form = AuthenticationForm()
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect("home")
    return render(request, "chat/login.html", context={"form": form})


@unauthenticated_user
def register_user(request):
    form = UserCreationForm()
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("login")
    return render(request, "chat/register.html", context={"form": form})


def logout_user(request):
    logout(request)
    return redirect("login")


def custom_404_view(request, *args, **kwargs):
    return render(request, "404.html", {})
