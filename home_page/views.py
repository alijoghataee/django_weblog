from django.shortcuts import render


def home_page_view(request):
    return render(request, 'home_page/home.html')


def contact_us_view(request):
    return render(request, 'contact_us/contact_us.html')

