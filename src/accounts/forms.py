from django.forms import ValidationError

from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth import authenticate, get_user_model

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field, Submit, Column

from core.utils import send_verify_email


User = get_user_model()


class LoginForm(AuthenticationForm):
    """
    A form for user authentication that extends the AuthenticationForm.
    This form uses crispy-forms to render the form fields with custom CSS classes
    and placeholders.
    """
    
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
            Submit('submit', 'Sign In', css_class='btn btn-dark w-100 rounded-0 fw-semibold'),
        )


class RegisterForm(UserCreationForm):
    """
    A custom user registration form that extends the UserCreationForm.
    """

    class Meta:
        model = User
        fields = [
            'email', 'username', 'password1', 'password2'
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.helper = FormHelper()
        self.helper.form_method = 'post'

        self.helper.layout = Layout(
            Column(
                Field('email', css_class='form-control rounded-3', autofocus=True, placeholder='Email', required=True),
                css_class='mb-3 text-start'
            ),
            Column(
                Field('username', css_class='form-control rounded-3', placeholder='Username', required=True),
                css_class='mb-3 text-start'
            ),
            Column(
                Field('password1', css_class='form-control rounded-3', placeholder='Password', required=True),
                css_class='mb-3 text-start'
            ),
            Column(
                Field('password2', css_class='form-control rounded-3', placeholder='Repeat Password', required=True),
                css_class='mb-3 text-start'
            ),
            Submit('submit', 'Sign Up', css_class='btn btn-dark w-100 rounded-0 fw-semibold'),
        )

    def save(self, commit=True):
        user = super().save(commit=False)

        user.is_active = False

        if commit:
            user.save()
            send_verify_email(user)

        return user


    def clean_email(self):
        email = self.cleaned_data.get('email')

        if User.objects.filter(email=email).exists():
            raise ValidationError('Email is already taken')
        
        return email

    def clean_username(self):
        username = self.cleaned_data.get('username').lower()

        if User.objects.filter(username=username).exists():
            raise ValidationError('Username is already taken')

        return username
