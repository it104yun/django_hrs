from django.utils import timezone
from datetime import date,datetime
from crispy_forms.helper import FormHelper
from crispy_forms.layout import (HTML, Button, ButtonHolder , Column, Div, Field, Fieldset,
                                 Layout, Row, Submit)

from django.conf import settings
from django import forms
from django.db.models import F, Q
from django.urls import reverse_lazy

from crispy_forms.bootstrap import (InlineRadios,
                                    TabHolder,Tab,
                                    FormActions
                                    )

from components.easyui_components import EasyForm
from common.models import UserDefCode
from apps.kpi.models import (EmployeeInfoEasy,
                             WorkcodeMapping,
                             DeptSupervisor
                             )
# from django.utils.translation import gettext_lazy as _
from django.utils.translation import gettext as _

from .models import (
                    JobTitle,
                    JobSkill,
                    JobTitleSkill,
                    EmployeeTitle,
                    StudyPlan,
                    MatrixMaster,
                    Factory,
                    PdcaMaster
                    )



dateToday = date.today()
Year = dateToday.year
Month = dateToday.month
Day = dateToday.day
Week = dateToday.weekday()


class EmployeeInfoEasyForm(EasyForm):

    class Meta:
        model = EmployeeInfoEasy
        fields = [
            'work_code',
            'chi_name',
            'factory',
            'factory_area',      #2021/07/22 add
            'dept_flevel',       #2021/07/22 add
            'dept',
            # 'dept_desc',         #2021/07/22 add
            'dept_description',
            'pos',
            'director',
            'direct_supv',       #2021/07/22 add v
            'arrival_date',
            'resign_date',
            'bonus_factor',
            'rank',
            'nat',
            'eval_class',
            'labor_type',
            'bonus_type',
            'email',
            'service_status',    #2021/07/22 add
            'trans_date',
            'trans_type',
            'kpi_diy',
            'pdca_agent',
        ]

    def __init__(self, *args, **kwargs):
        tz = timezone.get_current_timezone()
        today = timezone.now().astimezone(tz)
        super(EmployeeInfoEasyForm, self).__init__(*args, **kwargs)
        self.fields['kpi_diy'].widget = forms.widgets.Input(attrs={'type': 'checkbox'})
        self.fields['pdca_agent'].widget = forms.widgets.Input(attrs={'type': 'checkbox'})
        self.fields['arrival_date'].widget = forms.widgets.Input(attrs={'type': 'date'})
        self.fields['resign_date'].widget = forms.widgets.Input(attrs={'type': 'date'})
        self.fields['trans_date'].widget = forms.widgets.Input(attrs={'type': 'date'})
        dept_desc = UserDefCode.objects.filter(topic_code_id='dept_desc_id').order_by('description')
        dept_desc_choices = [('','---------------------------------------------------------------------------------------------------------')]
        dept_desc_choices = dept_desc_choices + [(desc.id,desc.description) for desc in dept_desc ]
        self.fields['dept_desc'] = forms.ChoiceField(choices=dept_desc_choices, label='部門全稱')
        self.helper = FormHelper(self)
        self.helper.form_action = '/sk_api/data/employee_info_easy'
        self.helper.form_id = "main_form"
        self.helper.layout = Layout(
            Div(
                Row(
                    HTML('<span style="padding: 10px;"></span>'),
                    Field('work_code', style="width: 120px;height:35px;", css_class="form-control", required=True),
                    HTML('<span style="padding: 5px;"></span>'),
                    Field('chi_name',  style="width: 120px;height:35px;", css_class="form-control", required=True),
                    HTML('<span style="padding: 5px;"></span>'),
                    Field('factory', style="10px;width: 150px;height:35px;",css_class="form-control", required=True),
                    HTML('<span style="padding: 5px;"></span>'),
                    Field('nat', style="width: 120px;height:35px;", css_class="form-control", required=True),
                ),
                HTML('<div style="height:5px;"></div>'),
                Row(
                    HTML('<span style="padding: 10px;"></span>'),
                    Field('service_status', style="width: 120px;height:35px;", type="email", css_class="form-control",
                          placeholder="name@example.com"),
                    HTML('<span style="padding: 5px;"></span>'),
                    Field('factory_area', style="10px;width: 120px;height:35px;", css_class="form-control",
                      required=True),
                    HTML('<span style="padding: 5px;"></span>'),
                    Field('email', style="width: 280px;height:35px;", type="email", css_class="form-control",
                          placeholder="name@example.com"),
                    HTML('<span style="padding: 10px;"></span>'),
                    Field('kpi_diy', css_class="form-control"),
                    HTML('<span style="padding: 10px;"></span>'),
                    Field('pdca_agent', css_class="form-control"),
                ),
                css_class="p-2 h7 text-dark shadow-lg bg-white",
                style="border-radius: 7px;",
            ),
            HTML("<hr>"),
            Div(
                Row(
                    Field('dept_flevel', style="width: 350px;height:35px;", css_class="form-control", required=True),
                    HTML('<span style="padding: 5px;"></span>'),
                    Field('dept', style="width: 350px;height:35px;", css_class="form-control", required=True),
                    # HTML('<span style="padding: 5px;"></span>'),
                    # Field('dept_desc', style="width: 350px;height:35px;", css_class="form-control", required=True),
                ),
                HTML('<div style="height:10px;"></div>'),
                Row(
                    Field('dept_description', style="width: 710px;height:35px;", css_class="form-control", required=True),
                ),
                # HTML('<p style="padding: 2px;"></p>'),
                HTML('<div style="height:10px;"></div>'),
                Row(
                    Field('director', style="width: 200px;height:35px;", css_class="form-control"),
                    HTML('<span style="padding: 5px;"></span>'),
                    Field('direct_supv', style="width: 200px;height:35px;", css_class="form-control"),
                    HTML('<span style="padding: 5px;"></span>'),
                    Field('pos', style="width: 180px;height:35px;", css_class="form-control", required=True),
                    HTML('<span style="padding: 5px;"></span>'),
                    Field('labor_type', style="width: 100px;height:35px;", css_class="form-control", required=True),
                ),
                # HTML('<p style="padding: 4px;"></p>'),
                HTML('<div style="height:10px;"></div>'),
                Row(
                    Field('arrival_date', style="width: 200px;height:35px;", css_class="form-control", required=True,
                          value=today.strftime("%Y-%m-%d")),
                    HTML('<span style="padding: 5px;"></span>'),
                    Field('resign_date', style="width: 200px;height:35px;", css_class="form-control"),
                    HTML('<span style="padding: 5px;"></span>'),
                    Field('trans_date', style="width: 180px;height:35px;", css_class="form-control"),
                    HTML('<span style="padding: 5px;"></span>'),
                    Field('trans_type', style="width: 100px;height:35px;", css_class="form-control"),
                ),
                # HTML('<p style="padding: 4px;"></p>'),
                HTML('<div style="height:10px;"></div>'),
                Row(
                    # Field('labor_type', style="width: 150px;height:35px;", css_class="form-control", required=True),
                    Field('bonus_type', style="width: 200px;height:35px;", css_class="form-control", required=True),
                    HTML('<span style="padding: 5px;"></span>'),
                    Field('bonus_factor', style="width: 135px;height:35px;", css_class="form-control", required=True),
                    HTML('<span style="padding: 5px;"></span>'),
                    Field('rank', style="width: 100px;height:35px;", css_class="form-control", required=True),
                    HTML('<span style="padding: 5px;"></span>'),
                    Field('eval_class', style="width: 135px;height:35px;", css_class="form-control", required=True),

                ),
                css_class ="p-4 h6 text-white shadow-lg bg-secondary",
                style="border-radius: 7px;",
            ),
        )
        self.helper.disable_csrf = True


