import os
from django.conf import settings
from django.http import HttpResponse,HttpResponseRedirect,response,request
from django.shortcuts import render,redirect

from django.db.models import Q, F
from django.forms.models import model_to_dict
from django.urls import reverse_lazy
from django.utils import timezone
from django.utils.translation import gettext_lazy as _


import io,os
import pathlib
from pathlib import Path
from django.http import  FileResponse

#html 2 pdf 相關
from django.views.generic import TemplateView
from wkhtmltopdf.views import PDFTemplateView,PDFTemplateResponse
from django_pdfkit import PDFView
import pdfkit
from django.utils.encoding import escape_uri_path


from common.models import UserDefCode
from common.context_processors import set_language_code


from apps.kpi.models import (EmployeeInfoEasy,
                             WorkcodeMapping,
                             DeptSupervisor
                             )
from .models import (
                     JobTitle,
                     JobTitleForeign,
                     JobSkill,
                     JobTitleSkill,
                     EmployeeTitle,
                     StudyPlan,
                     MatrixMaster,
                     MatrixStatus,
                     # MatrixDetail,
                     PdcaMaster,
                     PdcaDetail,
                     PdcaDefinition,
                     PdcaDefinitionForeign,
                     FlowDefinition,
                     FlowDefinitionForeign,
                     CycleDefinition,
                     CycleDefinitionForeign,
                    )

from .forms import (
                    EmployeeInfoEasyForm,
                    EmployeeMatrixForm,
                    JobTitleForm,
                    JobSkillForm,
                    JobTitleSkillForm,
                    EmployeeTitleForm,
                    StudyPlanForm,
                    MatrixMasterForm,
                    # MatrixDetailForm,
                    EmployeeSearchForm1,
                    EmployeeSearchForm2,
                    EmployeeSearchForm3,
                    DepartmentChoiceForm,
                    EmployeePdcaForm_X,
                    EmployeePdcaForm,
                    WorkcodeMappingForm,
                    DeptSupervisorForm,
                    ChoiceLanguage
                   )

from common.views import ManipulateBaseView, DoubleView, SingleView, BaseLayoutView
from apps.api_skill import matrix_score,pdca_detail


current_tz = timezone.get_current_timezone()
now = timezone.now().astimezone(current_tz).strftime('%Y-%m-%d %H:%M:%S')


class TT002(SingleView):
    main_model = EmployeeInfoEasy
    form_param = {}
    form_class = EmployeeInfoEasyForm
    template_name = 'skill_pdca/tt002.html'
    title = 'TT002 人事基本資料'

    """ GRID 資料 """
    main_fields =  [
        'work_code',
        'chi_name',
        'direct_supv',
        'director',
        'factory',
        'dept_flevel',
        'dept',
        'pos',
        'nat',
        'rank',
        'eval_class',
        'kpi_diy',
        'pdca_agent',
        'bonus_type',   #
        'bonus_factor', #
        'factory_area',
        'email',
        'arrival_date',
        'resign_date',
        'trans_date',
        'trans_type',
        'labor_type',   #
        'service_status'   #
        # 'dept_desc',
    ]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["main_dg_config"]["source_url"] = '/sk_api/data/employee_info_easy'   #<--/api/ or /sk_api/ 僅記, 在hrs/urls定義的....別再犯傻了
        context["import_url"] = '/api/employee_import_update/'                    #由 excel 匯入的處理網址
        context["copy_url"] = '/api/employee_copy/'                        #複製的處理網址
        context["ee_search_form1"] = EmployeeSearchForm1
        context["ee_search_form2"] = EmployeeSearchForm2
        context["ee_search_form3"] = EmployeeSearchForm3
        return context


class TT004(SingleView):
    main_model = WorkcodeMapping
    form_param = {}
    form_class = WorkcodeMappingForm
    template_name = 'skill_pdca/tt004.html'
    title = 'TT002 HR海外工號對照表'

    """ GRID 資料 """
    main_fields =  [
        'factory',
        'work_code',
        'work_code_x',
        'chi_name',
        'alias_name',
        'factory_area',
    ]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["main_dg_config"]["source_url"] = '/sk_api/data/workcode_mapping'   #<--/api/ or /sk_api/ 僅記, 在hrs/urls定義的....別再犯傻了
        return context

class TT006(SingleView):
    main_model = DeptSupervisor
    form_param = {}
    form_class = DeptSupervisorForm
    template_name = 'skill_pdca/tt006.html'
    title = 'TT006 HR部門主管對照表'

    """ GRID 資料 """
    main_fields =  [
        'factory',
        'dept',
        'dept_upper',
        'dept_flevel',
        'dept_supervisor',
        'dept_description',
    ]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["main_dg_config"]["source_url"] = '/sk_api/data/dept_supervisor'   #<--/api/ or /sk_api/ 僅記, 在hrs/urls定義的....別再犯傻了
        return context


class TT202(SingleView):
    main_model = JobTitle
    main_sort = 'job_code'
    form_param = {}
    form_class = JobTitleForm  #main_form(center)
    template_name = 'skill_pdca/tt202.html'
    title = 'TT202 職務名稱維護'

    """ 下面GRID config-->display_fields """
    main_fields = [
        'job_parent',
        'job_code',
        'job_name',
        # 'job_desc',
        'level_number'
    ]

    def level_job(self,level_number):
        results = JobTitle.objects.filter(level_number=level_number).values('level_number','job_code', 'job_name')
        dataList = []
        for dt in results:
            dataList.append({
                'level': dt.get("level_number"),
                'value': dt.get("job_code"),
                'text': dt.get("job_code") +" "+ dt.get("job_name"),
            })
        return dataList


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["main_dg_config"]["source_url"] = '/sk_api/data/job_title'
        context['l1_jobtitles'] = self.level_job(1)
        context['l2_jobtitles'] = self.level_job(2)
        return context



class TT204(SingleView):
    main_model = JobSkill
    main_sort = 'skill_code'
    form_param = {}
    form_class = JobSkillForm  #main_form(center)
    template_name = 'skill_pdca/tt204.html'
    title = 'TT204 職能名稱維護'

    """ 下面GRID config-->display_fields """
    main_fields = [
        'skill_class',
        # 'job_level',
        'skill_code',
        'skill_name',
        # 'skill_desc',
    ]


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["main_dg_config"]["source_url"] = '/sk_api/data/job_skill'
        return context



class TT206(SingleView):
    main_model = JobTitleSkill
    main_sort = ['job_code']
    form_param = {}
    form_class = JobTitleSkillForm  #main_form(center)
    template_name = 'skill_pdca/tt206.html'
    title = 'TT206 職務綁定職能維護'

    """ 下面GRID config-->display_fields """
    main_fields = [
        'order_number',
        'job_skill',
        # 'enable',
        # 'disable_date',
        # 'enable_date',
    ]


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["main_dg_config"]["source_url"] = '/sk_api/data/job_title_skill'
        context.update({
            "job_title_dg_config": {
                "display_fields": [
                    {'name': 'job_code', 'verbose_name':'職務代號'},
                    {'name': 'job_name', 'verbose_name':'職務名稱'},
                ],
                "model": None,
                # "source_url": reverse_lazy('model_handler', kwargs={'model': 'job_title'}),
                "source_url": reverse_lazy('get_job_title_l3'),
            }
        })
        return context


class TT208(SingleView):
    main_model = EmployeeTitle
    main_sort = [
        'work_code',
        'job_title',
        ]

    form_param = {}
    form_class = EmployeeTitleForm  #main_form(center)
    template_name = 'skill_pdca/tt208.html'
    title = 'TT208 人員職務名稱維護'

    """ 下面GRID config-->display_fields """
    main_fields = [
        # 'work_code',
        'job_title',
        # 'enable',
        # 'disable_date',
        # 'enable_date',
    ]


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["main_dg_config"]["source_url"] = '/sk_api/data/employee_title'
        context.update({
            "employee_title_dg_config": {
                "display_fields": [
                    {'name': 'work_code', 'verbose_name': '工號'},
                    {'name': 'chi_name', 'verbose_name': '姓名'},
                    {'name': 'job_code', 'verbose_name': '職務代號'},
                    {'name': 'job_name', 'verbose_name': '職務名稱'},
                    {'name': 'id', 'verbose_name': 'id'},
                ],
                "model": None,
                # "source_url": reverse_lazy('model_handler', kwargs={'model': 'employee_title'}),
                "source_url": reverse_lazy('employee_title'),
            }
        })
        return context




######技能盤點表----------------------------------------------------------------------------------------------------------------------BEGIN

class TT402(SingleView):
    main_model = StudyPlan
    main_sort = 'study_code'
    form_param = {}
    form_class = StudyPlanForm  #main_form(center)
    template_name = 'skill_pdca/tt402.html'
    title = 'TT402 教育訓練方式維護'

    """ 下面GRID config-->display_fields """
    main_fields = [
        'study_code',
        'study_name',
        'study_course',
    ]


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["main_dg_config"]["source_url"] = '/sk_api/data/study_plan'
        return context


class TT404(BaseLayoutView):
    template_name = 'skill_pdca/tt404.html'
    title = 'TT404 技能盤點底稿產生'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class TT406(BaseLayoutView):
    # form_param = {}
    # form_class = EmployeeMatrixForm
    template_name = 'skill_pdca/tt406.html'
    title = 'TT406 技能盤點作業'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["all_dept_form"] = DepartmentChoiceForm(self.request.user.username,self.request.user)
        return context


