from django.urls import path
from . import views
urlpatterns = [
    path('',views.show_side_bar,name="basic_sidebar_view"),
    path('addCity/',views.add_city,name="add_city"),
    path('addSpot/',views.add_spot,name="add_spot"),
    path('All_City_List/',views.show_all_cities,name="all_cities"),
    path('All_Spot_List/',views.show_all_spots,name="all_spots"),


]