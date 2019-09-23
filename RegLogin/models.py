from django.db import models
from django.contrib.auth.models import User
from django.utils.html import mark_safe

class PROFILE(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE,null=True)
#first_name, last_name, password, username, email
    Phone = models.PositiveIntegerField()
    Address = models.CharField(max_length=1000)
    is_Guide=models.BooleanField()
    image=models.ImageField(upload_to="allImages/", default='noimage.jpg' )
    about=models.CharField(max_length=1000, blank=True)
    gender=models.CharField(max_length=10, blank=True)

    def image_tag(self):
        return mark_safe('<img src="{}" width="100" height="50" />'.format(str(self.image.url)))

    image_tag.short_description = 'Image'

