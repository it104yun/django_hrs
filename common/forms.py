from django.utils import timezone
from datetime import date,datetime

import re
from crispy_forms.helper import FormHelper
from crispy_forms.layout import (
    HTML,Button, Div, Field, Layout,
)
from django.utils.translation import gettext_lazy as _

from django import forms
from django.urls import reverse_lazy

from components.easyui_components import EasyForm

from common.models import (
                            TopicOfUdc,
                            UserDefCode,
                            ProcessOptionsTxtDef,
                            RegActRules,
                            GoogleLanguage
                            )




class SearchForm(forms.Form):

    def __init__(self, display_fields, model_class=None, ukey='', *args, **kwargs):
        super(SearchForm, self).__init__(*args, **kwargs)
        self.model_class = model_class
        if model_class:
            self.display_fields = [(f.name, f.verbose_name) for f in model_class._meta.fields
                                   if f.name in display_fields]
        else:
            self.display_fields = [(item['name'], item['verbose_name']) for item in display_fields]
        self.data = []
        self.fields['keyword'] = forms.CharField(label=_('Query Keyword'), required=True)
        self.fields['field'] = forms.ChoiceField(label=_('Query Field'), choices=self.display_fields, required=True)
        self.helper = FormHelper(self)
        # self.helper.form_action = 'post'
        self.helper.form_id = ukey + "_monoSearchForm"
        self.helper.form_class = 'fm-search'
        self.helper.layout = Layout(
            Div(
                Field('field', id='field_' + ukey),
                css_class="p-2"
            ),
            Div(
                Field('keyword', id='keyword_' + ukey, size=60),
                css_class="p-2"
            ),
            Button('search_btn_' + ukey, _('Search'),
                   css_id='search_btn_' + ukey,
                   css_class="btn btn-sm btn-info btn-search")
        )

    def get_url(self):
        if self.model_class:
            url_parameter = self.convert_model_name()
            return reverse_lazy('model_handler', kwargs={'model': url_parameter})
        return '/'

    def convert_model_name(self):
        r = re.compile(r'[A-Z][a-z0-9]+')
        model_name = self.model_class.__name__
        url_parameter = ''
        while len(model_name) > 0:
            # 把Model名稱轉為url參數
            # e.x. PdsMain -> pds_main
            match = r.match(model_name)
            if match:
                word = match.group()
                model_name = model_name[len(word)::]
                url_parameter = '{}{}_'.format(url_parameter, word.lower())
            else:
                break
        url_parameter = url_parameter[0:-1]
        # 最後一個_拿掉
        return url_parameter



class ComplexSearchForm(SearchForm):

    def __init__(self, model_class, display_fields, ukey='', *args, **kwargs):
        super(ComplexSearchForm, self).__init__(model_class, display_fields, ukey, *args, **kwargs)
        logic_config = {
            'choices': (
                ('any', _('Any')),
                ('all', _('All')),
            ),
            'widget': forms.RadioSelect,
        }
        relation_choices = [
            ('>', _('Greater than')),
            ('=', _('Equal')),
            ('!=', _('Not Equal')),
            ('<', _('Less than')),
            ('include', _('Includes')),
            ('exclude', _('Not Includes')),
        ]
        self.fields['logic'] = forms.TypedChoiceField(
            **logic_config, label=_('Filter Logic'))
        self.fields['relation'] = forms.ChoiceField(
            choices=relation_choices, label=_('Match Logic'))

        self.helper = FormHelper(self)
        self.helper.form_action = reverse_lazy(
                'complex_search',
                kwargs={'model': self.convert_model_name()}
        )
        self.helper.form_id = "cpxSearchForm"
        self.helper.form_class = 'fm-cpx-search'
        self.helper.disable_csrf = True
        self.helper.layout = Layout(
            Div(
                Field('logic'),
                css_class="p-2 mb-1"
            ),
            Div(
                Div(
                    'field_' + ukey,
                    css_class="col-2 p-0"
                ),
                Div(
                    Field('relation'),
                    css_class="col-2 p-0"
                ),
                Div(
                    Field('keyword_' + ukey, size=55),
                    css_class="col-6 p-0"
                ),
                Div(
                    Button(
                        'add_filter_btn',
                        _('Add'),
                        css_id="add_filter_btn",
                        css_class="btn-sm position-absolute fixed-bottom btn-info"),
                    css_class="position-relative col-1 "
                ),
                css_class="p-2 d-flex col bg-light"
            ),
        )


