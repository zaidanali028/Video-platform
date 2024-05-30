from django import forms
from admin_app.models import Video

class VideoForm(forms.ModelForm):
    class Meta:
        model = Video
        fields = ['title', 'description', 'categories', 'genres', 'status', 'thumb_image_url','video_url','show']

    def __init__(self, *args, **kwargs):
        super(VideoForm, self).__init__(*args, **kwargs)
        self.fields['status'].widget = forms.RadioSelect(choices=self.fields['status'].choices)

    def clean_thumb_image_url(self):
        thumb_image_url = self.cleaned_data.get('thumb_image_url')
        if not thumb_image_url:
            raise forms.ValidationError("An image thumb is required.")
        return thumb_image_url
    
    
    

    def clean_video_url(self):
        video_url = self.cleaned_data.get('video_url')
        if not video_url:
            raise forms.ValidationError("A video file is required.")
        return video_url