from django.shortcuts import render,redirect
from database.models import CITY, CITYPREFERENCE, PREFERENCE, SPOTPREFERENCE, SPOT, SPOTREVIEW
from django.http import HttpResponse
from django.template import loader
from .distance import *
from .weather import *
import time
from datetime import date, timedelta
from RegLogin import views,urls
import ast

# Create your views here.
def display_cityChoice_page(request):
    template = loader.get_template('cityChoice.html')
    context = {}
    all_cities=CITY.objects.all()
    no_of_cities=all_cities.count()
    rows=int(no_of_cities/3)
    if (no_of_cities%3) != 0:
        rows=rows+1
    counter=0
    city_ids=[]
    city_names={}
    city_images={}
    city_descs={}
    for i in range(0,rows):
        ids=[]
        for j in range(0,3):
            if counter < no_of_cities:
                index=all_cities[counter].id
                ids.append(index)
                city_names[index]=all_cities[counter].cityName
                city_images[index]=str(all_cities[counter].image)
                city_descs[index]=all_cities[counter].description
                counter=counter+1
        city_ids.append(ids)

    context['city_ids']=city_ids
    context['city_names']=city_names
    context['city_descs']=city_descs
    context['city_images']=city_images

    if request.user.is_authenticated:
        context['logged_in']=True
    else:
        context['logged_in'] =False
    return HttpResponse(template.render(context, request))

def city_choice_page(request):

    context={}
    all_city = CITY.objects.all()
    city_names={}
    city_images={}
    city_ids={}
    count={}
    counter=0
    for a in all_city:
        city_names[a.pk] = a.cityName
        city_images[a.pk] = str(a.image)
        counter = counter + 1


    print(counter)
    rows=int(counter/3)

    if(counter%3!=0):
        rows=rows+1
    print(rows)
    context['rows']=rows

    context['city_names'] = city_names
    context['images']=city_images
    context['city_ids']=city_ids
    context['count']=count
    if request.user.is_authenticated:
        context['logged_in']=True
    else:
        context['logged_in'] =False
    return render(request, 'cityChoice.html', context)


