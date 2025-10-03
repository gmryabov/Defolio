from django.shortcuts import render
from .models import Slider

def home(request):
    context = {
        'title': 'Главная',
        'sliders': Slider.objects.filter(is_active=True).order_by('sort_order'),
    }
    return render(request, 'root/index.html', context=context)