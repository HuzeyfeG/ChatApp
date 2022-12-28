from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.views import View
import requests
from datetime import datetime

# Create your views here.


class IndexView(View):
    def get(self, request):
        if request.user.is_authenticated:
            res = requests.post("http://localhost:8000/api/chats",data={"recieverID": str(request.user.id)})
            if res.status_code == 200:
                return render(request, "index.html", {"chats": res.json()["chats"]})
            else:
                return redirect("index")
        else:
            return render(request, "index.html", {"message": "Welcome Strangerr! Login or Signup"})

class LoginView(View):
    def get(self, request):
        if request.user.is_authenticated:
            return redirect("index")
        else:
            return render(request, "login.html")
    def post(self, request):
        username = request.POST["username"]
        password = request.POST["password"]
        res = requests.post("http://localhost:8000/api/login", data={"username": username, "password": password} )
        if res.status_code == 200:
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect("index")
        else:
            return render(request, "login.html", {"message": res.json()["message"]})

class SignupView(View):
    def get(self, request):
        if request.user.is_authenticated:
            return redirect("index")
        else:
            return render(request, "signup.html")
    def post(self, request):
        username = request.POST["username"]
        email = request.POST["email"]
        password = request.POST["password"]
        res = requests.post("http://localhost:8000/api/signup", data={"username": username, "email": email, "password": password})
        if res.status_code == 200:
            return render(request, "signup.html", {"message": res.json()["message"]})
        else:
            return render(request, "signup.html", {"message": res.json()["message"]})

class LogoutView(View):
    def get(self, request):
        logout(request)
        return redirect("login")

class NewChatView(View):
    def get(self, request):
        if request.user.is_authenticated:
            res = requests.post("http://localhost:8000/api/users")
            if res.status_code == 200 :
                return render(request, "newchat.html", {"users": res.json()["users"]})
            else:
                return redirect("index")
        else:
            return render(request, "login.html")
    def post(self, request):
        if request.user.is_authenticated:
            transmitterID = request.POST["submit"]
            return redirect("chat", transmitterID)
        else:
            return render(request, "login.html")

class ChatView(View):
    def get(self, request, id):
        if request.user.is_authenticated:
            res = requests.post("http://localhost:8000/api/chat/" + str(id), data={"recieverID": str(request.user.id), "transmitterID": str(id)})
            return render(request, "chat.html", {"message":"", "transmitterID": str(id), "recieverID": str(request.user.id), "chat": res.json()["chat"]})
        else:
            return render(request, "login.html")
    def post(self, request, id):
        if request.user.is_authenticated:
            content = request.POST["content"]
            recieverID = request.user.id
            transmitterID = id
            sendingTime = datetime.now().strftime("%D %H:%M:%S")
            res = requests.post("http://localhost:8000/api/sendchat", data={"recieverID": recieverID,  "transmitterID": transmitterID, "sendingtime": sendingTime, "content": content})
            if res.status_code == 200:
                return redirect("chat", transmitterID)
            else:
                return render(request, "chat.html", {"message": res.json()["message"], "chat": res.json()["chat"]})
        else:
            return render(request, "login.html")

