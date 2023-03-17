from django.shortcuts import render , redirect
from .models import profile , skill , message
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import login,authenticate,logout
from django.contrib.auth.decorators import login_required
from .forms import CustomUserCreationForm ,profileForm ,skillForm , messageForm
from django.db.models import Q
from .util import searchProfiles ,paginateProfiles




def loginUser(request):

    page = 'login'
    if request.user.is_authenticated:
        return redirect('profiles')
    if request.method == 'POST':
        username = request.POST['username'].lower()
        password = request.POST['password']

        try:
            user =User.objects.get(username=username)
        except:
            messages.error(request ,'Username does not exist')

        user = authenticate(request,username=username,password=password)

        if user is not None:
            login(request,user)
            return redirect(request.GET['next'] if 'next' in request.GET else 'account')

        else:
            messages.error(request ,'username or password is incorrect')

    return render(request,'users/login-registration.html')


def logoutUser(request):
    logout(request)
    messages.info(request ,'Username was logged out!!')
    return redirect('login')



def registerUser(request):
    page = 'register'
    form = CustomUserCreationForm()
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST) 
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            messages.success(request,'user account was created!!')
            login(request,user)
            return redirect('account')

        else:
            messages.error(request,'an error has occurred!!')

    
    context={'page':page, 'form':form}
    return render(request,'users/login-registration.html',context)


def profiles(request):
    profiles , text = searchProfiles(request)
    profiles , custom_range = paginateProfiles(request , profiles , 6)
    context = {'profiles':profiles , 'text':text , 'custom_range':custom_range}
    return render(request, 'users/profiles.html', context)


def userProfile(request ,pk):
    userprofile = profile.objects.get(id=pk)
    topSkills = userprofile.skill_set.exclude(description__exact="")
    otherSkills = userprofile.skill_set.filter(description="")
    context = {'userprofile':userprofile,'topSkills':topSkills,'otherSkills':otherSkills}
    print(context)
    return render(request,'users/myuserprofile.html',context)

@login_required(login_url='login')
def userAccount(request):
    profile = request.user.profile
    skills = profile.skill_set.all()
    projects = profile.project_set.all()
    context = {'profile':profile , 'skills':skills , 'projects' :projects }
    return render(request , 'users/account.html' , context)


@login_required(login_url='login')
def editAccount(request):
    profile = request.user.profile
    form = profileForm(instance=profile)
    if request.method == 'POST':
        form = profileForm(request.POST , request.FILES , instance = profile)
        if form.is_valid():
            form.save()
            return redirect('account')
    context = {'form':form}
    return render(request , 'users/edit-account.html' , context)



@login_required(login_url='login')
def createSkill(request):
    profile = request.user.profile
    form = skillForm()
    if request.method == 'POST':
        form = skillForm(request.POST)
        if form.is_valid():
            skill = form.save(commit=False)
            skill.owner = profile
            skill.save()
            return redirect('account')
    context = {'form':form}
    return render(request , 'users/skill-form.html',context)



@login_required(login_url='login')
def updateSkill(request , pk):
    profile = request.user.profile
    skill = profile.skill_set.get(id=pk)
    form = skillForm(instance=skill)
    if request.method == 'POST':
        form = skillForm(request.POST , instance=skill)
        if form.is_valid():
            form.save()
            return redirect('account')
    context = {'form':form}
    return render(request,'users/skill-form.html',context)


@login_required(login_url="login")
def deleteSkill(request , pk):
    profile = request.user.profile
    skill = profile.skill_set.get(id=pk)
    if request.method == 'POST':
        skill.delete()
        return redirect('account')
    context = {'object':skill}
    return render(request , 'delete-template.html' , context)

@login_required(login_url='login')
def inbox(request):
    profile = request.user.profile
    messageRequests = profile.messages.all()
    unreadCount = messageRequests.filter(is_read=False).count()

    context = {'messageRequests':messageRequests , 'unreadCount':unreadCount}
    return render(request,'users/inbox.html', context)


@login_required(login_url='login')
def viewMessage(request , pk):
    profile = request.user.profile
    message = profile.messages.get(id=pk)
    if message.is_read == False:
        message.is_read = True
        message.save()
    context = {'message':message}
    return render(request , 'users/message.html' , context)

def createMessage(request , pk):
    recipient = profile.objects.get(id=pk)
    form = messageForm()

    try:
        sender = request.user.profile
    except:
        sender = None

    if request.method == 'POST':
        form = messageForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.sender = sender
            message.recipient = recipient

            if sender:
                message.name = sender.name
                message.email = sender.email
            message.save()
            
            return redirect('user-profile' , pk=recipient.id)

    context = {'recipient':recipient , 'form':form}
    return render(request , 'users/message_form.html' , context)