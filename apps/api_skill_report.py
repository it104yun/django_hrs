import os,io
import sysconfig
import logging
import json
import time

from django.conf import settings
from django.shortcuts import redirect,reverse
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect,FileResponse
from django.utils import timezone
from django.views import View
from django.db.models import F, Q
from pyreportjasper import JasperPy
from django.core.exceptions import ObjectDoesNotExist
from django.forms.models import model_to_dict
from django.urls import reverse_lazy

#html 2 pdf 相關
from django.views.generic import TemplateView
from django_pdfkit import PDFView

from apps.kpi.models import EmployeeInfoEasy
from apps.skill_pdca.models  import (
    MatrixMaster,
    MatrixStatus,
    MatrixDetail,
    JobTitle,
    JobSkill,
    JobTitleSkill,
    EmployeeTitle,
    StudyPlan,
)

from apps.skill_pdca.forms import (
                    EmployeeInfoEasyForm,
                    EmployeeMatrixForm,
                    JobTitleForm,
                    JobSkillForm,
                    JobTitleSkillForm,
                    EmployeeTitleForm,
                    StudyPlanForm,
                    MatrixMasterForm,
                    PdcaMaster,
                    # MatrixDetailForm,
                   )



from common.models import UserDefCode
from common.views import SingleView


logger = logging.getLogger('debug')
tracer = logging.getLogger('trace')

current_tz = timezone.get_current_timezone()
now = timezone.now().astimezone(current_tz)


def get_bpm_number(this_app):
    todayStr = timezone.now().astimezone(current_tz).strftime('%Y%m%d')
    if ( this_app == "SKILL"):
        last_number = MatrixStatus.objects.order_by('bpm_number').last()
    elif ( this_app == "PDCA"):
        last_number = PdcaMaster.objects.order_by('bpm_number').last()

    if ( last_number is None):    #資料庫第一筆資料
        next_bpm = 1
    else:
        if (this_app == "SKILL"):
            last_bpm = MatrixStatus.objects.order_by('bpm_number').last().bpm_number
        elif (this_app == "PDCA"):
            last_bpm = PdcaMaster.objects.order_by('bpm_number').last().bpm_number

        last_day = last_bpm[4:12]           #4開始,小於12(4~11)  (4,5,6,7,8,9,10,11-->日期取8位)
        if last_bpm:
            if ( last_day==todayStr ):
                next_bpm = int( last_bpm[12:] ) + 1  #今天bpm已有人送單
            else:                                    #今天bpm第一張單
                next_bpm = 1
        else:
            next_bpm = 1

    if (this_app == "SKILL"):
        prefix_bpm = "SKIL"
    elif (this_app == "PDCA"):
        prefix_bpm = "PDCA"

    bpmNum = ''
    bpmNum = prefix_bpm + todayStr + ("00" + str(next_bpm) if next_bpm < 9
                            else ("0" + str(next_bpm) if next_bpm >= 10 and next_bpm <= 99
                                  else  str(next_bpm)
                                  )
                            )
    return bpmNum


