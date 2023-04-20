import os,io
import sysconfig
import logging
import textwrap

from django.conf import settings
from django.shortcuts import redirect,reverse
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect,FileResponse
from django.utils import timezone
from django.views import View
from pyreportjasper import JasperPy
from django.core.exceptions import ObjectDoesNotExist

from common.models import UserDefCode
from apps.kpi.models import (EmployeeInfoEasy,
                             MetricsSetup,
                             MetricsCalc,
                             ScoreSheet,
                             ScoreStatus,
                             ReportQuarter)

from common.models import UserDefCode,ProcessOptionsTxtDef,RegActRules,FileActionLedger

logger = logging.getLogger('debug')
tracer = logging.getLogger('trace')

current_tz = timezone.get_current_timezone()
now = timezone.now().astimezone(current_tz).strftime('%Y-%m-%d %H:%M:%S')


#季度報表
class KPI_ReportQuarterView(View):
    def dispatch(self, request, *args, **kwargs):
        pass
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        get_param = request.GET.dict()
        return redirect('/media-files/reports/pdf/' + get_param.get('fileName',None))

    def post(self, request, *args, **kwargs):
        post_param = request.POST.dict()
        username = request.user.username
        year = post_param.get('date_yyyy', None)
        work_code = post_param.pop('work_code_id', None)
        director = post_param.pop('director_id', None)
        quarter = post_param.pop('date_quarter',None)

        temp_result = kpi_report_quarter_temp(year,quarter,work_code,username,director)     #將要列印的資料,轉成暫存檔,再提供給JasperReport列印

        current_tz = timezone.get_current_timezone()
        now = timezone.now().astimezone(current_tz).strftime('%Y%m%d')
        try:
            if temp_result:
                instance = ScoreStatus.objects.filter(order_type='KPI', work_code_id=work_code, date_yyyy=year,
                                                      quarter=quarter)
                report_id = ScoreStatus.objects.get(order_type='KPI',work_code_id=work_code,date_yyyy=year,quarter=quarter).id
                fileName = post_param.pop('fileName', None)
                report_param = {"score_status_id":str(report_id)}
                print("\n\n")
                print("="*200)
                print(report_param)
                print("="*200)
                print("\n\n")
                outfile = processing( fileName , report_param)
                processing( fileName , report_param)
                fileNamePDF = fileName + ".pdf"
                url = post_param.get('curr_url_prefix',None)+'%sreports/pdf/%s' % (settings.MEDIA_URL,fileNamePDF)

                kpi_diy = EmployeeInfoEasy.objects.get(work_code=work_code).kpi_diy
                bpmNum = set_bpm_number() if kpi_diy else '-'*15
                instance.update(
                    report_name = fileNamePDF ,
                    report_url = url,
                    bpm_number = bpmNum,
                )
                temp_instance = ReportQuarter.objects.filter(order_type='KPI',work_code=work_code,date_yyyy=year,quarter=quarter)
                temp_instance.delete()   #刪除暫存資料
                return JsonResponse({"success": True, "fileName": fileName,'bpm_number':bpmNum})
            else:
                return JsonResponse({"success": False, "err_msg": "重覆『 送至BPM 』\n 請至『PM806季報表送簽狀況查詢』"})
        except ObjectDoesNotExist:
            return JsonResponse({"success": False,"fileName":'...產生報表錯誤...'})


def processing(fileName,report_param):
    base_dir = os.path.dirname(os.path.abspath(__file__)) + "/kpi/"
    db_data = settings.DATABASES['default']
    jdbc_data = settings.DATABASES['report']
    con = {
        'driver': 'generic',
        'jdbc_driver': jdbc_data['CONNECT_STR'],
        'jdbc_url': jdbc_data['URL'] % (db_data['HOST'], db_data['PORT'], db_data['NAME']),
        'jdbc_dir': os.path.join(base_dir + '/static/reports/jar_extension/'),
        'username': db_data['USER'],
        'password': db_data['PASSWORD']
    }

    REPORTS_DIR = base_dir + "static/reports"
    input_file = os.path.join(REPORTS_DIR, "KPI_PM610_ReportQuarter_Landscape.jrxml")
    output_file = '%s/reports/pdf/%s' % (settings.MEDIA_ROOT,fileName)
    jasper = JasperPy()
    message_output=jasper.process(
        input_file,
        output_file,
        locale='zh_TW',
        db_connection=con,
        format_list=["pdf"],
        parameters=report_param,
    )
    print("\n"*2)
    print("="*220)
    print(message_output)
    print("="*220)
    print("\n"*2)
    return  output_file


