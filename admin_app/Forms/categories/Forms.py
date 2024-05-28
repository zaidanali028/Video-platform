from django import forms
from admin_app.models import Category

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name', 'status']

    def __init__(self, *args, **kwargs):
        super(CategoryForm, self).__init__(*args, **kwargs)
        self.fields['status'].widget = forms.RadioSelect(choices=self.fields['status'].choices)