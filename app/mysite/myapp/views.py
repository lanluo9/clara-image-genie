from django.shortcuts import render
from .models import Image
from .forms import SearchForm
import os
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.shortcuts import render, redirect
from .forms import ImageUploadForm


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



def display_images(request):
    #returns all images change to display select array of images
    images = Image.objects.all()
    return render(request, 'display.html', {'images': images})

def upload_images(request):
    if request.method == 'POST':
        form = ImageUploadForm(request.POST, request.FILES)
        if form.is_valid():
            uploaded_folder = request.FILES['folder']
            fs = FileSystemStorage()
            name = fs.save(uploaded_folder.name, uploaded_folder)
            folder_path = fs.path(name)
            for filename in os.listdir(folder_path):
                file_path = os.path.join(folder_path, filename)
                file = Image(file_path=file_path, title=filename)
                file.save()
            return redirect('success')
    else:
        form = ImageUploadForm()
    return render(request, 'upload.html', {'form': form})

def home(request):
    return render(request, 'home.html')