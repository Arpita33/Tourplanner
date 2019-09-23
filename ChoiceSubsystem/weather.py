import requests
import time

def getWeather( latitude, longitude ):
    #time.sleep(1.2)
    s = ('http://api.openweathermap.org/data/2.5/forecast?lat=%s&lon=%s&APPID=6af460a5aab80bcbd5f815bdfb3da5c1')%(latitude, longitude)
    v = requests.get(s).json()['list']
    description = []
    max_tempCelcius = []
    min_tempCelcius = []
    for x in v:
        description.append( x["weather"][0]["description"] )
        max_tempCelcius.append( x["main"]["temp_max"] - 273.16 )
        min_tempCelcius.append( x["main"]["temp_min"] - 273.16 )
        #print( x["dt_txt"] + ": " + x["weather"][0]["description"] )
    return (description[0], max_tempCelcius[0], min_tempCelcius[0])


#getWeather("23.71", "90.41" )
#print(des)
#print(mx)
#print(mn)