def preference_page(request, city):
   # pref_ids = CITYPREFERENCE.objects.select_related('preferenceID').filter(cityId_id=city)
    print("City: " + str(city) )
    if request.method == 'POST':
       some_var = request.POST.getlist('selected_spot[]')
       print("some_var1: " + str(some_var) )

       print(some_var)
       chosen_spots=request.session.get('chosen_spots',default=None)
       chosen_cities=request.session.get('chosen_cities',default=None)
       print("previous_spots: " + str(chosen_spots) )
       print("previous_cities: " + str(chosen_cities) )
       if chosen_spots is None:
           #print("chosen_spots_None")
           chosen_spots = some_var
           request.session.__setitem__('chosen_spots',chosen_spots)
       else:
           #print("chosen_spots_Not_None")
           chosen_spots=chosen_spots+some_var
           #chosen_spots=[]
           #print("chosen_spots2:" + str(chosen_spots) )
           request.session.__setitem__('chosen_spots',chosen_spots)

       print("Current Spots: " + str(chosen_spots) )

       if chosen_cities is None:
           if len(some_var)!=0:
               chosen_cities=[]
               chosen_cities.append(city)
               request.session.__setitem__('chosen_cities',chosen_cities)
       else:
           if len(some_var)!=0:
               chosen_cities.append(city)
               request.session.__setitem__('chosen_cities',chosen_cities)

       print("Current City: " + str(chosen_cities) )


       #if request.user.id is None
           #return

       if 'next' in request.POST:
            return render(request,"extraDetailsForm.html",{})
       elif 'add_more_cities' in request.POST:
            return redirect('city')
       #return city_choice_page(request)

    else:
        preference_list={}
        pref_spotName_list={}
        #pref_spotID_list={}
        pref_spotDescription_list = {}
        pref_spotImage_list={}
        pref_spotRating_list={}
        pref_ids=CITYPREFERENCE.objects.filter(cityID=city)
        for p in pref_ids:
            pID = p.preferenceID
            pName=pID.prefName
            preference_list[pID.id]=pID.prefName
            spot_ids=SPOTPREFERENCE.objects.filter(preferenceID=pID)
            spots={}
            #spotIDs={}
            spotImages={}
            spotDescriptions={}
            spotRatings={}
            for s in spot_ids:
                sID=s.spotID
                if sID.cityID.id == city:
                    spot_rating_qs=SPOTREVIEW.objects.filter(spotID=sID)
                    #print(spot_rating_qs)
                    avg_rating=0;
                    count=0;
                    for sr in spot_rating_qs:
                        #print(str(sr.spotID.id)+str(sr.rating))
                        avg_rating=avg_rating+float(sr.rating)
                        count=count+1;
                    if count!=0:
                        avg_rating=avg_rating/count;
                    print(avg_rating)
                    if (avg_rating>0 and avg_rating<0.25):
                        avg_rating=0.25
                    elif (avg_rating>0.25 and avg_rating<0.5):
                        avg_rating=0.5  
                    elif (avg_rating>0.5 and avg_rating<0.75):
                        avg_rating=0.75 
                    elif (avg_rating>0.75 and avg_rating<1.0):
                        avg_rating=1.0
                    elif (avg_rating>1.0 and avg_rating<1.25):
                        avg_rating=1.25
                    elif (avg_rating>1.25 and avg_rating<1.5):
                        avg_rating=1.5  
                    elif (avg_rating>1.5 and avg_rating<1.75):
                        avg_rating=1.75
                    elif (avg_rating>1.75 and avg_rating<2.0):
                        avg_rating=2.0
                    elif (avg_rating>2 and avg_rating<2.25):
                        avg_rating=2.25
                    elif (avg_rating>2.25 and avg_rating<2.5):
                        avg_rating=2.5  
                    elif (avg_rating>2.5 and avg_rating<2.75):
                        avg_rating=2.75
                    elif (avg_rating>2.75 and avg_rating<3.0):
                        avg_rating=3.0
                    elif (avg_rating>3 and avg_rating<3.25):
                        avg_rating=3.25
                    elif (avg_rating>3.25 and avg_rating<3.5):
                        avg_rating=3.5  
                    elif (avg_rating>3.5 and avg_rating<3.75):
                        avg_rating=3.75
                    elif (avg_rating>3.75 and avg_rating<4.0):
                        avg_rating=4.0
                    elif (avg_rating>4 and avg_rating<4.25):
                        avg_rating=4.25
                    elif (avg_rating>4.25 and avg_rating<4.5):
                        avg_rating=4.5  
                    elif (avg_rating>4.5 and avg_rating<4.75):
                        avg_rating=4.75
                    elif (avg_rating>4.75 and avg_rating<5.0):
                        avg_rating=5.0
                    spots[sID.id]=sID.spotName
                    spotImages[sID.id]=sID.image
                    spotRatings[sID.id]=avg_rating
                    spotDescriptions[sID.id]=sID.spotInfo
                    #print(sID.spotInfo)
                    #print(city, sID.spotName, pID.prefName)
            pref_spotName_list[pID.id]=spots
            pref_spotImage_list[pID.id]=spotImages
            pref_spotDescription_list[pID.id]=spotDescriptions
            pref_spotRating_list[pID.id]=spotRatings
           # print(pref_spotDescription_list)


        all_city=CITY.objects.all()
        other_cities={}
        for c in all_city:
            #print(c.id)
            if c.id!=city:
                other_cities[c.id]=c.cityName

        if request.user.is_authenticated:
            logged_var=True    
        else:
            logged_var=False
                   

        return render(request, 'prefV2.html', {'preference_list':preference_list,
                                                   'pref_spotName_list':pref_spotName_list,
                                                   'pref_spotDescription_list': pref_spotDescription_list,
                                                   'pref_spotImage_list': pref_spotImage_list,
                                                   'pref_spotRating_list': pref_spotRating_list,
                                                    'other_cities':other_cities,
                                                    'logged_in':logged_var,
                                                   })

def data_form_view_page(request):
    template = loader.get_template('extraDetailsForm.html')
    context={}
    return HttpResponse(template.render(context,request))
def plan_page_temp(request):
    template = loader.get_template('ShowPlanPage.html')
    context={}
    return HttpResponse(template.render(context,request))


