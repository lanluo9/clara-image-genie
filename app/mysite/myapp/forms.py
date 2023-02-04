from django import forms
from .models import Image

class SearchForm(forms.Form):
    SEARCH_CHOICES = [
        ('Image description', 'Image description'),
        ('OCR', 'OCR'),
        ('Object detection', 'Object detection'),
    ]
    query = forms.CharField(label='Search', max_length=100)
    search_by = forms.ChoiceField(choices=SEARCH_CHOICES)


class ImageUploadForm(forms.ModelForm):
    class Meta:
        model = Image
        fields = ['file_name', 'file_path']