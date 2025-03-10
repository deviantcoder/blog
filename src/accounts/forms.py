from django.forms import ValidationError

from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, get_user_model

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field, Submit, Column


User = get_user_model()


class LoginForm(AuthenticationForm):
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.helper = FormHelper()
        self.helper.form_method = 'post'

        self.helper.layout = Layout(
            Column(
                Field('username', css_class='form-control rounded-3', placeholder='Username or Email', required=True),
                css_class='mb-3 text-start'
            ),
            Column(
                Field('password', css_class='form-control rounded-3', placeholder='Password', required=True),
                css_class='mb-3 text-start'
            ),
            Submit('submit', 'Sign In', css_class='btn btn-primary w-100 rounded-3 fw-semibold'),
        )
