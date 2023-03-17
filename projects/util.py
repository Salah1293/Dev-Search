from django.db.models import Q
from .models import project , Tag
from django.core.paginator import Paginator , PageNotAnInteger , EmptyPage


def searchProject(request):
    text =''
    if request.GET.get('text'):
        text = request.GET.get('text')
    tags = Tag.objects.filter(name__icontains=text)
    projects = project.objects.distinct().filter(
        Q(title__icontains=text) |
        Q(description__icontains=text) |
        Q(owner__name__icontains=text) |
        Q(tags__in=tags)
        )
    return projects , text


def paginateProjects(request , projects ,results ):
    page = request.GET.get('page')

    paginator = Paginator(projects , results)
    try:
        projects = paginator.page(page)
    except PageNotAnInteger:
        page = 1
        projects = paginator.page(page)
    except EmptyPage:
        page = paginator.num_pages
        projects = paginator.page(page)

    leftIndex = (int(page) - 4)
    if leftIndex < 1:
        leftIndex = 1
    rightIndex = (int(page) + 5)
    if rightIndex > paginator.num_pages:
        rightIndex = paginator.num_pages + 1

    custom_range = range(leftIndex , rightIndex)
    return projects , custom_range
