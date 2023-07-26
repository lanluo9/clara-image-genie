from django.shortcuts import render
from .models import Image
from .forms import SearchForm
import os
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.shortcuts import render, redirect
from .forms import ImageUploadForm
from .backend.image_content_extract import img2text
from django.views.decorators.csrf import csrf_protect


@csrf_protect
def search(request):
    print('Request method is ' + str(request.method))
    form = SearchForm()
    return render(request, 'search.html', {'form': form})


def display_images(request):
    #returns all images change to display select array of images
    print('-----request.method is ' + str(request.method) + '-----')
    if request.method == 'POST': # should use POST for submission of sensitive / long data: https://stackoverflow.com/questions/3477333/what-is-the-difference-between-post-and-get
        form = SearchForm(request.POST)
        print(form.errors)
        if form.is_valid():
            print(f'---------form keys are {form.cleaned_data.keys()}---------')
            query = form.cleaned_data['query']
            search_by = form.cleaned_data['search_type']
            print('---------query is ' + query + '---------')
            print('---------search_by is ' + search_by + '---------')
    image_paths = img2text(search_by, query)
    images = [Image(file_path=p.rsplit('app/mysite')[1], file_name=os.path.basename(p)) for p in image_paths]
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