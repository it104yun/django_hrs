from django.http import HttpResponse,HttpResponseRedirect
from django.shortcuts import render

from django.db.models import Q, F
from django.forms.models import model_to_dict
from django.urls import reverse_lazy

import io
from django.http import  FileResponse

from common.models import UserDefCode,ProcessOptionsTxtDef,RegActRules


from .models import (EmployeeInfoEasy,
                     MetricsSetup,
                     MetricsCalc,
                     ScoreSheet,
                     ScoreStatus,
                     WorkingYM,
                     SignatureModel,
                     # EeAttendDetails,
                     # EeAttendSummary,
                     )

from common.views import ManipulateBaseView, DoubleView, SingleView, BaseLayoutView
from .forms import (
                    EmployeeCommonMetricForm,
                    # EmployeeInfoEasyForm,
                    MetricsSetupForm,
                    MetricsSetupCommonForm,
                    MetricsSetupEasyForm,
                    MetricsCalcForm,
                    WorkingYMForm,
                    CloseWorkingYMForm,
                    UploadFileForm,
                    ScoreStatusForm,
                    SignatureForm,
                    # EeAttendDetailsForm,
                    # EeAttendSummaryForm,
                    )

from apps.skill_pdca.forms import EmployeeInfoEasyForm

class PM004(SingleView):
    main_model = EmployeeInfoEasy
    form_param = {}
    form_class = EmployeeInfoEasyForm
    template_name = 'kpi/pm004.html'
    title = '員工簡易資料'

    """ GRID 資料 """
    main_fields = [
        'work_code',
        'chi_name',
        'dept',
        'director',
        'factory',
    ]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["main_dg_config"]["source_url"] = '/api/data/employee_info_easy'
        context["import_url"] = '/api/employee_import_update/'                    #由 excel 匯入的處理網址
        context["copy_url"] = '/api/employee_copy/'                        #複製的處理網址
        return context

''''
class PM006(SingleView):
    main_model = EeAttendSummary
    form_param = {}
    form_class = EeAttendSummaryForm
    template_name = 'kpi/pm006.html'
    title = '員工出勤彙總'

    """ GRID 資料 """
    main_fields = [
        'work_code',
        'date_yyyy',
    ]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["main_dg_config"]["source_url"] = '/api/data/ee_attend_summary'
        context["import_url"] = '/api/ee_attend_summary_import/'                    #由 excel 匯入的處理網址
        return context
'''

class PM202(SingleView):
    main_model = WorkingYM
    form_param = {}
    form_class = WorkingYMForm
    template_name = 'kpi/pm202.html'
    title = '評核年月設定'

    """ GRID 資料 """
    main_fields = [
        'date_yyyy',
        'date_mm',
    ]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["main_dg_config"]["source_url"] = '/api/data/working_y_m'
        return context



class PM203(SingleView):
    main_model = WorkingYM
    form_param = {}
    form_class = CloseWorkingYMForm
    template_name = 'kpi/pm203.html'
    title = '評核年月關帳'

    """ GRID 資料 """
    main_fields = [
        'date_yyyy',
        'date_mm',
        'diy_date',
        'before_lastdate',
    ]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['before_lastdate']=WorkingYM.objects.get(id=1).before_lastdate
        context["main_dg_config"]["source_url"] = '/api/data/working_y_m'
        return context


