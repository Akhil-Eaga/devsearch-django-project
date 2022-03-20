from django.forms import ModelForm
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Profile, Skill, Message

# inheriting from the UserCreationForm provides us with all the attributes and methods of that ModelForm


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        # password1 refers to the password and password2 refers to the password confirmation
        fields = ['first_name', "email", "username", "password1", "password2"]
        labels = {
            'first_name': 'Name'
        }

    def __init__(self, *args, **kwargs):
        super(CustomUserCreationForm, self).__init__(*args, **kwargs)

        # this method of updating the form fields individually is very lengthy and cumbersome
        # self.fields['title'].widget.attrs.update({'class': 'input', 'placeholder': "Add Title"})
        # self.fields['description'].widget.attrs.update({'class': 'input', 'placeholder': "Add a detailed description"})

        for name, field in self.fields.items():
            field.widget.attrs.update({'class': 'input'})


class ProfileForm(ModelForm):
    class Meta:
        model = Profile
        fields = ['name', 'email', 'username', 'location', 'short_intro', 'bio', 'profile_image', 'social_github',
                  'social_stackoverflow', 'social_twitter', 'social_linkedin', 'social_youtube', 'social_website']

    def __init__(self, *args, **kwargs):
        super(ProfileForm, self).__init__(*args, **kwargs)

        # this method of updating the form fields individually is very lengthy and cumbersome
        # self.fields['title'].widget.attrs.update({'class': 'input', 'placeholder': "Add Title"})
        # self.fields['description'].widget.attrs.update({'class': 'input', 'placeholder': "Add a detailed description"})

        for name, field in self.fields.items():
            field.widget.attrs.update({'class': 'input'})


class SkillForm(ModelForm):
    class Meta:
        model = Skill
        fields = '__all__'
        # the __all__ uses all the fields excluding the ones declared by the exclude array below
        exclude = ['owner']

    def __init__(self, *args, **kwargs):
        super(SkillForm, self).__init__(*args, **kwargs)

        for name, field in self.fields.items():
            field.widget.attrs.update({'class': 'input'})


class MessageForm(ModelForm):
    class Meta:
        model = Message
        fields = ['name', 'email', 'subject', 'body']
        labels = {
            'body': 'Message'
        }

    def __init__(self, *args, **kwargs):
        super(MessageForm, self).__init__(*args, **kwargs)

        for name, field in self.fields.items():
            field.widget.attrs.update({'class': 'input'})