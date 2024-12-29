from django.shortcuts import redirect, render
from .models import Connection, Message
from django.contrib.auth import authenticate, login
from django.http import HttpResponse
from django.db.models import Q


def index(request):
    user = request.user
    print('user.is_authenticated')
    if not user.is_authenticated:
        return redirect("login")
    connections = Connection.objects.filter(Q(user1=user) | Q(user2=user))
    return render(request, "chat/index.html", {"connections": connections, 'user': user})

def login_view(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect("chat")
        else:
            return HttpResponse("Invalid credentials")
    return render(request, "auth/login.html")

def chat(request, connection_id):
    connection = Connection.objects.get(id=connection_id)
    messages = Message.objects.filter(connection=connection)
    return render(request, "chat/chat.html" , {"connection": connection, 'user': request.user, 'messages': messages})