class PM204(SingleView):
    main_model = MetricsSetup
    main_sort = 'work_code'
    custom_model = EmployeeInfoEasy
    custom_sort = 'work_code'
    form_param = {}
    form_class = MetricsSetupCommonForm   #main_form(center)
    template_name = 'kpi/pm204.html'
    title = '共同衡量指標設定'

    """ 下面GRID config-->display_fields """
    main_fields = [
        'order_number',
        'order_item',
        'metrics_content',
        'unit_Mcalc',
        'low_limit',
        'allocation',
        'metrics_txt1',
        'metrics_number',
        'metrics_txt2',
        'score_type',
    ]

    custom_fields = [
        'work_code',
        'chi_name',
        'director_id',
    ]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # context["main_dg_config"]["source_url"] = '/api/data/metrics_setup'
        # context["main_dg_config"]["source_url"] = '/api/metrics_setup'
        context["expand_url"] = '/api/metrics_setup_expand/'                      #展開的處理網址
        context["copy_url"] = '/api/metrics_setup_copy/'                        #複製的處理網址
        context["expandCommon_url"] = '/api/metrics_setup_expandCommon/'                      #展開的處理網址
        context["recallCommon_url"] = '/api/metrics_setup_recallCommon/'                      #展開的處理網址

        # north side's grid
        context.update({
            "employee_info_easy_dg_config": {
                "display_fields": [
                    {'name': 'work_code', 'verbose_name': '工號'},
                    {'name': 'chi_name', 'verbose_name': '姓名'},
                    {'name': 'dept_name', 'verbose_name': '部門'},
                    {'name': 'pos_name', 'verbose_name': '職位'},
                    {'name': 'director_id', 'verbose_name': '主管工號'},
                    {'name': 'director_name', 'verbose_name': '主管名稱'},
                    {'name': 'arrival_date', 'verbose_name': '到職日'},
                    {'name': 'resign_date', 'verbose_name': '離職日'},
                    {'name': 'rank', 'verbose_name': '職等'},
                    {'name': 'bonus_factor', 'verbose_name': '點數'},
                    {'name': 'eval_class', 'verbose_name': 'BSC/KPI'},
                    {'name': 'nat', 'verbose_name': '國籍'},
                ],
                "model": None,
                "source_url": reverse_lazy('get_metrics_setup_common'),     # 使用自己定義的Grid
            }
        })

        # east side's grid(js 要記得定義metrics_setupDate_dg, 不然資料跑不出來)
        context.update({
            "metrics_setupDate_dg_config":{
                "display_fields": [
                    {'name': 'work_code', 'verbose_name': '工號',},
                    {'name': 'date_yyyy', 'verbose_name': '年份',},
                    {'name': 'date_mm', 'verbose_name': '月份',},
                ],
                "model": None,
                "source_url":reverse_lazy('get_metrics_setupDate_data',),
            }
        })
        return context


class PM206(SingleView):
    main_model = MetricsCalc
    form_param = {}
    form_class = MetricsCalcForm  # main_form(center)
    main_sort = 'metrics_id'
    template_name = 'kpi/pm206.html'
    title = '共同衡量計算方式'

    """ 下面GRID 資料 """
    main_fields = [
        'order_number',
        'calc_content',
        'lower_limit',
        'upper_limit',
        'score',
    ]


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # north side's grid
        context.update({
            "employee_info_easy_dg_config": {
                "display_fields": [
                    {'name': 'work_code', 'verbose_name': '工號'},
                    {'name': 'chi_name', 'verbose_name': '姓名'},
                    {'name': 'dept_name', 'verbose_name': '部門'},
                    {'name': 'pos_name', 'verbose_name': '職位'},
                    {'name': 'director_id', 'verbose_name': '主管工號'},
                    {'name': 'director_name', 'verbose_name': '主管名稱'},
                    {'name': 'arrival_date', 'verbose_name': '到職日'},
                    {'name': 'resign_date', 'verbose_name': '離職日'},
                    {'name': 'rank', 'verbose_name': '職等'},
                    {'name': 'bonus_factor', 'verbose_name': '點數'},
                    {'name': 'eval_class', 'verbose_name': 'BSC/KPI'},
                    {'name': 'nat', 'verbose_name': '國籍'},
                ],
                "model": None,
                "source_url": reverse_lazy('get_metrics_setup_common'),     # 使用自己定義的Grid
            }
        })

        # south side's grid(js 要記得定義, 不然資料跑不出來)
        context.update({
            "metrics_setup_dg_config": {
                "display_fields": [
                    {'name': 'order_number', 'verbose_name': '順序'},
                    {'name': 'metrics_content', 'verbose_name': '衡量指標*內容'},
                    {'name': 'allocation', 'verbose_name': '衡量指標*配分'},
                ],
                "model": None,
                "source_url": reverse_lazy(
                    'model_handler', kwargs={'model': 'metrics_setup'}),
            }
        })
        # east side's grid(js 要記得定義metrics_setupDate_dg, 不然資料跑不出來)
        context.update({
            "metrics_setupDate_dg_config":{
                "display_fields": [
                    {'name': 'work_code', 'verbose_name': '工號',},
                    {'name': 'date_yyyy', 'verbose_name': '年份',},
                    {'name': 'date_mm', 'verbose_name': '月份',},
                ],
                "model": None,
                "source_url":reverse_lazy('get_metrics_setupDate_data',),
            }
        })
        return context





