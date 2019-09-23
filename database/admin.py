from django.contrib import admin
from .models import *
# Register your models here.

'''
class PROFILEAdmin(admin.ModelAdmin):
    list_display = ['id', 'email', 'firstName', 'lastName', 'password', 'cityID',
                    'address', 'contact', 'image_tag', 'about', 'gender','isGuide']
'''


class SPOTREVIEWAdmin(admin.ModelAdmin):
    list_display = ['id', 'userID', 'spotID', 'rating', 'review']

admin.site.register(SPOTREVIEW, SPOTREVIEWAdmin)

class GROUPAdmin(admin.ModelAdmin):
    list_display = ['id', 'groupName']

class GROUPMESSAGEAdmin(admin.ModelAdmin):
    list_display = ['id','groupID', 'userName', 'message', 'time']

class CITYAdmin(admin.ModelAdmin):
    list_display = ['id', 'cityName', 'longitude', 'latitude', 'description', 'image_tag']


class HOTELAdmin(admin.ModelAdmin):
    list_display = ['id', 'hotelName', 'longitude', 'latitude', 'image_tag', 'cityID']


class BLOGAdmin(admin.ModelAdmin):
    list_display = ['id', 'blogCaption', 'blogPostDate', 'blogData', 'userID', 'image_tag']


class PREFERENCEAdmin(admin.ModelAdmin):
    list_display = ['id', 'prefName', 'image_tag']


class ACTIVITYAdmin(admin.ModelAdmin):
    list_display = ['id', 'activityName', 'activityCost', 'image_tag']


class SPOTAdmin(admin.ModelAdmin):
    list_display = ['id', 'spotName', 'spotInfo', 'cityID', 'longitude', 'latitude', 'totalVisitTime', 'openTime', 'closeTime','holiday' ,'image_tag']


class TOURINFOAdmin(admin.ModelAdmin):
    list_display = ['id', 'userID', 'startDate', 'endDate', 'startTime', 'endTime', 'startLocation', 'context']


admin.site.register(GROUP, GROUPAdmin)
admin.site.register(CITY, CITYAdmin)
admin.site.register(HOTEL, HOTELAdmin)
admin.site.register(BLOG, BLOGAdmin)
admin.site.register(PREFERENCE, PREFERENCEAdmin)
admin.site.register(ACTIVITY, ACTIVITYAdmin)
admin.site.register(SPOT, SPOTAdmin)
admin.site.register(TOURINFO, TOURINFOAdmin)
admin.site.register(GROUPMESSAGE, GROUPMESSAGEAdmin)


class PROFILEGROUPAdmin(admin.ModelAdmin):
    list_display = ['id', 'userID', 'groupID']


class HOTELTOURINFOAdmin(admin.ModelAdmin):
    list_display = ['id', 'tourID', 'hotelID']


class CITYPROFILEAdmin(admin.ModelAdmin):
    list_display = ['id', 'cityID']


class GUIDETOURINFOAdmin(admin.ModelAdmin):
    list_display = ['id', 'guideID', 'tourID']


class CITYTOURINFOAdmin(admin.ModelAdmin):
    list_display = ['id', 'tourID', 'cityID']


class PREFERENCETOURINFOAdmin(admin.ModelAdmin):
    list_display = ['id','tourID', 'preferenceID']


class TOURINFOSPOTAdmin(admin.ModelAdmin):
    list_display = ['id', 'tourID', 'spotID']


class CITYPREFERENCEAdmin(admin.ModelAdmin):
    list_display = ['id', 'cityID', 'preferenceID']


class SPOTPREFERENCEAdmin(admin.ModelAdmin):
    list_display = ['id', 'spotID', 'preferenceID']


class TOURINFOPREFERENCEAdmin(admin.ModelAdmin):
    list_display = ['id', 'tourID', 'preferenceID']


class SPOTACTIVITYAdmin(admin.ModelAdmin):
    list_display = ['id', 'spotID', 'activityID', 'description', 'image_tag']


class TOURINFOACTIVITYAdmin(admin.ModelAdmin):
    list_display = ['id', 'tourID', 'activityID']


class TOURINFOGROUPAdmin(admin.ModelAdmin):
    list_display = ['id', 'tourID', 'groupID']


admin.site.register(PROFILEGROUP, PROFILEGROUPAdmin)
admin.site.register(HOTELTOURINFO, HOTELTOURINFOAdmin)
admin.site.register(CITYPROFILE, CITYPROFILEAdmin)
admin.site.register(GUIDETOURINFO, GUIDETOURINFOAdmin)
admin.site.register(CITYTOURINFO, CITYTOURINFOAdmin)
admin.site.register(PREFERENCETOURINFO, PREFERENCETOURINFOAdmin)
admin.site.register(TOURINFOSPOT, TOURINFOSPOTAdmin)
admin.site.register(CITYPREFERENCE, CITYPREFERENCEAdmin)
admin.site.register(SPOTPREFERENCE, SPOTPREFERENCEAdmin)
admin.site.register(TOURINFOPREFERENCE, TOURINFOPREFERENCEAdmin)
admin.site.register(SPOTACTIVITY, SPOTACTIVITYAdmin)
admin.site.register(TOURINFOACTIVITY, TOURINFOACTIVITYAdmin)
admin.site.register(TOURINFOGROUP, TOURINFOGROUPAdmin)
