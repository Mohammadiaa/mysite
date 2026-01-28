from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from website.models import Contact
from website.forms import NamForm, ContactForm


def index_view(request):
    return render(request, "website/index.html")


def about_view(request):
    return render(request, "website/about.html")


def contact_view(request):
    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            
            return redirect('/')
        else:
            print("Form is NOT valid! Errors found:")
           
    form = ContactForm()
    return render(request, "website/contact.html", {'form': form})


def test_view(request):
    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()

            return HttpResponse('done')
        else:
            return HttpResponse('not valid')
    form = ContactForm()
    return render(request, "myblog/test.html", {'form': form})
