from dataclasses import field
from django.forms import ModelForm
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import profile , skill , message


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['first_name' , 'email' , 'username' , 'password1' , 'password2']
        labels = {
            'first_name' : 'Name',
        }

    def __init__(self, *args , **kwargs):
        super(CustomUserCreationForm,self).__init__(*args , **kwargs)


        for name , field in self.fields.items():
            field.widget.attrs.update({'class':'input'})



class profileForm(ModelForm):
    class Meta:
        model = profile
        fields = ['name' , 'email' , 'location' , 'username' , 'short_intro' , 'bio' ,
         'profile_image' , 'social_github' ,'social_twitter' ,
          'social_linkedin' , 'social_youtube' , 'social_website'] 


    def __init__(self, *args , **kwargs):
        super(profileForm,self).__init__(*args , **kwargs)


        for name , field in self.fields.items():
            field.widget.attrs.update({'class':'input'})



class skillForm(ModelForm):
    class Meta:
        model = skill
        fields = '__all__'
        exclude = ['owner']


    def __init__(self, *args , **kwargs):
        super(skillForm,self).__init__(*args , **kwargs)


        for name , field in self.fields.items():
            field.widget.attrs.update({'class':'input'})



class messageForm(ModelForm):
    class Meta:
        model = message
        fields = ['name' , 'subject' , 'email' , 'body']
        


    def __init__(self, *args , **kwargs):
        super(messageForm,self).__init__(*args , **kwargs)


        for name , field in self.fields.items():
            field.widget.attrs.update({'class':'input'})


        