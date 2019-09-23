import random
import time
from datetime import date, timedelta
import requests
from database.models import *
import math
ALL_VISITED = None

def getDistance( latitude1, longitude1, latitude2, longitude2 ):
    time.sleep(1.2)
    s = ('https://api.mapbox.com/directions/v5/mapbox/driving/%s,%s;%s,%s?access_token=pk.eyJ1IjoidG11dHRhcXVlZW4iLCJhIjoiY2p4eWM3b2NuMDBmbjNub2J1ejZ3ZXZkbSJ9.cmOI397iM8GxEdwpfpfnKA')%( longitude1, latitude1, longitude2, latitude2)
    v = requests.get(s).json()
    return round(v['routes'][0]['distance'],2)

def getDuration( latitude1, longitude1, latitude2, longitude2 ):
    time.sleep(1.2)
    s = ('https://api.mapbox.com/directions/v5/mapbox/driving/%s,%s;%s,%s?access_token=pk.eyJ1IjoidG11dHRhcXVlZW4iLCJhIjoiY2p4eWM3b2NuMDBmbjNub2J1ejZ3ZXZkbSJ9.cmOI397iM8GxEdwpfpfnKA')%( longitude1, latitude1, longitude2, latitude2)
    v = requests.get(s).json()
    return round(v['routes'][0]['duration'],2)

def dateToString( date_in ):
    return date_in.strftime("%A, %d %B, %Y")

def tsp( mask, last, dp, to, dist, n):
    if mask == ALL_VISITED:
        return dp[mask][last]

    if to[mask][last] != -1:
        return dp[mask][last]


    v = 1000*1000*1000
    nxt = -1
    for i in range(n):
        if mask&(1<<i) != 0:
            continue

        val = dist[last][i] + tsp(mask|(1<<i), i, dp, to, dist, n)

        if val < v:
            nxt = i
            v = val

    to[mask][last] = nxt
    dp[mask][last] = v

    #print( "dp: "+ str(dp) )
    #print( str(mask) + " " + str(last) + " " + str(v) )
    return dp[mask][last]


def get_city_sequence(citylist):
    random.seed(61)
    n = len(citylist) - 1
    print(citylist)
    print(n)
    INF = 1000*1000*1000

    dist = [ [0 for x in range(n+1)] for y in range(n+1) ]

    for i in range(n+1):
        xx = CITY.objects.get( id = citylist[i] )
        #print(xx.cityName)

    for x in range(n+1):
        for y in range(n+1):
            xx = CITY.objects.get( id = citylist[x] )
            yy = CITY.objects.get( id = citylist[y] )
            #print( str(citylist[x]) + " " + str( citylist[y] )  )
            dist[x][y] = getDistance( xx.latitude, xx.longitude, yy.latitude, yy.longitude )

    '''dist = [ [random.randint(1, 10) for x in range(n+1)] for y in range(n+1) ]
    for i in range(n+1):
        for j in range(n+1):
            if i == j:
                dist[i][j] = 0'''
    #print(dist)
    dp = [ [INF]*n for x in range(1<<n)]
    to = [ [-1]*n for x in range(1<<n)]
    ALL_VISITED = (1<<n) - 1
    for x in range(n):
        dp[ALL_VISITED][x] = dist[x][n]
        to[ALL_VISITED][x] = n

    print(tsp(1,0, dp, to, dist, n))
    seq = []
    seq.append(0)
    mask = 1
    for i in range(n):
        nxt = to[mask][ seq[i] ]
        mask = mask|(1<<nxt)
        seq.append(nxt)
    #print(seq)
    for i in range(n+1):
        seq[i] = citylist[ seq[i] ]
    #print(seq)
    return seq


'''ct = [1,3,4,5,6,1]
get_city_sequence(ct)'''

def get_city_from_spot( spotlist, start_city, end_city  ):
    city = set()
    for s in spotlist:
        spot = SPOT.objects.get(id=s)
        city.add(spot.cityID.id)

    city.discard(start_city)
    city.discard(end_city)
    citylist = []
    citylist.append(start_city)
    for v in city:
        citylist.append(v)

    citylist.append(end_city)
    citylist = get_city_sequence(citylist)
    return citylist

def generate_city_spot( spotlist, start_city, end_city ):
    citylist = get_city_from_spot(spotlist, start_city, end_city)
    #print(citylist)
    city_spot = {}
    for v in citylist:
        city_spot[v] = []

    for s in spotlist:
        spot = SPOT.objects.get(id = s)
        city_spot[spot.cityID.id].append(s)
    #print(city_spot)
    return (citylist, city_spot)


'''spot = [7,8,9,10,11,12,13]
start_city = 1
end_city = 1
generate_city_spot(spot, start_city, end_city)'''






