from django.shortcuts import render
from .models import Image
from .forms import SearchForm
import os
from django.conf import settings

def search(request):
    query = None
    images = []
    if 'query' in request.GET:
        form = SearchForm(request.GET)
        if form.is_valid():
            query = form.cleaned_data['query']
            images = Image.objects.filter(title__icontains=query)
    else:
        form = SearchForm()
    return render(request, 'search.html', {'form': form, 'query': query, 'images': images})

def home(request):
    return render(request, 'home.html')


def display_images(request):
    image_list = []
    for filename in os.listdir(os.path.join(settings.MEDIA_ROOT, 'images')):
        if filename.endswith('.jpg') or filename.endswith('.jpeg') or filename.endswith('.png'):
            image_list.append(filename)
    return render(request, 'search.html', {'image_list': image_list})
