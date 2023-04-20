from django.urls import path

from apps import api_kpi as kapi
from apps import api_kpi_report as kapi_r
import system.api as sapi
from common.api import system_tree, _set



urlpatterns = [
    #app:common
    path('data/<str:model>/<str:pk>', kapi.ModelHandleView.as_view()),
    path('cpx/<str:model>', kapi.cmpx_search_handle, name="complex_search"),
    path('data/<str:model>', kapi.ModelHandleView.as_view(), name='model_handler'),    # context["main_dg_config"]["source_url"] ='/api/data/employee_info_easy'
    path('data/<str:model>', kapi.ModelHandleDistinctView.as_view(), name='model_distinct_handler'),
    #app:kpi
    path('employee_info_easy', kapi.employee_info_easy_handle),
    path('employee_info_easy/<str:pk>', kapi.employee_info_easy_handle),
    # path('ee_attend_details', kapi.ee_attend_details_handle),
    # path('ee_attend_details/<str:pk>', kapi.ee_attend_details_handle),
    # path('ee_attend_summary', kapi.ee_attend_summary_handle),
    # path('ee_attend_summary/<str:pk>', kapi.ee_attend_summary_handle),
    path('metrics_setup', kapi.metrics_setup_handle),
    path('metrics_setup/<str:pk>', kapi.metrics_setup_handle),
    path('metrics_calc', kapi.metrics_calc_handle),
    path('metrics_calc/<str:pk>', kapi.metrics_calc_handle),
    path('score_sheet', kapi.score_sheet_handle),
    path('score_sheet/<str:pk>', kapi.score_sheet_handle),
    ###-----------------------------------------
    path('get_common_udc/<str:pk>', kapi.get_common_udc, name="get_common_udc"),     #20210707取得udc資料 pk:topic_code
    path('get_dept_data_by_factory/<str:pk1>/<str:pk2>', kapi.get_dept_data_by_factory, name="get_dept_data_by_factory"),    #pk1 : udc topic_code   pk2:factory(corp)
    path('get_metrics_calc/<int:pk>', kapi.get_metrics_calc, name="get_metrics_calc"),
    path('get_calc_score/<int:pk>', kapi.get_calc_score, name="get_calc_score"),
    path('get_employee_data/', kapi.get_employee_data, name="get_employee_data"),           #20210225 原人事基本資料複製使用

    path('get_factory_employee_data/<str:pk1>/<str:pk2>', kapi.get_factory_employee_data, name="get_factory_employee_data"),           #20210225 原人事基本資料複製使用

    path('get_employee_data/<str:pk>', kapi.get_employee_data, name="get_employee_data"),   #20210225:加入pk, 主管的工號
    path('get_employee_data_factory', kapi.get_employee_data_factory, name="get_employee_data_factory"),    # 20210804:移除pk公司
    path('get_director_data_factory', kapi.get_director_data_factory, name="get_director_data_factory"),    # 20210804:移除pk公司
    path('get_manager_data/<str:pk>', kapi.get_manager_data, name="get_manager_data"),    # pk : 評核主管/直接主管

    path('get_employee_common_data/', kapi.get_employee_common_data, name="get_employee_common_data"),              #共同指標,choice
    path('get_employee_common_data/<int:pk1>/<int:pk2>', kapi.get_employee_common_data, name="get_employee_common_data"),      #共同指標,choice
    # path('get_employee_data/<str:pk1>/<str:pk2>', kapi.get_employee_data, name="get_employee_data"),   #20210225:加入pk, 主管的工號

    path('get_all_factory', kapi.get_all_factory, name="get_all_factory"),
    path('get_dept_data/<str:pk1>', kapi.get_dept_data, name="get_dept_data"),

    path('get_metrics_setup_data/', kapi.get_metrics_setup_data, name="get_metrics_setup_data"),
    path('get_metrics_setup_data/<str:pk1>/<str:pk2>/<str:pk3>/<str:pk4>', kapi.get_metrics_setup_data, name="get_metrics_setup_data_pk4"),
    path('get_metrics_setup_subs_data', kapi.get_metrics_setup_subs_data, name="get_metrics_setup_subs_data"),                                  #取得下屬的metrics_setup
    path('get_metrics_setup_subs_data/<str:pk1>', kapi.get_metrics_setup_subs_data, name="get_metrics_setup_subs_data"),                        #取得下屬的metrics_setup
    path('get_metrics_setup_subs_data/<str:pk1>/<str:pk2>', kapi.get_metrics_setup_subs_data, name="get_metrics_setup_subs_data"),                        #取得下屬的metrics_setup
    path('get_metrics_setup_common', kapi.get_metrics_setup_common, name="get_metrics_setup_common"),                        #共同指標


    path('get_metrics_setupDate_data', kapi.get_metrics_setupDate_data, name="get_metrics_setupDate_data"),                                     #South Grid with work_code(distinct)
    path('get_metrics_setupDate_data/<str:pk1>', kapi.get_metrics_setupDate_data, name="get_metrics_setupDate_data_pk1"),                       #East Grid with work_code+date_yyyy+date_mm(distinct)
    path('get_metrics_setupDate_data/<str:pk1>/<int:pk2>', kapi.get_metrics_setupDate_data, name="get_metrics_setupDate_data_pk2"),             #承上 search with date_yyyy(西元年)
    path('get_metrics_setupDate_data/<str:pk1>/<int:pk2>/<int:pk3>', kapi.get_metrics_setupDate_data, name="get_metrics_setupDate_data_pk3"),   #個人評核

    path('get_metrics_setupDate_data_search', kapi.get_metrics_setupDate_data_search, name="get_metrics_setupDate_data_search"),   #個人評核
    path('get_metrics_setupDate_data_search/<str:pk1>', kapi.get_metrics_setupDate_data_search, name="get_metrics_setupDate_data_search_pk1"),   #個人評核
    path('get_metrics_setupDate_data_search/<str:pk1>/<int:pk2>', kapi.get_metrics_setupDate_data_search, name="get_metrics_setupDate_data_search_pk2"),   #個人評核
    path('get_metrics_setupDate_data_search/<str:pk1>/<int:pk2>/<int:pk3>', kapi.get_metrics_setupDate_data_search, name="get_metrics_setupDate_data_search_pk3"),   #個人評核

    path('metrics_setup_score_sheet_pm402', kapi.metrics_setup_score_sheet_pm402, name="metrics_setup_score_sheet_pm402"),   #自評
    path('metrics_setup_score_sheet_pm406', kapi.metrics_setup_score_sheet_pm406, name="metrics_setup_score_sheet_pm406"),   #主管審核

    path('set_score_sheet_status/<int:pk1>/<str:pk2>/<str:pk3>', kapi.set_score_sheet_status, name="set_score_sheet_status"),   #個人評核,送出/收回..狀態確認
    path('get_score_sheet_sendmail/<str:pk1>/<int:pk2>/<int:pk3>', kapi.get_score_sheet_sendmail, name="get_score_sheet_sendmail"),   #主管送出評核,mail通知下屬查看
    path('get_score_sheet_sendmail_to_director/<str:pk1>/<int:pk2>/<int:pk3>', kapi.get_score_sheet_sendmail_to_director, name="get_score_sheet_sendmail_to_director"),   #下屬送出評核,mail通知主管查看

    path('get_metrics_order_number/<str:pk1>/<int:pk2>/<int:pk3>', kapi.get_metrics_order_number, name="get_metrics_order_number"),   #取得最後一號
    path('get_metricsCalc_order_number/<int:pk1>', kapi.get_metricsCalc_order_number, name="get_metricsCalc_order_number"),   #取得最後一號
    path('get_metrics_order_item/<str:pk1>/<int:pk2>/<int:pk3>/<int:pk4>', kapi.get_metrics_order_item, name="get_metrics_order_item"),   #取得最後一號

    # path('valid_all_metrics/<str:pk1>/<str:pk2>/<str:pk3>/<str:pk4>',kapi.valid_all_metrics, name="valid_all_metrics"),  # 關帳的檢核
    # <str:pk1>   <int:pk1> : 不論前端傳int or str，這兒是<int:pk1>就是int，這兒是<str:pk1>就是str
    path('valid_all_metrics/<int:pk1>/<int:pk2>/<int:pk3>/<int:pk4>',kapi.valid_all_metrics, name="valid_all_metrics"),  # 關帳的檢核
    path('valid_my_metrics/<str:pk1>/<int:pk2>/<int:pk3>',kapi.valid_my_metrics, name="valid_my_metrics"),          # pm402.js 個人衡量指標的檢核

    ###-----------------------------------------copy,import,expand,validation
    path('employee_export/', kapi.employee_export, name="employee_export"),
    # path('employee_import/', kapi.employee_import, name="employee_import"),
    path('employee_import_update/', kapi.employee_import_update, name="employee_import_update"),
    path('employee_copy/',kapi.EmployeeCopyView.as_view(), name="employee_copy"),
    # path('ee_attend_summary_import/', kapi.ee_attend_summary_import, name="ee_attend_summary_import"),
    path('metrics_setup_copy/',kapi.MetricsSetupCopyView.as_view(), name="metrics_setup_copy"),
    path('metrics_setup_expand/',kapi.MetricsSetupExpandView.as_view(), name="metrics_setup_expand"),
    path('metrics_setup_batch_dele/', kapi.MetricsBatchDeleView.as_view(), name="metrics_setup_batch_dele"),
    path('metrics_setup_expandCommon/', kapi.MetricsSetupExpandCommonView.as_view(), name="metrics_setup_expandCommon"),
    path('metrics_setup_recallCommon/', kapi.MetricsSetupRecallCommonView.as_view(), name="metrics_setup_recallCommon"),
    path('score_sheet_process', kapi.ScoreSheetProcessView.as_view(), name="score_sheet_process"),        #處理實績評核資料

    path('synchronize_hr_employee/', kapi.synchronize_hr_employee, name="synchronize_hr_employee"),
    path('get_add_update_employee_data/<str:pk>', kapi.get_add_update_employee_data, name="get_add_update_employee_data"),

    # path('metrics_setup_distinct_ym/<str:work_code>',kapi.MetricsSetupDistinctYmView.as_view(), name="metrics_setup_distinct_ym"),
    ###-----------------------------------------report
    path('kpi_report_quarter/', kapi_r.KPI_ReportQuarterView.as_view(), name="kpi_report_quarter"),

    # app:system data handle
    path('program_auth', sapi.program_auth_handle),
    path('program_auth/<int:pk>', sapi.program_auth_handle),
    path('user_data', sapi.user_data_handle),
    path('user_data/<str:pk>', sapi.user_data_handle),
    path('program_factory', sapi.program_factory_handler),
    path('program_factory/<str:pk>', sapi.program_factory_handler),
    # sy120,sy130 自建search
    path('get_factory_program_id/<str:pk1>/<str:pk2>', sapi.get_factory_program_id),
    path('get_factory_auth_user/<str:pk1>', sapi.get_factory_auth_user),
    # app:system login's tree
    path('set', _set, name="_set"),
    path('system_tree', system_tree, name="system_tree"),

    # 會議管理系統app url
    # path('http://192.168.5.75/api/score_statistics/<str:uu>/<str:score_type>/<str:year>/<str:month>' , name="score_statistics"),
]