class PM208(SingleView):
    main_model = MetricsSetup
    main_sort = 'work_code'
    custom_model = EmployeeInfoEasy
    custom_sort = 'work_code'
    form_param = {}
    form_class = MetricsSetupForm   #main_form(center)
    template_name = 'kpi/pm208.html'
    title = '個人衡量指標設定'

    """ 下面GRID config-->display_fields """
    main_fields = [
        'order_number',
        'order_item',
        'asc_desc',
        'asc_desc_score',
        'metrics_content',
        'unit_Mcalc',
        'allocation',
        'confirmed',
        'metrics_txt1',
        'metrics_number',
        'metrics_txt2',
    ]

    custom_fields = [
        'work_code',
        'chi_name',
        'director_id',
    ]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # context["main_dg_config"]["source_url"] = '/api/data/metrics_setup'
        # context["main_dg_config"]["source_url"] = '/api/metrics_setup'
        context["expand_url"] = '/api/metrics_setup_expand/'                      #展開的處理網址
        context["copy_url"] = '/api/metrics_setup_copy/'                        #複製的處理網址
        # context["batch_dele_url"] = '/api/metrics_setup_batch_dele/'                        #複製的處理網址

        # 2021/2/25修改
        commQ = Q(eval_class__in=UserDefCode.objects.filter(Q(topic_code_id='eval_class_id'),~Q(desc1='BSC')))  # 2021/07/14 ADD 拿掉BSC的人
        commQ1 = ~Q(work_code__endswith='-000')  # '-000'共同指標, '-100'出勤指標
        commQ2 = ~Q(work_code__endswith='-100')
        commQ3 = Q(director=self.request.user.username)
        sub_employee_dict = {}

        sub_employee_list = list(EmployeeInfoEasy.objects.values_list('work_code', 'chi_name').filter(commQ1,commQ2,commQ3,commQ))  # '-000'共同指標, '-100'出勤指標
        for T in sub_employee_list:
            sub_employee_dict[T[0]] = T[1]

        # north side's grid
        context.update({
            "employee_info_easy_dg_config": {
                "display_fields": [
                    {'name': 'work_code', 'verbose_name': '工號'},
                    {'name': 'chi_name', 'verbose_name': '姓名'},
                    {'name': 'dept_name', 'verbose_name': '部門'},
                    {'name': 'pos_name', 'verbose_name': '職位'},
                    {'name': 'director_id', 'verbose_name': '主管工號'},
                    {'name': 'director_name', 'verbose_name': '主管名稱'},
                    {'name': 'arrival_date', 'verbose_name': '到職日'},
                    {'name': 'resign_date', 'verbose_name': '離職日'},
                    {'name': 'rank', 'verbose_name': '職等'},
                    {'name': 'bonus_factor', 'verbose_name': '點數'},
                    {'name': 'eval_class', 'verbose_name': 'BSC/KPI'},
                    {'name': 'nat', 'verbose_name': '國籍'},
                ],
                "model": None,
                # "source_url": reverse_lazy('get_metrics_setup_data'),        # 使用自己定義的Grid
                "source_url": reverse_lazy('get_metrics_setup_subs_data'),     # 使用自己定義的Grid
            }
        })

        # east side's grid(js 要記得定義metrics_setupDate_dg, 不然資料跑不出來)
        context.update({
            "metrics_setupDate_dg_config":{
                "display_fields": [
                    {'name': 'work_code', 'verbose_name': '工號',},
                    {'name': 'date_yyyy', 'verbose_name': '年份',},
                    {'name': 'date_mm', 'verbose_name': '月份',},
                ],
                "model": None,
                "source_url":reverse_lazy('get_metrics_setupDate_data',),
            }
        })
        return context


