from django.shortcuts import redirect, render
from .models import Topic, Choice
from django.utils import timezone
# Create your views here.

def create(request):
    if request.method == "POST":
        sub = request.POST.get("sub")
        con = request.POST.get("con")
        t = Topic(subject=sub, writer=request.user, pubdate=timezone.now(), content=con)
        names = request.POST.getlist("cho_name")
        coms = request.POST.getlist("cho_com")
        pics = request.FILES.getlist("cho_pic")
        t.save()
        for name, com, pic in zip(names, coms, pics):
            Choice(subject=t, name=name, pic=pic, comment=com).save()
        return redirect("vote:index")
    return render(request, "vote/create.html")

def cancel(request, tpk):
    t = Topic.objects.get(id=tpk)
    u = request.user
    if u in t.voter.all():
        t.voter.remove(u)
        u.choice_set.get(subject=t).choicer.remove(u)
    return redirect("vote:detail", tpk=tpk)

def index(request):
    t = Topic.objects.all()
    context = {
        "tlist" : t
    }
    return render(request, "vote/index.html", context)

def detail(request, tpk):
    t = Topic.objects.get(id=tpk)
    c = t.choice_set.all()
    context = {
        "to" : t,
        "clist" : c
    }
    return render(request, "vote/detail.html", context)

def vote(request, tpk):
    t = Topic.objects.get(id=tpk)
    if not request.user in t.voter.all():
        t.voter.add(request.user)
        cho = request.POST.get("cho")
        c = Choice.objects.get(id=cho)
        c.choicer.add(request.user)
    return redirect("vote:detail", tpk=tpk)