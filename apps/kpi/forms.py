from django.utils import timezone
import calendar
from datetime import date,datetime,timedelta
from crispy_forms.helper import FormHelper
from crispy_forms.layout import (HTML, Button, ButtonHolder , Column, Div, Field, Fieldset,
                                 Layout, Row, Submit)


from django import forms
from django.db.models import F, Q
from django.urls import reverse_lazy
from jsignature.forms import JSignatureField
from jsignature.widgets import JSignatureWidget


from components.easyui_components import EasyForm
from .models import (EmployeeInfoEasy,
                     MetricsSetup,
                     MetricsCalc,
                     ScoreSheet,
                     WorkingYM,
                     ScoreStatus,
                     SignatureModel,
                     # EeAttendDetails,
                     # EeAttendSummary,
                     )

dateToday = date.today()
Year = dateToday.year
Month = dateToday.month
Day = dateToday.day
Week = dateToday.weekday()


class EmployeeCommonMetricForm(EasyForm):
    class Meta:
        model = EmployeeInfoEasy
        fields = [
            'work_code',
            # 'corp',
            'factory',
        ]

    def __init__(self, *args, **kwargs):
        tz = timezone.get_current_timezone()
        today = timezone.now().astimezone(tz)
        super().__init__(*args, **kwargs)
        self.fields["work_code"] = forms.CharField(label="共同指標代號")
        self.helper = FormHelper(self)
        self.helper.form_action = '/api/data/employee_info_easy'
        self.helper.form_id = "main_form"
        self.helper.disable_csrf = True
        self.helper.layout = Layout(
            Div(
                Field('work_code',style="width: 120px;", required=True),
                # HTML("&nbsp;&nbsp;&nbsp;&nbsp;"),
                # Field('corp',  style="width: 120px;", required=True),
                HTML("&nbsp;&nbsp;&nbsp;&nbsp;"),
                Field('factory', style="width: 120px;", required=True),
                css_class="p-3",
            )
        )