class PM210(SingleView):
    main_model = MetricsCalc
    form_param = {}
    form_class = MetricsCalcForm  # main_form(center)
    main_sort = 'metrics_id'
    template_name = 'kpi/pm210.html'
    title = '衡量指標計算方式'

    """ 下面GRID 資料 """
    main_fields = [
        'order_number',
        'calc_content',
        'lower_limit',
        'upper_limit',
        'score',
    ]


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # north side's grid
        context.update({
            "employee_info_easy_dg_config": {
                "display_fields": [
                    {'name': 'work_code', 'verbose_name': '工號'},
                    {'name': 'chi_name', 'verbose_name': '姓名'},
                    {'name': 'dept_name', 'verbose_name': '部門'},
                    {'name': 'pos_name', 'verbose_name': '職位'},
                    {'name': 'director_id', 'verbose_name': '主管工號'},
                    {'name': 'director_name', 'verbose_name': '主管名稱'},
                    {'name': 'arrival_date', 'verbose_name': '到職日'},
                    {'name': 'resign_date', 'verbose_name': '離職日'},
                    {'name': 'rank', 'verbose_name': '職等'},
                    {'name': 'bonus_factor', 'verbose_name': '點數'},
                    {'name': 'eval_class', 'verbose_name': 'BSC/KPI'},
                    {'name': 'nat', 'verbose_name': '國籍'},
                ],
                "model": None,
                "source_url": reverse_lazy('get_metrics_setup_subs_data'),     # 使用自己定義的Grid
            }
        })

        # south side's grid(js 要記得定義, 不然資料跑不出來)
        context.update({
            "metrics_setup_dg_config": {
                "display_fields": [
                    {'name': 'order_number', 'verbose_name': '順序'},
                    {'name': 'metrics_content', 'verbose_name': '衡量指標*內容'},
                    {'name': 'allocation', 'verbose_name': '衡量指標*配分'},
                ],
                "model": None,
                "source_url": reverse_lazy(
                    'model_handler', kwargs={'model': 'metrics_setup'}),
            }
        })
        # east side's grid(js 要記得定義metrics_setupDate_dg, 不然資料跑不出來)
        context.update({
            "metrics_setupDate_dg_config":{
                "display_fields": [
                    {'name': 'work_code', 'verbose_name': '工號',},
                    {'name': 'date_yyyy', 'verbose_name': '年份',},
                    {'name': 'date_mm', 'verbose_name': '月份',},
                ],
                "model": None,
                "source_url":reverse_lazy('get_metrics_setupDate_data',),
            }
        })
        return context



