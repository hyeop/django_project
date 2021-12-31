from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from .models import User
from django.contrib.auth.hashers import check_password
from django.contrib import messages
# Create your views here.
def index(request):
    return render(request, "acc/index.html")

def userlogin(request):
    if request.method == "POST":
        un = request.POST.get("un")
        pw = request.POST.get("pw")
        user = authenticate(username=un, password=pw)
        if user:
            messages.success(request, "LOGIN SUCCESS")
            login(request, user)
            return redirect("acc:index")
        else:
            messages.error(request, "LOGIN FAIL")
    return render(request, "acc/login.html")

def userlogout(request):
    logout(request)
    return redirect("acc:index")

def signup(request):
    if request.method == "POST":
        un = request.POST.get("un")
        pw = request.POST.get("pw")
        age = request.POST.get("age")
        com = request.POST.get("comment")
        pic = request.FILES.get("pic")
        User.objects.create_user(username=un, password=pw, age=age, comment=com, pic=pic)
        return redirect("acc:login")
    return render(request, "acc/signup.html")
    
def profile(request):
    return render(request, "acc/profile.html")

def delete(request):
    pw = request.POST.get("pw")
    if check_password(pw, request.user.password):
        request.user.delete()
    else: # 삭제하려는데 pw 틀리면 안내해줄것!! (나중에 추가)
        pass
    return redirect("acc:index")

def update(request):
    if request.method == "POST":
        u = request.user
        pw = request.POST.get("pw")
        if pw:
            u.set_password(pw)
        com = request.POST.get("comment")
        u.comment = com
        pic = request.FILES.get("pic")
        if pic:
            u.pic.delete()
            u.pic = pic
        u.save()
        login(request, u)
        return redirect("acc:profile")

    return render(request, "acc/update.html")