class CustomSearchForm(forms.Form):

    def __init__(self, display_fields, model_class=None, ukey='', *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.model_class = model_class
        if model_class:
            self.display_fields = [(f.name, f.verbose_name) for f in model_class._meta.fields
                                   if f.name in display_fields]
        else:
            self.display_fields = [(item['name'], item['verbose_name']) for item in display_fields]
        self.data = []
        self.fields['keyword'] = forms.CharField(label=_('Query Keyword'), required=True)
        self.fields['field'] = forms.ChoiceField(label=_('Query Field'), choices=self.display_fields, required=True)
        self.helper = FormHelper(self)
        # self.helper.form_action = 'post'
        self.helper.form_id = ukey + "_monoSearchForm"
        self.helper.form_class = 'fm-search'
        self.helper.layout = Layout(
            Div(
                Field('field', id='field_' + ukey),
                css_class="p-2"
            ),
            Div(
                Field('keyword', id='keyword_' + ukey, size=60),
                css_class="p-2"
            ),
            Button('search_btn_' + ukey, _('Search'),
                   css_id='search_btn_' + ukey,
                   css_class="btn btn-sm btn-info btn-search")
        )

    def get_url(self):
        if self.model_class:
            url_parameter = self.convert_model_name()
            return reverse_lazy('model_handler', kwargs={'model': url_parameter})
        return '/'

    def convert_model_name(self):
        r = re.compile(r'[A-Z][a-z0-9]+')
        model_name = self.model_class.__name__
        url_parameter = ''
        while len(model_name) > 0:
            # 把Model名稱轉為url參數
            # e.x. PdsMain -> pds_main
            match = r.match(model_name)
            if match:
                word = match.group()
                model_name = model_name[len(word)::]
                url_parameter = '{}{}_'.format(url_parameter, word.lower())
            else:
                break
        url_parameter = url_parameter[0:-1]
        # 最後一個_拿掉
        return url_parameter



class CustomComplexSearchForm(SearchForm):

    def __init__(self, model_class, display_fields, ukey='', *args, **kwargs):
        super().__init__(model_class, display_fields, ukey, *args, **kwargs)
        logic_config = {
            'choices': (
                ('any', _('Any')),
                ('all', _('All')),
            ),
            'widget': forms.RadioSelect,
        }
        relation_choices = [
            ('>', _('Greater than')),
            ('=', _('Equal')),
            ('!=', _('Not Equal')),
            ('<', _('Less than')),
            ('include', _('Includes')),
            ('exclude', _('Not Includes')),
        ]
        self.fields['logic'] = forms.TypedChoiceField(
            **logic_config, label=_('Filter Logic'))
        self.fields['relation'] = forms.ChoiceField(
            choices=relation_choices, label=_('Match Logic'))

        self.helper = FormHelper(self)
        self.helper.form_action = reverse_lazy(
                'complex_search',
                kwargs={'model': self.convert_model_name()}
        )
        self.helper.form_id = "cpxSearchForm"
        self.helper.form_class = 'fm-cpx-search'
        self.helper.disable_csrf = True
        self.helper.layout = Layout(
            Div(
                Field('logic'),
                css_class="p-2 mb-1"
            ),
            Div(
                Div(
                    'field_' + ukey,
                    css_class="col-2 p-0"
                ),
                Div(
                    Field('relation'),
                    css_class="col-2 p-0"
                ),
                Div(
                    Field('keyword_' + ukey, size=55),
                    css_class="col-6 p-0"
                ),
                Div(
                    Button(
                        'add_filter_btn',
                        _('Add'),
                        css_id="add_filter_btn",
                        css_class="btn-sm position-absolute fixed-bottom btn-info"),
                    css_class="position-relative col-1 "
                ),
                css_class="p-2 d-flex col bg-light"
            ),
        )



class TopicOfUdcForm(EasyForm):
    class Meta:
        model = TopicOfUdc
        fields = [
            'topic_code',
            'topic_name',
            'app_model',
        ]

    def __init__(self, *args, **kwargs):
        tz = timezone.get_current_timezone()
        today = timezone.now().astimezone(tz)
        super().__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_action = '/api/data/topic_of_udc'
        self.helper.form_id = "main_form"
        self.helper.disable_csrf = True
        self.helper.layout = Layout(
            Div(
                Field('topic_code',style="width: 200px;", required=True),
                HTML("<p></p>"),
                Field('topic_name', style="width: 400px;", required=True),
                HTML("<p></p>"),
                Field('app_model', style="width: 120px;", required=True),
                css_class="p-3",
            )
        )


class UserDefCodeForm(EasyForm):
    class Meta:
        model = UserDefCode
        fields = [
            # 'parent',
            'topic_code',
            'udc',
            'desc1',
            'desc2',
            'description',
        ]

    def __init__(self, *args, **kwargs):
        tz = timezone.get_current_timezone()
        today = timezone.now().astimezone(tz)
        super().__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_action = '/api/data/user_def_code'
        self.helper.form_id = "main_form"
        self.helper.disable_csrf = True
        self.helper.layout = Layout(
            Div(
                Field('topic_code', style="width: 160px;", required=True),
                HTML('<p></p>'),
                Field('udc', style="width: 80px;",required=True),
                HTML('<p></p>'),
                Field('desc1', style="width: 150px;", required=True),
                HTML('<p></p>'),
                Field('desc2', style="width: 150px;", required=True),
                HTML('<p></p>'),
                Field('description', style="width:800px;", required=True),
                css_class="p-3",
            )
        )


class GoogleLanguageForm(EasyForm):
    class Meta:
        model = GoogleLanguage
        fields = [
            'lang_code',
            'lang_desc',
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_action = '/api/data/google_language'
        self.helper.form_id = "main_form"
        self.helper.disable_csrf = True
        self.helper.layout = Layout(
            Div(
                Field('lang_code', style="width: 160px;", required=True),
                HTML('<p></p>'),
                Field('lang_desc', style="width:300px;",required=False),
                css_class="p-3",
            )
        )