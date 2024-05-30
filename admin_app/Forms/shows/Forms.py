# forms.py
from django import forms
from admin_app.models import Show

class ShowForm(forms.ModelForm):
    class Meta:
        model = Show
        fields = ['title', 'status', 'cover_image_url']

    def __init__(self, *args, **kwargs):
        super(ShowForm, self).__init__(*args, **kwargs)
        self.fields['status'].widget = forms.RadioSelect(choices=self.fields['status'].choices)
        # If you want checkboxes for many-to-many field

    def clean_cover_image_url(self):
        cover_image_url = self.cleaned_data.get('cover_image_url')
        if not cover_image_url:
            raise forms.ValidationError("A cover image URL is required.")
        return cover_image_url
 