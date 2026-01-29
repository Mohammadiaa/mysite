from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from website.models import Contact
from website.forms import NamForm, ContactForm, newsletterForm
from django.contrib import messages

def index_view(request):
    return render(request, "website/index.html")


def about_view(request):
    return render(request, "website/about.html")


def contact_view(request):
    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            messages.add_message(request,messages.SUCCESS, "your ticket submited successfully")
        else:
            messages.add_message(request,messages.ERROR, "your ticket didnot submited")

            return redirect('/')
        
    else:
        messages.error(request, 'Please correct the errors in the form')


    form = ContactForm()
    return render(request, "website/contact.html", {'form': form})


def newsletter_view(request):
    if request.method == 'POST':
        form = newsletterForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/')  # بازگشت به صفحه اصلی، یا مسیر دلخواه
        else:
            print("--- Newsletter Validation Failed ---")
            print(form.errors)
            return redirect('/')
 


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