class WorkcodeMappingForm(EasyForm):

    class Meta:
        model = WorkcodeMapping
        fields = [
            'factory',
            'work_code',
            'work_code_x',
            'chi_name',
            'alias_name',
            'factory_area',
        ]

    def __init__(self, *args, **kwargs):
        tz = timezone.get_current_timezone()
        today = timezone.now().astimezone(tz)
        super().__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_action = '/sk_api/data/workcode_mapping'
        self.helper.form_id = "main_form"
        # self.helper.layout = Layout(
        #     Div(
        #     )
        # )
        self.helper.disable_csrf = True


class DeptSupervisorForm(EasyForm):
    class Meta:
        model = DeptSupervisor
        fields = [
            'factory',
            'dept',
            'dept_upper',
            'dept_flevel',
            'dept_supervisor',
            'dept_description',
        ]

    def __init__(self, *args, **kwargs):
        tz = timezone.get_current_timezone()
        today = timezone.now().astimezone(tz)
        super().__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_action = '/sk_api/data/dept_supervisor'
        self.helper.form_id = "main_form"
        # self.helper.layout = Layout(
        #     Div(
        #     )
        # )
        self.helper.disable_csrf = True



class EmployeeMatrixForm(forms.Form):
    def __init__(self,*args, **kwargs):
        super().__init__(*args, **kwargs)      # 呼叫父類別(forms.form)的__init__(*args,**kwargs)
        self.helper = FormHelper(self)         # 由crispy_forms.helper 的  FormHelper來處理(而不用django預設的formhelper)
        self.helper.form_method = 'post'
        self.helper.form_id = "main_form"
        self.fields['work_code'] = forms.CharField(label='工號',disabled=True)
        self.fields['chi_name'] = forms.CharField(label='姓名',disabled=True)
        self.fields['dept_desc'] = forms.CharField(label='部門',disabled=True)
        self.fields['arrival_date'] = forms.CharField(label='到職日',disabled=True)
        self.fields['trans_date'] = forms.CharField(label='異動日',disabled=True)
        self.fields['trans_type'] = forms.CharField(label='異動類別',disabled=True)
        self.fields['rank_desc'] = forms.CharField(label='職等',disabled=True)
        self.fields['pos_desc'] = forms.CharField(label='職稱(位)',disabled=True)
        self.fields['factory_desc'] = forms.CharField(label='公司',disabled=True)
        # self.fields['pos_shc1'] = forms.CharField(label='主管職',disabled=True)
        # self.fields['pos_shc2'] = forms.CharField(label='營業報告書(是否需評核)',disabled=True)

        self.helper.layout = Layout(
            Div(
                Row(
                    Field('dept_desc', style="width: 200px;height:35px;", css_class="form-control",),
                    HTML('<span style="padding: 10px;"></span>'),
                    Field('arrival_date', style="width: 120px;height:35px;", css_class="form-control",),
                    HTML('<span style="padding: 10px;"></span>'),
                    Field('trans_date', style="width: 120px;height:35px;", css_class="form-control",),
                    HTML('<span style="padding: 10px;"></span>'),
                    Field('trans_type', style="width: 60px;height:35px;", css_class="form-control",),
                    HTML('<span style="padding: 10px;"></span>'),
                    Field('rank_desc', style="width: 40px;height:35px;", css_class="form-control",),
                    HTML('<span style="padding: 10px;"></span>'),
                    Field('pos_desc', style="width: 120px;height:35px;", css_class="form-control",),
                    HTML('<span style="padding: 10px;"></span>'),
                    Field('factory_desc', style="width: 100px;height:35px;",css_class="form-control",),
                    # HTML('<span style="padding: 10px;"></span>'),
                    # Field('pos_shc1', style="width: 100px;height:35px;", css_class="form-control", ),
                    # HTML('<span style="padding: 5px;"></span>'),
                    # Field('pos_shc2', style="width: 100px;height:35px;", css_class="form-control", ),
                    css_class="p-2 h7 text-dark shadow-lg bg-white  rounded",
                ),

            ),
            HTML("<hr>"),
        )
        self.helper.disable_csrf = True