def generatePlanFirstTime(request):
    print("gen first time ->")
    template = loader.get_template('ShowPlanPage.html')
    start_date = request.POST['start_date']
    end_date = request.POST['end_date']
    start_time=request.POST['start_time']
    end_time=request.POST['end_time']
    start_city=request.POST['start_location']

    request.session.__setitem__('user_start_date', start_date )
    request.session.__setitem__('user_start_time', start_time )
    request.session.__setitem__('user_end_date', end_date )
    request.session.__setitem__('user_end_time', end_time )
    request.session.__setitem__('user_start_location', start_city )
    #budget=request.POST['budget']
    context = {}
    if request.user.is_authenticated:
        context['logged_in'] = True
    else:
        context['logged_in'] = False 

    chosen_spots = request.session.get('chosen_spots', default=None)
    chosen_cities = request.session.get('chosen_cities', default=None)

    print( start_city )
    print(start_date)
    print(end_date)
    print(start_time)
    print(end_time)
    print(chosen_spots)
    

    start_city = CITY.objects.get(cityName=start_city).id
    end_city = start_city

    city_list, city_spot = generate_city_spot(chosen_spots, start_city,end_city)
    #print(city_spot)
    #print(city_list)


    temp = start_date.split('-')
    start_date = date( int( temp[0] ), int(temp[1]), int(temp[2]) )
    total_city = len(city_list)
    cur_date = start_date
    cityName_list = []
    desc_data = {}
    distance_data = {}
    time_data = {}
    weather_data = {}
    for i in range(total_city):
        if i == total_city - 1:
            continue
        cur_city = city_list[i]
        nxt_city = city_list[i+1]
        #visit_by_day_description, visit_by_day_time, visit_by_day_distance, cur_date = generate_plan(cur_city, city_spot[cur_city], nxt_city, cur_date )
        visit_by_day_description, visit_by_day_time, visit_by_day_distance, cur_date = generate_plan2(cur_city, city_spot[cur_city], nxt_city, cur_date, start_time, end_time )
        #print(visit_by_day_distance)
        #rint(visit_by_day_time)
        #print(visit_by_day_description)
        cc = CITY.objects.get( id = cur_city )
        cityName = cc.cityName
        desc_data[ cityName ] = visit_by_day_description
        distance_data[ cityName ] = visit_by_day_distance
        time_data[cityName ] = visit_by_day_time
        weather_data[ cityName ], baad1, baad2 = getWeather(cc.latitude, cc.longitude)
        #print(cur_date)
        cityName_list.append( cityName )
    #print("Time Data: "+ str(time_data))
    #print("City Spot: "+ str(city_spot))
    city_travel_start_dates={}
    city_travel_total_days={}
    for temp in cityName_list:
        l=time_data[temp]
        #print(len(l))
        #print(list(l.keys())[0])
        city_travel_start_dates[temp]=list(l.keys())[0]
        city_travel_total_days[temp]=len(l)
    
    cityName_spotName={}
    cityName_spotTime={}
    for k,v in city_spot.items():
        cc = CITY.objects.get( id = k )
        cn=cc.cityName
        temp_list_1=[]
        temp_list_2=[]
        for s in v:
            spot=SPOT.objects.get(id=s)
            spotName=spot.spotName
            spotTime=spot.totalVisitTime
            spotTime=spotTime.split(' ')[0]
            temp_list_1.append(spotName)
            temp_list_2.append(spotTime)
        cityName_spotName[cn]=temp_list_1
        cityName_spotTime[cn]=temp_list_2

    
        

    context['cityName'] = cityName_list
    context['description_data'] = desc_data
    context[ 'distance_data' ] = distance_data
    context[ 'time_data' ] = time_data
    context[ 'weather_data' ] = weather_data

    

    request.session.__setitem__('plan_city_list',cityName_list)
    request.session.__setitem__('plan_city_start_dates',city_travel_start_dates)
    request.session.__setitem__('plan_city_total_days',city_travel_total_days)
    request.session.__setitem__('plan_spots_names',cityName_spotName)
    request.session.__setitem__('plan_spots_times',cityName_spotTime)

    #request.session.__setitem__('',chosen_cities)
    request.session.__setitem__('context_for_saving',context)
    if request.user.is_authenticated:
        
        return HttpResponse(template.render(context, request))
    else:
        request.session.__setitem__('plan_context_data',context)
        return  redirect('login',view_func_name="tour_plan")