class PM402(SingleView):
    main_model = MetricsSetup
    main_sort = 'work_code'
    form_param = {}
    form_class = MetricsSetupEasyForm   #main_form(center)
    template_name = 'kpi/pm402.html'
    title = 'KPI評核'

    """ 下面GRID config-->display_fields """
    main_fields = [
        'order_number',
        'order_item',
        'metrics_content',
        'unit_Mcalc',
        'allocation',
    ]


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["main_dg_config"]["source_url"] = '/api/metrics_setup_score_sheet_pm402'

        # 取得上一狀態/下一狀態---------------------------------------------------------------------------begin
        # po_code : 在『自評/審核/列印/人資審核』存檔時,請以此值存入(任何有狀態流程的 "存檔/確認 "時,都以此值存入)
        poCode01 = ProcessOptionsTxtDef.objects.get\
            (app_model='KPI', view_code='PM402', model_class='RegActRules', topic_code='order_type', action='blank').po_code
        poCode02 = ProcessOptionsTxtDef.objects.get\
            (app_model='KPI', view_code='PM402', model_class='RegActRules', topic_code='last_status', action='new').po_code
        results = RegActRules.objects.filter(order_type=poCode01, last_status=poCode02).values_list('last_status',
                                                                                                    'next_status')
        poCode03 = ProcessOptionsTxtDef.objects.get\
            (app_model='KPI', view_code='PM402', model_class='RegActRules', topic_code='last_status', action='submit').po_code

        poCode04 = ProcessOptionsTxtDef.objects.get\
            (app_model='KPI', view_code='PM402', model_class='RegActRules', topic_code='last_status', action='recall').po_code

        for dataTuple in results:
            # last_status=dataTuple[0]
            context["last_status"]=dataTuple[0]
            # next_status=dataTuple[1]
            context["next_status"]=dataTuple[1]
        context["status_new"] = poCode02  # 初評已送出
        context["status_submit"] = poCode03      #初評已送出
        context["status_recall"] = poCode04      #初評已收回
        # 取得上一狀態/下一狀態---------------------------------------------------------------------------ending

        # east side's grid(js 要記得定義metrics_setupDate_dg, 不然資料跑不出來)
        context.update({
            "metrics_setupDate_dg_config":{
                "display_fields": [
                    {'name': 'work_code', 'verbose_name': '工號',},
                    {'name': 'date_yyyy', 'verbose_name': '年份',},
                    {'name': 'date_mm', 'verbose_name': '月份',},
                ],
                "model": None,
                "source_url":reverse_lazy('get_metrics_setupDate_data',),
            }
        })
        # SubGrid ,( js 要記得定義score_sheet_input_dg, 不然資料跑不出來 )
        context.update({
            "get_metrics_calc_dg_config": {
                "display_fields": [
                    {'name': 'order_number', 'verbose_name': '計算順序', },
                    {'name': 'calc_content', 'verbose_name': '計算方式', },
                    {'name': 'lower_limit', 'verbose_name': '下限', },
                    {'name': 'upper_limit', 'verbose_name': '上限', },
                    {'name': 'score', 'verbose_name': '得分', },
                ],
                "model": None,
                "source_url": reverse_lazy('get_metrics_calc', ),
            }
        })
        return context