class TT407(SingleView):
    form_param = {}
    form_class = EmployeeMatrixForm                 #main_form(center)
    template_name = 'skill_pdca/tt407.html'
    # title = 'TT407 技能盤點作業(tt406連結)'
    title = 'TT406 技能盤點作業'

    main_model = MatrixMaster
    main_sort = [
        'work_code_title',
        'year',
        'month',
        # 'bpm_status',
        ]


    """ 下面GRID config-->display_fields """
    main_fields = [
        'work_code',
        'chi_name',
        'year',
        'month',
        # 'bpm_status',
    ]

    # def get(self, request, *args, **kwargs):
    #     get_param = request.GET.dict()
    #     select_dept = get_param.get('select_dept',None)
    #     return super().get(self,request, *args, **kwargs)

    def get_skills(self,job_title):
        dataList = []
        cr = JobSkill.objects.values_list('skill_name', flat=True).filter(
            skill_class=UserDefCode.objects.get(udc='S001'))  # 核心職能
        for idx, itm in enumerate(cr):
            # field_name = 'cr' + ('00' if idx < 9 else '0' if idx>9 and idx < 99 else '') + str(idx + 1)
            field_name = 'cr' + ('00' if idx < 9 else '0' if idx>8 and idx < 99 else '') + str(idx + 1)
            dataList.append({
                'name': field_name,
                'verbose_name': itm,
            })

        # ma = JobSkill.objects.values_list('skill_name',flat=True).filter(
        ma = JobSkill.objects.values_list('skill_name','chk_yn').filter(
            skill_class=UserDefCode.objects.get(udc='S002'))  # 管理職能
        for idx,itm in enumerate(ma):
            # field_name = 'ma' + ('00' if idx < 9 else '0' if idx>9 and idx < 99 else '') + str(idx + 1)
            field_name = 'ma' + ('00' if idx < 9 else '0' if idx>8 and idx < 99 else '') + str(idx + 1)
            dataList.append({
                'name': field_name,
                'verbose_name': itm[0],
                'chk_yn': itm[1],
            })


        ge = JobSkill.objects.values_list('skill_name', flat=True).filter(
            skill_class=UserDefCode.objects.get(udc='S003'))  # 一般職能
        for idx, itm in enumerate(ge):
            # field_name = 'ge' + ('00' if idx < 9 else '0' if idx>9 and idx < 99 else '') + str(idx + 1)
            field_name = 'ge' + ('00' if idx < 9 else '0' if idx>8 and idx < 99 else '') + str(idx + 1)
            dataList.append({
                'name': field_name,
                'verbose_name': itm,
            })

        ot = JobSkill.objects.values_list('skill_name', flat=True).filter(
            skill_class=UserDefCode.objects.get(udc='S005'))  # 其他職能
        for idx, itm in enumerate(ot):
            # field_name = 'ot' + ('00' if idx < 9 else '0' if idx>9 and idx < 99 else '') + str(idx + 1)
            field_name = 'ot' + ('00' if idx < 9 else '0' if idx>8 and idx < 99 else '') + str(idx + 1)
            dataList.append({
                'name': field_name,
                'verbose_name': itm,
            })


        pr = JobSkill.objects.values_list('skill_name', flat=True).filter(
            skill_code__in=JobTitleSkill.objects.values_list('job_skill').filter(job_title=job_title))  #專業職能，只有專業職能，會依不同職務而不同
        for idx, itm in enumerate(pr):  # 結果:[{}]<---List's element have namy dict-->to js-->Array have many element
            # field_name = 'pr' + ('00' if idx < 9 else '0' if idx>9 and idx < 99 else '') + str(idx + 1)
            field_name = 'pr' + ('00' if idx < 9 else '0' if idx>8 and idx < 99 else '') + str(idx + 1)
            dataList.append({
                'name': field_name,
                'verbose_name': itm,
            })

        dataList.append({
            'name': 'xa001',
            'verbose_name': '佔總分的比率<br> ％',
        })

        dataList.append({
            'name': 'xa002',
            'verbose_name': '生手級/新手級/半熟手級/熟手級/高手級',
        })

        dataList.append({
            'name': 'xb001',
            'verbose_name': '教育訓練<br>(可複選)',
        })

        dataList.append({
            'name': 'xb002',
            'verbose_name': '(承左.教育訓練)<br>課程名稱',
        })

        dataList.append({
            'name': 'xb003',
            'verbose_name': '預定輪調的職務<br>(可複選)',
        })
        return dataList

    def get_job_title_to_tabs(self):
        select_dept = self.request.session.get('select_dept', None)
        fields = ['work_code_title__work_code',
                  'work_code_title__job_title',
                  'work_code_title__enable',
                  'year',
                  'month',
                  'bpm',
                  # 'bpm__bpm_status',
                  'bpm__bpm_status_desc1',
                  # 'bpm__bpm_status_desc2',
                  ]
        qr0 = Q(bpm__isnull=True)
        qr1 = Q(bpm__bpm_status_desc1__exact='')   #未送BPM   留待js控制按鈕
        qr2 = Q(bpm__bpm_status_desc1='reject')    #BPM退回   留待js控制按鈕
        userID = self.request.user.username
        # x_work_code = EmployeeInfoEasy.objects.filter(direct_supv=userID)
        # qr3 = Q(work_code_title__work_code__in=EmployeeInfoEasy.objects.filter(direct_supv=userID))     # 找到『直接主管』是userID的工號
        qr3 = Q(work_code_title__work_code__in=EmployeeInfoEasy.objects.filter(direct_supv=userID,dept_flevel_id=select_dept))     # 找到『直接主管』是userID的工號,找到"一級部門"
        results = MatrixMaster.objects.filter( (qr0 | qr1 | qr2), qr3 ).values(*fields)                       # 要搭app  class matrix_score
        # results = MatrixMaster.objects.filter( qr3 ).values(*fields)                                  # 要搭app  class matrix_score(這裏是編輯/未送BPM才顯示)
        dataList = []
        if results:
            # for dataTuple in results:
            for dt in results:
                fieldsList = ['chi_name', 'dept', ]

                ee = model_to_dict(EmployeeInfoEasy.objects.get(work_code=dt['work_code_title__work_code']), fields=fieldsList)
                dataList.append({
                    'job_title': dt['work_code_title__job_title'],
                    'job_title_desc': JobTitle.objects.get(job_code=dt['work_code_title__job_title']).job_name,
                })
        single_dataList = [dict(t) for t in {tuple(d.items()) for d in dataList}]  # 去除list 裏重覆的dict
        cleanedList = sorted(single_dataList, key=lambda i: i['job_title'])    #字典排序
        return cleanedList

    def get_skill_score(self):
        results = UserDefCode.objects.filter(topic_code_id='skill_matrix_id').values_list('shc1','desc2','desc1')
        dataList = []
        for dataTuple in results:
            dataList.append({
                # 'value': dataTuple[0],
                'value':  dataTuple[1],
                'text': dataTuple[1]+" "+dataTuple[2],
            })
        return  dataList



    def get_skill_score(self):
        results = UserDefCode.objects.filter(topic_code_id='skill_matrix_id').values_list('shc1','desc2','desc1','description','shc1_desc')
        dataList = []
        for dataTuple in results:
            dataList.append({
                # 'value': dataTuple[0],
                'value':  dataTuple[1],
                'text': dataTuple[1]+" "+dataTuple[2],
                'desc1': dataTuple[2],
                'desc2': dataTuple[1],
                'description': dataTuple[3],
                'image':dataTuple[4]
            })
        return  dataList



    def get_skill_score_x(self):
        results = UserDefCode.objects.filter(topic_code_id='skill_matrix_id').values_list('shc1','desc2','desc1','description','shc1_desc')
        dataList = []
        for dataTuple in results:
            if (dataTuple[1]!='X'):
                dataList.append({
                    # 'value': dataTuple[0],
                    'value':  dataTuple[1],
                    'text': dataTuple[1]+" "+dataTuple[2],
                    'desc1': dataTuple[2],
                    'desc2': dataTuple[1],
                    'description': dataTuple[3],
                    'image':dataTuple[4]
                })
        return  dataList



    def get_skill_study(self):
        results = StudyPlan.objects.all().values_list('study_code','study_name','study_course')
        dataList = [{
            'value': '無須教育訓練',
            'text': '無須教育訓練',
            'course': '',
        }]
        for dataTuple in results:
            dataList.append({
                # 'value': dataTuple[0],
                'value':  dataTuple[1],
                'text': dataTuple[1],
                'course': dataTuple[2],
            })
        return dataList

    def get_rotation_job(self):
        results = JobTitle.objects.filter(level_number=3).values_list('job_code','job_name')
        dataList =[{
            'value': '無',
            'text': '無',
        }]
        for dataTuple in results:
            dataList.append({
                'value':  dataTuple[1],
                'text': dataTuple[1],
            })
        return dataList

    def get_employee_title(self,userId):
        ee = EmployeeInfoEasy.objects.filter(direct_supv = userId).values_list('work_code',flat=True)
        dataList = []
        for itm in ee:
            job_name = [ code for code in EmployeeTitle.objects.filter(work_code=itm).values_list('job_title__job_name',flat=True) ]
            dataList.append({
                'work_code':itm,
                'job_name':job_name
            })
        return dataList


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        tabs = self.get_job_title_to_tabs()    #清理過後的職務資料( distinct+sort )
        tab_context_list = []
        tab_fields = []

        for tab in tabs:
            job_title = tab.get('job_title')
            display_fields = []
            this_node_id = 'tab'+job_title+'_dg'
            display_fields.extend(self.get_skills(job_title))
            tab_context_list.append({
                'job_title': job_title,
                'job_title_desc': tab.get('job_title_desc'),
                'node_id' : this_node_id,
                "main_dg_config": {
                    "display_fields": display_fields,
                    "model": None,
                    "source_url": reverse_lazy('matrix_score'),  # 使用自己定義的Grid,取得下屬的metrics_setup
                },
            })
            tab_fields.append(display_fields),
        context.update({
            'tabs':tabs,
            'tab_context_list':tab_context_list,
            'tab_fields':tab_fields,
            'score_choices_x':self.get_skill_score_x(),
            'score_choices':self.get_skill_score(),
            'study_choices':self.get_skill_study(),        #教育訓練
            'rotation_jobs':self.get_rotation_job(),       #輪調職務
            'ee_jobs':self.get_employee_title(self.request.user.username),
        })
        return context



