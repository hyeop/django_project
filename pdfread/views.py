from django.shortcuts import render
import pdfplumber

# Create your views here.
def index(request):
    context = {}
    if request.method == "POST":
        p = request.FILES.get("pdf")
        pdf = pdfplumber.open(p)
        text = ""
        for i in range(len(pdf.pages)):
            page = pdf.pages[i]
            text += "\n" + "="*30 + f"\n{i+1} PAGE TEXT\n" + "="*30 + "\n"
            text += page.extract_text()
            
        pdf.close()
        context["t"] = text
    return render(request, "pdfread/index.html",context)