class PM406(SingleView):
    main_model = MetricsSetup
    main_sort = 'work_code'
    custom_model = EmployeeInfoEasy
    custom_sort = 'work_code'
    form_param = {}
    form_class = MetricsSetupEasyForm   #main_form(center)
    template_name = 'kpi/pm406.html'
    title = 'KPI審核'

    """ 下面GRID config-->display_fields """
    main_fields = [
        'order_number',
        'order_item',
        'metrics_content',
        'unit_Mcalc',
        'allocation',
    ]

    custom_fields = [
        'work_code',
        'chi_name',
        'director_id',
    ]


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["main_dg_config"]["source_url"] = '/api/metrics_setup_score_sheet_pm406'

        # 取得上一狀態/下一狀態---------------------------------------------------------------------------begin
        # po_code : 在『自評/審核/列印/人資審核』存檔時,請以此值存入(任何有狀態流程的 "存檔/確認 "時,都以此值存入)
        poCode01 = ProcessOptionsTxtDef.objects.get\
            (app_model='KPI', view_code='PM406', model_class='RegActRules', topic_code='order_type', action='blank').po_code

        poCode02 = ProcessOptionsTxtDef.objects.get\
            (app_model='KPI', view_code='PM402', model_class='RegActRules', topic_code='last_status', action='submit').po_code

        poCode02_new = ProcessOptionsTxtDef.objects.get \
            (app_model='KPI', view_code='PM406', model_class='RegActRules', topic_code='last_status',
             action='new').po_code

        poCode03 = ProcessOptionsTxtDef.objects.get\
            (app_model='KPI', view_code='PM406', model_class='RegActRules', topic_code='last_status', action='submit').po_code

        results = RegActRules.objects.filter(order_type=poCode01, last_status=poCode03).values_list('next_status',
                                                                                                    flat=True)
        poCode04 = ProcessOptionsTxtDef.objects.get\
            (app_model='KPI', view_code='PM406', model_class='RegActRules', topic_code='last_status', action='return').po_code

        context["last_status"] = poCode02         # 上一流程送出的狀態
        context["next_status"] = results[0]       # 本流程下一狀態
        context["status_new"] = poCode02_new      # 主管已審核
        context["status_submit"] = poCode03       # 本流程送出的狀態
        context["status_return"] = poCode04       # 上一流程送出的狀態
        # 取得上一狀態/下一狀態---------------------------------------------------------------------------ending

        # north side's grid
        context.update({
            "employee_info_easy_dg_config": {
                "display_fields": [
                    {'name': 'work_code', 'verbose_name': '工號'},
                    {'name': 'chi_name', 'verbose_name': '姓名'},
                    {'name': 'dept_name', 'verbose_name': '部門'},
                    {'name': 'pos_name', 'verbose_name': '職位'},
                    {'name': 'director_id', 'verbose_name': '主管工號'},
                    {'name': 'director_name', 'verbose_name': '主管名稱'},
                    {'name': 'arrival_date', 'verbose_name': '到職日'},
                    {'name': 'resign_date', 'verbose_name': '離職日'},
                    {'name': 'rank', 'verbose_name': '職等'},
                    {'name': 'bonus_factor', 'verbose_name': '點數'},
                    {'name': 'eval_class', 'verbose_name': 'BSC/KPI'},
                    {'name': 'nat', 'verbose_name': '國籍'},
                ],
                "model": None,
                "source_url": reverse_lazy('get_metrics_setup_subs_data'),     # 使用自己定義的Grid,取得下屬的metrics_setup
            }
        })

        # east side's grid(js 要記得定義metrics_setupDate_dg, 不然資料跑不出來)
        context.update({
            "metrics_setupDate_dg_config":{
                "display_fields": [
                    {'name': 'work_code', 'verbose_name': '工號',},
                    {'name': 'date_yyyy', 'verbose_name': '年份',},
                    {'name': 'date_mm', 'verbose_name': '月份',},
                ],
                "model": None,
                "source_url":reverse_lazy('get_metrics_setupDate_data',),
            }
        })

        # SubGrid ,( js 要記得定義score_sheet_input_dg, 不然資料跑不出來 )
        context.update({
            "get_metrics_calc_dg_config": {
                "display_fields": [
                    {'name': 'order_number', 'verbose_name': '計算順序', },
                    {'name': 'calc_content', 'verbose_name': '計算方式', },
                    {'name': 'lower_limit', 'verbose_name': '下限', },
                    {'name': 'upper_limit', 'verbose_name': '上限', },
                    {'name': 'score', 'verbose_name': '得分', },
                ],
                "model": None,
                "source_url": reverse_lazy('get_metrics_calc', ),
            }
        })
        return context



class PM408(SingleView):
    main_model = ScoreStatus
    form_param = {}
    form_class = ScoreStatusForm                  #main_form(center)
    template_name = 'kpi/pm408.html'
    title = 'PM408 KPI員工簽名確認'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["main_dg_config"]["source_url"] = '/api/data/score_status'

        return context


class PM411(SingleView):
    main_model = SignatureModel
    form_param = {}
    form_class = SignatureForm                  #main_form(center)
    template_name = 'kpi/pm411.html'
    title = 'PM411 PDF簽名測試1'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        return context


class PM412(SingleView):
    main_model = ScoreStatus
    form_param = {}
    form_class = ScoreStatusForm                  #main_form(center)
    template_name = 'kpi/pm412.html'
    title = 'PM412 PDF簽名測試2'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["main_dg_config"]["source_url"] = '/api/data/score_status'

        return context


'''
class PM602(BaseLayoutView):
    template_name = 'kpi/pm602.html'
    title = '績效列印_KPI年度目標'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class PM604(BaseLayoutView):
    template_name = 'kpi/pm604.html'
    title = '績效列印_KPI季度報表'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class PM606(BaseLayoutView):
    template_name = 'kpi/pm606.html'
    title = '績效列印_KPI年度報表'
'''


class PM610(BaseLayoutView):
    template_name = 'kpi/pm610.html'
    title = '績效列印_KPI季度報表'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context



