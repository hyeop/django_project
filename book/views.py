from django.shortcuts import redirect, render
from .models import Book
from django.contrib import messages

def delete(request, bpk):
    b = Book.objects.get(id=bpk)
    if request.user == b.user:
        b.delete()
    else:
        messages.warning(request, "NO Hack!")
    return redirect("book:index")


def create(request):
    if request.method == "POST":
        sn = request.POST.get("sname")
        su = request.POST.get("surl")
        co = request.POST.get("com")
        im = bool(request.POST.get("impo"))
        Book(user=request.user, site_name=sn, site_url=su, comment=co, impo=im).save()
        return redirect("book:index")
    return render(request, "book/create.html")

# Create your views here.
def index(request):
    b = request.user.book.all()
    context = {
        "blist":b
    }
    return render(request, "book/index.html", context)