from django import forms

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field, Submit, Column

from .models import Profile



class ProfileForm(forms.ModelForm):

    class Meta:
        model = Profile
        fields = ('image', 'display_name')
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.attrs = {
            'enctype': 'multipart/form-data',
        }

        self.helper.layout = Layout(
            Column(
                Field('image', css_class='form-control rounded-3', placeholder='Username or Email'),
                css_class='mb-3 text-start'
            ),
            Column(
                Field('display_name', css_class='form-control rounded-3'),
                css_class='mb-3 text-start'
            ),
            Submit('submit', 'Save', css_class='btn btn-dark w-100 rounded-0 fw-semibold'),
        )

