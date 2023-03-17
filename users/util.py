from .models import profile ,skill
from django.db.models import Q
from django.core.paginator import Paginator , PageNotAnInteger , EmptyPage

def paginateProfiles(request , profiles , results ):
    page = request.GET.get('page')
    paginator = Paginator(profiles , results)
    try:
        profiles = paginator.page(page)
    except PageNotAnInteger:
        page = 1
        profiles = paginator.page(page)
    except EmptyPage:
        page = paginator.num_pages
        profiles = paginator.page(page)

    leftIndex = (int(page) - 4)
    if leftIndex < 1:
        leftIndex = 1
    rightIndex = (int(page) + 5)
    if rightIndex > paginator.num_pages:
        rightIndex = paginator.num_pages + 1

    custom_range = range(leftIndex , rightIndex)
    return profiles , custom_range




def searchProfiles(request):
    text = ''
    if request.GET.get("text"):
        text = request.GET.get("text")
    
    skills = skill.objects.filter(name__icontains=text)

    profiles = profile.objects.distinct().filter(
     Q(name__icontains=text) |
     Q(short_intro__icontains=text) |
     Q(skill__in=skills)
     )
    return profiles , text