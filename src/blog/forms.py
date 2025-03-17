from django import forms

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Row, Submit, Field, Column, HTML

from .models import Post


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('title', 'header_image', 'content')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.attrs = {
            'enctype': 'multipart/form-data',
        }

        self.helper.layout = Layout(
            Column(
                Field('title', css_class='form-control rounded-3', placeholder='Post title', required=True),
                css_class='mb-3 text-start'
            ),
            Column(
                Field('header_image', css_class='form-control rounded-3'),
                css_class='mb-3 text-start'
            ),
            Column(
                Field('content', css_class='form-control rounded-3', placeholder='Start to write here...', required=True),
                css_class='mb-3 text-start'
            ),
            Row(
                Column(
                    Submit('submit', 'Publish', css_class='btn btn-dark rounded-0 fw-semibold w-100'),
                    css_class='col-md-6 mb-2'
                ),
                Column(
                    HTML("<a href='' class='btn btn-outline-dark rounded-0 fw-semibold w-100'>Save as Draft</a>"),
                    css_class='col-md-6 mb-2'
                ),
                css_class='justify-content-center'
            )
        )