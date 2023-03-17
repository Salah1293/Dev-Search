from django.test import tag
from rest_framework import serializers
from projects.models import project , Tag , review
from users.models import profile



class reviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = review
        fields = '__all__'

class profileSerializer(serializers.ModelSerializer):
    class Meta:
        model = profile
        fields = '__all__'


class tagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = '__all__'


class projectSerializer(serializers.ModelSerializer):
    owner = profileSerializer(many=False)
    tags = tagSerializer(many=True)
    reviews = serializers.SerializerMethodField()

    class Meta:
        model = project
        fields = '__all__'

    def get_reviews(self , project):
        reviews = project.review_set.all()
        serialzer = reviewSerializer(reviews , many=True)
        return serialzer.data