class EmployeePdcaForm_X(forms.Form):
    def __init__(self,*args, **kwargs):
        super().__init__(*args,**kwargs)       # 呼叫父類別(forms.form)的__init__(*args,**kwargs)
        self.helper = FormHelper(self)         # 由crispy_forms.helper 的  FormHelper來處理(而不用django預設的formhelper)
        self.helper.form_method = 'post'
        self.helper.form_id = "X_form"


class EmployeePdcaForm(forms.Form):
    def __init__(self,userId,chi_name,*args, **kwargs):
        super().__init__(*args,**kwargs)      # 呼叫父類別(forms.form)的__init__(*args,**kwargs)
        self.helper = FormHelper(self)         # 由crispy_forms.helper 的  FormHelper來處理(而不用django預設的formhelper)
        self.helper.form_method = 'post'
        self.helper.form_id = "main_form"
        self.fields['work_code'] = forms.CharField(initial=userId,label=_("工號"),disabled=True)
        self.fields['chi_name'] = forms.CharField(initial=chi_name,label=_("姓名"),disabled=True)
        fields = ['dept_id__desc1',
                  'arrival_date',
                  'trans_date',
                  'trans_type',
                  'rank_id__desc1',
                  'pos_id__desc1',
                  'factory_id__name',
                  ]
        ee =EmployeeInfoEasy.objects.values_list(*fields).get(work_code=userId)

        self.fields['dept_desc'] = forms.CharField(initial=ee[0],label=_("部門"),disabled=True)
        self.fields['arrival_date'] = forms.CharField(initial=ee[1],label=_("到職日"),disabled=True)
        self.fields['trans_date'] = forms.CharField(initial=ee[2],label=_("異動日"),disabled=True)
        self.fields['trans_type'] = forms.CharField(initial=ee[3],label=_("異動類別"),disabled=True)
        self.fields['rank_desc'] = forms.CharField(initial=ee[4],label=_("職等"),disabled=True)
        self.fields['pos_desc'] = forms.CharField(initial=ee[5],label=_("職稱(位)"),disabled=True)
        self.fields['factory_desc'] = forms.CharField(initial=ee[6],label=_("公司"),disabled=True)

        qr1 = Q(work_code=userId)
        result = PdcaMaster.objects.values_list('the_time','bpm_status_desc1').filter( qr1 ).order_by('the_time').last()

        if result:
            last_time = result[0]
        else:
            last_time = 1

        the_time_show = _('第') + str(last_time) + _('版')

        self.fields['the_time'] = forms.CharField(initial=last_time,label=_('版本'),disabled=True)
        self.helper.layout = Layout(
            Div(
                Fieldset(
                    the_time_show,
                    Row(
                        # Field('the_time', style="display:none"),
                        Field('the_time',style="width: 40px;height:35px;", css_class="form-control", ),
                        HTML('<span style="padding: 10px;"></span>'),
                        Field('factory_desc', style="width: 100px;height:35px;", css_class="form-control", ),
                        HTML('<span style="padding: 10px;"></span>'),
                        Field('dept_desc', style="width: 200px;height:35px;", css_class="form-control", ),
                        HTML('<span style="padding: 10px;"></span>'),
                        Field('work_code', style="width: 100px;height:35px;", css_class="form-control"),
                        HTML('<span style="padding: 10px;"></span>'),
                        Field('chi_name', style="width: 80px;height:35px;", css_class="form-control", ),
                        HTML('<span style="padding: 10px;"></span>'),
                        Field('arrival_date', style="width: 120px;height:35px;", css_class="form-control",),
                        # HTML('<span style="padding: 10px;"></span>'),
                        # Field('trans_date', style="width: 120px;height:35px;", css_class="form-control",),
                        # HTML('<span style="padding: 10px;"></span>'),
                        # Field('trans_type', style="width: 60px;height:35px;", css_class="form-control",),
                        HTML('<span style="padding: 10px;"></span>'),
                        Field('rank_desc', style="width: 50px;height:35px;", css_class="form-control",),
                        HTML('<span style="padding: 10px;"></span>'),
                        Field('pos_desc', style="width: 120px;height:35px;", css_class="form-control",),
                        css_class="p-2 h7 text-dark shadow bg-white  rounded",
                    ),
                ),
            ),
            HTML("<hr>"),
        )
        self.helper.disable_csrf = True


