from django.forms import ModelForm
from django import forms
from .models import Project

class ProjectForm(ModelForm):
    class Meta:
        model = Project
        fields = ['title', 'description', 'featured_image', 'demo_link', 'source_link', 'tags']
        # fields = '__all__' # this basically allows to create form fields for all model fields
        widgets = {
            'tags': forms.CheckboxSelectMultiple(),
        }

        # widgets class field can help us overwrite the type of form field a particular field is
        # we have modified the tags form field to be multi select check box instead multi select list

    def __init__(self, *args, **kwargs):
        super(ProjectForm, self).__init__(*args, **kwargs)

        # this method of updating the form fields individually is very lengthy and cumbersome
        # self.fields['title'].widget.attrs.update({'class': 'input', 'placeholder': "Add Title"})
        # self.fields['description'].widget.attrs.update({'class': 'input', 'placeholder': "Add a detailed description"})

        for name, field in self.fields.items():
            field.widget.attrs.update({'class': 'input'}) 
