from django.urls import path
from . import views
urlpatterns = [
    path('createPost/',views.createPost_view, name="createPost"),
    path('personalBlogPosts/', views.view_personal_blog_posts, name="personalBlogposts"),
    path('AllBlogPosts/',views.all_blog_posts,name="AllBlogPosts"),
    path('CreateGroup/',views.createGroup, name="create_group"),
    path('existingGroups/',views.show_existing_groups,name="existing_groups"),
    path('showMessages/<int:group_id>', views.show_messages, name="show_messages" ),
]