def generatePlanEdit(request):
    print("edit plan ->")
    context = {}
    
    template = loader.get_template('ShowPlanPage.html')
    start_date = request.session.get('user_start_date',default=None)
    end_date = request.session.get('user_end_date',default=None)
    start_time = request.session.get('user_start_time',default=None)
    end_time = request.session.get('user_end_time',default=None)
    start_city = request.session.get('user_start_location',default=None)
    chosen_spots = request.session.get('chosen_spots', default=None)
    
    chosen_cities = request.session.get('chosen_cities', default=None)

    city_time = {}

    start_city = CITY.objects.get(cityName=start_city).id
    end_city = start_city

    city_list, city_spot = generate_city_spot(chosen_spots, start_city,end_city)
    #print(city_spot)
    #print(city_list)
    print("post----->")
    print( request.POST ) 
    for c in city_list:
        ls = city_spot[c]
        tm = {}
        for s in ls:
            spt = SPOT.objects.get( id = s )
            name = spt.spotName
            print( name + " " + str(request.POST[name]) )
            tm[s] =  float(request.POST[name])
            
        city_time[c] = tm

    

    print( start_city )
    print(start_date)
    print(end_date)
    print(start_time)
    print(end_time)
    print(chosen_spots)
    


    temp = start_date.split('-')
    start_date = date( int( temp[0] ), int(temp[1]), int(temp[2]) )
    total_city = len(city_list)
    cur_date = start_date
    cityName_list = []
    desc_data = {}
    distance_data = {}
    time_data = {}
    weather_data = {}
    for i in range(total_city):
        if i == total_city - 1:
            continue
        cur_city = city_list[i]
        nxt_city = city_list[i+1]
        #visit_by_day_description, visit_by_day_time, visit_by_day_distance, cur_date = generate_plan(cur_city, city_spot[cur_city], nxt_city, cur_date )
        visit_by_day_description, visit_by_day_time, visit_by_day_distance, cur_date = generate_plan2(cur_city, city_spot[cur_city], nxt_city, cur_date, start_time, end_time, city_time[cur_city] )
        #print(visit_by_day_distance)
        #rint(visit_by_day_time)
        #print(visit_by_day_description)
        cc = CITY.objects.get( id = cur_city )
        cityName = cc.cityName
        desc_data[ cityName ] = visit_by_day_description
        distance_data[ cityName ] = visit_by_day_distance
        time_data[cityName ] = visit_by_day_time
        weather_data[ cityName ], baad1, baad2 = getWeather(cc.latitude, cc.longitude)
        #print(cur_date)
        cityName_list.append( cityName )
    #print("Time Data: "+ str(time_data))
    #print("City Spot: "+ str(city_spot))
    city_travel_start_dates={}
    city_travel_total_days={}
    for temp in cityName_list:
        l=time_data[temp]
        #print(len(l))
        #print(list(l.keys())[0])
        city_travel_start_dates[temp]=list(l.keys())[0]
        city_travel_total_days[temp]=len(l)
    
    cityName_spotName={}
    cityName_spotTime={}

    for k,v in city_spot.items():
        cc = CITY.objects.get( id = k )
        cn=cc.cityName
        temp_list_1=[]
        temp_list_2=[]
        for s in v:
            spot=SPOT.objects.get(id=s)
            spotName=spot.spotName
            spotTime=spot.totalVisitTime
            spotTime=spotTime.split(' ')[0]
            temp_list_1.append(spotName)
            temp_list_2.append(spotTime)
        cityName_spotName[cn]=temp_list_1
        cityName_spotTime[cn]=temp_list_2

    
        

    context['cityName'] = cityName_list
    context['description_data'] = desc_data
    context[ 'distance_data' ] = distance_data
    context[ 'time_data' ] = time_data
    context[ 'weather_data' ] = weather_data

    request.session.__setitem__('plan_city_list',cityName_list)
    request.session.__setitem__('plan_city_start_dates',city_travel_start_dates)
    request.session.__setitem__('plan_city_total_days',city_travel_total_days)
    request.session.__setitem__('plan_spots_names',cityName_spotName)
    request.session.__setitem__('plan_spots_times',cityName_spotTime)

    #request.session.__setitem__('',chosen_cities)
    request.session.__setitem__('context_for_saving',context)
    if request.user.is_authenticated:
        return HttpResponse(template.render(context, request))
    else:
        request.session.__setitem__('plan_context_data',context)
        return  redirect('login',view_func_name="tour_plan")