class JobTitleForm(EasyForm):

    class Meta:
        model = JobTitle
        fields = [
            'job_code',
            'job_name',
            # 'job_desc',
            'level_number',
            'job_parent'
        ]

    def __init__(self, *args, **kwargs):
        tz = timezone.get_current_timezone()
        today = timezone.now().astimezone(tz)
        super().__init__(*args, **kwargs)
        self.fields['level_number'] = forms.CharField(label='職務階層', disabled=True)
        l1_choices = [ (T[0],T[0]+" "+T[1]) for T in JobTitle.objects.filter(level_number=1).values_list('job_code', 'job_name') ]
        self.fields['job_parent_parent'] = forms.ChoiceField(choices=l1_choices,label="大分類")
        self.fields['job_parent'].label = '中分類'
        self.helper = FormHelper(self)
        self.helper.form_id = "main_form"
        self.helper.form_action = '/sk_api/data/job_title'
        self.helper.layout = Layout(
            Div(
                Row(
                    HTML('<span style="padding: 5px;"></span>'),
                    Field('job_parent_parent', style="width: 250px;height:35px;font-size: large;color:blue;", required=True),
                ),
                HTML('<p style="padding: 10px;"></p>'),
                Row(
                    HTML('<span style="padding: 10px;"></span>'),
                    Field('job_parent', style="width: 250px;height:35px;font-size: large;color:blue;", required=True),
                ),
            ),
            HTML('<p style="padding: 10px;"></p>'),
            Div(
                Row(
                    Field('job_code',style="height:35px;", required=True),
                    HTML('<span style="padding: 5px;"></span>'),
                    Field('job_name',style="width: 300px;height:35px;", required=True),
                    HTML('<span style="padding: 5px;"></span>'),
                ),
                # HTML('<p style="padding: 4px;"></p>'),
                # Row(
                #     Field('job_desc', style="width: 600px;height:35px;", required=True),
                # ),
                css_class="p-4 h6 text-white shadow-lg bg-secondary",
                style="border-radius: 5px;",
            ),
        )


        self.helper.disable_csrf = True