def generate_plan2( cur_city, spot_list, nxt_city, cur_date, start_time, end_time, spot_visit_time = None  ):
    #print( "cur city: " + str(cur_city))
    #print( "spot_list: " + str(spot_list) )
    #print("nxt_city: "  + str(nxt_city) )
    if spot_visit_time == None:
        spot_visit_time = {}
        for s in spot_list:
            dbs = SPOT.objects.get( id = s )
            spot_visit_time[s] = float(dbs.totalVisitTime.split()[0])
        
    #print(start_time)
    #print(end_time)
    h1 = int(start_time.split(':')[0])
    m1 = int(start_time.split(':')[1])
    h2 = int(end_time.split(':')[0])
    m2 = int(end_time.split(':')[1])
    
    start_global = h1*60 + m1
    end_global = h2*60 + m2
    #print("start end:")
    #print(start_global)
    #print(end_global)
    
    #print(type(cur_date))
    #print(cur_date)
   
    src = CITY.objects.get( id = cur_city )
    dst = CITY.objects.get( id = nxt_city )
    #tm.append( getDuration( src.latitude, src.longitude, dst.latitude, dst.longitude )/3600.0 )
    tot_spot = len(spot_list)
    spot_flag = [0]*tot_spot
    spot_it = 0
    visit_by_day_spotlist = {}
    visit_by_day_description = {}
    visit_by_day_time = {}
    visit_by_day_distance = {}

    new_date = cur_date

    #print( "spot day: " + str(spot_day))
    count = 0
    prev_spot = None
    spot_day = 0
    spots = []
    start = start_global

    while(True):
        #print("count: " + str(count))
        #print("start: " + str(start))
        next_spot = None
        nexttm = None
        finishtm = None
        ind = None
        if count == tot_spot:
            if count == 0:
                break
            s = dateToString(new_date)
            #print(s)
            #print(spots)
            spot_day = spot_day + 1
            visit_by_day_spotlist[s] = spots
            break
        
        for x in range(tot_spot):
            if spot_flag[x] == 1:
                continue
            cur_spot = spot_list[x]
            #print( "ccc " + str( type(cur_spot) ) )
            spot_vis_tm = spot_visit_time[cur_spot]*60
            dbs = SPOT.objects.get( id = cur_spot )
            bar = new_date.strftime('%A')
            if bar.lower() == dbs.holiday.lower():
                continue
            #print(dbs.openTime)
            #print(dbs.closeTime)
            open_h = int(dbs.openTime)/100
            open_m = int(dbs.openTime)%100
            close_h = int(dbs.closeTime)/100
            close_m = int(dbs.closeTime)%100
            travel_time = 0;
            if prev_spot != None:
                xx = SPOT.objects.get(id = cur_spot)
                yy = SPOT.objects.get(id = prev_spot)
                travel_time = math.ceil(getDuration(xx.latitude, xx.longitude, yy.latitude, yy.longitude)/60.0)
            #print(open_h*60+open_m)

            #if open_h*60+open_m <= start:
            #print("open: " + str(open_h*60+open_m) + " travel time: " + str(travel_time) + " spot_vistm: " + str(spot_vis_tm) )
            finish = max( open_h*60+open_m, start + travel_time ) + spot_vis_tm
            #print("finish: " + str(finish) )
            #print("ok")
            if finish > end_global or finish > close_h*60+close_m:
                continue

            if next_spot == None:
                next_spot = cur_spot
                nexttm = open_h*60+open_m
                finishtm = finish
                ind = x
            elif finish < finishtm:
                next_spot = cur_spot
                nexttm = open_h*60+open_m
                finishtm = finish
                ind = x
        
        if next_spot == None:
            s = dateToString(new_date)
            #print(s)
            #print(spots)
            spot_day = spot_day + 1
            visit_by_day_spotlist[s] = spots
            spots = []
            new_date = new_date + timedelta(days = 1)
            start = start_global
            prev_spot = None
        else:
            spots.append(next_spot)
            start = finishtm
            count += 1
            spot_flag[ind] = 1
            prev_spot = next_spot

    for i in range(spot_day):
        new_date = cur_date + timedelta(days = i)
        s = dateToString(new_date)
        spots = visit_by_day_spotlist[s]
        #print(s + " " + str(spots))
        visit_by_day_description[s] = []
        visit_by_day_time[s] = []
        visit_by_day_distance[s] = []
        if len(spots) == 0:
            visit_by_day_description[s].append("Take Rest. Nothing to do today. Everything is closed. Chill!")
            visit_by_day_time[s].append(  "-" )
            visit_by_day_distance[s].append( "-" )
            continue
    
        n = len(spots)
        for j in range(n):
            x = spots[j]
            xx = SPOT.objects.get(id = x)
            visit_by_day_description[s].append( ("Visit Spot: %s")%(xx.spotName) )
            visit_by_day_time[s].append(  str( round(spot_visit_time[x]*60.0, 2) ) + " Minutes"  )
            visit_by_day_distance[s].append( "-" )
            if j+1 < n:
                yy = SPOT.objects.get(id = spots[j+1])
                visit_by_day_description[s].append( ("Travel from spot %s to spot %s")%(xx.spotName, yy.spotName) )
                visit_by_day_distance[s].append( str( round(getDistance( xx.latitude, xx.longitude, yy.latitude, yy.longitude )/1000.0, 2)) + " Kilometers" )
                visit_by_day_time[s].append( str(round(getDuration(xx.latitude, xx.longitude, yy.latitude, yy.longitude)/60.0,2)) + " Minutes" )
    new_date = cur_date + timedelta(days = spot_day)
    s = dateToString(new_date)
    #print(s)
    visit_by_day_description[s] = []
    visit_by_day_distance[s] = []
    visit_by_day_time[s] = []
    visit_by_day_description[s].append( ("Travel from city %s to city %s")%(src.cityName, dst.cityName) )
    visit_by_day_distance[s].append( str(round(getDistance( src.latitude, src.longitude, dst.latitude, dst.longitude )/1000.0, 2)) + " Kilometers" )
    visit_by_day_time[s].append( str(round(getDuration(src.latitude, src.longitude, dst.latitude, dst.longitude)/60.0,2)) + " Minutes" )
    #print( visit_by_day_description )
    #print( visit_by_day_time )
    #print( visit_by_day_distance )
    next_date = cur_date + timedelta( days= spot_day + 1 )
    return ( visit_by_day_description, visit_by_day_time, visit_by_day_distance, next_date )