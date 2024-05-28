from django import forms
from admin_app.models import Genre

class GenreForm(forms.ModelForm):
    class Meta:
        model = Genre
        fields = ['name', 'status']
    

    # overriding the default selectfield for status into a rado  field
    def __init__(self, *args, **kwargs):
        super(GenreForm, self).__init__(*args, **kwargs)
        self.fields['status'].widget = forms.RadioSelect(choices=self.fields['status'].choices)
       