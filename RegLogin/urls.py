from django.urls import path
from . import views
urlpatterns = [

    path('',views.index, name="home"),
    path('register/user/', views.user_registration_view, name="register_as_user"),
    path('login/<str:view_func_name>/', views.login_view, name="login"),
    path('logout/', views.logout_view, name="logout"),
    path('profile/', views.Profile_Page_View, name="profile"),
    path('edit_profile/',views.edit_profile_page_view, name="edit_profile"),
    path('change_password/',views.change_password, name="change_password"),

]