class TT407_2PDF(PDFTemplateView):

    def get(self, request, *args, **kwargs):
        todayStr = timezone.now().astimezone(current_tz).strftime('%Y%m%d%H%M%S%f')
        get_param = request.GET.dict()
        filename = get_param.get('fileName', 'SKIL'+todayStr+".pdf")
        template_name = 'skill_pdca/tt407_2pdf.html'
        pdf_template = 'skill_pdca/tt407_2pdf_open.html'
        title = 'TT407_2pdf 技能盤點作業_2PDF(tt407連結)'


        # generate response

        response = PDFTemplateResponse(
            request=request,
            template=template_name,                     #input
            filename=filename,                          #output
            context=self.get_context_data(),            #input's source context
            cmd_options={                               #pdf's format
                'quiet': None,
                'enable-local-file-access': True,
                # 'encoding': 'utf8',
                'page-size': 'A3',
                'orientation': 'Landscape',
                'title': "matrix_skill 2022-03-18 Version 1.3",
                'footer-spacing': 5,              #Spacing between footer and content in mm
                'footer-line':True,
                'footer-center': 'page:' + '[page] / [toPage]',
                'footer-font-size':10,
                # 'footer-font-name':'標楷體',
                'footer-left': 'date:' + '[isodate]',
                'footer-right': 'time:' + '[time]',
            }
        )
        output_file = '%s/reports/pdf/%s' % (settings.MEDIA_ROOT, filename)     #Where be save?
        with open(output_file, "wb") as f:                                      #Actual practice save
            f.write(response.rendered_content)
        return render(request,pdf_template,{'filename':output_file.split("..")[1]})           #Open the distinct(pdf) file


    # 報表.表頭"核心職能/管理職能/一般職能/專業職能" colspan使用
    def get_skills_length(self, job_title):
        cr = JobSkill.objects.values_list('skill_name', flat=True).filter(
            skill_class=UserDefCode.objects.get(udc='S001')).count()  # 核心職能

        ma = JobSkill.objects.values_list('skill_name', flat=True).filter(
            skill_class=UserDefCode.objects.get(udc='S002')).count()  # 管理職能

        ge = JobSkill.objects.values_list('skill_name', flat=True).filter(
            skill_class=UserDefCode.objects.get(udc='S003')).count()  # 一般職能

        pr = JobSkill.objects.values_list('skill_name', flat=True).filter(
            skill_code__in=JobTitleSkill.objects.values_list('job_skill').filter(job_title=job_title)).count()  #專業職能，只有專業職能，會依不同職務而不同
        return {
            "cr_length" : cr,
            "ma_length" : ma,
            "ge_length" : ge,
            "pr_length" : pr,
        }


    def get_skills(self,job_title):
        dataList = []
        cr = JobSkill.objects.values_list('skill_name', flat=True).filter(
            skill_class=UserDefCode.objects.get(udc='S001'))  # 核心職能
        for idx, itm in enumerate(cr):
            # field_name = 'cr' + ('00' if idx < 9 else '0' if idx>9 and idx < 99 else '') + str(idx + 1)
            field_name = 'cr' + ('00' if idx < 9 else '0' if idx>8 and idx < 99 else '') + str(idx + 1)
            dataList.append({
                'name': field_name,
                'verbose_name': itm,
            })

        ma = JobSkill.objects.values_list('skill_name', flat=True).filter(
            skill_class=UserDefCode.objects.get(udc='S002'))  # 管理職能
        for idx, itm in enumerate(ma):
            # field_name = 'ma' + ('00' if idx < 9 else '0' if idx>9 and idx < 99 else '') + str(idx + 1)
            field_name = 'ma' + ('00' if idx < 9 else '0' if idx>8 and idx < 99 else '') + str(idx + 1)
            dataList.append({
                'name': field_name,
                'verbose_name': itm,
            })

        ge = JobSkill.objects.values_list('skill_name', flat=True).filter(
            skill_class=UserDefCode.objects.get(udc='S003'))  # 一般職能
        for idx, itm in enumerate(ge):
            # field_name = 'ge' + ('00' if idx < 9 else '0' if idx>9 and idx < 99 else '') + str(idx + 1)
            field_name = 'ge' + ('00' if idx < 9 else '0' if idx>8 and idx < 99 else '') + str(idx + 1)
            dataList.append({
                'name': field_name,
                'verbose_name': itm,
            })

        ot = JobSkill.objects.values_list('skill_name', flat=True).filter(
            skill_class=UserDefCode.objects.get(udc='S005'))  # 其他職能
        for idx, itm in enumerate(ot):
            # field_name = 'ot' + ('00' if idx < 9 else '0' if idx>9 and idx < 99 else '') + str(idx + 1)
            field_name = 'ot' + ('00' if idx < 9 else '0' if idx>8 and idx < 99 else '') + str(idx + 1)
            dataList.append({
                'name': field_name,
                'verbose_name': itm,
            })


        pr = JobSkill.objects.values_list('skill_name', flat=True).filter(
            skill_code__in=JobTitleSkill.objects.values_list('job_skill').filter(job_title=job_title))  #專業職能，只有專業職能，會依不同職務而不同
        for idx, itm in enumerate(pr):  # 結果:[{}]<---List's element have namy dict-->to js-->Array have many element
            # field_name = 'pr' + ('00' if idx < 9 else '0' if idx>9 and idx < 99 else '') + str(idx + 1)
            field_name = 'pr' + ('00' if idx < 9 else '0' if idx>8 and idx < 99 else '') + str(idx + 1)
            dataList.append({
                'name': field_name,
                'verbose_name': itm,
            })

        dataList.append({
            'name': 'xa001',
            'verbose_name': '佔總分的比率％',
        })

        dataList.append({
            'name': 'xa002',
            'verbose_name': '生手級/新手級/半熟手級/熟手級/高手級',
        })

        dataList.append({
            'name': 'xb001',
            'verbose_name': '教育訓練',
        })

        dataList.append({
            'name': 'xb002',
            'verbose_name': '課程名稱',
        })

        dataList.append({
            'name': 'xb003',
            'verbose_name': '預定輪調的職務',
        })
        return dataList

    def get_job_title_to_tabs(self):
        select_dept = self.request.session.get('select_dept', None)
        fields = ['work_code_title__work_code',
                  'work_code_title__job_title',
                  'work_code_title__enable',
                  'year',
                  'month',
                  'bpm',
                  # 'bpm__bpm_status',
                  'bpm__bpm_status_desc1',
                  # 'bpm__bpm_status_desc2',
                  ]
        qr0 = Q(bpm__isnull=True)
        qr1 = Q(bpm__bpm_status_desc1__exact='')   #未送BPM   留待js控制按鈕
        qr2 = Q(bpm__bpm_status_desc1='reject')    #BPM退回   留待js控制按鈕
        userID = self.request.user.username
        qr3 = Q(work_code_title__work_code__in=EmployeeInfoEasy.objects.filter(direct_supv=userID,dept_flevel_id=select_dept))     # 找到『直接主管』是userID的工號
        results = MatrixMaster.objects.filter( (qr0 | qr1 | qr2), qr3 ).values(*fields)                       # 要搭app  class matrix_score
        # results = MatrixMaster.objects.filter( (qr1 | qr2), qr3 ).values(*fields)                       # 要搭app  class matrix_score
        dataList = []
        if results:
            for dt in results:
                fieldsList = ['chi_name', 'dept', ]
                ee = model_to_dict(EmployeeInfoEasy.objects.get(work_code=dt['work_code_title__work_code']), fields=fieldsList)
                desc1 = JobTitle.objects.get(job_code=dt['work_code_title__job_title'][0:2]).job_name
                desc2 = JobTitle.objects.get(job_code=dt['work_code_title__job_title'][0:4]).job_name
                desc3 = JobTitle.objects.get(job_code=dt['work_code_title__job_title']).job_name
                desc_tree = desc1 + "_" + desc2 + "_" + desc3
                dataList.append({
                    'job_title': dt['work_code_title__job_title'],
                    'job_title_desc': JobTitle.objects.get(job_code=dt['work_code_title__job_title']).job_name,
                    'job_title_desc_tree': desc_tree,
                })
        single_dataList = [dict(t) for t in {tuple(d.items()) for d in dataList}]  # 去除list 裏重覆的dict
        cleanedList = sorted(single_dataList, key=lambda i: i['job_title'])    #字典排序
        return cleanedList

    def get_skill_score(self):
        results = UserDefCode.objects.filter(topic_code_id='skill_matrix_id').values_list('shc1','desc1','desc2','description')
        dataList = []
        for dataTuple in results:
            dataList.append({
                'schc1':  dataTuple[0],
                'desc1': dataTuple[1],
                'desc2': dataTuple[2],
                'description': dataTuple[3],
            })
        return  dataList

    # def get_skill_study(self):
    #     results = StudyPlan.objects.all().values_list('study_code','study_name','study_course')
    #     dataList = []
    #     for dataTuple in results:
    #         dataList.append({
    #             # 'value': dataTuple[0],
    #             'value':  dataTuple[1],
    #             'text': dataTuple[1],
    #             'course': dataTuple[2],
    #         })
    #     return dataList

    # def get_rotation_job(self):
    #     results = JobTitle.objects.all().values_list('job_code','job_name')
    #     dataList = []
    #     for dataTuple in results:
    #         dataList.append({
    #             # 'value': dataTuple[0],
    #             'value':  dataTuple[1],
    #             # 'text': dataTuple[0]+dataTuple[1],
    #             'text': dataTuple[1],
    #         })
    #     return dataList

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        tabs = self.get_job_title_to_tabs()    #清理過後的職務資料( distinct+sort )
        tab_context_list = []
        tab_fields = []
        tab_datas = []
        group_numbers = []
        for tab in tabs:
            job_title = tab.get('job_title')
            display_fields = []
            display_datas = []
            display_fields.extend(self.get_skills(job_title))
            display_datas.extend( matrix_score(self.request,job_title,self.request.user.username) )     # 在api_skill.py 的(def matrix_score )
            group_numbers.append( self.get_skills_length(job_title) )
            tab_fields.append(display_fields),
            tab_datas.append(display_datas),
        context.update({
            'tabs':tabs,
            # 'tab_context_list':tab_context_list,
            'groups':group_numbers,
            'tab_fields':tab_fields,
            'tab_datas':tab_datas,
            'score_choices':self.get_skill_score(),
            # 'study_choices':self.get_skill_study(),        #教育訓練
            # 'rotation_jobs':self.get_rotation_job(),       #輪調職務
        })
        return context


class TT408(SingleView):
    main_model = MatrixMaster
    main_sort = [
        # 'work_code_title',
        # 'year',
        # 'month',
        ]

    form_param = {}
    form_class = MatrixMasterForm                  #main_form(center)
    template_name = 'skill_pdca/tt408.html'
    title = 'TT408 技能盤點底稿維護'

    """ 下面GRID config-->display_fields """
    main_fields = [
        # 'work_code_title',
        # 'year',
        # 'month',
        # 'bpm',
    ]


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # context["main_dg_config"]["source_url"] = '/sk_api/data/matrix_master'
        context.update({
            "main_dg_config": {
                "display_fields": [
                    {'name': 'direct_supv', 'verbose_name': '主管'},
                    {'name': 'supv_name', 'verbose_name': '主管'},
                    {'name': 'dept', 'verbose_name': '部門'},
                    {'name': 'work_code', 'verbose_name': '工號'},
                    {'name': 'chi_name', 'verbose_name': '姓名'},
                    {'name': 'job_code', 'verbose_name': '職務代號'},
                    {'name': 'job_name', 'verbose_name': '職務名稱'},
                    {'name': 'year', 'verbose_name': '年'},
                    {'name': 'month', 'verbose_name': '月'},
                    {'name': 'bpm', 'verbose_name': 'BPM單號'},
                    {'name': 'bpm_desc1', 'verbose_name': 'BPM狀態'},
                    {'name': 'bpm_desc2', 'verbose_name': '狀態說明'},
                    {'name': 'report_url', 'verbose_name': '報表'},
                    {'name': 'detail_yn','verbose_name': 'id'},
                    {'name': 'id',},
                ],
                "model": None,
                # "source_url": reverse_lazy('model_handler', kwargs={'model': 'employee_title'}),
                "source_url": reverse_lazy('matrix_master_employee'),
            }
        })

        context.update({
            "east_dg_config": {
                "display_fields": [
                    {'name': 'direct_supv', 'verbose_name': '主管'},
                    {'name': 'supv_name', 'verbose_name': '主管'},
                    {'name': 'dept', 'verbose_name': '部門'},
                    # {'name': 'work_code', 'verbose_name': '工號'},
                    # {'name': 'chi_name', 'verbose_name': '姓名'},
                    # {'name': 'job_code', 'verbose_name': '職務代號'},
                    # {'name': 'job_name', 'verbose_name': '職務名稱'},
                    {'name': 'year', 'verbose_name': '年'},
                    {'name': 'month', 'verbose_name': '月'},
                    {'name': 'bpm', 'verbose_name': 'BPM單號'},
                    {'name': 'bpm_desc1', 'verbose_name': 'BPM狀態'},
                    {'name': 'bpm_desc2', 'verbose_name': '狀態說明'},
                    {'name': 'report_url', 'verbose_name': '報表'},
                    {'name': 'dept_udc', 'verbose_name': 'dept_udc'},
                ],
                "model": None,
                # "source_url": reverse_lazy('model_handler', kwargs={'model': 'employee_title'}),
                "source_url": reverse_lazy('matrix_master_director'),
            }
        })

        return context


