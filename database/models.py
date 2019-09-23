from django.db import models
from django.utils.html import mark_safe
from RegLogin.models import PROFILE
from django.contrib.auth.models import User
from django import forms

# Create your models here.


class CITY(models.Model):
    cityName = models.CharField(max_length=200)
    longitude = models.CharField(max_length=30, blank=True)
    latitude = models.CharField(max_length=30, blank=True)
    description = models.CharField(max_length=300, blank=True)
    image = models.ImageField(upload_to='allImages/', default='noimage.jpg' )

    def image_tag(self):
        return mark_safe('<img src="{}" width="100" height="50" />'.format(str(self.image.url)))

    image_tag.short_description = 'Image'

    '''def __str__(self):
        return str(self.pk) + "," + self.cityName + "," + self.longitude + "," \
               + self.latitude + "," + self.image'''


class HOTEL(models.Model):
    hotelName = models.CharField(max_length=200)
    image = models.ImageField( upload_to='allImages/' )
    longitude = models.CharField(max_length=30, blank=True)
    latitude = models.CharField(max_length=30, blank=True)
    cityID = models.ForeignKey(CITY, on_delete=models.CASCADE )

    def image_tag(self):
        return mark_safe('<img src="{}" width="100" height="50" />'.format(str(self.image.url)))
    image_tag.short_description = 'Image'
    '''def __str__(self):
        return str(self.pk) + "," + self.hotelName + "," + self.image + "," \
               + self.longitude + "," + self.latitude + "," + str(self.cityID)'''


class GROUP(models.Model):
    groupName = models.CharField(max_length=100)
    '''def __str__(self):
        return str(self.pk) + "," + self.groupName'''


class BLOG(models.Model):
    blogCaption = models.CharField(max_length=200)
    blogPostDate = models.DateField( auto_now_add=True )
    blogData = models.TextField(max_length=2000)
    userID = models.ForeignKey(PROFILE, on_delete=models.CASCADE, null=True)
    image = models.ImageField( upload_to='allImages/', default='noimage.jpg' )

    def image_tag(self):
        return mark_safe('<img src="{}" width="100" height="50" />'.format(str(self.image.url)))

    image_tag.short_description = 'Image'
    '''def __str__(self):
        return str(self.pk) + "," + self.blogCaption + "," + str(self.blogPostDate)+","+self.blogData+","\
               +str(self.guideID)+","+str(self.userID) + "," + self.images'''


class SPOT(models.Model):
    spotName = models.CharField(max_length=75)
    spotInfo = models.CharField(max_length=2000)
    cityID = models.ForeignKey(CITY, on_delete=models.CASCADE)
    longitude = models.CharField(max_length=30, blank=True)
    latitude = models.CharField(max_length=30, blank=True)
    totalVisitTime = models.CharField(max_length=30, blank=True)
    openTime = models.CharField(max_length=30, blank=True)
    closeTime = models.CharField(max_length=30, blank=True)
    holiday = models.CharField(max_length=30,blank=True)
    image = models.ImageField(upload_to='allImages/', default='noimage.jpg')

    def image_tag(self):
        return mark_safe('<img src="{}" width="100" height="50" />'.format(str(self.image.url)))

    image_tag.short_description = 'Image'
    '''def __str__(self):
        return str(self.pk) + "," + self.spotName + "," + self.spotInfo + "," + str(self.cityID) + "," \
               + self.longitude + "," + self.latitude + "," + self.touristSpotImages'''


class ACTIVITY(models.Model):
    activityName = models.CharField(max_length=50)
    activityCost = models.IntegerField(default= -2147483647)
    image = models.ImageField( upload_to='allImages/' )

    def image_tag(self):
        return mark_safe('<img src="{}" width="100" height="50" />'.format(str(self.image.url)))

    image_tag.short_description = 'Image'

    '''def __str__(self):
        return str(self.pk) + "," + self.activityName + "," + str(self.activityCost) + "," + self.activityImages'''


class PREFERENCE(models.Model):
    prefName = models.CharField(max_length=50)
    image = models.ImageField(upload_to='allImages/' )

    def image_tag(self):
        return mark_safe('<img src="{}" width="100" height="50" />'.format(str(self.image.url)))

    image_tag.short_description = 'Image'
    '''def __str__(self):
        return str(self.pk) + "," + self.preferenceName + "," + self.preferenceImages'''


class TOURINFO(models.Model):
    userID = models.ForeignKey(PROFILE, on_delete=models.CASCADE, blank=True )
    startDate = models.CharField(max_length=20, blank=True)
    endDate = models.CharField(max_length=20, blank=True)
    startTime = models.CharField(max_length=20, blank=True)
    endTime = models.CharField(max_length=20, blank=True)
    startLocation = models.CharField(max_length=50, blank=True)
    context = models.CharField(max_length = 1000, blank = True )
    '''def __str__(self):
        return str(self.pk) + "," + str(self.groupID) + "," + str(self.userID)+","\
               +str(self.guideID)+","+str(self.startDate)+","+str(self.endDate)++","\
               +str(self.dailyTravelTime)+","+str(self.description) + "," + str(self.finished)'''

class SPOTREVIEW(models.Model):
    userID = models.ForeignKey(PROFILE, on_delete=models.CASCADE)
    spotID = models.ForeignKey(SPOT, on_delete=models.CASCADE)
    rating = models.CharField(max_length=5, blank=True, default='0')
    review = models.CharField(max_length=300, blank=True, default='-')

