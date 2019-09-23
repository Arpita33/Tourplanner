from django.urls import path
from . import views
urlpatterns = [

    path('',views.show_search_page, name="view_search_page"),
    path('search_results/',views.show_search_results, name="show_search_results"),

]