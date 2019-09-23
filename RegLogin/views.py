from django.http import HttpResponse
from django.template import loader
from .forms import LoginForm
from django.shortcuts import render,redirect
from django.contrib.auth import authenticate, login,logout
from django.contrib import messages
from .forms import ProfileForm, UserCreateForm
from django.contrib.auth.models import User
from .models import PROFILE
temp = None

def debug(s):
    print( "\n\n\n" + s + "\n\n\n" )

def index(request):
    #request.session.flush()
    if 'chosen_spots' in request.session:
        del request.session['chosen_spots']
    if 'chosen_cities' in request.session:
        del request.session['chosen_cities']

    template = loader.get_template('homepage.html')
    if request.user.is_authenticated:
        context = {'logged_in':True, }
    else:
        context = {'logged_in': False, }
    return HttpResponse(template.render(context, request))

def display_registration_page(request):
    template = loader.get_template('registrationPage.html')
    context = {}
    return HttpResponse(template.render(context, request))



def Profile_Page_View(request):
    context={}
    if request.user.is_authenticated:
        context={'logged_in':True, 'user':request.user.username, 'email':request.user.email,
                 'first_name':request.user.first_name, 'last_name':request.user.last_name,
                 'address':request.user.profile.Address, 'phone':request.user.profile.Phone,
                 }
    template = loader.get_template('testProfile.html')
    return HttpResponse(template.render(context, request))


def edit_profile_page_view(request):
    context={}
    if request.method == 'POST':
        #user_name=request.POST['user_name']
        first_name=request.POST['first_name']
        last_name=request.POST['last_name']
        address=request.POST['address']
        contact=request.POST['phone']

        user_edit = User.objects.get(id=request.user.id)
        profile = PROFILE.objects.get(user=request.user)
        #user_edit.username=user_name
        user_edit.first_name=first_name
        user_edit.last_name=last_name
        profile.Address=address
        profile.Phone=contact
        user_edit.save()
        profile.save()
        return redirect('profile')
    else:
        id=request.user.id
        profile = PROFILE.objects.get(user=request.user)
        user_name=request.user.username
        first_name=request.user.first_name
        last_name=request.user.last_name
        address=profile.Address
        contact=profile.Phone
        context['user_name']=user_name
        context['first_name']=first_name
        context['last_name']=last_name
        context['address']=address
        context['contact']=contact
        template = loader.get_template('editProfile.html')
    return HttpResponse(template.render(context, request))

def change_password(request):
    error=[]
    context={}
    if request.method == 'POST':
        old_pass=request.POST['oldPassword']
        new_pass=request.POST['password1']
        retype_pass=request.POST['password2']
        user_edit = User.objects.get(id=request.user.id)
        oldPassFromDB=user_edit.password
        if user_edit.check_password(old_pass) and new_pass==retype_pass:
            user_edit.password=new_pass
            user_edit.set_password(new_pass)
            user_edit.save()
            print( old_pass + " " + oldPassFromDB + "\n" + new_pass + " " + user_edit.password )
            print("password saved!")
            return redirect('profile')

        ret= user_edit.check_password(old_pass)
        if ret is False:
            error.append('Incorrect old password')

        if new_pass!=retype_pass:
            error.append('New password and retyped password did not match!')
    context['error']=error
    template = loader.get_template('ChangePass.html')
    return HttpResponse(template.render(context, request))

def login_view(request, view_func_name):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = LoginForm(request.POST)

        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            # ...
            # redirect to a new URL:
            user=form.cleaned_data.get('username')
            password=form.cleaned_data.get('password')
            user = authenticate(username=user, password=password)
            if user is not None:
                if user.is_active:
                    request.session['user_id'] = user.id
                    login(request, user)
                    if view_func_name=="home":
                        return redirect('home')
                    elif view_func_name=="tour_plan":
                        context = request.session.get('plan_context_data', default=None)
                        template = loader.get_template('ShowPlanPage.html')
                        return HttpResponse(template.render(context, request))
                else:
                    messages.error(request, 'disabled account')
                    # Return a 'disabled account' error message
            else:
                messages.error(request, 'username or password not correct')
                # Return an 'invalid login' error message.

    # if a GET (or any other method) we'll create a blank form
    else:
        form = LoginForm()

    return render(request, 'login.html', {'form': form})

def user_registration_view(request):
    submitted = False
    if request.method == 'POST':
        userform = UserCreateForm(request.POST)
        profileform = ProfileForm(request.POST)
        if userform.is_valid() and profileform.is_valid():
            user = userform.save()
            profile = profileform.save(commit=False)
            profile.user = user
            profile.is_Guide=False #remove it later
            profile.save()
            new_user = authenticate(username=userform.cleaned_data['username'],
                                    password=userform.cleaned_data['password1'],
                                    )
            request.session['user_id'] = user.id
            login(request, new_user)
            print('Account created successfully')
            return redirect('home')

        else:
            print('ERRRR')
            print(userform.errors)
    else:
        userform = UserCreateForm()
        profileform = ProfileForm()
    return render(request, "registration.html", {'type':"User",'userform': userform, 'profileform': profileform, 'submitted': submitted})

def logout_view(request):
    logout(request)
    return redirect('home')