class submit_bpm(View):
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        # time.sleep(15)           #等待前端報表產生後,再執行相關資料的更新
        username = self.request.user.username
        dept_flevel =  self.request.session.get('select_dept', None)
        post_param = request.POST.dict()  # 整個所有物件內容, 是一個key
        data_param1 = dict( list(post_param.items())[0:4] )
        data_param2 = dict( list(post_param.items())[4:] )
        dt = model_to_dict( UserDefCode.objects.get(Q(topic_code_id='bpm_status'),Q(udc='BPM03')), fields=['id','desc1', 'desc2'] )
        url = post_param.get('report_url', None) + '%sreports/pdf/%s' % (settings.MEDIA_URL, post_param.get('report_name', None))
        url = url.replace("media-files","media")      # add 2022/01/10

        qr= Q(work_code__in = EmployeeInfoEasy.objects.filter(direct_supv_id=username,dept_flevel_id=dept_flevel).values_list("work_code",flat=True))    #找出,直接主管=username, 部門=session部門...之所有員工,工號
        subordinate = EmployeeTitle.objects.filter(qr).values_list("work_code",flat=True).order_by('work_code_id').distinct('work_code_id')
        work_codes = ""
        for work_code in subordinate:
            work_codes += work_code+","
        work_codes = work_codes[0:len(work_codes)-1]   #去除最後一個逗號

        try:
            status_instance = MatrixStatus.objects.filter(
                direct_supv=username,
                dept_flevel=dept_flevel,
                year=data_param1.get('year'),
                month=data_param1.get('month'),
            )
        except:
            print("Data creation error")
        else:
            if not status_instance:
                data_param1.update({
                    'creator': username,
                    'changer': username,
                    'bpm_number': get_bpm_number("SKILL"),
                    'bpm_status_desc1': dt.get('desc1'),
                    'direct_supv_id': username,
                    'dept_flevel_id': dept_flevel,
                    'subordinate': work_codes,
                    'report_name':post_param.get('report_name', None),
                    'report_url': url,
                })
                status_instance = MatrixStatus.objects.create(**data_param1)
                id = [  val for key,val in data_param2.items() ]
                master_instance = MatrixMaster.objects.filter(id__in=id)
                master_instance.update(bpm_id=status_instance)
                return JsonResponse({"success": True})
            else:
                id = [val for key, val in data_param2.items()]
                msg_true = 0
                for item in id:
                    master_instance = MatrixMaster.objects.get(id=item).bpm
                    if master_instance==None:             # BPM重送:若有增加下屬名單,補bpm_number
                        master_instance = MatrixMaster.objects.filter(id=item)
                        master_instance.update(bpm_id=status_instance[0])
                        msg_true += 1
                bpm_status = MatrixStatus.objects.get(
                    direct_supv=username,
                    dept_flevel=dept_flevel,
                    year=data_param1.get('year'),
                    month=data_param1.get('month'),
                ).bpm_status_desc1
                if (bpm_status=='reject'):
                    print(item,"退回的BPM, 將再送出")
                    data_param1.update({
                        'creator': username,
                        'changer': username,
                        'change_time':now,
                        'bpm_status_desc1': dt.get('desc1'),
                        'report_name': post_param.get('report_name', None),
                        'report_url': url,
                    })
                    try:
                        status_instance.update(**data_param1)
                        return JsonResponse({"success": True})
                    except:
                        print("BPM retransmission failed")
                        return JsonResponse({"success": False})
                else:
                    return JsonResponse({"success": False})
                    print("BPM number already exists")



                # if msg_true>0:     # 大於0 : 表示有更新存在
                #     return JsonResponse({"success": True})
                # else:               # 等於0 : 表示沒有更新存在
                #     return JsonResponse({"success": False})


class submit_bpm_pdca(View):
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        username = self.request.user.username
        select_work_code = self.request.session.get('select_work_code', None)                        #20220616加入
        update_work_code = username if select_work_code==username else select_work_code              #20220616加入
        post_to_dict = request.POST.dict()  # 整個所有物件內容, 是一個key
        print("\n"*2)
        print("="*200)
        print(select_work_code==username,"username=",username,"select_work_code=",select_work_code,"update_work_code=",update_work_code,)
        print("*"*200)
        for key_string in post_to_dict:
            post_param = json.loads(key_string)
        dt = model_to_dict( UserDefCode.objects.get(Q(topic_code_id='bpm_status'),Q(udc='BPM03')), fields=['id','desc1', 'desc2'] )
        url = post_param.get('report_url', None) + '%sreports/pdf/%s' % (settings.MEDIA_URL, post_param.get('report_name', None))
        url = url.replace("media-files", "media")  # add 2022/01/10

        try:
            instance = PdcaMaster.objects.filter(
                # work_code=username,
                work_code=update_work_code,              #20220616修改
                the_time=post_param.get('the_time'),
                job_title__in=post_param.get('job_titles'),
            )
            print("*" * 5, "PdcaMaster filter 資料",instance, "*" * 5)
            print()
            print("the_time=",post_param.get('the_time'),"job_titles=",post_param.get('job_titles'))
            print("\n" * 2)
        except:
            print("*"*5,"PdcaMaster查無資料","*"*5)
        else:
            job_titles = post_param.get('job_titles')
            data_param = {
                'change_time':now,
                'changer':request.user.username,
                # 'create_time':now,
                'creator':request.user.username,
                'bpm_number':get_bpm_number("PDCA"),
                'bpm_status_desc1':dt.get('desc1'),
                'report_name':post_param.get('report_name', None),
                'report_url':url
            }
            try:
                instance.update(**data_param)
                return JsonResponse({"success": True})
            except:
                print("*" * 5, "PdcaMaster更新失敗", "*" * 5)
                return JsonResponse({"success": False})

