from django import forms
from database.models import BLOG
from django.contrib.auth.models import User


class BlogForm(forms.ModelForm):
    class Meta:
        model = BLOG
        fields = ['blogCaption', 'blogData', 'image']

    def __init__(self, *args, **kwargs):
        super(BlogForm,self).__init__(*args, **kwargs)