class JobSkillForm(EasyForm):

    class Meta:
        model = JobSkill
        fields = [
            'skill_class',
            # 'job_level',
            'skill_code',
            'skill_name',
            # 'skill_desc',
        ]

    def __init__(self, *args, **kwargs):
        tz = timezone.get_current_timezone()
        today = timezone.now().astimezone(tz)
        super().__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_id = "main_form"
        self.helper.form_action = '/sk_api/data/job_skill'
        self.helper.layout = Layout(
            Div(
                Row(
                    HTML('<span style="padding: 5px;"></span>'),
                    Field('skill_class', style="width: 200px;height:35px;font-size: large;color:blue;",
                          required=True),
                ),
            ),
            HTML('<p style="padding: 10px;"></p>'),
            Div(
                Row(
                    Field('skill_code', style="height:35px;", required=True),
                    HTML('<span style="padding: 5px;"></span>'),
                    Field('skill_name', style="width: 550px;height:35px;", required=True),
                    HTML('<span style="padding: 5px;"></span>'),
                ),

                css_class="p-4 h6 text-white shadow-lg bg-secondary",
                style="border-radius: 5px;",
            ),
        )
        self.helper.disable_csrf = True




class JobTitleSkillForm(EasyForm):

    class Meta:
        model = JobTitleSkill
        fields = [
            'job_title',
            'order_number',
            'job_skill',
            # 'enable',
            # 'disable_date',
            # 'enable_date',
        ]

    def __init__(self, *args, **kwargs):
        tz = timezone.get_current_timezone()
        today = timezone.now().astimezone(tz)
        super().__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_id = "main_form"
        self.helper.form_action = '/sk_api/data/job_title_skill'

        job_title_l3 = JobTitle.objects.filter(level_number=3)
        l3_choices = [ (l3.job_code,l3.job_code+" "+l3.job_name)  for l3 in job_title_l3 ]
        self.fields['job_title'] = forms.ChoiceField(choices=l3_choices, label='職務')
        pr_choices = [('','-'*30)]
        pr_id = UserDefCode.objects.get(topic_code_id='skill_class_id',desc1='專業職能').id
        pr_all = JobSkill.objects.filter(skill_class_id=pr_id)
        pr_choices = pr_choices + [ (pr.skill_code,pr.skill_code+" "+pr.skill_name)  for pr in pr_all ]
        self.fields['job_skill'] = forms.ChoiceField(choices=pr_choices, label='職能')

        self.helper.layout = Layout(
            Div(
                Row(
                    HTML('<span style="padding: 5px;"></span>'),
                    Field('job_title', style="width: 200px;height:35px;",required=True),
                    HTML('<span style="padding: 20px;"></span>'),
                    Field('order_number', style="width: 80px;height:35px;", required=True),
                    HTML('<span style="padding: 20px;"></span>'),
                    Field('job_skill', style="width: 500px;height:35px;", required=True),
                ),
            ),
        )
        self.helper.disable_csrf = True


class EmployeeTitleForm(EasyForm):

    class Meta:
        model = EmployeeTitle
        fields = [
            'work_code',
            'job_title',
            # 'enable',
            # 'disable_date',
            # 'enable_date',
        ]

    def __init__(self, *args, **kwargs):
        tz = timezone.get_current_timezone()
        today = timezone.now().astimezone(tz)
        super().__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_id = "main_form"
        self.helper.form_action = '/sk_api/data/employee_title'


        employee = EmployeeInfoEasy.objects.filter( ~Q(work_code__endswith='-000') )
        employee_choices = [ (ee.work_code,ee.work_code+" "+ee.chi_name)  for ee in employee ]
        self.fields['work_code'] = forms.ChoiceField(choices=employee_choices, label='工號/姓名')

        job_title_l3 = JobTitle.objects.filter(level_number=3)
        l3_choices = [ (l3.job_code,l3.job_code+" "+l3.job_name)  for l3 in job_title_l3 ]
        self.fields['job_title'] = forms.ChoiceField(choices=l3_choices, label='職務')


        self.helper.layout = Layout(
            Div(
                Row(
                    HTML('<span style="padding: 5px;"></span>'),
                    Field('work_code', style="width: 300px;height:35px;",required=True),
                ),
                HTML('<p style="padding: 10px;"></p>'),
                Row(
                    HTML('<span style="padding: 5px;"></span>'),
                    Field('job_title', style="width: 520px;height:35px;", required=True),
                ),
            ),
        )
        self.helper.disable_csrf = True



class StudyPlanForm(EasyForm):

    class Meta:
        model = StudyPlan
        fields = [
            'study_code',
            'study_name',
            # 'study_course',
        ]

    def __init__(self, *args, **kwargs):
        tz = timezone.get_current_timezone()
        today = timezone.now().astimezone(tz)
        super().__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_id = "main_form"
        self.helper.form_action = '/sk_api/data/study_plan'
        self.helper.layout = Layout(
            Div(
                Row(
                    Field('study_code', style="height:35px;", required=True),
                ),
                HTML('<p style="padding: 10px;"></p>'),
                Row(
                    Field('study_name', style="width: 550px;height:35px;", required=True),
                ),
                css_class="p-4 h6 text-white shadow-lg bg-secondary",
                style="border-radius: 5px;",
            ),
        )
        self.helper.disable_csrf = True