class TT421(BaseLayoutView):
    template_name = 'skill_pdca/tt421.html'
    title = 'TT421 開發方向探索測試'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class TT422(BaseLayoutView):
    template_name = 'skill_pdca/tt422.html'
    title = 'TT422 技能盤點資料匯出'

    def get_job_titles(self):
        results = JobTitle.objects.filter(level_number=3).values_list('job_code','job_name')
        dataList =[]
        for dataTuple in results:
            dataList.append({
                'code':  dataTuple[0],
                'name': dataTuple[1],
            })
        return dataList

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'job_titles':self.get_job_titles(),       #輪調職務
        })
        return context
######技能盤點表----------------------------------------------------------------------------------------------------------------------ENDING


######工作事項明細表-------------------------------------------------------------------------------------------------------------------BEGIN
class TT602(SingleView):
    main_model = PdcaMaster
    main_sort = [
        'work_code',
        'order_number',
        ]

    form_param = {}
    form_class = EmployeePdcaForm_X                #main_form(center)
    template_name = 'skill_pdca/tt602.html'
    title = _('TT602 工作事項明細填寫')


    """ 下面GRID config-->display_fields """
    main_fields = [
        'work_code',
        'order_number',
    ]

    def for_pdca_calc(self):
        dataList = []
        pdca = PdcaDefinition.objects.all().values_list('order_number','pdca_choice','pdca_desc')
        for idx, itm in enumerate(pdca):
            dataList.append({
                'pdca': itm[1],
                'verbose_name': itm[2],
            })

        return dataList

    def get_display_fields(self,language):
        dataList = []
        pdca = PdcaDefinition.objects.all().values_list('order_number','pdca_choice','pdca_desc','id')
        for idx, itm in enumerate(pdca):
            if language == "zh-hant":
                pdca_desc = itm[2]
            else:
                pdca_desc_foreign = PdcaDefinitionForeign.objects.values('pdca_desc').filter(pdca_id=itm[3])
                if pdca_desc_foreign:
                    pdca_desc = pdca_desc_foreign[0]['pdca_desc']
                else:
                    pdca_desc = itm[2]
            field_name = 'pdca' + ('0' if idx < 9 else '') + str(idx + 1)
            dataList.append({
                'name':field_name,
                'pdca': itm[1],
                'verbose_name': pdca_desc,
            })

        flow = FlowDefinition.objects.all().values_list('order_number','flow_desc','id')
        for idx, itm in enumerate(flow):
            if language == "zh-hant":
                flow_desc = itm[1]
            else:
                flow_desc_foreign = FlowDefinitionForeign.objects.values('flow_desc').filter(flow_id=itm[2])
                if flow_desc_foreign:
                    flow_desc = flow_desc_foreign[0]['flow_desc']
                else:
                    flow_desc = itm[1]
            field_name = 'flow' + ('0' if idx < 9 else '') + str(idx + 1)
            dataList.append({
                'name':field_name,
                'verbose_name': flow_desc,
            })

        dataList.append({
            'name': 'calc01',
            'verbose_name': _('(分鐘/次)'),
        })

        dataList.append({
            'name': 'cycl01',
            'verbose_name': _('週期<br>(擇一)'),
        })

        dataList.append({
            'name': 'cycl02',
            'verbose_name': _('次數'),
        })

        dataList.append({
            'name': 'calc02',
            'verbose_name': _('(分鐘數)'),
        })

        p_content = ''
        for itm in pdca:
            if (itm[1]=='P'):
                if language == "zh-hant":
                    contact_word = itm[2]
                else:
                    contact_word_foreign = PdcaDefinitionForeign.objects.values('pdca_desc').filter(pdca_id=itm[3])
                    if contact_word_foreign:
                        contact_word = contact_word_foreign[0]['pdca_desc']
                    else:
                        contact_word = itm[2]
                p_content += contact_word + '<br>'
        dataList.append({
            'name': 'ptot01',
            'verbose_name': p_content,
        })

        d_content = ''
        for itm in pdca:
            if (itm[1]=='D'):
                if language == "zh-hant":
                    contact_word = itm[2]
                else:
                    contact_word_foreign = PdcaDefinitionForeign.objects.values('pdca_desc').filter(pdca_id=itm[3])
                    if contact_word_foreign:
                        contact_word = contact_word_foreign[0]['pdca_desc']
                    else:
                        contact_word = itm[2]
                d_content += contact_word+'<br>'
        dataList.append({
            'name': 'dtot01',
            'verbose_name': d_content,
        })

        pdca_c = PdcaDefinition.objects.filter(pdca_choice='C').values_list('order_number', 'pdca_choice', 'pdca_desc','id')
        for idx, itm in enumerate(pdca_c):
            if (itm[1]=='C'):
                if language == "zh-hant":
                    contact_word = itm[2]
                else:
                    contact_word_foreign = PdcaDefinitionForeign.objects.values('pdca_desc').filter(pdca_id=itm[3])
                    if contact_word_foreign:
                        contact_word = contact_word_foreign[0]['pdca_desc']
                    else:
                        contact_word = itm[2]
                field_name = 'ctot' + ('0' if idx < 9 else '') + str(idx + 1)
                dataList.append({
                    'name':field_name,
                    'verbose_name': contact_word,
                })

        a_content = ''
        for itm in pdca:
            if (itm[1]=='A'):
                if language == "zh-hant":
                    contact_word = itm[2]
                else:
                    contact_word_foreign = PdcaDefinitionForeign.objects.values('pdca_desc').filter(pdca_id=itm[3])
                    if contact_word_foreign:
                        contact_word = contact_word_foreign[0]['pdca_desc']
                    else:
                        contact_word = itm[2]
                a_content += contact_word
        dataList.append({
            'name': 'atot01',
            'verbose_name': a_content,
        })

        dataList.append({
            'name': 'okyn01',
            'verbose_name': _("依公式"),
        })

        return dataList

    def get_cycle_choice(self,language):
        results = CycleDefinition.objects.all().values_list('id','order_number','cycle_desc','basic','months')
        dataList = []
        for dataTuple in results:
            if language == "zh-hant":
                cycle_text = dataTuple[2]
            else:
                cycle_desc_foreign = CycleDefinitionForeign.objects.values('cycle_desc').filter(cycle_id=dataTuple[0])
                if cycle_desc_foreign:
                    cycle_text = cycle_desc_foreign[0]['cycle_desc']
                else:
                    cycle_text = dataTuple[2]

            dataList.append({
                'value':  dataTuple[0],
                'order_number': dataTuple[1],
                'text': cycle_text,
                'multiplicand': dataTuple[3]/dataTuple[4],
            })

        return dataList

    def get_nation_work_hours(self,language):
        # qr0 = Q( work_code=self.request.user.username )
        # qr1 = Q( resign_date__isnull=True )             #排除離職者
        # qr2 = Q( id = EmployeeInfoEasy.objects.values_list('nat_id').get(qr0,qr1)[0] )
        # results = UserDefCode.objects.filter(qr2).values_list('shc1','shc2','shc2_desc','shc3')     # 依員工國籍選工時
        # results = UserDefCode.objects.filter(topic_code_id='nat_id',shc3=language).values_list('shc1','shc2','shc2_desc','shc3')   # 依語系選工時

        choice_factory = self.request.session.get('factory')
        results = UserDefCode.objects.filter(id=choice_factory.get('nat_id')).values_list('shc1', 'shc2','shc2_desc','shc3')  # 依選擇的公司選工時
        dataList = []
        if results:
            for dataTuple in results:
                hours_desc = ''
                if dataTuple[3] == 'zh-hant':
                    hours_desc = _('台灣.中國.工時標準：60分*')
                elif dataTuple[3] == 'vi':
                    hours_desc = _('越南.工時標準：60分*')
                else:
                    hours_desc = _('台灣.中國.工時標準：60分*')

                dataList.append({
                    'hours_day': int(dataTuple[0]),
                    'days_month': int(dataTuple[1]),
                    'labor_hours_desc': hours_desc,
                })
        return dataList

    def get_job_title_to_tabs(self,language):
        fields = [
              'job_title_id',
              'job_title',
              'job_title__job_name',
              ]
        qr0 = Q( work_code=self.request.user.username )
        qr1 = Q( resign_date__isnull=True )             #排除離職者
        qr2 = Q( work_code = EmployeeInfoEasy.objects.values_list('work_code').get(qr0,qr1) )
        results =EmployeeTitle.objects.values(*fields).filter(qr2)
        dataList = []
        if results:
            for dt in results:
                if language=="zh-hant":
                    job_title_desc= dt['job_title__job_name']
                else:
                    job_name_foreign = JobTitleForeign.objects.values('job_name').filter(job_code=dt['job_title_id'],lang_code=language)
                    if job_name_foreign:
                        # 有對應的翻譯文字
                        job_title_desc = job_name_foreign[0]['job_name']
                    else:
                        # 無對應的翻譯文字, 使用中文
                        job_title_desc = dt['job_title__job_name']

                dataList.append({
                    'job_title': dt['job_title'],
                    'job_title_desc': job_title_desc,
                })
        return dataList

    def get_the_time(self,userId):
        qr1 = Q(work_code=userId)
        r = PdcaMaster.objects.values_list('the_time','bpm_status_desc1','bpm_number').filter( qr1 ).order_by('the_time').last()

        if r:
            if ( r[1] in ['','reject'] ):                #bpm_status_desc1
                # '',未送出bpm,繼續編輯
                # 退回 : 繼續編輯
                last_time = r[0]
            else:
                if ( r[1] == 'signed' ):
                    last_time = r[0]+1
                else:
                    # 未簽核完成，不允繼續寫一下個版本，由前端控制
                    last_time = 999999
        else:
            last_time = 1


        if last_time == 1:
            # return {"last":last_time,"current":last_time,"bpm_number":"","status":""}
            return {
                "last": last_time,
                "current": last_time,
                "bpm_number": "",
                "bpm_desc1": "",
                "bpm_desc2": ""
            }
        else:
            return {
                "last":last_time,
                "current":r[0],
                "bpm_number":r[2],
                "bpm_desc1":r[1],
                "bpm_desc2":UserDefCode.objects.get(topic_code_id='bpm_status',desc1=r[1]).desc2 if r[1] else ''
            }


    def get_context_data(self, **kwargs):
        language_code = set_language_code(self.request)
        context = super().get_context_data(**kwargs)
        context['pdca_agent'] = EmployeeInfoEasy.objects.values_list("pdca_agent",flat=True).filter(work_code=self.request.user.username)[0]
        context['form'] =  EmployeePdcaForm(self.request.user.username,self.request.user)
        context['choice_lang_form'] = ChoiceLanguage(self.request.session.get('choice_language'))
        tabs = self.get_job_title_to_tabs(language_code)    #清理過後的職務資料( distinct+sort )
        tab_context_list = []
        tab_fields = []
        pdca_list = self.get_display_fields(language_code)
        for tab in tabs:
            job_title = tab.get('job_title')
            display_fields = []
            this_node_id = 'tab'+job_title+'_dg'
            display_fields.extend(pdca_list)
            tab_context_list.append({
                'job_title': job_title,
                'job_title_desc': tab.get('job_title_desc'),
                'node_id' : this_node_id,
                "main_dg_config": {
                    "display_fields": display_fields,
                    "model": None,
                    "source_url": reverse_lazy('matrix_score'),  # 使用自己定義的Grid,取得下屬的metrics_setup
                },
            })
            tab_fields.append(display_fields),

        context.update({
            'tabs' : tabs,
            'tab_context_list' : tab_context_list,
            'tab_fields': tab_fields,
            'cycle_choices' : self.get_cycle_choice(language_code),
            'pdca_calc' : self.for_pdca_calc(),
            'working_hours' : self.get_nation_work_hours(language_code),
            'the_time': self.get_the_time(self.request.user.username),
            'labor_time':8,
            'choice_language':language_code
        })
        return context



