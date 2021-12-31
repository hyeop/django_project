from django.shortcuts import render, redirect
from .models import Board, Reply
from django.utils import timezone
from django.core.paginator import Paginator
from acc.models import User
from django.contrib import messages

def unlikey(request, bpk):
    b = Board.objects.get(id=bpk)
    b.likey.remove(request.user)
    return redirect("board:detail", bpk=bpk)

def likey(request, bpk):
    b = Board.objects.get(id=bpk)
    b.likey.add(request.user)
    return redirect("board:detail", bpk=bpk)

# Create your views here.
def index(request):
    cate = request.GET.get("cate", "")
    kw = request.GET.get("kw","")
    pg = request.GET.get("page", 1)
    
    if cate == "sub":
        b = Board.objects.filter(subject__startswith=kw)
    elif cate == "wri":
        u = User.objects.get(username=kw)
        b = Board.objects.filter(writer=u)
    elif cate == "con":
        b = Board.objects.filter(content__contains=kw)
    else:
        b = Board.objects.all()
    b = b.order_by('-pubdate')  #  레코드들에다 .order_by()    'field'  '-field'
    pag = Paginator(b, 10)
    obj = pag.get_page(pg)
    context = {
        "blist" : obj ,
        "cate":cate,
        "kw":kw
    }
    return render(request, "board/index.html", context)



def dreply(request, bpk, rpk):
    r = Reply.objects.get(id=rpk)
    if request.user == r.replyer:
        r.delete()
    else:
        messages.warning(request, "NO HACK")
    return redirect("board:detail", bpk=bpk)

def creply(request, bpk):
    b = Board.objects.get(id=bpk)
    com = request.POST.get("com")
    Reply(b=b, replyer=request.user, comment=com, pubdate=timezone.now()).save()
    return redirect("board:detail", bpk=bpk)


def update(request, bpk):
    b = Board.objects.get(id=bpk)
    
    if request.user != b.writer:
        messages.warning(request, "NO HACK!!")
        return redirect("board:index")

    if request.method == "POST":
        b.subject = request.POST.get("sub")
        b.content = request.POST.get("con")
        b.save()
        return redirect("board:detail", bpk=bpk)
    context = {
        "bo" : b
    }
    return render(request, "board/update.html", context)

def create(request):
    if request.method == "POST":
        sub = request.POST.get("sub")
        con = request.POST.get("con")
        if sub:
            Board(subject=sub, writer=request.user, content=con, pubdate=timezone.now()).save()
        else:
            messages.info(request, "No subjects can't make board")
        return redirect("board:index")
    return render(request, "board/create.html")



def detail(request, bpk):
    b = Board.objects.get(id=bpk)
    r = b.reply_set.all()
    context = {
        "bo" : b,
        "rlist" : r,
    }
    return render(request, "board/detail.html", context)

def delete(request, bpk):
    b = Board.objects.get(id=bpk)
    if b.writer == request.user:
        b.delete()
    else: # 메세지시간에 넣어주세요!!! (경고창)
        messages.warning(request,"No Hack") 
    return redirect("board:index")

