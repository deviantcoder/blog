from django import forms

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Row, Submit, Field, Column, HTML

from .models import Post


class PostForm(forms.ModelForm):
    tags = forms.CharField(
        required=False,
        help_text='Enter up to 5 tags, separated by commas (e.g., python, django, tutorial)',
        label='Tags'
    )

    class Meta:
        model = Post
        fields = ('title', 'header_image', 'content', 'tags')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if self.instance and self.instance.pk and self.instance.tags.exists():
            self.initial['tags'] = ', '.join(tag.name for tag in self.instance.tags.all())
        else:
            self.initial['tags'] = ''

        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.attrs = {
            'enctype': 'multipart/form-data',
            'id': 'postForm',
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
                Field('content', css_class='form-control rounded-3', placeholder='Start to write here...', required=False),
                css_class='mb-3 text-start'
            ),
            Column(
                Field('tags', css_class='form-control rounded-3 tag-input', placeholder='Add tags...'),
                HTML('<div id="tag-container" class="tag-container"></div>'),
                HTML('<input type="text" id="tag-input-field" class="tag-input-field" list="tag-suggestions" placeholder="Type a tag and press Enter...">'),
                HTML('<datalist id="tag-suggestions"></datalist>'),
                css_class='mb-3 text-start'
            ),
            Row(
                Column(
                    Submit('submit', 'Publish', css_class='btn btn-dark rounded-0 fw-semibold w-100'),
                    css_class='col-md-6 mb-2'
                ),
                Column(
                    HTML("<button type='submit' name='save_draft' class='btn btn-outline-dark rounded-0 fw-semibold w-100'>Save as Draft</button>"),
                    css_class='col-md-6 mb-2'
                ),
                css_class='justify-content-center'
            )
        )