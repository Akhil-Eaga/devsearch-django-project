from django.forms import ModelForm
from django import forms
from .models import Project, Review

class ProjectForm(ModelForm):
    class Meta:
        model = Project
        fields = ['title', 'description', 'featured_image', 'demo_link', 'source_link', 'tags']
        # fields = '__all__' # this basically allows to create form fields for all model fields
        widgets = {
            'tags': forms.CheckboxSelectMultiple(),
        }

        # "widgets" class field can help us overwrite the type of form field a particular field is
        # we have modified the tags form field to be multi select check box instead multi select list

    # this __init__ helps in adding some CSS classes to the input fields that are generated by modelforms
    def __init__(self, *args, **kwargs):
        super(ProjectForm, self).__init__(*args, **kwargs)

        # this method of updating the form fields individually is very lengthy and cumbersome
        # self.fields['title'].widget.attrs.update({'class': 'input', 'placeholder': "Add Title"})
        # self.fields['description'].widget.attrs.update({'class': 'input', 'placeholder': "Add a detailed description"})

        for name, field in self.fields.items():
            field.widget.attrs.update({'class': 'input'}) 


class ReviewForm(ModelForm):
    class Meta:
        model = Review
        fields = ['value', 'body']

        # the "labels" class field helps in renaming the form fields similar to how we use "widgets" to override the field type
        # here we are modifying the value and body fields of the form to have descriptive names in the template
        # also note the indentation level of the labels field, it has to be inside the Meta class
        labels = {
            'value': 'Place your vote',
            'body': 'Add a comment with your vote'
        }

    # Note that the indentation level of the 
    def __init__(self, *args, **kwargs):
        super(ReviewForm, self).__init__(*args, **kwargs)

        for name, field in self.fields.items():
            field.widget.attrs.update({'class': 'input'})