class PM620(SingleView):
    template_name = 'kpi/pm620.html'
    title = '績效列印_KPI季度報表'
    main_model = ScoreStatus
    form_param = {}
    form_class = ScoreStatusForm

    """ GRID 資料 """
    main_fields = [
            'work_code',
            'director',
            'date_yyyy',
            'quarter',
            'report_url',
            'bpm_number',
            'bpm_status',
        ]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["main_dg_config"]["source_url"] = '/api/data/score_status'
        return context



class PM802(SingleView):
    main_model = MetricsCalc
    form_param = {}
    form_class = MetricsCalcForm  # main_form(center)
    main_sort = 'metrics_id'
    template_name = 'kpi/pm802.html'
    title = '指標計算方式'

    """ 下面GRID 資料 """
    main_fields = [
        'order_number',
        'calc_content',
        'lower_limit',
        'upper_limit',
        'score',
    ]


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # north side's grid
        context.update({
            "employee_info_easy_dg_config": {
                "display_fields": [
                    {'name': 'work_code', 'verbose_name': '工號'},
                    {'name': 'chi_name', 'verbose_name': '姓名'},
                    {'name': 'dept_name', 'verbose_name': '部門'},
                    {'name': 'pos_name', 'verbose_name': '職位'},
                    {'name': 'director_id', 'verbose_name': '主管工號'},
                    {'name': 'director_name', 'verbose_name': '主管名稱'},
                    {'name': 'arrival_date', 'verbose_name': '到職日'},
                    {'name': 'resign_date', 'verbose_name': '離職日'},
                    {'name': 'rank', 'verbose_name': '職等'},
                    {'name': 'bonus_factor', 'verbose_name': '點數'},
                    {'name': 'eval_class', 'verbose_name': 'BSC/KPI'},
                    {'name': 'nat', 'verbose_name': '國籍'},
                ],
                "model": None,
                "source_url": reverse_lazy('get_metrics_setup_subs_data'),     # 使用自己定義的Grid
            }
        })

        # south side's grid(js 要記得定義, 不然資料跑不出來)
        context.update({
            "metrics_setup_dg_config": {
                "display_fields": [
                    {'name': 'order_number', 'verbose_name': '順序'},
                    {'name': 'metrics_content', 'verbose_name': '衡量指標*內容'},
                    {'name': 'allocation', 'verbose_name': '衡量指標*配分'},
                ],
                "model": None,
                "source_url": reverse_lazy(
                    'model_handler', kwargs={'model': 'metrics_setup'}),
            }
        })
        # east side's grid(js 要記得定義metrics_setupDate_dg, 不然資料跑不出來)
        context.update({
            "metrics_setupDate_dg_config":{
                "display_fields": [
                    {'name': 'work_code', 'verbose_name': '工號',},
                    {'name': 'date_yyyy', 'verbose_name': '年份',},
                    {'name': 'date_mm', 'verbose_name': '月份',},
                ],
                "model": None,
                "source_url":reverse_lazy('get_metrics_setupDate_data_search',),
            }
        })
        return context


