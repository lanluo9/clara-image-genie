from django.shortcuts import render
from .models import Image
from .forms import SearchForm
import os
from django.conf import settings
from django.core.files.storage import FileSystemStorage

#def search(request):
def search(request):
    form = SearchForm(request.GET)
    if form.is_valid():
        query = form.cleaned_data['query']
        search_by = form.cleaned_data['search_by']
        # Use the query and search_by variables to perform your search
        # ...
    else:
        form = SearchForm()
    return render(request, 'search.html', {'form': form})

    # query = None
    # images = []
    # if 'query' in request.GET:
    #     form = SearchForm(request.GET)
    #     if form.is_valid():
    #         query = form.cleaned_data['query']
    #         images = Image.objects.filter(title__icontains=query)
    # else:
    #     form = SearchForm()
    # return render(request, 'search.html', {'form': form, 'query': query, 'images': images})

def home(request):
    return render(request, 'home.html')

def upload_folder(request):
    if request.method == 'POST':
        files = request.FILES.getlist('folder')
        fs = FileSystemStorage()
        for file in files:
            filename = fs.save(file.name, file)
        return render(request, 'upload.html', {'uploaded_files': files})
    return render(request, 'upload.html')



def display_images(request):
    image_list = []
    for filename in os.listdir(os.path.join(settings.MEDIA_ROOT, 'images')):
        if filename.endswith('.jpg') or filename.endswith('.jpeg') or filename.endswith('.png'):
            image_list.append(filename)
    return render(request, 'search.html', {'image_list': image_list})
