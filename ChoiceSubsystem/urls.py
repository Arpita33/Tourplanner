from django.urls import path
from . import views
urlpatterns = [
    path('detailsForm',views.data_form_view_page,name="dataFormDisplay"),
    path('planTour/<str:function_name>',views.extra_data_fetching,name="plan"),
    path('preference/<int:city>', views.preference_page, name="preference"),
    path('', views.display_cityChoice_page, name="city"),
    path('test/',views.plan_page_temp),
    path('editPlan/', views.plan_edit_options_view_page, name="edit_plan"),
    path('spot/<int:spot_id>/', views.spotDetail, name='spotDetail'),
    path('savePlan/saved/', views.save_plan_view_page, name="save_plan"),
    path('savedPlan/<int:plan_id>',views.show_chosen_previous_plan, name="show_particular_plan"),
    path('previousPlans/',views.list_all_previous_plans,name="previous_plans")

]