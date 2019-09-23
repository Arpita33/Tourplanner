# Create your views here.
from database.models import *
from django.http import HttpResponse
from django.shortcuts import render, redirect
from .forms import *
from RegLogin.models import PROFILE
import datetime

# Create your views here.
def createPost_view(request):
    #print(request.user.id)

    if request.method == 'POST':
        form = BlogForm(request.POST, request.FILES)

        if form.is_valid():
            print("Here")
            print(request.user.id)
            #form.userID=request.user.id
            post=form.save()
            print(post.pk)
            bo=BLOG.objects.get(pk=post.pk)
            bo.userID=PROFILE.objects.get(user=request.user)
            bo.save()
            #print(k)
            #bo.userID=request.user.id
            #post.userID=request.user.id
            #post.save()
            #return HttpResponse('successfuly uploaded')
            return redirect('personalBlogposts')
        else:
            print("Not Valid")
    else:
        form = BlogForm()
    return render(request, 'createPost.html', {'form': form})


def view_personal_blog_posts(request):
    id=request.user.id
    print(id)
    profile=PROFILE.objects.get(user=request.user)
    bps=BLOG.objects.filter(userID=profile)
    print(profile)
    caption={}
    data={}
    post_date={}
    image={}
    for bp in bps:
        caption[bp.id]=bp.blogCaption
        data[bp.id]=bp.blogData
        post_date[bp.id]=bp.blogPostDate
        image[bp.id]=bp.image

    context={'caption':caption, 'data':data, 'post_date':post_date,
             'image':image}
    return render(request, 'blogPostsPersonal.html', context)

def all_blog_posts(request):
    blogs = BLOG.objects.all()
    caption={}
    data={}
    post_date={}
    image={}
    who_posted={}
    for b in blogs:
        prof=b.userID
        user_obj=User.objects.get(id=prof.user.id)
        user_name=user_obj.first_name
        who_posted[b.id]=user_name
        caption[b.id]=b.blogCaption
        data[b.id]=b.blogData
        post_date[b.id]=b.blogPostDate
        image[b.id]=b.image
    
    context={'caption':caption, 'data':data, 'post_date':post_date,
             'image':image, 'who_posted':who_posted}
    if request.user.is_authenticated:
        context['logged_in'] = True
    else:
        context['logged_in'] = False 
    return render(request, 'blogPosts.html', context)

def success(request):
    return HttpResponse('successfuly uploaded')

def createGroup(request):
    context={}
    if request.method == 'POST':
        name=request.POST.get('title')
        selected_members=request.POST.getlist('selected_member[]')
        print(name)
        print(selected_members)
        group=GROUP()
        group.groupName=name
        group.save()
        current_profile=PROFILE.objects.get(user=request.user)
        current_group=GROUP.objects.get(groupName=name)
        pg = PROFILEGROUP()
        pg.groupID = current_group
        pg.userID = current_profile
        pg.save()
        for sm in selected_members:
            pg=PROFILEGROUP()
            pg.groupID=current_group
            pg.userID=PROFILE.objects.get(pk=sm)
            pg.save()
        print("group created successfully")
        #return HttpResponse('group created successfully')
        return redirect('existing_groups')
    else:
        users=PROFILE.objects.all()
        username_list={}
        print(request.user.id)
        print(request.user.username)
        for u in users:
            if request.user.id != u.user.id:
                username_list[u.id]=u.user.username
        context['username_list']=username_list
    return render(request, 'createGroup.html', context)

def show_existing_groups(request):
    current_user=request.user
    current_user_profile=PROFILE.objects.get(user=request.user)
    profile_groups=PROFILEGROUP.objects.all()
    groups={}
    for pg in profile_groups:
        if(pg.userID == current_user_profile):
            name=pg.groupID.groupName
            group=pg.groupID
            groups[group.id]=name
    context={}
    print(groups)
    context['groups']=groups
    context['show_messages']=False
    context['message_list']=[]
    context['username']=request.user.username
    request.session.__setitem__('group_list',groups)
    #return render(request, 'existingGroups.html', context)
    return render(request, 'chat_UI.html', context)
    
def show_messages(request,group_id):
    context={}
    if request.method=="POST":
        print("here")
        if 'meSSage' in request.POST:
            print("uewdgk")
        else:
            print('None')
        message=request.POST.get('meSSage',False)
        print("printing from here: "+ message)
        print(datetime.datetime.now())
        group_message=GROUPMESSAGE()
        group_message.groupID=GROUP.objects.get(id=group_id)
        group_message.message=message
        group_message.userName=request.user.username
        group_message.time=now = datetime.datetime.now()
        group_message.save()       
                
    context['groups']=request.session.get('group_list',default=None)
    current_group=GROUP.objects.get(id=group_id)
    context['Groupname']=current_group.groupName
    context['username']=request.user.username
    message_list={}
    user_list={}
    sent_reply_indicator={}
    counter=0;
    group_message_list=GROUPMESSAGE.objects.all()
    for gm in group_message_list:
        if gm.groupID.id == group_id:
            #message_list.append(gm.message)
            message_list[counter] = gm.message
            user_list[counter] = gm.userName
            if(gm.userName == request.user.username):
                sent_reply_indicator[counter]="sent"
            else:
                sent_reply_indicator[counter]="replies"
            counter=counter+1
    context['message_list']=message_list
    context['user_list']=user_list
    context['sent_reply_indicator']=sent_reply_indicator
    context['show_messages']=True
    print(message_list)
    return render(request, 'chat_UI.html', context)
    #return render(request, 'existingGroups.html', context)
    
    
    
    
    