class TT602_2PDF(PDFTemplateView):

    def get(self, request, *args, **kwargs):
        todayStr = timezone.now().astimezone(current_tz).strftime('%Y%m%d%H%M%S%f')
        get_param = request.GET.dict()
        filename = get_param.get('fileName', 'PDCA'+todayStr+".pdf")
        template_name = 'skill_pdca/tt602_2pdf.html'
        # pdf_template = 'skill_pdca/tt602_2pdf_open.html'
        pdf_template = 'skill_pdca/pdf_open_download.html'
        title = _('TT602_2pdf 工作事項明細_2PDF(tt602連結)')


        # generate response

        response = PDFTemplateResponse(
            request=request,
            template=template_name,                     #input
            filename=filename,                          #output
            context=self.get_context_data(),            #input's source context
            cmd_options={                               #pdf's format
                'quiet': None,
                'enable-local-file-access': True,
                'encoding': 'utf8',
                'page-size': 'A3',
                'orientation': 'Landscape',
                'title': "pdca 2022-03-18 Version 1.3",
                'footer-spacing': 5,              #Spacing between footer and content in mm
                'footer-line':True,
                'footer-center': 'page:' + '[page] / [toPage]',
                'footer-font-size':10,
                # 'footer-font-name':'標楷體',
                'footer-left': 'date:' + '[isodate]',
                'footer-right': 'time:' + '[time]',
            }
        )
        if ( filename[0:7] == 'PREVIEW'):
            output_file = '%s/PREVIEW/%s' % (settings.MEDIA_ROOT, filename)       #Where be save?
        else:
            output_file = '%s/reports/pdf/%s' % (settings.MEDIA_ROOT, filename)   #Where be save?
        with open(output_file, "wb") as f:                                        #Actual practice save
            f.write(response.rendered_content)
        return render(request,pdf_template,{'filename':output_file.split("..")[1]})    #Open the distinct(pdf) file


    def for_pdca_calc(self):
        dataList = []
        pdca = PdcaDefinition.objects.all().values_list('order_number','pdca_choice','pdca_desc')
        for idx, itm in enumerate(pdca):
            dataList.append({
                'pdca': itm[1],
                'verbose_name': itm[2],
            })

        return dataList

    def get_display_fields(self,language):
        dataList = []
        pdca = PdcaDefinition.objects.all().values_list('order_number','pdca_choice','pdca_desc','id')
        for idx, itm in enumerate(pdca):
            if language == "zh-hant":
                pdca_desc = itm[2]
            else:
                pdca_desc_foreign = PdcaDefinitionForeign.objects.values('pdca_desc').filter(pdca_id=itm[3])
                if pdca_desc_foreign:
                    pdca_desc = pdca_desc_foreign[0]['pdca_desc']
                else:
                    pdca_desc = itm[2]
            field_name = 'pdca' + ('0' if idx < 9 else '') + str(idx + 1)
            dataList.append({
                'name':field_name,
                'pdca': itm[1],
                'verbose_name': pdca_desc,
            })

        flow = FlowDefinition.objects.all().values_list('order_number','flow_desc','id')
        for idx, itm in enumerate(flow):
            if language == "zh-hant":
                flow_desc = itm[1]
            else:
                flow_desc_foreign = FlowDefinitionForeign.objects.values('flow_desc').filter(flow_id=itm[2])
                if flow_desc_foreign:
                    flow_desc = flow_desc_foreign[0]['flow_desc']
                else:
                    flow_desc = itm[1]
            field_name = 'flow' + ('0' if idx < 9 else '') + str(idx + 1)
            dataList.append({
                'name':field_name,
                'verbose_name': flow_desc,
            })

        dataList.append({
            'name': 'calc01',
            'verbose_name': _('分鐘/次'),
        })

        dataList.append({
            'name': 'cycl01',
            'verbose_name': _('週期'),
        })

        dataList.append({
            'name': 'cycl02',
            'verbose_name': _('次數'),
        })

        dataList.append({
            'name': 'calc02',
            'verbose_name': _('分鐘'),
        })

        p_content = ''
        for itm in pdca:
            if (itm[1]=='P'):
                if language == "zh-hant":
                    contact_word = itm[2]
                else:
                    contact_word_foreign = PdcaDefinitionForeign.objects.values('pdca_desc').filter(pdca_id=itm[3])
                    if contact_word_foreign:
                        contact_word = contact_word_foreign[0]['pdca_desc']
                    else:
                        contact_word = itm[2]
            p_content += contact_word + '<br>'
        dataList.append({
            'name': 'ptot01',
            'verbose_name': p_content,
        })

        d_content = ''
        for itm in pdca:
            if (itm[1]=='D'):
                if language == "zh-hant":
                    contact_word = itm[2]
                else:
                    contact_word_foreign = PdcaDefinitionForeign.objects.values('pdca_desc').filter(pdca_id=itm[3])
                    if contact_word_foreign:
                        contact_word = contact_word_foreign[0]['pdca_desc']
                    else:
                        contact_word = itm[2]
                d_content += contact_word+'<br>'
        dataList.append({
            'name': 'dtot01',
            'verbose_name': d_content,
        })

        pdca_c = PdcaDefinition.objects.filter(pdca_choice='C').values_list('order_number', 'pdca_choice', 'pdca_desc','id')
        for idx, itm in enumerate(pdca_c):
            if (itm[1]=='C'):
                if language == "zh-hant":
                    contact_word = itm[2]
                else:
                    contact_word_foreign = PdcaDefinitionForeign.objects.values('pdca_desc').filter(pdca_id=itm[3])
                    if contact_word_foreign:
                        contact_word = contact_word_foreign[0]['pdca_desc']
                    else:
                        contact_word = itm[2]
                field_name = 'ctot' + ('0' if idx < 9 else '') + str(idx + 1)
                dataList.append({
                    'name':field_name,
                    'verbose_name': contact_word,
                })

        a_content = ''
        for itm in pdca:
            if (itm[1]=='A'):
                if language == "zh-hant":
                    contact_word = itm[2]
                else:
                    contact_word_foreign = PdcaDefinitionForeign.objects.values('pdca_desc').filter(pdca_id=itm[3])
                    if contact_word_foreign:
                        contact_word = contact_word_foreign[0]['pdca_desc']
                    else:
                        contact_word = itm[2]
                a_content += contact_word
        dataList.append({
            'name': 'atot01',
            'verbose_name': a_content,
        })

        dataList.append({
            'name': 'okyn01',
            'verbose_name': _("依公式"),
        })

        return dataList

    def get_cycle_choice(self,language):
        results = CycleDefinition.objects.all().values_list('id','order_number','cycle_desc','basic','months')
        dataList = []
        for dataTuple in results:
            if language == "zh-hant":
                cycle_text = dataTuple[2]
            else:
                cycle_desc_foreign = CycleDefinitionForeign.objects.values('cycle_desc').filter(cycle_id=dataTuple[0])
                if cycle_desc_foreign:
                    cycle_text = cycle_desc_foreign[0]['cycle_desc']
                else:
                    cycle_text = dataTuple[2]
            dataList.append({
                'value':  dataTuple[0],
                'order_number': dataTuple[1],
                'text': cycle_text,
                'multiplicand': dataTuple[3]/dataTuple[4],
            })
        return dataList

    def get_nation_work_hours(self,language):
        # qr0 = Q( work_code=self.request.user.username )
        # qr1 = Q( resign_date__isnull=True )             #排除離職者
        # qr2 = Q( id = EmployeeInfoEasy.objects.values_list('nat_id').get(qr0,qr1)[0] )
        # results = UserDefCode.objects.filter(qr2).values_list('shc1','shc2','shc2_desc','shc3')     # 依員工國籍選工時
        # results = UserDefCode.objects.filter(topic_code_id='nat_id',shc3=language).values_list('shc1','shc2','shc2_desc','shc3')   # 依語系選工時

        choice_factory = self.request.session.get('factory')
        results = UserDefCode.objects.filter(id=choice_factory.get('nat_id')).values_list('shc1', 'shc2','shc2_desc','shc3')  # 依選擇的公司選工時
        dataList = []
        if results:
            for dataTuple in results:
                hours_desc = ''
                if dataTuple[3] == 'zh-hant':
                    hours_desc = _('台灣.中國.工時標準：60分*')
                elif dataTuple[3] == 'vi':
                    hours_desc = _('越南.工時標準：60分*')
                else:
                    hours_desc = _('台灣.中國.工時標準：60分*')

                dataList.append({
                    'hours_day': int(dataTuple[0]),
                    'days_month': int(dataTuple[1]),
                    'labor_hours_desc': hours_desc,
                })
        return dataList


    # 報表.表頭"核心職能/管理職能/一般職能/專業職能" colspan使用
    def get_title_length(self):
        PL= PdcaDefinition.objects.filter(pdca_choice='P').count()
        DL = PdcaDefinition.objects.filter(pdca_choice='D').count()
        CL = PdcaDefinition.objects.filter(pdca_choice='C').count()
        AL = PdcaDefinition.objects.filter(pdca_choice='A').count()
        FL = FlowDefinition.objects.all().count()

        return {
            "P_length" : PL,
            "D_length" : DL,
            "C_length" : CL,
            "A_length" : AL,
            "F_length" : FL,
        }

    def get_employee_data(self,userId,userName):
        fields = ['dept_id__desc1',
                  'arrival_date',
                  'trans_date',
                  'trans_type',
                  'rank_id__desc1',
                  'pos_id__desc1',
                  'factory_id__name',
                  ]
        result = EmployeeInfoEasy.objects.filter(work_code=userId).values_list(*fields)
        for T in result:
            dt = {
                "work_code":userId,
                "chi_name":userName,
                "dept": T[0],
                "arrival_date": T[1],
                "trans_date": T[2],
                "trans_type": T[3],
                "rank": T[4],
                "pos": T[5],
                "factory": T[6],
            }
        return dt


    def get_job_title_to_tabs(self,language):
        fields = ['job_title',
                  'job_title__job_name',
                  ]

        qr0 = Q( work_code=self.request.user.username )
        qr1 = Q( resign_date__isnull=True )             #排除離職者
        qr2 = Q( work_code = EmployeeInfoEasy.objects.values_list('work_code').get(qr0,qr1) )
        results =EmployeeTitle.objects.values(*fields).filter(qr2)
        dataList = []
        # print("\n"*3)
        # print("="*200)
        if results:
            for dt in results:
                # print(dt)
                # print("-"*50)
                if language=="zh-hant":
                    job_title_desc= dt['job_title__job_name']
                else:
                    job_name_foreign = JobTitleForeign.objects.values('job_name').filter(job_code=dt['job_title'],lang_code=language)
                    if job_name_foreign:
                        # 有對應的翻譯文字
                        job_title_desc = job_name_foreign[0]['job_name']
                    else:
                        # 無對應的翻譯文字, 使用中文
                        job_title_desc = dt['job_title__job_name']

                dataList.append({
                    'job_title': dt['job_title'],
                    'job_title_desc': job_title_desc,
                })
        # print("="*200)
        # print('\n'*3)
        return dataList

    def get_context_data(self, **kwargs):
        language_code = set_language_code(self.request)
        context = super().get_context_data(**kwargs)
        context['form'] =  EmployeePdcaForm(self.request.user.username,self.request.user)
        tabs = self.get_job_title_to_tabs(language_code)    #清理過後的職務資料( distinct+sort )
        tab_context_list = []
        tab_fields = []
        pdca_list = self.get_display_fields(language_code)
        tab_datas = []
        group_numbers = []
        for tab in tabs:
            job_title = tab.get('job_title')
            display_fields = []
            display_datas = []
            this_node_id = 'tab'+job_title+'_dg'
            display_datas.extend( pdca_detail(self.request, job_title, self.request.user.username ,"X") )
            tab_context_list.append({
                'job_title': job_title,
                'job_title_desc': tab.get('job_title_desc'),
                'node_id' : this_node_id,
                "main_dg_config": {
                    "display_fields": display_fields,
                    "model": None,
                    "source_url": reverse_lazy('matrix_score'),  # 使用自己定義的Grid,取得下屬的metrics_setup
                },
            })
            tab_datas.append(display_datas)
        display_fields.extend(pdca_list)
        tab_fields.append(display_fields)
        group_numbers.append(self.get_title_length())
        context.update({
            'employee': self.get_employee_data(self.request.user.username,self.request.user),
            'tabs' : tabs,
            'tab_context_list' : tab_context_list,
            'groups': group_numbers,
            'tab_fields': tab_fields,
            'tab_datas': tab_datas,
            'cycle_choices' : self.get_cycle_choice(language_code),
            'pdca_calc' : self.for_pdca_calc(),
            'working_hours' : self.get_nation_work_hours(language_code),
        })
        return context