'''
class EeAttendDetailsForm(EasyForm):
    class Meta:
        model = EeAttendDetails
        fields = [
            'work_code',
            'attend_date',
            'attend_type_01',
            'attend_value_01',
            'attend_type_02',
            'attend_value_02',
            'attend_type_03',
            'attend_value_03',
            'attend_type_04',
            'attend_value_04',
            'attend_type_05',
            'attend_value_05',
            'attend_type_06',
            'attend_value_06',
            'attend_type_07',
            'attend_value_07',
            'attend_type_08',
            'attend_value_08',
            'attend_type_09',
            'attend_value_09',
            'attend_type_10',
            'attend_value_10',
            'attend_type_11',
            'attend_value_11',
        ]

    def __init__(self, *args, **kwargs):
        super(EeAttendDetailsForm, self).__init__(*args, **kwargs)
        self.fields['attend_date'].widget = forms.widgets.Input(attrs={'type': 'date'})
        self.helper = FormHelper(self)
        self.helper.form_action = '/api/data/ee_attend_details'
        self.helper.form_id = "main_form"
        self.helper.disable_csrf = True
        self.helper.layout = Layout(
            Div(
                Row(
                    Field('work_code', required=True),
                    HTML("&nbsp;&nbsp;&nbsp;&nbsp;"),
                    Field('attend_date', required=True),
                    css_class="p-3",
                ),
            ),
            HTML("<hr>"),
            Div(
                Row(
                    Field('attend_type_01',
                          style="width: 100px;border-style:hidden;color:yellow;font-weight: bold;background-color: darkblue;"),
                    HTML("&nbsp;&nbsp;&nbsp;&nbsp;"),
                    Field('attend_type_02',
                          style="width: 100px;border-style:hidden;color:yellow;font-weight: bold;background-color: darkblue;"),
                    HTML("&nbsp;&nbsp;&nbsp;&nbsp;"),
                    Field('attend_type_03',
                          style="width: 100px;border-style:hidden;color:yellow;font-weight: bold;background-color: darkblue;"),
                    HTML("&nbsp;&nbsp;&nbsp;&nbsp;"),
                    Field('attend_type_04',
                          style="width: 100px;border-style:hidden;color:yellow;font-weight: bold;background-color: darkblue;"),
                    HTML("&nbsp;&nbsp;&nbsp;&nbsp;"),
                    Field('attend_type_05',
                          style="width: 100px;border-style:hidden;color:yellow;font-weight: bold;background-color: darkblue;"),
                    css_class="p-1",
                ),
                Row(
                    Field('attend_value_01', style="width:100px; text-align: right;"),
                    HTML("&nbsp;&nbsp;&nbsp;&nbsp;"),
                    Field('attend_value_02', style="width:100px; text-align: right;"),
                    HTML("&nbsp;&nbsp;&nbsp;&nbsp;"),
                    Field('attend_value_03', style="width:100px; text-align: right;"),
                    HTML("&nbsp;&nbsp;&nbsp;&nbsp;"),
                    Field('attend_value_04', style="width:100px; text-align: right;"),
                    HTML("&nbsp;&nbsp;&nbsp;&nbsp;"),
                    Field('attend_value_05', style="width:100px; text-align: right;"),
                    css_class="p-1",
                ),
                HTML("<hr>"),
                Row(
                    Field('attend_type_06',
                          style="width: 100px;border-style:hidden;color:yellow;font-weight: bold;background-color: darkblue;"),
                    HTML("&nbsp;&nbsp;&nbsp;&nbsp;"),
                    Field('attend_type_07',
                          style="width: 100px;border-style:hidden;color:yellow;font-weight: bold;background-color: darkblue;"),
                    HTML("&nbsp;&nbsp;&nbsp;&nbsp;"),
                    Field('attend_type_08',
                          style="width: 100px;border-style:hidden;color:yellow;font-weight: bold;background-color: darkblue;"),
                    css_class="p-1",
                ),
                Row(
                    Field('attend_value_06', style="width:100px; text-align: right;"),
                    HTML("&nbsp;&nbsp;&nbsp;&nbsp;"),
                    Field('attend_value_07', style="width:100px; text-align: right;"),
                    HTML("&nbsp;&nbsp;&nbsp;&nbsp;"),
                    Field('attend_value_08', style="width:100px; text-align: right;"),
                    css_class="p-1",
                ),
                HTML("<hr>"),
                Row(
                    Field('attend_type_09',
                          style="width: 100px;border-style:hidden;color:white;font-weight: bold;background-color: darkblue;"),
                    HTML("&nbsp;&nbsp;&nbsp;&nbsp;"),
                    Field('attend_type_10',
                          style="width: 100px;border-style:hidden;color:white;font-weight: bold;background-color: darkblue;"),
                    HTML("&nbsp;&nbsp;&nbsp;&nbsp;"),
                    Field('attend_type_11',
                          style="width: 100px;border-style:hidden;color:white;font-weight: bold;background-color: darkblue;"),
                    css_class="p-1",
                ),
                Row(
                    Field('attend_value_09', style="width:100px; text-align: right;"),
                    HTML("&nbsp;&nbsp;&nbsp;&nbsp;"),
                    Field('attend_value_10', style="width:100px; text-align: right;"),
                    HTML("&nbsp;&nbsp;&nbsp;&nbsp;"),
                    Field('attend_value_11', style="width:100px; text-align: right;"),
                    css_class="p-1",
                ),
                css_class="container p-3 my-3 bg-secondary text-white",
            )
        )



class EeAttendSummaryForm(EasyForm):
    class Meta:
        model = EeAttendSummary
        fields = [
            'work_code',
            # 'metrics',
            'date_yyyy',
            # 'date_mm',
            'attend_type_01',
            'attend_value_01',
            'attend_type_02',
            'attend_value_02',
            'attend_type_03',
            'attend_value_03',
            'attend_type_04',
            'attend_value_04',
            'attend_type_05',
            'attend_value_05',
            'attend_type_06',
            'attend_value_06',
            'attend_type_07',
            'attend_value_07',
            'attend_type_08',
            'attend_value_08',
            'attend_type_09',
            'attend_value_09',
            'attend_type_10',
            'attend_value_10',
            'attend_type_11',
            'attend_value_11',

        ]

    def __init__(self, *args, **kwargs):
        super(EeAttendSummaryForm, self).__init__(*args, **kwargs)
        YEAR_CHOICES = [
            (Year-1,Year-1),
            (Year,Year),
        ]
        self.fields['date_yyyy'] = forms.ChoiceField(choices=YEAR_CHOICES, label='年份')
        self.helper = FormHelper(self)
        self.helper.form_action = '/api/data/ee_attend_summary'
        self.helper.form_id = "main_form"
        self.helper.disable_csrf = True
        self.helper.layout = Layout(
            Div(
                Row(
                    Field('work_code', required=True),
                    HTML("&nbsp;&nbsp;&nbsp;&nbsp;"),
                    Field('date_yyyy', required=True),
                    HTML("&nbsp;&nbsp;&nbsp;&nbsp;"),
                    # Field('date_mm', required=True, disabled=True, style="width: 100px;"),
                    css_class="p-3",
                ),
            ),
            HTML("<hr>"),
            Div(
                Row(
                    Field('attend_type_01', disabled=True,
                          style="width: 100px;border-style:hidden;color:yellow;font-weight: bold;background-color: darkblue;"),
                    HTML("&nbsp;&nbsp;&nbsp;&nbsp;"),
                    Field('attend_type_02', disabled=True,
                          style="width: 100px;border-style:hidden;color:yellow;font-weight: bold;background-color: darkblue;"),
                    HTML("&nbsp;&nbsp;&nbsp;&nbsp;"),
                    Field('attend_type_03', disabled=True,
                          style="width: 100px;border-style:hidden;color:yellow;font-weight: bold;background-color: darkblue;"),
                    HTML("&nbsp;&nbsp;&nbsp;&nbsp;"),
                    Field('attend_type_04', disabled=True,
                          style="width: 100px;border-style:hidden;color:yellow;font-weight: bold;background-color: darkblue;"),
                    HTML("&nbsp;&nbsp;&nbsp;&nbsp;"),
                    Field('attend_type_05', disabled=True,
                          style="width: 100px;border-style:hidden;color:yellow;font-weight: bold;background-color: darkblue;"),
                    css_class="p-1",
                ),
                Row(
                    Field('attend_value_01', style="width:100px; text-align: right;"),
                    HTML("&nbsp;&nbsp;&nbsp;&nbsp;"),
                    Field('attend_value_02', style="width:100px; text-align: right;"),
                    HTML("&nbsp;&nbsp;&nbsp;&nbsp;"),
                    Field('attend_value_03', style="width:100px; text-align: right;"),
                    HTML("&nbsp;&nbsp;&nbsp;&nbsp;"),
                    Field('attend_value_04', style="width:100px; text-align: right;"),
                    HTML("&nbsp;&nbsp;&nbsp;&nbsp;"),
                    Field('attend_value_05', style="width:100px; text-align: right;"),
                    css_class="p-1",
                ),
                HTML("<hr>"),
                Row(
                    Field('attend_type_06',disabled=True,
                          style="width: 100px;border-style:hidden;color:yellow;font-weight: bold;background-color: darkblue;"),
                    HTML("&nbsp;&nbsp;&nbsp;&nbsp;"),
                    Field('attend_type_07',disabled=True,
                          style="width: 100px;border-style:hidden;color:yellow;font-weight: bold;background-color: darkblue;"),
                    HTML("&nbsp;&nbsp;&nbsp;&nbsp;"),
                    Field('attend_type_08',disabled=True,
                          style="width: 100px;border-style:hidden;color:yellow;font-weight: bold;background-color: darkblue;"),
                    css_class="p-1",
                ),
                Row(
                    Field('attend_value_06', style="width:100px; text-align: right;"),
                    HTML("&nbsp;&nbsp;&nbsp;&nbsp;"),
                    Field('attend_value_07', style="width:100px; text-align: right;"),
                    HTML("&nbsp;&nbsp;&nbsp;&nbsp;"),
                    Field('attend_value_08', style="width:100px; text-align: right;"),
                    css_class="p-1",
                ),
                HTML("<hr>"),
                Row(
                    Field('attend_type_09',disabled=True,
                          style="width: 100px;border-style:hidden;color:white;font-weight: bold;background-color: darkblue;"),
                    HTML("&nbsp;&nbsp;&nbsp;&nbsp;"),
                    Field('attend_type_10',disabled=True,
                          style="width: 100px;border-style:hidden;color:white;font-weight: bold;background-color: darkblue;"),
                    HTML("&nbsp;&nbsp;&nbsp;&nbsp;"),
                    Field('attend_type_11',disabled=True,
                          style="width: 100px;border-style:hidden;color:white;font-weight: bold;background-color: darkblue;"),
                    css_class="p-1",
                ),
                Row(
                    Field('attend_value_09', style="width:100px; text-align: right;"),
                    HTML("&nbsp;&nbsp;&nbsp;&nbsp;"),
                    Field('attend_value_10', style="width:100px; text-align: right;"),
                    HTML("&nbsp;&nbsp;&nbsp;&nbsp;"),
                    Field('attend_value_11', style="width:100px; text-align: right;"),
                    css_class="p-1",
                ),
                css_class="container p-3 my-3 bg-secondary text-white",
            ),

        )
'''

