from rest_framework.response import Response
from rest_framework.decorators import api_view , permission_classes
from rest_framework.permissions import IsAuthenticated
from projects.models import project , review
from .serializer import projectSerializer
from api import serializer




@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getProjects(request):
    projects = project.objects.all()
    serializer = projectSerializer(projects , many=True)
    return Response(serializer.data)


@api_view(["GET"])
def getproject(request , pk):
    single_project = project.objects.get(id=pk)
    serializer = projectSerializer(single_project , many=False)
    return Response(serializer.data)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def projectVote(request , pk):
    one_project = project.objects.get(id=pk)
    user = request.user.profile
    data = request.data

    new_review , created = review.objects.get_or_create(
        owner = user,
        project = one_project,
    )

    new_review.value = data['value']
    new_review.save()
    one_project.getVoteCount

    serializer = projectSerializer(one_project , many=False)
    return Response(serializer.data)
