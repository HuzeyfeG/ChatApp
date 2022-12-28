from rest_framework.response import Response
from rest_framework import status
from .serializers import SignUpSerializer, LogInSerializer, ChatSerializer
from .models import ChatModel
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from rest_framework.decorators import api_view
from django.db.models import Q


# Create your views here.

@api_view(["POST"])
def signupRes(request):
    serializer = SignUpSerializer(data=request.data)
    if serializer.is_valid():
        if User.objects.filter(username=serializer.data["username"]).exists():
            return Response({"message": "Username is taken!"}, status=status.HTTP_401_UNAUTHORIZED)
        elif User.objects.filter(email=serializer.data["email"]).exists():
            return Response({"message": "Email is taken!"}, status=status.HTTP_401_UNAUTHORIZED)
        else:
            user = User.objects.create_user(username=serializer.data["username"], email=serializer.data["email"], password=serializer.data["password"])
            user.save()
            return Response({"message": "Succesfully signed up!"}, status=status.HTTP_200_OK)
    else:
        return Response({"message": "Validation Error!"}, status=status.HTTP_400_BAD_REQUEST)

@api_view(["POST"])
def loginRes(request):
    serializer = LogInSerializer(data=request.data)
    if serializer.is_valid():
        user = authenticate(request, username=serializer.data["username"], password=serializer.data["password"])
        if user is not None:
            return Response(status=status.HTTP_200_OK)
        else:
            return Response({"message": "Username or password not correct!"}, status=status.HTTP_401_UNAUTHORIZED)
    else:
        return Response({"message": "Validation Error!"}, status=status.HTTP_400_BAD_REQUEST)


@api_view(["POST"])
def usersRes(request):
    users = User.objects.values()
    return Response({"message": "", "users": users}, status=status.HTTP_200_OK)

@api_view(["POST"])
def sendchatRes(request):
    serializer = ChatSerializer(data=request.data)
    if serializer.is_valid():
        ChatModel.objects.create(recieverID=serializer.data["recieverID"],  transmitterID=serializer.data["transmitterID"], sendingtime=serializer.data["sendingtime"], content=serializer.data["content"])
        chat = ChatModel.objects.values().filter(recieverID=serializer.data["recieverID"], transmitterID=serializer.data["transmitterID"])
        return Response({"message": "", "chat": chat}, status=status.HTTP_200_OK)
    else:
        return Response({"message": "Validation Error!", "chat": []}, status=status.HTTP_400_BAD_REQUEST)

@api_view(["POST"])
def chatsRes(request):
    chatArray = []
    chats = ChatModel.objects.values().filter(Q(recieverID=request.data["recieverID"]) | Q(transmitterID=request.data["recieverID"]))
    for chat in chats:
        if not chat["transmitterID"] in chatArray and chat["transmitterID"] != request.data["recieverID"]:
            username = User.objects.get(id=chat["transmitterID"]).username
            chatArray.append({"userID": chat["transmitterID"], "username": username})
        elif not chat["recieverID"] in chatArray and chat["recieverID"] != request.data["recieverID"]:
            username = User.objects.get(id=chat["recieverID"]).username
            chatArray.append({"userID": chat["recieverID"], "username": username})
    return Response({"message": "", "chats": [dict(t) for t in {tuple(d.items()) for d in chatArray}]}, status=status.HTTP_200_OK)


@api_view(["POST"])
def chatRes(request, id):
    if request.data["transmitterID"] != None:
        chat = ChatModel.objects.values().filter(Q(recieverID=request.data["recieverID"] , transmitterID=request.data["transmitterID"]) | Q(transmitterID=request.data["recieverID"] , recieverID=request.data["transmitterID"]))
        return Response({"message": "", "chat": chat}, status=status.HTTP_200_OK)
    else:
        return Response({"message": "Validation Error!", "chat": []}, status=status.HTTP_400_BAD_REQUEST)