class TOURINFOGROUP(models.Model):
    tourID = models.ForeignKey(TOURINFO, on_delete=models.CASCADE)
    groupID = models.ForeignKey(GROUP, on_delete=models.CASCADE)
    '''def __str__(self):
        return str(self.pk) + "," + str(self.tourID) + "," + str(self.groupID)'''


class TOURINFOACTIVITY(models.Model):
    activityID = models.ForeignKey(ACTIVITY, on_delete=models.CASCADE)
    tourID = models.ForeignKey(TOURINFO, on_delete=models.CASCADE)
    '''def __str__(self):
        return str(self.pk) + "," + str(self.tourID) + "," + str(self.activityID)'''


class TOURINFOSPOT(models.Model):
    spotID = models.ForeignKey(SPOT, on_delete=models.CASCADE)
    tourID = models.ForeignKey(TOURINFO, on_delete=models.CASCADE)
    '''def __str__(self):
        return str(self.pk) + "," + str(self.tourID) + "," + str(self.spotID)'''


class PROFILEGROUP(models.Model):
    userID = models.ForeignKey(PROFILE, on_delete=models.CASCADE)
    groupID = models.ForeignKey(GROUP, on_delete=models.CASCADE)
    '''def __str__(self):
        return str(self.pk) + "," + str(self.userID) + "," + str(self.groupID)'''
        
class GROUPMESSAGE(models.Model):
    groupID = models.ForeignKey(GROUP, on_delete=models.CASCADE)
    userName=models.CharField(max_length=50)
    message=models.CharField(blank=True, max_length=1000)
    time=models.CharField(max_length=50, blank=True)

class GUIDETOURINFO(models.Model):
    guideID = models.ForeignKey(PROFILE, on_delete=models.CASCADE)  # Did Edit Here. Guide to PROFILE
    tourID = models.ForeignKey(TOURINFO, on_delete=models.CASCADE)
    '''def __str__(self):
        return str(self.pk) + "," + str(self.guideID) + "," + str(self.tourID)'''


class CITYTOURINFO(models.Model):
    cityID = models.ForeignKey(CITY, on_delete=models.CASCADE)
    tourID = models.ForeignKey(TOURINFO, on_delete=models.CASCADE)
    '''def __str__(self):
        return str(self.pk) + "," + str(self.tourID) + "," + str(self.cityID)'''


class PREFERENCETOURINFO(models.Model):
    preferenceID = models.ForeignKey(PREFERENCE, on_delete=models.CASCADE)
    tourID = models.ForeignKey(TOURINFO, on_delete=models.CASCADE)
    '''def __str__(self):
        return str(self.pk) + "," + str(self.tourID) + "," + str(self.preferenceID)'''


class CITYPROFILE(models.Model):
    cityID = models.ForeignKey(CITY, on_delete=models.CASCADE)
    userID = models.ForeignKey(PROFILE, on_delete=models.CASCADE)    # Did Edit Here. Guide to PROFILE
    '''def __str__(self):
        return str(self.pk) + "," + str(self.cityID) + "," + str(self.guideID)'''


class SPOTACTIVITY(models.Model):
    activityID = models.ForeignKey(ACTIVITY, on_delete=models.CASCADE)
    spotID = models.ForeignKey(SPOT, on_delete=models.CASCADE)
    description = models.CharField(max_length=1000)
    image = models.ImageField( upload_to='allImages/' )
    def image_tag(self):
        return mark_safe('<img src="{}" width="100" height="50" />'.format(str(self.image.url)))
    image_tag.short_description = 'Image'
    '''def __str__(self):
        return str(self.pk) + "," + str(self.spotID) + "," + str(self.activityID) + "," \
               + self.description + "," + self.image'''


class SPOTPREFERENCE(models.Model):
    preferenceID = models.ForeignKey(PREFERENCE, on_delete=models.CASCADE)
    spotID = models.ForeignKey(SPOT, on_delete=models.CASCADE)
    def image_tag(self):
        return mark_safe('<img src="{}" width="100" height="50" />'.format(str(self.image.url)))
    image_tag.short_description = 'Image'
    '''def __str__(self):
        return str(self.pk) + "," + str(self.spotID) + "," + str(self.preferenceID) + "," +\
               self.description + "," + self.image'''


class CITYPREFERENCE(models.Model):
    cityID = models.ForeignKey(CITY, on_delete=models.CASCADE)
    preferenceID = models.ForeignKey(PREFERENCE, on_delete=models.CASCADE)
    '''def __str__(self):
        return str(self.pk) + "," + str(self.cityID) + "," \
               + str(self.preferenceID)'''


class TOURINFOPREFERENCE(models.Model):
    tourID = models.ForeignKey(TOURINFO, on_delete=models.CASCADE)
    preferenceID = models.ForeignKey(PREFERENCE, on_delete=models.CASCADE)
    '''def __str__(self):
        return str(self.pk) + "," + str(self.tourID) + "," + str(self.preferenceID)'''


class HOTELTOURINFO(models.Model):
    tourID = models.ForeignKey(TOURINFO, on_delete=models.CASCADE)
    hotelID = models.ForeignKey(HOTEL, on_delete=models.CASCADE)
    '''def __str__(self):
        return str(self.pk) + "," + str(self.tourID) + "," + str(self.hotelID)'''