class MatrixMasterForm(EasyForm):

    class Meta:
        model = MatrixMaster
        fields = [
            'work_code_title',
            'year',
            'month',
        ]
        # fields = [
        #     'work_code_title__work_code__direct_supv',
        #     'work_code_title__work_code__direct_supv__chi_name',
        #     'work_code_title__work_code__dept_flevel__desc1',
        #     'work_code_title__work_code',
        #     'work_code_title__work_code__chi_name',
        #     'work_code_title__job_title',
        #     'work_code_title__job_title__job_name',
        #     'year',
        #     'month',
        #     'bpm',
        #     'bpm__bpm_status_desc1',
        #     'bpm__report_url',
        # ]

    def __init__(self, *args, **kwargs):
        tz = timezone.get_current_timezone()
        today = timezone.now().astimezone(tz)
        super().__init__(*args, **kwargs)
        self.fields["direct_supv"] = forms.CharField(label="主管工號")
        self.fields["supv_name"] = forms.CharField(label="主管姓名")
        self.fields["dept"] = forms.CharField(label="一級部門")
        self.helper = FormHelper(self)
        self.helper.form_id = "main_form"
        self.helper.form_action = '/sk_api/data/matrix_master'
        self.helper.layout = Layout(
            Div(
                Row(
                    Field('direct_supv', style="width:120px;height:30px;", disabled=True),
                    HTML('<p style="padding: 5px;"></p>'),
                    Field('supv_name', style="width:120px;height:30px;", disabled=True),
                    HTML('<p style="padding: 5px;"></p>'),
                    Field('year', style="width: 100px;height:30px;", required=True),
                    HTML('<p style="padding: 5px;"></p>'),
                    Field('month', style="width: 80px;height:30px;", required=True),
                ),
                Row(
                    Field('dept', style="width:450px;height:30px;", disabled=True),
                ),
                Row(
                    Field('work_code_title', style="width: 450px;height:35px;",required=True),
                ),
                css_class="p-4 text-white shadow-lg bg-secondary",
                style="border-radius: 5px;width:500px",
            ),
        )
        self.helper.disable_csrf = True


class EmployeeSearchForm1(forms.Form):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.disable_csrf = True
        self.helper.form_class = 'form-horizontal'
        # self.helper.label_class = 'col-lg-2'
        # self.helper.field_class = 'col-lg-8'


        # corp_choices = [('','所有資料')]
        results = Factory.objects.all()
        corp_choices = [(udc.id,udc.name) for udc in results ]
        self.fields['all_corp'] = forms.ChoiceField(choices=corp_choices, label='公司&nbsp;&nbsp;')

        results = UserDefCode.objects.filter(topic_code_id='dept_id')
        dept_choices = [(udc.id,udc.desc1) for udc in results ]
        self.fields['all_corp'] = forms.ChoiceField(choices=corp_choices, label='公司&nbsp;&nbsp;')
        self.fields['all_dept'] = forms.ChoiceField(choices=dept_choices, label='部門&nbsp;&nbsp;')

        self.helper.layout = Layout(
            Div(
              Row(
                  HTML('<span style="padding-left: 30px;"></span>'),
                  Field('all_corp', style="height:35px;"),
                  # HTML('<p style="padding: 15px;"></p>'),
                  # Button('clear_btn', '清除查詢', css_id='clear_btn', css_class='btn btn-warning' , style="height:35px;"),
              ),
                Row(
                    HTML('<span style="padding-left: 30px;"></span>'),
                    Field('all_dept', style="height:35px;width:300px;"),
                    HTML('<span style="padding: 10px;"></span>'),
                    Button('search_btn', '查詢', css_id='search_btn', css_class='btn btn-info', style="height:35px;"),
                    # HTML('<p style="padding: 15px;"></p>'),
                    # Button('clear_btn', '清除查詢', css_id='clear_btn', css_class='btn btn-warning' , style="height:35px;"),
                )
            ),
        )


