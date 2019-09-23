from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from database.models import CITY, CITYPREFERENCE, PREFERENCE, SPOTPREFERENCE, SPOT
# Create your views here



def show_side_bar(request):
    template = loader.get_template('admin_sidebar.html')
    context={}
    return HttpResponse(template.render(context,request))

def add_city(request):
    if request.method == "POST":
        city_name=request.POST['name']
        lattitude=request.POST['lattitude']
        longitude=request.POST['longitude']
        description=request.POST['description']
        city_obj=CITY()
        city_obj.cityName=city_name
        city_obj.latitude=lattitude
        city_obj.longitude=longitude
        city_obj.description=description
        city_obj.save()
        all_pref_objects=PREFERENCE.objects.all()
        for p in all_pref_objects:
            city_pref_obj=CITYPREFERENCE()
            city_pref_obj.cityID=city_obj
            city_pref_obj.preferenceID=p
            city_pref_obj.save()
        return HttpResponse("City added successfully")
    else:
        template = loader.get_template('addCity.html')
        context={}
        return HttpResponse(template.render(context,request))


def show_all_cities(request):
    all_cities=CITY.objects.all()
    name={}
    desc={}
    image={}
    latitude={}
    longitude={}

    for c in all_cities:
        name[c.id]=c.cityName
        desc[c.id]=c.description
        image[c.id]=c.image
        latitude[c.id]=c.latitude
        longitude[c.id]=c.longitude
    context={}
    context['name']=name
    context['desc']=desc
    context['image']=image
    context['latitude']=latitude
    context['longitude']=longitude
    template = loader.get_template('List_of_all_cities.html')
    return HttpResponse(template.render(context,request))


def add_spot(request):  
    context={}
    if request.method == 'POST':      
        spot_name=request.POST['name']
        lattitude=request.POST['lattitude']
        longitude=request.POST['longitude']
        description=request.POST['description']
        open_time=request.POST['open_time']
        close_time=request.POST['close_time']
        travel_time=request.POST['travel_time']
        city=request.POST['city']
        preference=request.POST['preference']
        #imagefile=request.FILES['image_file']
        print(spot_name)
        print(lattitude)
        print(longitude)
        print(description)
        print(open_time)
        print(close_time)
        print(travel_time)
        print(city)
        print(preference)
        city_obj=CITY.objects.filter(id=int(city)).first()
        pref_obj=PREFERENCE.objects.filter(id=int(preference)).first()
        spot_obj=SPOT()
        spot_obj.spotName=spot_name
        spot_obj.spotInfo=description
        spot_obj.latitude=lattitude
        spot_obj.longitude=longitude
        spot_obj.openTime=open_time
        spot_obj.closeTime=close_time
        spot_obj.totalVisitTime=travel_time
        spot_obj.cityID=city_obj
        spot_obj.save()
        spot_pref_obj=SPOTPREFERENCE()
        spot_pref_obj.spotID=spot_obj
        spot_pref_obj.preferenceID=pref_obj
        spot_pref_obj.save()
        #print(imagefile)
        return HttpResponse("Spot added successfully")
    else:
        template = loader.get_template('addSpot.html')
        cityList={}
        city_list=CITY.objects.all()
        for c in city_list:
            cityList[c.pk]=c.cityName
        preferenceList={}
        pref_list=PREFERENCE.objects.all()
        for p in pref_list:
            preferenceList[p.id]=p.prefName
            
        context["cityList"]=cityList
        context["preferenceList"]=preferenceList
        return HttpResponse(template.render(context,request))

def show_all_spots(request):
    all_spots=SPOT.objects.all()
    name={}
    desc={}
    image={}
    latitude={}
    longitude={}
    open_times={}
    close_times={}
    visit_times={}
    for s in all_spots:
        name[s.id]=s.spotName
        desc[s.id]=s.spotInfo
        image[s.id]=s.image
        latitude[s.id]=s.latitude
        longitude[s.id]=s.longitude
        visit_times[s.id]=s.totalVisitTime
        open_times[s.id]=s.openTime
        close_times[s.id]=s.closeTime

    context={}
    context['name']=name
    context['desc']=desc
    context['image']=image
    context['latitude']=latitude
    context['longitude']=longitude
    context['close_times']=close_times
    context['open_times']=open_times
    context['visit_times']=visit_times
    template = loader.get_template('List_of_all_spots.html')
    return HttpResponse(template.render(context,request))    