class MetricsSetupForm(EasyForm):
    class Meta:
        model = MetricsSetup
        fields = [
            'work_code',
            'metrics_type',
            'date_yyyy',
            'date_mm',
            'order_number',
            'order_item',
            # 'metrics_content',
            'metrics_txt1',
            'metrics_number',
            'metrics_txt2',
            'unit_Mcalc',
            'allocation',
            'asc_desc',
            'asc_desc_score',
            'confirmed',
            # 'auto_alloc',
            # 'alloc_range',
            # 'low_limit',
        ]


    def __init__(self, *args, **kwargs):
        super(MetricsSetupForm, self).__init__(*args, **kwargs)
        month_choices = [('', '---'), ]
        month_choices = month_choices + [(m, m) for m in range(0,13)]
        self.fields['date_mm'] = forms.ChoiceField(choices=month_choices,label="月份")
        self.fields['allocation_tot'] = forms.IntegerField(label='配分合計', disabled=True)
        self.fields['metrics_txt1']= forms.CharField(widget=forms.Textarea,label='衡量指標(前綴)')
        self.fields['metrics_number'].label = '(關鍵數字)'
        self.fields['metrics_txt2'].label = '衡量指標(後綴)'
        self.fields['metrics_txt1'] = forms.CharField(label='衡量指標(前綴)')
        self.fields['confirmed'].label = ''
        # self.fields['confirmed'] = forms.CharField(widget=forms.TextInput,label='確認')
        self.helper = FormHelper(self)
        self.helper.form_action = '/api/data/metrics_setup'
        self.helper.form_id = "main_form"

        self.helper.layout = Layout(
            Div(
                Row(
                    HTML("&nbsp;&nbsp;&nbsp;&nbsp;"),
                    Field('work_code',style="height:35px;",  required=True ),
                    HTML("&nbsp;&nbsp;&nbsp;&nbsp;"),
                    Field('metrics_type', style="height:35px;", required=True),
                    HTML("&nbsp;&nbsp;&nbsp;&nbsp;"),
                    Field('date_yyyy', style="width:90px;height:35px;text-align: right;", required=True),
                    HTML("&nbsp;&nbsp;&nbsp;&nbsp;"),
                    Field('date_mm', style="width:75px;height:35px;text-align: right;", required=True),
                    HTML("&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;"),
                    HTML("*計算方式:"),
                    Field('asc_desc', style="width:75px;height:35px;text-align: right;",required=True),
                    HTML("&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;"),
                    HTML("*得分:"),
                    Field('asc_desc_score', style="width:75px;height:35px;text-align: right;", required=True),
                    HTML("&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;"),
                    HTML("&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;"),
                    HTML("&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;"),
                    HTML("&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;"),
                    Field('allocation_tot',style="width:100px;height:35px;text-align: right;color:blue;font-weight:bold;",),
                    HTML("&nbsp;&nbsp;&nbsp;&nbsp;"),
                    Field('confirmed', style="width:0px;height:0px;text-align: right;display:none",),
                    css_class="pb-1",
                ),
            ),
            Div(
                Row(
                    HTML("&nbsp;&nbsp;"),
                    Field('order_number', style="width:70px;height:35px;text-align: right;", required=True),
                    HTML("&nbsp;&nbsp;"),
                    Field('order_item', style="width:70px;height:35px;text-align: right;", required=True),
                    HTML("&nbsp;&nbsp;"),
                    Field('metrics_txt1', style="width:400px;height:35px;", required=True),
                    HTML("&nbsp;&nbsp;"),
                    Field('metrics_number', style="width:100px;height:35px;text-align:right;", required=True),
                    HTML("&nbsp;&nbsp;"),
                    Field('unit_Mcalc', style="width:80px;height:35px;", required=True),
                    HTML("&nbsp;&nbsp;"),
                    Field('metrics_txt2', style="width:160px;height:35px;"),
                    HTML("&nbsp;&nbsp;"),
                    Field('allocation', style="width:100px;height:35px;text-align: right;", required=True),
                    HTML("&nbsp;&nbsp;"),
                ),
                css_class="container pb-1 my-3 bg-secondary text-white",
            ),
            HTML("<hr>")
        )
        self.helper.disable_csrf = True