######工作事項明細表(代填)-------------------------------------------------------------------------------------------------------------------BEGIN
class TT603(SingleView):
    main_model = PdcaMaster
    main_sort = [
        'work_code',
        'order_number',
        ]

    custom_model = EmployeeInfoEasy
    custom_sort = 'work_code'

    form_param = {}
    form_class = EmployeePdcaForm_X                #main_form(center)
    template_name = 'skill_pdca/tt603.html'
    title = _('TT603 工作事項明細填寫(代填)')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # north side's grid
        # 2022/06/13
        context.update({
            "employee_info_easy_dg_config": {
                "display_fields": [
                    {'name': 'work_code', 'verbose_name': _('工號')},
                    {'name': 'chi_name', 'verbose_name': _('姓名')},
                    {'name': 'dept_name', 'verbose_name': _('部門')},
                    {'name': 'pos_name', 'verbose_name': _('職位')},
                    {'name': 'director_id', 'verbose_name': _('主管工號')},
                    {'name': 'director_name', 'verbose_name': _('主管名稱')},
                    {'name': 'arrival_date', 'verbose_name': _('到職日')},
                    {'name': 'resign_date', 'verbose_name': _('離職日')},
                    {'name': 'rank', 'verbose_name': _('職等')},
                    {'name': 'bonus_factor', 'verbose_name': _('點數')},
                    {'name': 'eval_class', 'verbose_name': 'BSC/KPI'},
                    {'name': 'nat', 'verbose_name': _('國籍')},
                    {'name': 'the_time', 'verbose_name': _('最新版本')},
                ],
                "model": None,
                "source_url": reverse_lazy('get_pdca_subs_data'),  # 使用自己定義的Grid
            }
        })

        return context

