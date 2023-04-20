from crispy_forms.helper import FormHelper
from crispy_forms.layout import Div, Field, Layout, Row
from components.easyui_components import EasyForm

from django import forms
from django.contrib.auth.forms import AuthenticationForm as DjangoAuthenticationForm
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.conf import settings

from .models import (
    Factory,
    FactoryProgram,
    Program,
    ProgramAuth,
    UserData,
    FactoryAuth
)


class UserDataForm(EasyForm):
    """
    SY110 表單
    融合了三個表單的欄位: User、UserData、FactoryAuth
    但是以UserData為主要model，另外的採用人工加入。
    資料處理的URL為另外開的API接口 /api/user_data
    """

    class Meta:
        model = UserData
        fields = [
            'section_manager',
            'director',
        ]

    def __init__(self, *args, **kwargs):
        super(UserDataForm, self).__init__(*args, **kwargs)
        factories = Factory.objects.all()
        factory_choices = [(f.id, f.name) for f in factories]
        self.fields['username'] = forms.CharField(label=_("username"))
        self.fields['name'] = forms.CharField(label=_("name"), required=False)
        self.fields['factory'] = forms.MultipleChoiceField(
            required=False,
            widget=forms.CheckboxSelectMultiple,
            choices=factory_choices,
            label=_('factory')
        )

        self.helper = FormHelper(self)
        self.helper.form_action = '/api/user_data'
        self.helper.form_id = "main_form"
        self.helper.form_class = 'form'
        self.helper.form_method = 'POST'
        self.helper.disable_csrf = True       #查詢用或顯示用表單, 不需要csrf_token
        self.helper.layout = Layout(
            Div(
                'username',
                Field('name', disabled=True),
                # 'section_manager',
                # 'director',
                Row(
                    Field('factory', required=True),
                    css_class="mt-4"
                )
            ),
        )


class SimpleProgramMainForm(EasyForm):
    class Meta:
        model = Program
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(SimpleProgramMainForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_action = '#'
        self.helper.disable_csrf = True      #查詢用或顯示用表單, 不需要csrf_token
        self.helper.form_id = "form"
        self.helper.layout = Layout(
            Div(
                Field('enable', disabled=True),
                Field('program_id', readonly=True),
                Field('program_name', readonly=True),
                Field('module', disabled=True),
                css_class="text-white bg-dark"
            ),
        )


class AuthFormProgram(EasyForm):
    class Meta:
        model = ProgramAuth
        fields = '__all__'

    def __init__(self, user, *args, **kwargs):
        super(AuthFormProgram, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_action = reverse_lazy('model_handler', kwargs={'model': 'ProgramAuth'})
        self.helper.form_id = "main_form"
        self.helper.form_class = 'form'
        self.helper.form_method = 'POST'
        self.helper.disable_csrf = True     #查詢用或顯示用表單, 不需要csrf_token
        self.helper.layout = Layout(
            Div(
                Div(
                    Field('program'),
                )
            )
        )


class AuthFormUser(EasyForm):
    """
    SN130 表單
    """

    class Meta:
        model = ProgramAuth
        fields = [
            'program',
            'user',
            'create',
            'delete',
            'update',
            'read',
            'self_data',
            'all_data',
        ]

    def __init__(self, factory, *args, **kwargs):
        super(AuthFormUser, self).__init__(*args, **kwargs)
        programs = FactoryProgram.objects.filter(factory_id=factory['id'])
        program_choices = [(p.pk, p.program.program_name) for p in programs]
        self.fields['user_id'] = forms.CharField(widget=forms.HiddenInput())
        self.fields['program'].choices = program_choices
        self.helper = FormHelper(self)
        self.helper.form_action = '/api/program_auth'
        self.helper.form_id = "main_form"
        self.helper.form_class = 'form'
        self.helper.disable_csrf = True      #查詢用或顯示用表單, 不需要csrf_token
        self.helper.form_method = 'POST'
        self.helper.layout = Layout(
            Row(
                Field('program'),
                Field('user_id'),
                css_class="pb-3"
            ),
            Row(
                Field('create', css_class="pr-2", checked=True),
                Field('delete', css_class="pr-2", checked=True),
                Field('update', css_class="pr-2", checked=True),
                Field('read', css_class="pr-2", checked=True),
                Field('self_data', css_class="pr-2", checked=True),
                Field('all_data', css_class="pr-2", checked=True),
                css_class="d-flex"
            )
        )


class ProgramAuthForm(EasyForm):
    class Meta:
        model = ProgramAuth
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(ProgramAuthForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_action = reverse_lazy('model_handler', kwargs={'model': 'user'})
        self.helper.form_id = "main_form"
        self.helper.layout = Layout(
            Div(
                Div(
                    Field('user', css_class='mr-2'),
                    Field('program', css_class='mr-2'),
                    Field('read')
                )
            )
        )


class ProgramFactoryForm(EasyForm):
    class Meta:
        model = Factory
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(ProgramFactoryForm, self).__init__(*args, **kwargs)
        factories = Factory.objects.all()
        factory_choices = [(f.id, f.name) for f in factories]
        self.fields['factory'] = forms.MultipleChoiceField(
            required=False,
            widget=forms.CheckboxSelectMultiple,
            choices=factory_choices,
            label=_('Factory')
        )
        self.helper = FormHelper(self)
        self.helper.form_action = '/api/program_factory'
        self.helper.form_id = "main_form"
        self.helper.disable_csrf = True     #查詢用或顯示用表單, 不需要csrf_token
        self.helper.layout = Layout(
            Div(
                Field('factory', css_class='mr-2'),
            )
        )


class ProgramUserForm(EasyForm):
    """
    SN130 表單
    """

    class Meta:
        model = ProgramAuth
        fields = [
            'program',
            'user',
            'create',
            'delete',
            'update',
            'read',
            'self_data',
            'all_data',
        ]

    def __init__(self, factory, *args, **kwargs):
        super(ProgramUserForm, self).__init__(*args, **kwargs)
        users = FactoryAuth.objects.filter(factory_id=factory['id'])
        user_choices = [(p.user.username, p.user.name) for p in users]
        self.fields['program_id'] = forms.CharField(widget=forms.HiddenInput())
        self.fields['user'].choices = user_choices
        self.helper = FormHelper(self)
        self.helper.form_action = '/api/program_auth'
        self.helper.form_id = "main_form"
        self.helper.form_class = 'form'
        self.helper.disable_csrf = True              #查詢用或顯示用表單, 不需要csrf_token
        self.helper.form_method = 'POST'
        self.helper.layout = Layout(
            Row(
                Field('program_id'),
                Field('user'),
                css_class="pb-3"
            ),
            Row(
                Field('create', css_class="pr-2", checked=True),
                Field('delete', css_class="pr-2", checked=True),
                Field('update', css_class="pr-2", checked=True),
                Field('read', css_class="pr-2", checked=True),
                Field('self_data', css_class="pr-2", checked=True),
                Field('all_data', css_class="pr-2", checked=True),
                css_class="d-flex"
            )
        )


class AuthenticationForm(DjangoAuthenticationForm):
    error_messages = {
        'invalid_login': _("Please enter a correct %(username)s and password. "
                           "Or make sure you have the permission."),
    }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        language_choices = settings.LANGUAGES
        factory_choices = [(factory.id, factory.name) for factory in Factory.objects.all()]
        self.fields['factory'] = forms.ChoiceField(label=_('公司'), choices=factory_choices, required=True)
        self.fields['language'] = forms.ChoiceField(label=_('語言'), choices=language_choices)