def set_bpm_number():
    todayStr = timezone.now().astimezone(current_tz).strftime('%Y%m%d')
    if (ScoreStatus.objects.order_by('bpm_number').last() is None):         #資料庫第一筆資料
        next_bpm = 1
    else:
        last_bpm = ScoreStatus.objects.order_by('bpm_number').last().bpm_number
        last_day = last_bpm[3:11]     #3開始，小於11 (3,4,5,6,7,8,9,10-->日期取8位)
        if last_bpm is not None:
            if ( last_day==todayStr ):            #今天bpm已有人送單
                next_bpm = int( last_bpm[11:] ) + 1
            else:                                 #今天bpm第一張單
                next_bpm = 1
        else:
            next_bpm = 1

    bpmNum = 'KPI' + todayStr + ("000" + str(next_bpm) if next_bpm < 9
                            else ("00" + str(next_bpm) if next_bpm >= 10 and next_bpm <= 99
                                  else ("0" + str(next_bpm) if next_bpm >= 100 and next_bpm <= 999
                                        else str(next_bpm)
                                        )
                                  )
                            )
    return bpmNum


def kpi_report_quarter_temp(year,quarter,work_code,username,director):      #寫入暫存檔
    #寫入BPM狀態檔:表頭-----------------------------------------------------------------------------------------------begin
    data = {
        'create_time':now,
        'change_time':now,
        'changer':username,
        'creator':username,
        'order_type':'KPI',
        'work_code_id':work_code,
        'director_id':director if director else '',
        'date_yyyy':year,
        'quarter':quarter,
        'bpm_status':'1_draft',
    }

    try:
        instance = ScoreStatus.objects.get(order_type='KPI',work_code_id=work_code,date_yyyy=year,quarter=quarter)
        create_temp = False
    except ObjectDoesNotExist:
        try:
            instance = ScoreStatus.objects.create(**data)
            create_temp = True
        except Exception as e:
            print("ScoreStatus.objects.create 檔案建立失敗")


    if create_temp:
        # 寫入BPM狀態檔:表頭-----------------------------------------------------------------------------------------------ending
        ee_results = EmployeeInfoEasy.objects.values('chi_name', 'dept_id').get(work_code=work_code)
        chi_name = ee_results.get('chi_name', None)
        dept_id = ee_results.get('dept_id', None)
        dept_desc = UserDefCode.objects.get(id=dept_id).desc1

        metrics_fields = ['work_code',
                          'work_code__chi_name',
                          'work_code__dept',
                          'metrics_type',
                          'metrics_id',
                          'score_type',
                          'order_number',
                          'order_item',
                          'metrics_content',
                          'allocation',
                          'date_yyyy',
                          'date_mm',
                          ]
        calc_fields = ['calc_content','score']
        score_fields = ['actual_score', 'metrics_calc']  # 實績,得分

        #定義1年4個QUARTER分屬那4個月
        if quarter == '1':
            month1,month2,month3 = 1,2,3
        elif quarter == '2':
            month1,month2,month3 = 4,5,6
        elif quarter == '3':
            month1,month2,month3 = 7,8,9
        elif quarter == '4':
            month1,month2,month3 = 10,11,12

        metrics_results = MetricsSetup.objects.values(*metrics_fields).filter(date_yyyy=year, date_mm__range=[month1,month3] , work_code=work_code , order_number__lt=900)

        dataList = []
        idx1 = 0
        idx2 = 0
        idx3 = 0
        count = 0
        last_rec = len(metrics_results)
        allocation1_tot = 0
        allocation2_tot = 0
        allocation3_tot = 0
        metrics_calc1_tot = 0
        metrics_calc2_tot = 0
        metrics_calc3_tot = 0
        month1_numbers = 0
        month2_numbers = 0
        month3_numbers = 0         #有衡量指標的月份
        for dt in metrics_results:
            metrics_id = dt.get('metrics_id')
            curr_month = dt.get('date_mm')
            try:
                calc_results = MetricsCalc.objects.values(*calc_fields).filter(metrics_id=metrics_id).order_by('metrics_id','order_number')
                calc_results_tf = True
            except ObjectDoesNotExist:
                calc_results_tf = False
                calc_results = '沒有計算方式'

            try:
                score_results = ScoreSheet.objects.values(*score_fields).get(metrics_id=metrics_id)
                score_results_tf = True
            except ObjectDoesNotExist:
                score_results_tf = False

            allocation = dt.get('allocation',0)
            metrics_calc_X = score_results.get('metrics_calc',0) if score_results_tf else 0
            metrics_calc = 0 if metrics_calc_X is None else metrics_calc_X
            if calc_results_tf:
                xlist = list(calc_results)
                if curr_month == month1:
                    allocation1_tot += allocation
                    metrics_calc1_tot += metrics_calc
                    month1_numbers += 1
                elif curr_month == month2:
                    allocation2_tot += allocation
                    metrics_calc2_tot += metrics_calc
                    month2_numbers += 1
                elif curr_month == month3:
                    allocation3_tot += allocation
                    metrics_calc3_tot += metrics_calc
                    month3_numbers += 1

                idx_m1 = 0
                idx_m2 = 0
                idx_m3 = 0
                for calc_dt in calc_results:
                    calc_content_str =""
                    calc_content_str = calc_dt.get('calc_content')+str(calc_dt.get('score'))+'分'

                    if curr_month==month1:
                        metrics_content_all = "-" if dt.get('metrics_content',None) is None else dt.get('metrics_content')
                        metrics_list = textwrap.wrap(metrics_content_all, width=21)
                        metrics_list_len = len(metrics_list)
                        dataList.append({
                            'order_type': 'KPI',
                            'work_code' : work_code,
                            'chi_name': chi_name,
                            'dept': dept_desc,
                            'metrics_type' : UserDefCode.objects.get(id=dt.get('metrics_type','-')).desc1,
                            'metrics_id' : metrics_id,
                            'score_type' : dt.get('score_type','-'),
                            'order_number' : dt.get('order_number','-'),
                            'order_item' : dt.get('order_item','-'),
                            # 'metrics_content': "" if dt.get('metrics_content') is None else dt.get('metrics_content'),
                            'metrics_content': metrics_list[idx_m1] if idx_m1 < metrics_list_len else "",
                            'date_yyyy' : dt.get('date_yyyy','-'),
                            'quarter' : quarter,

                            'date_mm1':month1,
                            'allocation1': allocation,
                            'calc_content1':calc_content_str,
                            'actual_score1':score_results.get('actual_score',0) if score_results_tf else 0,
                            'metrics_calc1':metrics_calc,
                        })
                        idx_m1 += 1
                    elif curr_month==month2:
                        try:
                            #month1,已有資料, 用update
                            dataList[idx2].update({
                                'date_mm2': month2,
                                'allocation2': allocation,
                                'calc_content2': calc_content_str,
                                'actual_score2': score_results.get('actual_score',0) if score_results_tf else 0,
                                'metrics_calc2': metrics_calc,
                            })
                        except:
                            #month1,沒有資料, 用append
                            metrics_content_all = "-" if dt.get('metrics_content', None) is None else dt.get('metrics_content')
                            metrics_list = textwrap.wrap(metrics_content_all, width=21)
                            metrics_list_len = len(metrics_list)
                            dataList.append({
                                'order_type': 'KPI',
                                'work_code': work_code,
                                'chi_name': chi_name,
                                'dept': dept_desc,
                                'metrics_type': UserDefCode.objects.get(id=dt.get('metrics_type', '-')).desc1,
                                'metrics_id' : metrics_id,
                                'score_type': dt.get('score_type', '-'),
                                'order_number': dt.get('order_number', '-'),
                                'order_item': dt.get('order_item', '-'),
                                # 'metrics_content': "" if dt.get('metrics_content') is None else dt.get('metrics_content'),
                                'metrics_content': metrics_list[idx_m2] if idx_m2 < metrics_list_len else "",
                                'date_yyyy': dt.get('date_yyyy', '-'),
                                'quarter': quarter,

                                'date_mm2': month2,
                                'allocation2': allocation,
                                'calc_content2': calc_content_str,
                                'actual_score2': score_results.get('actual_score',0) if score_results_tf else 0,
                                'metrics_calc2': metrics_calc,
                            })
                        idx_m2 += 1
                        idx2 += 1
                    elif curr_month==month3:
                        try:
                            # month1,month2 已有資料, 用update
                            dataList[idx3].update({
                                'date_mm3': month3,
                                'allocation3': allocation,
                                'calc_content3': calc_content_str,
                                'actual_score3': score_results.get('actual_score',0) if score_results_tf else 0,
                                'metrics_calc3': metrics_calc,
                            })
                        except:
                               # month1,month2 沒有資料, 用append
                               metrics_content_all = "-" if dt.get('metrics_content', None) is None else dt.get('metrics_content')
                               metrics_list = textwrap.wrap(metrics_content_all, width=21)
                               metrics_list_len = len(metrics_list)
                               dataList.append({
                                'order_type': 'KPI',
                                'work_code': work_code,
                                'chi_name': chi_name,
                                'dept': dept_desc,
                                'metrics_type': UserDefCode.objects.get(id=dt.get('metrics_type', None)).desc1,
                                'metrics_id' : metrics_id,
                                'score_type': dt.get('score_type', None),
                                'order_number': dt.get('order_number', None),
                                'order_item': dt.get('order_item', None),
                                # 'metrics_content': "" if dt.get('metrics_content') is None else dt.get('metrics_content'),
                                'metrics_content': metrics_list[idx_m3] if idx_m3 < metrics_list_len else "",
                                'date_yyyy': dt.get('date_yyyy', None),
                                'quarter': quarter,

                                'date_mm3': month3,
                                'allocation3': allocation,
                                'calc_content3': calc_content_str,
                                'actual_score3': score_results.get('actual_score',0) if score_results_tf else 0,
                                'metrics_calc3': metrics_calc,
                            })
                        idx_m3 += 1
                        idx3 += 1


            count += 1
            if (last_rec == count):
                # order_number : 888  report印出出"個人指標"的小計
                # allocation1,2,3-->做累加吧!
                # metrics_calc1,2,3-->做累加吧!
                dataList.append({
                    'order_type': 'KPI',
                    'work_code': work_code,
                    'chi_name': chi_name,
                    'dept': dept_desc,
                    'metrics_type': UserDefCode.objects.get(id=dt.get('metrics_type', '-')).desc1,
                    'metrics_id': metrics_id,
                    'score_type': dt.get('score_type', '-'),
                    'order_number': 888,
                    'order_item': 0,
                    'metrics_content': "",
                    'date_yyyy': dt.get('date_yyyy', '-'),
                    'quarter': quarter,

                    'date_mm1': month1,
                    'date_mm2': month2,
                    'date_mm3': month3,
                    'allocation1_tot': allocation1_tot,
                    'allocation2_tot': allocation2_tot,
                    'allocation3_tot': allocation3_tot,
                    'metrics_calc1_tot': metrics_calc1_tot,
                    'metrics_calc2_tot': metrics_calc2_tot,
                    'metrics_calc3_tot': metrics_calc3_tot,
                })



        metrics_results = MetricsSetup.objects.values(*metrics_fields).filter(date_yyyy=year,date_mm__range=[month1, month3],work_code=work_code, order_number__gt=900)
        dataList900 = []
        idx1 = 0
        idx2 = 0
        idx3 = 0
        count = 0
        last_rec = len(metrics_results)
        allocation1_tot = 0
        allocation2_tot = 0
        allocation3_tot = 0

        metrics_calc1_tot_mon = metrics_calc1_tot
        metrics_calc2_tot_mon = metrics_calc2_tot
        metrics_calc3_tot_mon = metrics_calc3_tot

        metrics_calc1_tot = 0
        metrics_calc2_tot = 0
        metrics_calc3_tot = 0
        for dt in metrics_results:
            metrics_id = dt.get('metrics_id')
            curr_month = dt.get('date_mm')
            try:
                calc_results = MetricsCalc.objects.values(*calc_fields).filter(metrics_id=metrics_id)
                calc_results_tf = True
            except ObjectDoesNotExist:
                calc_results_tf = False
                calc_results = '沒有計算方式'

            try:
                score_results = ScoreSheet.objects.values(*score_fields).get(metrics_id=metrics_id)
                score_results_tf = True
            except ObjectDoesNotExist:
                score_results_tf = False

            allocation = dt.get('allocation',0)
            metrics_calc_X = score_results.get('metrics_calc',0) if score_results_tf else 0
            metrics_calc = 0 if metrics_calc_X == None else metrics_calc_X
            if calc_results_tf:
                xlist = list(calc_results)
                if curr_month == month1:
                    allocation1_tot += allocation
                    metrics_calc1_tot += metrics_calc
                elif curr_month == month2:
                    allocation2_tot += allocation
                    metrics_calc2_tot += metrics_calc
                elif curr_month == month3:
                    allocation3_tot += allocation
                    metrics_calc3_tot += metrics_calc
                idx_m1 = 0
                idx_m2 = 0
                idx_m3 = 0
                for calc_dt in calc_results:
                    calc_content_str = ""
                    calc_content_str = calc_dt.get('calc_content')+str(calc_dt.get('score'))+'分'

                    if curr_month==month1:
                        metrics_content_all = "-" if dt.get('metrics_content',None) is None else dt.get('metrics_content')
                        metrics_list = textwrap.wrap(metrics_content_all, width=21)
                        metrics_list_len = len(metrics_list)
                        dataList900.append({
                            'order_type': 'KPI',
                            'work_code' : work_code,
                            'chi_name': chi_name,
                            'dept': dept_desc,
                            'metrics_type' : UserDefCode.objects.get(id=dt.get('metrics_type',None)).desc1,
                            'metrics_id' : metrics_id,
                            'score_type' : dt.get('score_type',None),
                            'order_number' : dt.get('order_number',None),
                            'order_item' : dt.get('order_item',None),
                            # 'metrics_content' : dt.get('metrics_content',None),
                            'metrics_content' : metrics_list[idx_m1] if idx_m1 < metrics_list_len else "",
                            'date_yyyy' : dt.get('date_yyyy',None),
                            'quarter' : quarter,

                            'date_mm1':month1,
                            'allocation1': allocation,
                            'calc_content1':calc_content_str,
                            'actual_score1':score_results.get('actual_score',0) if score_results_tf else 0,
                            'metrics_calc1':metrics_calc,
                        })
                        idx_m1 += 1
                        idx1 += 1
                    elif curr_month==month2:
                        try:
                            dataList900[idx2].update({
                                'date_mm2': month2,
                                'allocation2': allocation,
                                'calc_content2': calc_content_str,
                                'actual_score2': score_results.get('actual_score',0) if score_results_tf else 0,
                                'metrics_calc2': metrics_calc,
                            })
                        except:
                            metrics_content_all = "-" if dt.get('metrics_content', None) is None else dt.get('metrics_content')
                            metrics_list = textwrap.wrap(metrics_content_all, width=21)
                            metrics_list_len = len(metrics_list)
                            dataList900.append({
                                'order_type': 'KPI',
                                'work_code': work_code,
                                'chi_name': chi_name,
                                'dept': dept_desc,
                                'metrics_type': UserDefCode.objects.get(id=dt.get('metrics_type', None)).desc1,
                                'metrics_id' : metrics_id,
                                'score_type': dt.get('score_type', None),
                                'order_number': dt.get('order_number', None),
                                'order_item': dt.get('order_item', None),
                                # 'metrics_content': dt.get('metrics_content', None),
                                'metrics_content': metrics_list[idx_m2] if idx_m2 < metrics_list_len else "",
                                'date_yyyy': dt.get('date_yyyy', None),
                                'quarter': quarter,

                                'date_mm2': month2,
                                'allocation2': allocation,
                                'calc_content2': calc_content_str,
                                'actual_score2': score_results.get('actual_score',0) if score_results_tf else 0,
                                'metrics_calc2': metrics_calc,
                            })
                        idx_m2 += 1
                        idx2 += 1
                    elif curr_month==month3:
                        try:
                            dataList900[idx3].update({
                                'date_mm3': month3,
                                'allocation3': allocation,
                                'calc_content3': calc_content_str,
                                'actual_score3': score_results.get('actual_score',0) if score_results_tf else 0,
                                'metrics_calc3': metrics_calc,
                            })
                        except:
                            metrics_content_all = "-" if dt.get('metrics_content', None) is None else dt.get(
                                'metrics_content')
                            metrics_list = textwrap.wrap(metrics_content_all, width=21)
                            metrics_list_len = len(metrics_list)
                            dataList900.append({
                                'order_type': 'KPI',
                                'work_code': work_code,
                                'chi_name': chi_name,
                                'dept': dept_desc,
                                'metrics_type': UserDefCode.objects.get(id=dt.get('metrics_type', None)).desc1,
                                'metrics_id' : metrics_id,
                                'score_type': dt.get('score_type', None),
                                'order_number': dt.get('order_number', None),
                                'order_item': dt.get('order_item', None),
                                # 'metrics_content': dt.get('metrics_content', None),
                                'metrics_content': metrics_list[idx_m3] if idx_m3 < metrics_list_len else "",
                                'date_yyyy': dt.get('date_yyyy', None),
                                'quarter': quarter,

                                'date_mm3': month3,
                                'allocation3': allocation,
                                'calc_content3': calc_content_str,
                                'actual_score3': score_results.get('actual_score',0) if score_results_tf else 0,
                                'metrics_calc3': metrics_calc,
                            })
                        idx_m3 += 1
                        idx3 += 1
            count += 1
            if ( last_rec==count):
                # order_number : 999 report印出出"共同指標"的小計
                # allocation1,2,3-->做累加吧!
                # metrics_calc1,2,3-->做累加吧!
                dataList900.append({
                    'order_type': 'KPI',
                    'work_code' : work_code,
                    'chi_name': chi_name,
                    'dept': dept_desc,
                    'metrics_type' : UserDefCode.objects.get(id=dt.get('metrics_type',None)).desc1,
                    'metrics_id' : metrics_id,
                    'score_type' : dt.get('score_type',None),
                    'order_number' : 991,                #共同指標,得分合計
                    'order_item' : 0,
                    'metrics_content' : "",
                    'date_yyyy' : dt.get('date_yyyy',None),
                    'quarter' : quarter,

                    'date_mm1': month1,
                    'date_mm2': month2,
                    'date_mm3': month3,
                    'allocation1_tot': allocation1_tot,
                    'allocation2_tot': allocation2_tot,
                    'allocation3_tot': allocation3_tot,
                    'metrics_calc1_tot': metrics_calc1_tot,
                    'metrics_calc2_tot': metrics_calc2_tot,
                    'metrics_calc3_tot': metrics_calc3_tot,
                })

                metrics_calc1_tot_mon += metrics_calc1_tot
                metrics_calc2_tot_mon += metrics_calc2_tot
                metrics_calc3_tot_mon += metrics_calc3_tot
                if (month1_numbers>0 and month2_numbers>0 and month3_numbers>0):
                    month_numbers = 3
                elif (month1_numbers==0 and month2_numbers>0 and month3_numbers>0) or (month1_numbers>0 and month2_numbers==0 and month3_numbers>0):
                    month_numbers = 2
                elif (month1_numbers==0 and month2_numbers==0 and month3_numbers>0):
                    month_numbers = 1


                mon_avg = ( (metrics_calc1_tot_mon if metrics_calc1_tot_mon!=None else 0)+( metrics_calc2_tot_mon if metrics_calc2_tot_mon!=None else 0) +( metrics_calc3_tot_mon if metrics_calc3_tot_mon!=None else 0) )/month_numbers
                dataList900.append({
                    'order_type': 'KPI',
                    'work_code' : work_code,
                    'chi_name': chi_name,
                    'dept': dept_desc,
                    'metrics_type' : UserDefCode.objects.get(id=dt.get('metrics_type',None)).desc1,
                    'metrics_id' : metrics_id,
                    'score_type' : dt.get('score_type',None),
                    'order_number' : 992,             #當月得分合計
                    'order_item' : 0,
                    'metrics_content' : "",
                    'date_yyyy' : dt.get('date_yyyy',None),
                    'quarter' : quarter,

                    'date_mm1': month1,
                    'date_mm2': month2,
                    'date_mm3': month3,
                    'metrics_calc1_tot': metrics_calc1_tot_mon,
                    'metrics_calc2_tot': metrics_calc2_tot_mon,
                    'metrics_calc3_tot': metrics_calc3_tot_mon,
                    'metrics_calc_avg': mon_avg,
                })
        dataList.extend(dataList900)

        #三季裏, 若有衡量指標的月份, date_mm1/date_mm2/date_mm3 會為『 0月 』
        for dict in dataList:
            index = dataList.index(dict)
            dataList[index].update({
                'date_mm1' : month1,
                'date_mm2' : month2,
                'date_mm3' : month3
            })

        bulk_data = [ReportQuarter(
            change_time=now,
            changer=username,
            create_time=now,
            creator=username,
            score_status= instance,
            order_type = dict.get('order_type',None),
            work_code = dict.get('work_code',None),
            chi_name = dict.get('chi_name',None),
            dept = dict.get('dept',None),
            metrics_type = dict.get('metrics_type',None),
            metrics_id = dict.get('metrics_id',None),
            score_type = dict.get('score_type',None),
            order_number = dict.get('order_number',None),
            order_item = dict.get('order_item',None),
            metrics_content = dict.get('metrics_content',None),
            date_yyyy = dict.get('date_yyyy',None),
            quarter = dict.get('quarter',None),
            # date_mm1  月份1
            date_mm1 = 0 if dict.get('date_mm1',None) is None else dict.get('date_mm1'),
            allocation1 =  0 if dict.get('allocation1', None) is None else dict.get('allocation1'),
            allocation1_tot =  0 if dict.get('allocation1_tot', None) is None else dict.get('allocation1_tot'),
            order_number1 = 0,
            calc_content1 = '' if dict.get('calc_content1',None) is None else dict.get('calc_content1'),
            actual_score1 = 0 if dict.get('actual_score1',None) is None else dict.get('actual_score1'),
            metrics_calc1 = 0 if dict.get('metrics_calc1',None) is None else dict.get('metrics_calc1'),
            metrics_calc1_tot = 0 if dict.get('metrics_calc1_tot',None) is None else dict.get('metrics_calc1_tot'),
            # date_mm2  月份2
            date_mm2 = 0 if dict.get('date_mm2',None) is None else dict.get('date_mm2'),
            allocation2 = 0 if dict.get('allocation2', None) is None else dict.get('allocation2'),
            allocation2_tot = 0 if dict.get('allocation2_tot', None) is None else dict.get('allocation2_tot'),
            order_number2=0,
            calc_content2 = '' if dict.get('calc_content2',None) is None else dict.get('calc_content2'),
            actual_score2 = 0 if dict.get('actual_score2',None) is None else dict.get('actual_score2'),
            metrics_calc2 = 0 if dict.get('metrics_calc2',None) is None else dict.get('metrics_calc2'),
            metrics_calc2_tot = 0 if dict.get('metrics_calc2_tot',None) is None else dict.get('metrics_calc2_tot'),
            # date_mm3  月份3
            date_mm3 = 0 if dict.get('date_mm3',None) is None else dict.get('date_mm3'),
            allocation3 = 0 if dict.get('allocation3',None) is None else dict.get('allocation3'),
            allocation3_tot = 0 if dict.get('allocation3_tot',None) is None else dict.get('allocation3_tot'),
            order_number3=0,
            calc_content3 = '' if dict.get('calc_content3',None) is None else dict.get('calc_content3'),
            actual_score3 = 0 if dict.get('actual_score3',None) is None else dict.get('actual_score3'),
            metrics_calc3 = 0 if dict.get('metrics_calc3',None) is None else dict.get('metrics_calc3'),
            metrics_calc3_tot = 0 if dict.get('metrics_calc3_tot',None) is None else dict.get('metrics_calc3_tot'),
            metrics_calc_avg = 0 if dict.get('metrics_calc_avg',None) is None else dict.get('metrics_calc_avg'),
        ) for dict in dataList]


        try:
            ReportQuarter.objects.bulk_create(bulk_data)
            bulk_create = True
        except:
            bulk_create = False

        return True
    else:
        return False
