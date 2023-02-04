from django import forms

# class SearchForm(forms.Form):
#     query = forms.CharField(label='Search', max_length=100)

class SearchForm(forms.Form):
    SEARCH_CHOICES = [
        ('Image description', 'Image description'),
        ('OCR', 'OCR'),
        ('Object detection', 'Object detection'),
    ]
    query = forms.CharField(label='Search', max_length=100)
    search_by = forms.ChoiceField(choices=SEARCH_CHOICES)