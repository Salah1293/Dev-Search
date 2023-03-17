from dataclasses import fields
from django.forms import ModelForm
from .models import project , review

from django import forms



class projectForm(ModelForm):
    class Meta:
        model = project
        fields = ['title', 'featured_image' ,'description','demo_link','source_link','tags']
        widgets = {
            'tags' : forms.CheckboxSelectMultiple(),
        }



    def __init__(self, *args , **kwargs):
        super(projectForm,self).__init__(*args , **kwargs)


        for name , field in self.fields.items():
            field.widget.attrs.update({'class':'input'})





class reviewForm(ModelForm):
    class Meta:
        model = review
        fields = ['value' , 'body']

        labels = {
            'value': 'Place your vote' ,
            'body': 'Add a comment eith your vote' ,
        }


    def __init__(self, *args , **kwargs):
        super(reviewForm,self).__init__(*args , **kwargs)


        for name , field in self.fields.items():
            field.widget.attrs.update({'class':'input'})