class DepartmentChoiceForm(forms.Form):
    def __init__(self, userId , chi_name , *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.disable_csrf = True
        self.helper.form_class = 'form-horizontal'
        self.helper.form_method= 'post'
        ee =EmployeeInfoEasy.objects.values_list('work_code','chi_name','dept_flevel_id__desc1').filter(direct_supv=userId).order_by('dept_flevel_id','work_code')   #印出明細, 不用distinct
        commQ = Q(id__in=EmployeeInfoEasy.objects.values_list('dept_flevel_id', flat=True).filter(direct_supv=userId).order_by('dept_flevel_id').distinct('dept_flevel_id') )     # 找到『直接主管』是userID的工號
        results = UserDefCode.objects.filter(commQ)
        dept_choices = [ (dept.id,dept.desc1) for dept in results ]
        self.fields['all_dept'] = forms.ChoiceField(choices=dept_choices, label='選擇部門&nbsp;&nbsp;')

        self.helper.layout = Layout(
            Div(
              Row(
                  HTML('<span  style="padding: 30px;text-align: center;color:red;"><h5>您好，因您管轄多個部門，需分開做盤點及BPM簽核<br>請選擇其中一個部門做盤點</h5></span>'),
              ),
              Row(
                  HTML('<p style="padding: 40px;"></p>'),
                  Field('all_dept', id="all_dept",style="height:35px;width:200px;"),
                  HTML('<p style="padding: 20px;"></p>'),
                  Button('check_btn', '確認', css_id='check_btn', css_class='btn btn-info', style="height:35px;"),
              ),
            ),
        )



class EmployeeSearchForm2(forms.Form):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.disable_csrf = True
        self.helper.form_class = 'form-horizontal'
        self.helper.form_method= 'post'
        qry = Q(id__in=EmployeeInfoEasy.objects.values_list('factory_id', flat=True).order_by('factory_id').distinct('factory_id') )     #部門
        results = Factory.objects.filter(qry)
        # corp_choices = [("all","全公司") + (corp.id,corp.name) for corp in results ]
        corp_choices = [("all","全部")] + [(corp.id,corp.name) for corp in results ]

        qry = Q(id__in=EmployeeInfoEasy.objects.values_list('dept_flevel_id', flat=True).order_by('dept_flevel_id').distinct('dept_flevel_id') )     #一級部門
        results = UserDefCode.objects.filter(qry)
        # dept_flevel_choices = [ ("all","所有部門") + (dept.id,dept.desc1) for dept in results ]
        dept_flevel_choices = [("all","全部")] +  [ (dept.id,dept.desc1) for dept in results ]

        qry = Q(id__in=EmployeeInfoEasy.objects.values_list('dept_id', flat=True).order_by('dept_id').distinct('dept_id') )     #部門
        results = UserDefCode.objects.filter(qry)
        # dept_choices = [ ("all","所有部門") + (dept.id,dept.desc1) for dept in results ]
        dept_choices = [("all","全部")] + [ (dept.id,dept.desc1) for dept in results ]

        # self.fields['all_corp'] = forms.ChoiceField(choices=corp_choices, label='公&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;司&nbsp;&nbsp;&nbsp;&nbsp;')
        self.fields['all_corp'] = forms.ChoiceField(choices=corp_choices, label='公司&nbsp;&nbsp;')
        self.fields['all_dept_flevel'] = forms.ChoiceField(choices=dept_flevel_choices, label='一級部門&nbsp;&nbsp;')
        self.fields['all_dept'] = forms.ChoiceField(choices=dept_choices, label='部&nbsp;&nbsp;門&nbsp;&nbsp;別&nbsp;&nbsp;')

        self.helper.layout = Layout(
            Div(
              Row(
                  # HTML('<p style="padding: 40px;"></p>'),
                  Field('all_corp', id="all_corp",style="height:35px;width:200px;"),
                  HTML('<p>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</p>'),
                  Button('ee_search_btn', '搜尋', css_id='ee_search_btn', css_class='btn btn-info', style="height:35px;"),
              ),
                # Row(
                #     # HTML('<p style="padding: 40px;"></p>'),
                #     Field('all_dept_flevel', id="all_dept_flevel", style="height:35px;width:200px;"),
                # ),
                # Row(
                #     # HTML('<p style="padding: 40px;"></p>'),
                #     Field('all_dept', id="all_dept", style="height:35px;width:200px;"),
                # ),
                # Row(
                #     Button('ee_search_btn', '搜尋', css_id='ee_search_btn', css_class='btn btn-info', style="height:35px;"),
                #     HTML('<p>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</p>'),
                #     Button('ee_clear_btn', '清除', css_id='ee_clear_btn', css_class='btn btn-info', style="height:35px;"),
                # ),
            ),
        )


class EmployeeSearchForm3(forms.Form):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.disable_csrf = True
        self.helper.form_class = 'form-horizontal'
        self.helper.form_method= 'post'
        qry = Q(id__in=EmployeeInfoEasy.objects.values_list('factory_id', flat=True).order_by('factory_id').distinct('factory_id') )     #部門
        results = Factory.objects.filter(qry)
        corp_choices = [("all","全部")] + [(corp.id,corp.name) for corp in results ]
        self.fields['all_corp'] = forms.ChoiceField(choices=corp_choices, label='公&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;司&nbsp;&nbsp;')
        self.fields['all_dept_flevel'] = forms.ChoiceField(label='一級部門&nbsp;&nbsp;')
        self.fields['all_dept'] = forms.ChoiceField(label='部&nbsp;&nbsp;門&nbsp;&nbsp;別&nbsp;&nbsp;')
        self.fields['all_director'] = forms.ChoiceField(label='評核主管&nbsp;&nbsp;')
        self.fields['all_direct_supv'] = forms.ChoiceField(label='直接主管&nbsp;&nbsp;')

        self.helper.layout = Layout(
            Div(
              Row(
                  # HTML('<p style="padding: 40px;"></p>'),
                  Field('all_corp', id="all_corp",name="all_corp",style="height:35px;width:150px;"),
                  HTML('<p style="padding-left:30px"></p>'),
                  HTML('<p style="background:#dddddd;color:red;height:35px;font-size:24px;font-weight: bolder;">單選</p>'),
              ),
                Row(
                    # HTML('<p style="padding: 40px;"></p>'),
                    Field('all_dept_flevel', id="all_dept_flevel", name="all_dept_flevel", style="height:35px;width:400px;",css_class='easyui-textbox text-center'),
                    # Field('all_dept_flevel', id="all_dept_flevel", name="all_dept_flevel", style="height:35px;width:400px;"),
                    HTML('<p style="padding-left:30px"></p>'),
                    HTML('<p style="background:navy;color:yellow;height:20px;width:50px;">可複選</p>'),
                ),
                Row(
                    # HTML('<p style="padding: 40px;"></p>'),
                    Field('all_dept', id="all_dept", name="all_dept", style="height:35px;width:400px;",css_class='easyui-textbox text-center'),
                    # Field('all_dept', id="all_dept", name="all_dept", style="height:35px;width:400px;"),
                    HTML('<p style="padding-left:30px"></p>'),
                    HTML('<p style="background:navy;color:yellow;height:20px;width:50px;">可複選</p>'),
                ),
                Row(
                    # HTML('<p style="padding: 40px;"></p>'),
                    Field('all_director', id="all_director", name="all_dept", style="height:35px;width:250px;",css_class='easyui-textbox text-center'),
                    # Field('all_director', id="all_director", name="all_dept", style="height:35px;width:250px;"),
                    HTML('<p style="padding-left:30px"></p>'),
                    HTML('<p style="background:navy;color:yellow;height:20px;width:50px;">可複選</p>'),
                ),
                Row(
                    # HTML('<p style="padding: 40px;"></p>'),
                    Field('all_direct_supv', id="all_direct_supv", name="all_dept", style="height:35px;width:250px;",css_class='easyui-textbox text-center'),
                    # Field('all_direct_supv', id="all_direct_supv", name="all_dept", style="height:35px;width:250px;"),
                    HTML('<p style="padding-left:30px"></p>'),
                    HTML('<p style="background:navy;color:yellow;height:20px;width:50px;">可複選</p>'),
                ),
                Row(
                    HTML('<p style="padding-left:100px"></p>'),
                    Button('ee_search_btn', '搜尋', css_id='ee_search_btn', css_class='btn btn-info', style="height:35px;"),
                    # Button('ee_search_btn', '搜尋', css_id='easyui-linkbutton', css_class='btn btn-info', style="height:35px;"),
                    HTML('<p style="padding-left:50px"></p>'),
                    Button('ee_clear_btn', '清除', css_id='ee_clear_btn', css_class='btn btn-info', style="height:35px;"),
                    # Button('ee_clear_btn', '清除', css_id='easyui-linkbutton', css_class='btn btn-info', style="height:35px;"),
                ),
            ),
        )



class ChoiceLanguage(forms.Form):
    def __init__(self,language_code,*args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.disable_csrf = True
        self.helper.form_class = 'form-horizontal'
        self.helper.form_method = 'get'
        self.helper.form_id = 'form_choice_lang'
        language = settings.LANGUAGES
        language_choices = language[1:len(language)]
        self.fields['choice_lang'] = forms.ChoiceField(initial=language_code,choices=language_choices, label='請選取語言／ Vui lòng chọn ngôn ngữ ')

        self.helper.layout = Layout(
            Row(
                Field('choice_lang', id="choice_lang",name="choice_lang",style="width:150px;height:30px;font-size:smaller;"),
            ),)