class TT603_TAB(SingleView):
    main_model = PdcaMaster
    main_sort = [
        'work_code',
        'order_number',
        ]

    form_param = {}
    form_class = EmployeePdcaForm_X                #main_form(center)
    template_name = 'skill_pdca/tt603_tab.html'
    title = _('TT602 工作事項明細填寫')


    """ 下面GRID config-->display_fields """
    main_fields = [
        'work_code',
        'order_number',
    ]

    def for_pdca_calc(self):
        dataList = []
        pdca = PdcaDefinition.objects.all().values_list('order_number','pdca_choice','pdca_desc')
        for idx, itm in enumerate(pdca):
            dataList.append({
                'pdca': itm[1],
                'verbose_name': itm[2],
            })

        return dataList

    def get_display_fields(self,language):
        dataList = []
        pdca = PdcaDefinition.objects.all().values_list('order_number','pdca_choice','pdca_desc','id')
        for idx, itm in enumerate(pdca):
            if language == "zh-hant":
                pdca_desc = itm[2]
            else:
                pdca_desc_foreign = PdcaDefinitionForeign.objects.values('pdca_desc').filter(pdca_id=itm[3])
                if pdca_desc_foreign:
                    pdca_desc = pdca_desc_foreign[0]['pdca_desc']
                else:
                    pdca_desc = itm[2]
            field_name = 'pdca' + ('0' if idx < 9 else '') + str(idx + 1)
            dataList.append({
                'name':field_name,
                'pdca': itm[1],
                'verbose_name': pdca_desc,
            })

        flow = FlowDefinition.objects.all().values_list('order_number','flow_desc','id')
        for idx, itm in enumerate(flow):
            if language == "zh-hant":
                flow_desc = itm[1]
            else:
                flow_desc_foreign = FlowDefinitionForeign.objects.values('flow_desc').filter(flow_id=itm[2])
                if flow_desc_foreign:
                    flow_desc = flow_desc_foreign[0]['flow_desc']
                else:
                    flow_desc = itm[1]
            field_name = 'flow' + ('0' if idx < 9 else '') + str(idx + 1)
            dataList.append({
                'name':field_name,
                'verbose_name': flow_desc,
            })

        dataList.append({
            'name': 'calc01',
            'verbose_name': _('(分鐘/次)'),
        })

        dataList.append({
            'name': 'cycl01',
            'verbose_name': _('週期<br>(擇一)'),
        })

        dataList.append({
            'name': 'cycl02',
            'verbose_name': _('次數'),
        })

        dataList.append({
            'name': 'calc02',
            'verbose_name': _('(分鐘數)'),
        })

        p_content = ''
        for itm in pdca:
            if (itm[1] == 'P'):
                if language == "zh-hant":
                    contact_word = itm[2]
                else:
                    contact_word_foreign = PdcaDefinitionForeign.objects.values('pdca_desc').filter(pdca_id=itm[3])
                    if contact_word_foreign:
                        contact_word = contact_word_foreign[0]['pdca_desc']
                    else:
                        contact_word = itm[2]

                p_content += contact_word + '<br>'
        dataList.append({
            'name': 'ptot01',
            'verbose_name': p_content,
        })

        d_content = ''
        for itm in pdca:
            if (itm[1] == 'D'):
                if language == "zh-hant":
                    contact_word = itm[2]
                else:
                    contact_word_foreign = PdcaDefinitionForeign.objects.values('pdca_desc').filter(pdca_id=itm[3])
                    if contact_word_foreign:
                        contact_word = contact_word_foreign[0]['pdca_desc']
                    else:
                        contact_word = itm[2]
                d_content += contact_word + '<br>'
        dataList.append({
            'name': 'dtot01',
            'verbose_name': d_content,
        })

        pdca_c = PdcaDefinition.objects.filter(pdca_choice='C').values_list('order_number', 'pdca_choice', 'pdca_desc',
                                                                            'id')
        for idx, itm in enumerate(pdca_c):
            if (itm[1] == 'C'):
                if language == "zh-hant":
                    contact_word = itm[2]
                else:
                    contact_word_foreign = PdcaDefinitionForeign.objects.values('pdca_desc').filter(pdca_id=itm[3])
                    if contact_word_foreign:
                        contact_word = contact_word_foreign[0]['pdca_desc']
                    else:
                        contact_word = itm[2]
                field_name = 'ctot' + ('0' if idx < 9 else '') + str(idx + 1)
                dataList.append({
                    'name': field_name,
                    'verbose_name': contact_word,
                })

        a_content = ''
        for itm in pdca:
            if (itm[1] == 'A'):
                if language == "zh-hant":
                    contact_word = itm[2]
                else:
                    contact_word_foreign = PdcaDefinitionForeign.objects.values('pdca_desc').filter(pdca_id=itm[3])
                    if contact_word_foreign:
                        contact_word = contact_word_foreign[0]['pdca_desc']
                    else:
                        contact_word = itm[2]
                a_content += contact_word
        dataList.append({
            'name': 'atot01',
            'verbose_name': a_content,
        })

        dataList.append({
            'name': 'okyn01',
            'verbose_name': _("依公式"),
        })

        return dataList

    def get_cycle_choice(self,language):
        results = CycleDefinition.objects.all().values_list('id','order_number','cycle_desc','basic','months')
        dataList = []
        for dataTuple in results:
            if language == "zh-hant":
                cycle_text = dataTuple[2]
            else:
                cycle_desc_foreign = CycleDefinitionForeign.objects.values('cycle_desc').filter(cycle_id=dataTuple[0])
                if cycle_desc_foreign:
                    cycle_text = cycle_desc_foreign[0]['cycle_desc']
                else:
                    cycle_text = dataTuple[2]

            dataList.append({
                'value':  dataTuple[0],
                'order_number': dataTuple[1],
                'text': cycle_text,
                'multiplicand': dataTuple[3]/dataTuple[4],
            })

        return dataList

    def get_nation_work_hours(self, language):
        # qr0 = Q( work_code=self.request.user.username )
        # qr1 = Q( resign_date__isnull=True )             #排除離職者
        # qr2 = Q( id = EmployeeInfoEasy.objects.values_list('nat_id').get(qr0,qr1)[0] )
        # results = UserDefCode.objects.filter(qr2).values_list('shc1','shc2','shc2_desc','shc3')     # 依員工國籍選工時
        # results = UserDefCode.objects.filter(topic_code_id='nat_id',shc3=language).values_list('shc1','shc2','shc2_desc','shc3')   # 依語系選工時

        choice_factory = self.request.session.get('factory')
        results = UserDefCode.objects.filter(id=choice_factory.get('nat_id')).values_list('shc1', 'shc2', 'shc2_desc',
                                                                                          'shc3')  # 依選擇的公司選工時
        dataList = []
        if results:
            for dataTuple in results:
                hours_desc = ''
                if dataTuple[3] == 'zh-hant':
                    hours_desc = _('台灣.中國.工時標準：60分*')
                elif dataTuple[3] == 'vi':
                    hours_desc = _('越南.工時標準：60分*')
                else:
                    hours_desc = _('台灣.中國.工時標準：60分*')

                dataList.append({
                    'hours_day': int(dataTuple[0]),
                    'days_month': int(dataTuple[1]),
                    'labor_hours_desc': hours_desc,
                })
        return dataList

    def get_job_title_to_tabs(self, language):
        fields = [
            'job_title_id',
            'job_title',
            'job_title__job_name',
        ]

        select_work_code = self.request.session.get('select_work_code', None)
        qr0 = Q( work_code=select_work_code )
        qr1 = Q( resign_date__isnull=True )             #排除離職者
        qr2 = Q( work_code = EmployeeInfoEasy.objects.values_list('work_code').get(qr0,qr1) )
        results = EmployeeTitle.objects.values(*fields).filter(qr2)
        dataList = []
        if results:
            for dt in results:
                if language == "zh-hant":
                    job_title_desc = dt['job_title__job_name']
                else:
                    job_name_foreign = JobTitleForeign.objects.values('job_name').filter(job_code=dt['job_title_id'],
                                                                                         lang_code=language)
                    if job_name_foreign:
                        # 有對應的翻譯文字
                        job_title_desc = job_name_foreign[0]['job_name']
                    else:
                        # 無對應的翻譯文字, 使用中文
                        job_title_desc = dt['job_title__job_name']

                dataList.append({
                    'job_title': dt['job_title'],
                    'job_title_desc': job_title_desc,
                })
        return dataList

    def get_the_time(self):
        qr1 = Q(work_code=self.request.session.get('select_work_code', None))
        r = PdcaMaster.objects.values_list('the_time','bpm_status_desc1','bpm_number').filter( qr1 ).order_by('the_time').last()
        print("\n"*3)
        print("="*200)
        print("work_code=",self.request.session.get('select_work_code', None)," result=",r)
        print("="*200)


        if r:
            if ( r[1] in ['','reject'] ):                #bpm_status_desc1
                # '',未送出bpm,繼續編輯
                # 退回 : 繼續編輯
                last_time = r[0]
            else:
                if ( r[1] == 'signed' ):
                    last_time = r[0]+1
                else:
                    # 未簽核完成，不允繼續寫一下個版本，由前端控制
                    last_time = 999999
        else:
            last_time = 1
        print(" last_time=",last_time)
        print("\n"*3)


        if last_time == 1:
            # return {"last":last_time,"current":last_time,"bpm_number":"","status":""}
            return {
                "last": last_time,
                "current": last_time,
                "bpm_number": "",
                "bpm_desc1": "",
                "bpm_desc2": ""
            }
        else:
            return {
                "last":last_time,
                "current":r[0],
                "bpm_number":r[2],
                "bpm_desc1":r[1],
                "bpm_desc2":UserDefCode.objects.get(topic_code_id='bpm_status',desc1=r[1]).desc2 if r[1] else ''
            }


    def get_context_data(self, **kwargs):
        language_code = set_language_code(self.request)
        context = super().get_context_data(**kwargs)
        context['choice_lang_form'] = ChoiceLanguage(self.request.session.get('choice_language'))
        tabs = self.get_job_title_to_tabs(language_code)    #清理過後的職務資料( distinct+sort )
        tab_context_list = []
        tab_fields = []
        pdca_list = self.get_display_fields(language_code)
        for tab in tabs:
            job_title = tab.get('job_title')
            display_fields = []
            this_node_id = 'tab'+job_title+'_dg'
            display_fields.extend(pdca_list)
            tab_context_list.append({
                'job_title': job_title,
                'job_title_desc': tab.get('job_title_desc'),
                'node_id' : this_node_id,
                "main_dg_config": {
                    "display_fields": display_fields,
                    "model": None,
                    "source_url": reverse_lazy('matrix_score'),  # 使用自己定義的Grid,取得下屬的metrics_setup
                },
            })
            tab_fields.append(display_fields),

        context.update({
            'tabs' : tabs,
            'tab_context_list' : tab_context_list,
            'tab_fields': tab_fields,
            'cycle_choices' : self.get_cycle_choice(language_code),
            'pdca_calc' : self.for_pdca_calc(),
            'working_hours' : self.get_nation_work_hours(language_code),
            'the_time': self.get_the_time(),
            'labor_time': 8,
            'choice_language': language_code,
            'select_work_code':self.request.session.get('select_work_code', None),
            'select_chi_name':self.request.session.get('select_chi_name', None),
        })
        return context




