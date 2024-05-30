# forms.py
from django import forms
from admin_app.models import Show
from  admin_app.models import Category,Genre
class ShowForm(forms.ModelForm):
    class Meta:
        model = Show
        fields = ['title', 'status', 'cover_image_url','categories', 'genres', ]

    def __init__(self, *args, **kwargs):
        # so when the form object is initialized, I want to override these actions...
        super(ShowForm, self).__init__(*args, **kwargs)
        
        # 1. the widget of the status field must be changed from the default select to radio field
        self.fields['status'].widget = forms.RadioSelect(choices=self.fields['status'].choices)
        
        # 2. categories and genres query set must only return active records
        self.fields['categories'].queryset = Category.objects.filter(status='active')
        self.fields['genres'].queryset = Genre.objects.filter(status='active')


    def clean_cover_image_url(self):
        cover_image_url = self.cleaned_data.get('cover_image_url')
        if not cover_image_url:
            raise forms.ValidationError("A cover image URL is required.")
        return cover_image_url
 