class MetricsSetupCommonForm(EasyForm):
    class Meta:
        model = MetricsSetup
        fields = [
            'work_code',
            'metrics_type',
            'date_yyyy',
            'date_mm',
            'order_number',
            'order_item',
            'metrics_txt1',
            'metrics_number',
            'metrics_txt2',
            'unit_Mcalc',
            'low_limit',
            'allocation',
            'score_type',
        ]


    def __init__(self, *args, **kwargs):
        super(MetricsSetupCommonForm, self).__init__(*args, **kwargs)

        #ForeignKey要指定初值，否則會將全部的relation data通通載入，
        #          PM204/PM208(KPI衡量指標設定)，速度上雖然有一點慢而已，定義初值，希望在上線後，員工增加後，不會拖跨速度
        # self.fields['work_code'] = forms.ChoiceField(choices=[],label='共同指標代號')   #2021/5/19 增加
        month_choices = [('', '---'), ]
        month_choices = month_choices + [(m, m) for m in range(0,13)]
        number_choices = [('', '---'), ]
        number_choices = number_choices + [(n, n) for n in range(0,51)]
        self.fields['date_mm'] = forms.ChoiceField(choices=month_choices,label="月份")
        self.fields['order_number'] = forms.ChoiceField(choices=number_choices, label="順序")
        self.fields['order_item'] = forms.ChoiceField(choices=number_choices, label="順序細項")
        self.fields['allocation_tot'] = forms.IntegerField(label='配分合計', disabled=True)
        self.fields['metrics_txt1']= forms.CharField(widget=forms.Textarea,label='衡量指標(前綴)')
        self.fields['metrics_number'].label = '(關鍵數字)'
        self.fields['metrics_txt2'].label = '衡量指標(後綴)'
        self.helper = FormHelper(self)
        self.helper.form_action = '/api/data/metrics_setup'
        self.helper.form_id = "main_form"

        self.helper.layout = Layout(
            Div(
                Row(
                    HTML("&nbsp;&nbsp;&nbsp;&nbsp;"),
                    Field('work_code',style="height:35px;",  required=True ),
                    HTML("&nbsp;&nbsp;&nbsp;&nbsp;"),
                    Field('metrics_type', style="height:35px;", required=True),
                    HTML("&nbsp;&nbsp;&nbsp;&nbsp;"),
                    Field('date_yyyy', style="width:90px;height:35px;text-align: right;", required=True),
                    HTML("&nbsp;&nbsp;&nbsp;&nbsp;"),
                    Field('date_mm', style="width:75px;height:35px;text-align: right;", required=True),
                    HTML("&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;"),
                    HTML("&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;"),
                    Field('score_type', style="width:120px;height:35px;text-align: right;", required=True ),
                    HTML("&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;"),
                    HTML("&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;"),
                    Field('allocation_tot',style="width:120px;height:35px;text-align: right;color:blue;font-weight:bold;",),
                    css_class="pb-1",
                ),
            ),
            Div(
                Row(
                    HTML("&nbsp;&nbsp;"),
                    Field('order_number', style="width:70px;height:35px;text-align: right;", required=True),
                    HTML("&nbsp;&nbsp;"),
                    Field('order_item', style="width:70px;height:35px;text-align: right;", required=True),
                    HTML("&nbsp;&nbsp;"),
                    Field('metrics_txt1', style="width:400px;height:35px;", required=True),
                    HTML("&nbsp;&nbsp;"),
                    Field('metrics_number', style="width:100px;height:35px;text-align:right;", required=True),
                    HTML("&nbsp;&nbsp;"),
                    Field('unit_Mcalc', style="width:80px;height:35px;", required=True),
                    HTML("&nbsp;&nbsp;"),
                    Field('metrics_txt2', style="width:160px;height:35px;"),
                    HTML("&nbsp;&nbsp;"),
                    Field('low_limit', style="width:100px;height:35px;text-align: right;", required=True),
                    HTML("&nbsp;&nbsp;"),
                    Field('allocation', style="width:100px;height:35px;text-align: right;", required=True),
                    HTML("&nbsp;&nbsp;"),
                ),
                # css_class="container pb-1 my-3 bg-secondary text-white",
                css_class="pb-1 my-3 bg-secondary text-white",
            ),
            HTML("<hr>")
        )
        self.helper.disable_csrf = True