def extra_data_fetching(request, function_name):
    #print("here")
    if function_name == 'extra_details':
        return generatePlanFirstTime(request)
    else:
        return generatePlanEdit(request)
    


def plan_edit_options_view_page(request):
    cityName_list=request.session.get('plan_city_list',default=None)
    city_travel_start_dates=request.session.get('plan_city_start_dates',default=None)
    city_travel_total_days=request.session.get('plan_city_total_days',default=None)
    cityName_spotName=request.session.get('plan_spots_names',default=None)
    cityName_spotTime=request.session.get('plan_spots_times',default=None)
    context={}
    if request.user.is_authenticated:
        context['logged_in'] = True
    else:
        context['logged_in'] = False
    context['cityName_list']=cityName_list
    context['city_travel_start_dates']=city_travel_start_dates
    context['city_travel_total_days']=city_travel_total_days
    context['cityName_spotName']=cityName_spotName
    context['cityName_spotTime']=cityName_spotTime
    print("plan edit options->")
    print(context)
    #print(cityName_list)
    #print(city_travel_start_dates)
    #print(city_travel_total_days)
    #print(cityName_spotName)
    #print(cityName_spotTime)
    template = loader.get_template('editPlan.html')
    return HttpResponse(template.render(context, request))


def spotDetail(request, spot_id):
    context = {}
    if request.method == 'POST':
        rt = request.POST['user_rating']
        rv = request.POST['user_review']
        temp = SPOTREVIEW.objects.filter(userID=PROFILE.objects.get(user=request.user), spotID=spot_id)
        if len(temp) > 0 :
            print("saving....")
            temp[0].rating = rt
            temp[0].review = rv
            temp[0].save()
        else:
            print('creating....')
            f = SPOTREVIEW.objects.create( userID = PROFILE.objects.get(user=request.user), spotID = SPOT.objects.get(id=spot_id), rating = rt, review = rv)
            f.save()
        
        return redirect('spotDetail', spot_id)
    else:    
        template = loader.get_template('spot_detail.html')
        
        profile = PROFILE.objects.get(user=request.user)
        
        temp = SPOTREVIEW.objects.filter(userID=profile, spotID=spot_id)
        if( len(temp) > 0 ):
            context['userrating'] = temp[0].rating
            context['userreview'] = temp[0].review
        else:
            context['userrating'] = '0'
            context['userreview'] = '-'

        s = SPOT.objects.get(id=spot_id)
        context['spotName'] = s.spotName 
        
        rating = {}
        review = {}
        temp = SPOTREVIEW.objects.filter(spotID=spot_id)
        totrating = 0
        for x in temp:
            rating[x.userID.user.username] = x.rating
            totrating += int(x.rating)
            review[x.userID.user.username] = x.review
        if( len(temp) > 0 ):
            context['avgrating'] = 1.0*totrating/len(temp)
        else:
            context['avgrating'] = 0
        context['allrating'] = rating
        context['allreview'] = review
        return HttpResponse(template.render(context, request))


def save_plan_view_page( request ):
    print("plan saving ->")
    template = loader.get_template('show_saved_plans.html')
    start_date = request.session.get('user_start_date', default = None )
    start_time = request.session.get('user_start_time', default = None )
    end_date = request.session.get('user_end_date', default = None )
    end_time = request.session.get('user_end_time', default = None )
    start_location = request.session.get('user_start_location', default = None )
    context = request.session.get('context_for_saving', default = None )
    print(context)
    f = TOURINFO.objects.create( userID = PROFILE.objects.get(user=request.user), startDate = start_date, endDate = end_date, startTime = start_time, endTime = end_time, startLocation = start_location, context = str(context) )
    f.save()

    return HttpResponse(template.render(context, request))

def show_chosen_previous_plan(request, plan_id):
    p=TOURINFO.objects.get(pk=plan_id)
    context=ast.literal_eval(p.context)
    template = loader.get_template('show_saved_plans.html')
    return HttpResponse(template.render(context, request))

def list_all_previous_plans(request):
    profile=PROFILE.objects.get(user=request.user)
    all_plans=TOURINFO.objects.filter(userID=profile)
    plans={}
    cnt = 0
    for p in all_plans:
        cnt += 1
        plans[p.id]="Plan no: "+ str(cnt)
    context={}
    context['all_plans']=plans
    template = loader.get_template('all_previous_plans.html')
    return HttpResponse(template.render(context, request))