class PM804(SingleView):
    main_model = MetricsSetup
    main_sort = 'work_code'
    custom_model = EmployeeInfoEasy
    custom_sort = 'work_code'
    form_param = {}
    form_class = MetricsSetupEasyForm  # main_form(center)
    template_name = 'kpi/pm804.html'
    title = 'KPI審核'

    """ 下面GRID config-->display_fields """
    main_fields = [
        'order_number',
        'order_item',
        'metrics_content',
        'unit_Mcalc',
        'allocation',
    ]

    custom_fields = [
        'work_code',
        'chi_name',
        'director_id',
    ]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["main_dg_config"]["source_url"] = '/api/metrics_setup_score_sheet_pm406'

        # 取得上一狀態/下一狀態---------------------------------------------------------------------------begin
        # po_code : 在『自評/審核/列印/人資審核』存檔時,請以此值存入(任何有狀態流程的 "存檔/確認 "時,都以此值存入)
        poCode01 = ProcessOptionsTxtDef.objects.get \
            (app_model='KPI', view_code='PM406', model_class='RegActRules', topic_code='order_type',
             action='blank').po_code

        poCode02 = ProcessOptionsTxtDef.objects.get \
            (app_model='KPI', view_code='PM402', model_class='RegActRules', topic_code='last_status',
             action='submit').po_code

        poCode02_new = ProcessOptionsTxtDef.objects.get \
            (app_model='KPI', view_code='PM406', model_class='RegActRules', topic_code='last_status',
             action='new').po_code

        poCode03 = ProcessOptionsTxtDef.objects.get \
            (app_model='KPI', view_code='PM406', model_class='RegActRules', topic_code='last_status',
             action='submit').po_code

        results = RegActRules.objects.filter(order_type=poCode01, last_status=poCode03).values_list('next_status',
                                                                                                    flat=True)
        poCode04 = ProcessOptionsTxtDef.objects.get \
            (app_model='KPI', view_code='PM406', model_class='RegActRules', topic_code='last_status',
             action='return').po_code

        context["last_status"] = poCode02  # 上一流程送出的狀態
        context["next_status"] = results[0]  # 本流程下一狀態
        context["status_new"] = poCode02_new  # 主管已審核
        context["status_submit"] = poCode03  # 本流程送出的狀態
        context["status_return"] = poCode04  # 上一流程送出的狀態
        # 取得上一狀態/下一狀態---------------------------------------------------------------------------ending

        # north side's grid
        context.update({
            "employee_info_easy_dg_config": {
                "display_fields": [
                    {'name': 'work_code', 'verbose_name': '工號'},
                    {'name': 'chi_name', 'verbose_name': '姓名'},
                    {'name': 'dept_name', 'verbose_name': '部門'},
                    {'name': 'pos_name', 'verbose_name': '職位'},
                    {'name': 'director_id', 'verbose_name': '主管工號'},
                    {'name': 'director_name', 'verbose_name': '主管名稱'},
                    {'name': 'arrival_date', 'verbose_name': '到職日'},
                    {'name': 'resign_date', 'verbose_name': '離職日'},
                    {'name': 'rank', 'verbose_name': '職等'},
                    {'name': 'bonus_factor', 'verbose_name': '點數'},
                    {'name': 'eval_class', 'verbose_name': 'BSC/KPI'},
                    {'name': 'nat', 'verbose_name': '國籍'},
                ],
                "model": None,
                "source_url": reverse_lazy('get_metrics_setup_subs_data'),  # 使用自己定義的Grid,取得下屬的metrics_setup
            }
        })

        # east side's grid(js 要記得定義metrics_setupDate_dg, 不然資料跑不出來)
        context.update({
            "metrics_setupDate_dg_config": {
                "display_fields": [
                    {'name': 'work_code', 'verbose_name': '工號', },
                    {'name': 'date_yyyy', 'verbose_name': '年份', },
                    {'name': 'date_mm', 'verbose_name': '月份', },
                ],
                "model": None,
                "source_url": reverse_lazy('get_metrics_setupDate_data', ),
            }
        })

        # SubGrid ,( js 要記得定義score_sheet_input_dg, 不然資料跑不出來 )
        context.update({
            "get_metrics_calc_dg_config": {
                "display_fields": [
                    {'name': 'order_number', 'verbose_name': '計算順序', },
                    {'name': 'calc_content', 'verbose_name': '計算方式', },
                    {'name': 'lower_limit', 'verbose_name': '下限', },
                    {'name': 'upper_limit', 'verbose_name': '上限', },
                    {'name': 'score', 'verbose_name': '得分', },
                ],
                "model": None,
                "source_url": reverse_lazy('get_metrics_calc', ),
            }
        })
        return context


class PM806(SingleView):
    main_model = ScoreStatus
    form_param = {}
    form_class = ScoreStatusForm                  #main_form(center)
    template_name = 'kpi/pm806.html'
    title = 'PM806 季報表送簽狀況查詢(人資)'

    ''' GRID 資料, 不設定, 就是全部
    main_fields = [
        'date_yyyy',
        'quarter',
        'work_code',
    ]
    '''

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["main_dg_config"]["source_url"] = '/api/data/score_status'

        return context


class PM808(SingleView):
    pass