class MetricsSetupEasyForm(EasyForm):
    class Meta:
        model = MetricsSetup
        fields = [
            'work_code',
            'metrics_type',
            'date_yyyy',
            'date_mm',
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['allocation_tot'] = forms.IntegerField(label='配分合計(個人指標)', disabled=True)
        self.fields['score_tot'] = forms.IntegerField(label='得分小計', disabled=True)
        self.helper = FormHelper(self)
        self.helper.form_action = '/api/data/metrics_setup'
        self.helper.form_id = "main_form"
        self.helper.layout = Layout(
            Div(
                Row(
                    Div(
                        Row(
                            HTML("&nbsp;&nbsp;&nbsp;&nbsp;"),
                            Field('work_code',style="height:35px;",),
                            HTML("&nbsp;&nbsp;&nbsp;&nbsp;"),
                            Field('metrics_type', style="height:35px;",),
                            HTML("&nbsp;&nbsp;&nbsp;&nbsp;"),
                            Field('date_yyyy', style="width:100px;height:35px;text-align: right;",),
                            HTML("&nbsp;&nbsp;&nbsp;&nbsp;"),
                            Field('date_mm', style="width:80px;height:35px;text-align: right;",),
                            HTML("&nbsp;&nbsp;&nbsp;&nbsp;"),
                            Field('allocation_tot',style="width:150px;height:35px;text-align: right;color:blue;font-weight:bold;",),
                            HTML("&nbsp;&nbsp;&nbsp;&nbsp;"),
                            css_class="pb-1 my-3 bg-secondary text-white",
                        ),
                    ),
                    HTML("&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;"),
                    HTML("&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;"),
                    Field('score_tot', style="width:200px;height:68px;text-align: right;font-size:28px;background:Black;color:White;",),
                ),
            ),
            HTML("<hr>")
        )
        self.helper.disable_csrf = True



class MetricsCalcForm(EasyForm):
    class Meta:
        model = MetricsCalc
        fields = [
            'metrics',
            'order_number',
            'calc_content',
            'lower_limit',
            'upper_limit',
            'score',
            # 'ef_date',
            # 'exp_date',
        ]

    def __init__(self, *args, **kwargs):
        super(MetricsCalcForm, self).__init__(*args, **kwargs)
        self.fields['order_number'].label = '計算順序'
        self.helper = FormHelper(self)
        self.helper.form_action = '/api/data/metrics_calc'
        #ForeignKey要指定初值，否則會將全部的relation data通通載入，
        #          PM206/PM210(KPI計算方式設定)，就是因為載入所有「metrics」的資料，才造成資料『初次載入』緩慢到１分鐘以上
        self.fields['metrics'] = forms.ChoiceField(choices=[])   #2021/5/19 增加
        # self.fields['metrics'] = forms.IntegerField()   #2021/5/20 修改
        self.helper.layout = Layout(
            Field('metrics',),
            Row(
                Field('order_number', style="width:60px;height:35px;", required=True),
                HTML("&nbsp;&nbsp;"),
                Field('calc_content', style="width:700px;height:35px;", required=True),
                HTML("&nbsp;&nbsp;"),
                Field('lower_limit', style="width:100px;height:35px;text-align:right;", required=True),
                HTML("&nbsp;&nbsp;"),
                Field('upper_limit', style="width:100px;height:35px;text-align:right;", required=True,),
                HTML("&nbsp;&nbsp;"),
                Field('score', style="width:100px;height:35px;text-align: right;", required=True),
                css_class="container pb-1 my-3 bg-secondary text-white",
                style="width: 1200px;",
            ),
        )
        self.helper.form_id = "main_form"
        self.helper.disable_csrf = True

#沒用到
class EmployeeImportForm(forms.Form):
    title = forms.CharField(max_length=50)
    file = forms.FileField()


#沒用到
class UploadFileForm(forms.Form):
    title = forms.CharField(max_length=50)
    file = forms.FileField()


#沒用到
class EmployeeCopyForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super(EmployeeCopyForm, self).__init__(*args,**kwargs);
        ee_choices = EmployeeInfoEasy.objects.values_list('work_code', 'chi_name').filter(
            ~Q(work_code__work_code__endswith='-000'),
            ~Q(work_code__work_code__endswith='-100'))  # '-000'共同指標, '-100'出勤指標

        all_list = []
        work_code = ''
        chi_name = ''
        for xx in ee_choices:
            for yy in xx:
                if xx.index(yy) == 0:
                    work_code = yy
                elif xx.index(yy) == 1:
                    chi_name = yy
            all_list.append((work_code,chi_name))
        xx_choices = [
            ('a', 'Arabic'),
            ('b', 'Bulgarian'),
            ('c', 'Catalan'),
        ]
        self.fields['work_code'] = forms.ChoiceField(
            choices=xx_choices, label='來源工號:')

        self.fields['copy_to_1'] = ""
        self.fields['copy_to_2'] = ""
        self.fields['copy_to_3'] = ""
        self.helper = FormHelper(self)
        # self.helper.form_action = reverse_lazy('employee_copy')
        self.helper.form_id = "copy_Form"
        self.helper.disable_csrf = True
        self.helper.layout = Layout(
            Div(
                Div(
                    Field('work_code', css_id="work_code",  required=True),
                    css_class="p-2 mb-1"
                ),
                Div(
                    Field('copy_to_1', css_id="copy_to_1", style="width:90%", required=True),
                    css_class="easyui-textbox"
                ),
                Div(
                    Field('copy_to_2', css_id="copy_to_2", style="width:90%"),
                    css_class="easyui-textbox"
                ),
                Div(
                    Field('copy_to_3', css_id="copy_to_3", style="width:90%"),
                    css_class="easyui-textbox"
                ),
                Div(
                    ButtonHolder(
                        Submit('submit', 'Submit',  style="width:80px"),
                        css_class = 'easyui-linkbutton'
                    ),
                css_class="easyui-panel"
                ),
            )
        )




class WorkingYMForm(EasyForm):
    class Meta:
        model = WorkingYM
        fields = [
            'date_yyyy',
            'date_mm',
        ]

    def __init__(self, *args, **kwargs):
        tz = timezone.get_current_timezone()
        today = timezone.now().astimezone(tz)
        super().__init__(*args, **kwargs)


        self.fields['date_yyyy'] = forms.ChoiceField(choices=((str(Y), Y) for Y in range(Year-2, Year+2)),label='年份')
        self.fields['date_mm'] = forms.ChoiceField(choices=((str(M), M) for M in range(0, 13)),label='月份')

        self.helper = FormHelper(self)
        self.helper.form_action = '/api/data/working_y_m'
        self.helper.form_id = "main_form"
        self.helper.disable_csrf = True
        self.helper.layout = Layout(
            Div(

                Row(
                    Field(HTML("***目前評核年月"),style="color:red;font-size:20px"),
                    HTML("&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;"),
                    Field("date_yyyy",style="width:80px;"),
                    HTML("&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;"),
                    Field("date_mm", style="width:80px;"),
                    css_class="container pb-1 my-3 bg-secondary text-white", style="width: 500px;",
                ),
            ),

        )


class CloseWorkingYMForm(EasyForm):
    class Meta:
        model = WorkingYM
        fields = [
            'date_yyyy',
            'date_mm',
            'before_lastdate',
            'diy_date',
        ]


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['date_yyyy'].label = ""
        self.fields['date_mm'].label = ""
        self.fields['new_date_yyyy'] = forms.IntegerField(initial=0,label='')
        self.fields['new_date_mm'] = forms.IntegerField(initial=0,label='')
        self.fields['diy_date'].label = ""
        self.fields['new_diy_date'] = forms.DateField(label='')
        self.fields['new_diy_date'].widget = forms.widgets.Input(attrs={'type': 'date'})
        self.helper = FormHelper(self)
        self.helper.form_action = '/api/data/working_y_m'
        self.helper.form_id = "main_form"
        self.helper.disable_csrf = True
        self.helper.layout = Layout(
            Div(
                Row(HTML("<h2>關帳前</h2>"),),
                Row(
                    HTML("評核年月"),
                    HTML("&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;"),
                    Field("date_yyyy",style="width:120px;text-align:center;",css_class="form-control",disabled=True),
                    # Field("date_yyyy",style="width:120px;text-align:center;",css_class="form-control",),
                    HTML("&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;"),
                    Field("date_mm", style="width:120px;text-align:center;",css_class="form-control",disabled=True),
                    # Field("date_mm", style="width:120px;text-align:center;",css_class="form-control",),
                    HTML("<hr style='width: 900px;border-top: 1px dotted black;'>"),
                    HTML("自評期限"),
                    HTML("&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;"),
                    Field("diy_date", style="width:200px;text-align:center;", css_class="form-control", disabled=True),
                    # Field("diy_date", style="width:200px;text-align:center;", css_class="form-control", ),
                    HTML("<hr style='width: 900px;border-top: 1px dotted black;'>"),
                    # HTML('<div  style="background-color:gray;color:yellow; border-radius: 5px;font-size: larger;text-align: center;"> 按下「確定關帳」後，關帳前的評核年月，將無法新增/修改/刪除，只可查詢</div>'),
                    css_class="h6 text-dark shadow-lg p-sm-5 bg-white",
                    style="border-radius: 20px; width: 650px;",
                ),
                Row(HTML("<p>&nbsp;</p>"), ),
                Row(HTML('<div  style="background-color:black;color:yellow;letter-spacing: 1px;font-size: large;;text-align: center;">&nbsp;按下「確定關帳」後，關帳前的評核年月，將無法新增/修改/刪除，只可查詢&nbsp;</div>'), ),
                Row(HTML("<p>&nbsp;</p>"), ),
                Row(HTML("<h1 style='color:red;font-weight:bolder;'>關帳後</h1>"), ),
                Row(
                    HTML("評核年月"),
                    HTML("&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;"),
                    Field("new_date_yyyy", style="width:102px;color:red;text-align:center;",css_class="form-control", disabled=True),
                    # Field("new_date_yyyy", style="width:102px;color:red;text-align:center;",css_class="form-control", ),
                    HTML("&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;"),
                    Field("new_date_mm", style="width:120px;color:red;text-align:center;",css_class="form-control", disabled=True),
                    # Field("new_date_mm", style="width:120px;color:red;text-align:center;",css_class="form-control", ),
                    HTML("<hr style='width: 900px;border-top: 1px dotted black;'>"),
                    HTML("自評期限"),
                    HTML("&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;"),
                    Field("new_diy_date", style="width:200px;color:red;text-align:center;", css_class="form-control"),
                    HTML("&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;"),
                    css_class="h6 text-white shadow-lg p-sm-5 bg-secondary",
                    style="border-radius: 20px;width: 650px;",
                ),
            ),

        )


class ScoreStatusForm(EasyForm):
    class Meta:
        model = ScoreStatus
        fields = [
            'work_code',
            'date_yyyy',
            'quarter',
            'report_url',
            'bpm_number',
            'bpm_status',
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        cancel_url = "http://127.0.0.1:8000/media-files/reports/pdf/KPI20211020162100599.pdf"
        self.helper = FormHelper(self)
        self.helper.form_action = '/api/data/score_status'
        self.helper.form_id = "main_form"
        self.helper.disable_csrf = True
        self.helper.layout = Layout(
            Div(
                # Row(
                #     Field('work_code',style="width: 120px;", disabled=True),
                #     HTML("&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;"),
                #     Field('date_yyyy', style="width: 120px;", disabled=True),
                #     HTML("&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;"),
                #     Field('quarter', style="width: 120px;", disabled=True),
                # ),
                # Row(
                #     Field('bpm_number', style="width: 150px;", disabled=True),
                #     HTML("&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;"),
                #     Field('bpm_status', style="width: 120px;", disabled=True),
                # ),
                # css_class="p-3",
            ),
        )


class SignatureForm(EasyForm):
    class Meta:
        model = SignatureModel
        fields = [
            'id',
            'signature',
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['signature']=JSignatureField(widget=JSignatureWidget(jsignature_attrs={'color': '#CCC'}))
        self.helper = FormHelper(self)
        self.helper.form_action = '/api/data/signature_model'
        self.helper.form_id = "main_form"
        self.helper.disable_csrf = True
        self.helper.layout = Layout(
            Div(
                Field('signature'),
            ),
        )

