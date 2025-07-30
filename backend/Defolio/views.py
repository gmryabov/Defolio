from django.shortcuts import render

def home(request):
    context = {
        'title': 'Главная'
    }
    return render(request, 'root/index.html', context=context)