class TT603_TAB2PDF(PDFTemplateView):

    def get(self, request, *args, **kwargs):
        todayStr = timezone.now().astimezone(current_tz).strftime('%Y%m%d%H%M%S%f')
        get_param = request.GET.dict()
        filename = get_param.get('fileName', 'PDCA'+todayStr+".pdf")
        template_name = 'skill_pdca/tt603_tab2pdf.html'
        pdf_template = 'skill_pdca/pdf_open_download.html'

        # generate response
        response = PDFTemplateResponse(
            request=request,
            template=template_name,                     #input
            filename=filename,                          #output
            context=self.get_context_data(),            #input's source context
            cmd_options={                               #pdf's format
                'quiet': None,
                'enable-local-file-access': True,
                'encoding': 'utf8',
                'page-size': 'A3',
                'orientation': 'Landscape',
                'title': "pdca 2022-03-18 Version 1.3",
                'footer-spacing': 5,              #Spacing between footer and content in mm
                'footer-line':True,
                'footer-center': 'page:' + '[page] / [toPage]',
                'footer-font-size':10,
                # 'footer-font-name':'標楷體',
                'footer-left': 'date:' + '[isodate]',
                'footer-right': 'time:' + '[time]',
            }
        )
        if ( filename[0:7] == 'PREVIEW'):
            output_file = '%s/PREVIEW/%s' % (settings.MEDIA_ROOT, filename)     #Where be save?
        else:
            output_file = '%s/reports/pdf/%s' % (settings.MEDIA_ROOT, filename)     #Where be save?
        with open(output_file, "wb") as f:                                      #Actual practice save
            f.write(response.rendered_content)
        return render(request,pdf_template,{'filename':output_file.split("..")[1]})           #Open the distinct(pdf) file

    def for_pdca_calc(self):
        dataList = []
        pdca = PdcaDefinition.objects.all().values_list('order_number','pdca_choice','pdca_desc')
        for idx, itm in enumerate(pdca):
            dataList.append({
                'pdca': itm[1],
                'verbose_name': itm[2],
            })

        return dataList

    def get_display_fields(self,language):
        dataList = []
        pdca = PdcaDefinition.objects.all().values_list('order_number','pdca_choice','pdca_desc','id')
        for idx, itm in enumerate(pdca):
            if language == "zh-hant":
                pdca_desc = itm[2]
            else:
                pdca_desc_foreign = PdcaDefinitionForeign.objects.values('pdca_desc').filter(pdca_id=itm[3])
                if pdca_desc_foreign:
                    pdca_desc = pdca_desc_foreign[0]['pdca_desc']
                else:
                    pdca_desc = itm[2]
            field_name = 'pdca' + ('0' if idx < 9 else '') + str(idx + 1)
            dataList.append({
                'name':field_name,
                'pdca': itm[1],
                'verbose_name': pdca_desc,
            })

        flow = FlowDefinition.objects.all().values_list('order_number','flow_desc','id')
        for idx, itm in enumerate(flow):
            if language == "zh-hant":
                flow_desc = itm[1]
            else:
                flow_desc_foreign = FlowDefinitionForeign.objects.values('flow_desc').filter(flow_id=itm[2])
                if flow_desc_foreign:
                    flow_desc = flow_desc_foreign[0]['flow_desc']
                else:
                    flow_desc = itm[1]
            field_name = 'flow' + ('0' if idx < 9 else '') + str(idx + 1)
            dataList.append({
                'name':field_name,
                'verbose_name': flow_desc,
            })

        dataList.append({
            'name': 'calc01',
            'verbose_name': _('(分鐘/次)'),
        })

        dataList.append({
            'name': 'cycl01',
            'verbose_name': _('週期<br>(擇一)'),
        })

        dataList.append({
            'name': 'cycl02',
            'verbose_name': _('次數'),
        })

        dataList.append({
            'name': 'calc02',
            'verbose_name': _('(分鐘數)'),
        })

        p_content = ''
        for itm in pdca:
            if (itm[1]=='P'):
                if language == "zh-hant":
                    contact_word = itm[2]
                else:
                    contact_word_foreign = PdcaDefinitionForeign.objects.values('pdca_desc').filter(pdca_id=itm[3])
                    if contact_word_foreign:
                        contact_word = contact_word_foreign[0]['pdca_desc']
                    else:
                        contact_word = itm[2]

                p_content += contact_word + '<br>'
        dataList.append({
            'name': 'ptot01',
            'verbose_name': p_content,
        })

        d_content = ''
        for itm in pdca:
            if (itm[1]=='D'):
                if language == "zh-hant":
                    contact_word = itm[2]
                else:
                    contact_word_foreign = PdcaDefinitionForeign.objects.values('pdca_desc').filter(pdca_id=itm[3])
                    if contact_word_foreign:
                        contact_word = contact_word_foreign[0]['pdca_desc']
                    else:
                        contact_word = itm[2]
                d_content += contact_word + '<br>'
        dataList.append({
            'name': 'dtot01',
            'verbose_name': d_content,
        })

        pdca_c = PdcaDefinition.objects.filter(pdca_choice='C').values_list('order_number', 'pdca_choice', 'pdca_desc','id')
        for idx, itm in enumerate(pdca_c):
            if (itm[1]=='C'):
                if language == "zh-hant":
                    contact_word = itm[2]
                else:
                    contact_word_foreign = PdcaDefinitionForeign.objects.values('pdca_desc').filter(pdca_id=itm[3])
                    if contact_word_foreign:
                        contact_word = contact_word_foreign[0]['pdca_desc']
                    else:
                        contact_word = itm[2]
                field_name = 'ctot' + ('0' if idx < 9 else '') + str(idx + 1)
                dataList.append({
                    'name':field_name,
                    'verbose_name': contact_word,
                })

        a_content = ''
        for itm in pdca:
            if (itm[1]=='A'):
                if language == "zh-hant":
                    contact_word = itm[2]
                else:
                    contact_word_foreign = PdcaDefinitionForeign.objects.values('pdca_desc').filter(pdca_id=itm[3])
                    if contact_word_foreign:
                        contact_word = contact_word_foreign[0]['pdca_desc']
                    else:
                        contact_word = itm[2]
                a_content += contact_word
        dataList.append({
            'name': 'atot01',
            'verbose_name': a_content,
        })

        dataList.append({
            'name': 'okyn01',
            'verbose_name': _("依公式"),
        })

        return dataList

    def get_cycle_choice(self,language):
        results = CycleDefinition.objects.all().values_list('id','order_number','cycle_desc','basic','months')
        dataList = []
        for dataTuple in results:
            if language == "zh-hant":
                cycle_text = dataTuple[2]
            else:
                cycle_desc_foreign = CycleDefinitionForeign.objects.values('cycle_desc').filter(cycle_id=dataTuple[0])
                if cycle_desc_foreign:
                    cycle_text = cycle_desc_foreign[0]['cycle_desc']
                else:
                    cycle_text = dataTuple[2]
            dataList.append({
                'value':  dataTuple[0],
                'order_number': dataTuple[1],
                'text': cycle_text,
                'multiplicand': dataTuple[3]/dataTuple[4],
            })
        return dataList

    def get_nation_work_hours(self, language):
        select_work_code = self.request.session.get('select_work_code', None)
        # qr0 = Q(work_code=select_work_code)
        # qr1 = Q( resign_date__isnull=True )             #排除離職者
        # qr2 = Q( id = EmployeeInfoEasy.objects.values_list('nat_id').get(qr0,qr1)[0] )
        # results = UserDefCode.objects.filter(qr2).values_list('shc1','shc2')
        choice_factory = self.request.session.get('factory')
        results = UserDefCode.objects.filter(id=choice_factory.get('nat_id')).values_list('shc1', 'shc2', 'shc2_desc',
                                                                                          'shc3')  # 依選擇的公司選工時

        dataList = []
        for dataTuple in results:
            hours_desc = ''
            if dataTuple[3] == 'zh-hant':
                hours_desc = _('台灣.中國.工時標準：60分*')
            elif dataTuple[3] == 'vi':
                hours_desc = _('越南.工時標準：60分*')
            else:
                hours_desc = _('台灣.中國.工時標準：60分*')

        dataList.append({
            'hours_day': int(dataTuple[0]),
            'days_month': int(dataTuple[1]),
            'labor_hours_desc': hours_desc,
        })
        return dataList


    # 報表.表頭"核心職能/管理職能/一般職能/專業職能" colspan使用
    def get_title_length(self):
        PL= PdcaDefinition.objects.filter(pdca_choice='P').count()
        DL = PdcaDefinition.objects.filter(pdca_choice='D').count()
        CL = PdcaDefinition.objects.filter(pdca_choice='C').count()
        AL = PdcaDefinition.objects.filter(pdca_choice='A').count()
        FL = FlowDefinition.objects.all().count()

        return {
            "P_length" : PL,
            "D_length" : DL,
            "C_length" : CL,
            "A_length" : AL,
            "F_length" : FL,
        }

    def get_employee_data(self,userId,userName):
        fields = ['dept_id__desc1',
                  'arrival_date',
                  'trans_date',
                  'trans_type',
                  'rank_id__desc1',
                  'pos_id__desc1',
                  'factory_id__name',
                  ]
        result = EmployeeInfoEasy.objects.filter(work_code=userId).values_list(*fields)
        for T in result:
            dt = {
                "work_code":userId,
                "chi_name":userName,
                "dept": T[0],
                "arrival_date": T[1],
                "trans_date": T[2],
                "trans_type": T[3],
                "rank": T[4],
                "pos": T[5],
                "factory": T[6],
            }
        return dt


    def get_job_title_to_tabs(self, language):
        fields = [
                  'job_title_id',
                  'job_title',
                  'job_title__job_name',
                  ]
        select_work_code = self.request.session.get('select_work_code', None)
        qr0 = Q( work_code=select_work_code )
        qr1 = Q( resign_date__isnull=True )             #排除離職者
        qr2 = Q( work_code = EmployeeInfoEasy.objects.values_list('work_code').get(qr0,qr1) )
        results =EmployeeTitle.objects.values(*fields).filter(qr2)
        dataList = []
        if results:
            for dt in results:
                if language == "zh-hant":
                    job_title_desc = dt['job_title__job_name']
                else:
                    job_name_foreign = JobTitleForeign.objects.values('job_name').filter(job_code=dt['job_title_id'],
                                                                                         lang_code=language)
                    if job_name_foreign:
                        # 有對應的翻譯文字
                        job_title_desc = job_name_foreign[0]['job_name']
                    else:
                        # 無對應的翻譯文字, 使用中文
                        job_title_desc = dt['job_title__job_name']
                dataList.append({
                    'job_title': dt['job_title'],
                    'job_title_desc': job_title_desc,
                })
        return dataList

    def get_context_data(self, **kwargs):
        language_code = set_language_code(self.request)
        context = super().get_context_data(**kwargs)
        select_work_code = self.request.session.get('select_work_code', None)
        select_chi_name = self.request.session.get('select_chi_name', None)
        tabs = self.get_job_title_to_tabs(language_code)    #清理過後的職務資料( distinct+sort )
        tab_context_list = []
        tab_fields = []
        pdca_list = self.get_display_fields(language_code)
        tab_datas = []
        group_numbers = []
        for tab in tabs:
            job_title = tab.get('job_title')
            display_fields = []
            display_datas = []
            this_node_id = 'tab'+job_title+'_dg'
            display_datas.extend( pdca_detail(self.request, job_title, select_work_code ,"X") )
            tab_context_list.append({
                'job_title': job_title,
                'job_title_desc': tab.get('job_title_desc'),
                'node_id' : this_node_id,
                "main_dg_config": {
                    "display_fields": display_fields,
                    "model": None,
                    "source_url": reverse_lazy('matrix_score'),  # 使用自己定義的Grid,取得下屬的metrics_setup
                },
            })
            tab_datas.append(display_datas)
        display_fields.extend(pdca_list)
        tab_fields.append(display_fields)
        group_numbers.append(self.get_title_length())
        context.update({
            'employee': self.get_employee_data(select_work_code,select_chi_name),
            'tabs' : tabs,
            'tab_context_list' : tab_context_list,
            'groups': group_numbers,
            'tab_fields': tab_fields,
            'tab_datas': tab_datas,
            'cycle_choices' : self.get_cycle_choice(language_code),
            'pdca_calc' : self.for_pdca_calc(),
            'working_hours' : self.get_nation_work_hours(language_code),
        })
        return context



class TT604(SingleView):
    main_model = PdcaMaster
    main_sort = []
    main_fields = []
    form_param = {}
    form_class = MatrixMasterForm                  #main_form(center)
    template_name = 'skill_pdca/tt604.html'
    title = 'TT604 工作明細填寫狀況查詢'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            "main_dg_config": {
                "display_fields": [
                    {'name': 'work_code', 'verbose_name': '工號'},
                    {'name': 'chi_name', 'verbose_name': '姓名'},
                    {'name': 'the_time', 'verbose_name': '次數'},
                    {'name': 'job_code', 'verbose_name': '職務代號'},
                    {'name': 'job_name', 'verbose_name': '職務名稱'},
                    {'name': 'bpm_number', 'verbose_name': 'BPM單號'},
                    {'name': 'bpm_desc1', 'verbose_name': 'BPM狀態'},
                    {'name': 'bpm_desc2', 'verbose_name': '狀態說明'},
                    {'name': 'report_name', 'verbose_name': '報表名稱'},
                    {'name': 'report_url', 'verbose_name': '報表開啟連結'},
                ],
                "model": None,
                "source_url": reverse_lazy('pdca_master'),
            }
        })

        return context

class TT621(BaseLayoutView):
    template_name = 'skill_pdca/tt621.html'
    title = 'TT621 開發方向探索測試'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class TT626(BaseLayoutView):
    template_name = 'skill_pdca/tt626.html'
    title = 'TT626 多國語言譯測試'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

######工作事項明細表-------------------------------------------------------------------------------------------------------------------ENDING