from multiprocessing import context
from turtle import title
from urllib import request
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.shortcuts import render , redirect
from .models import project , Tag
from django.db.models import Q
from .util import searchProject , paginateProjects
from .forms import projectForm ,reviewForm
from django.core.paginator import Paginator , PageNotAnInteger , EmptyPage


def projects(request):
    projects , text = searchProject(request)
    projects , custom_range = paginateProjects(request , projects , 6)

    context={'projects': projects , 'text':text , 'custom_range' : custom_range}
    return render(request,'projects/projects.html', context)




def single_project(request, pk):
    projectObj = project.objects.get(id = pk)
    form = reviewForm()
    if request.method == 'POST':
        form = reviewForm(request.POST)
        review = form.save(commit=False)
        review.project = projectObj
        review.owner = request.user.profile
        review.save()
        projectObj.getVoteCount
        return redirect('project' , pk=projectObj.id)
    return render(request,'projects/single-project.html' ,{'project':projectObj , 'form' :form})



@login_required(login_url='login')
def createProject(request):
    profile = request.user.profile
    form = projectForm()
    if request.method == 'POST':
        form = projectForm(request.POST, request.FILES)
        if form.is_valid():
            project = form.save(commit=False)
            project.owner = profile
            project.save()
            return redirect('account')

    context={'form':form}
    return render(request, 'projects/project-form.html', context)



@login_required(login_url='login')
def updateProject(request, pk):
    profile = request.user.profile
    updatedProject = profile.project_set.get(id=pk)
    form = projectForm(instance=updatedProject)
    if request.method == 'POST':
        form = projectForm(request.POST,request.FILES, instance=updatedProject)
        if form.is_valid():
            form.save()
            return redirect('account')

    context={'form':form}
    return render(request, 'projects/project-form.html', context)




@login_required(login_url='login')
def deleteProject(request , pk):
    profile = request.user.profile
    deletedProject = profile.project_set.get(id=pk)
    if request.method == 'POST':
        deletedProject.delete()
        return redirect('account')
    
    context ={'object':deletedProject}
    return render(request,'delete-template.html',context)


