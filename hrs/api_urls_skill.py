from django.urls import path

from apps import api_skill as sk_api
from apps import api_skill_report as sk_api_r
from apps.skill_pdca import views as sk_view

#app:pdca

urlpatterns = [
    # app:common
    path('data/<str:model>/<str:pk>', sk_api.ModelHandleView.as_view()),
    path('cpx/<str:model>', sk_api.cmpx_search_handle, name="complex_search"),
    path('data/<str:model>', sk_api.ModelHandleView.as_view(), name='model_handler'),
    path('data/<str:model>', sk_api.ModelHandleDistinctView.as_view(), name='model_distinct_handler'),

    # app:人事基本資料
    path('get_employee_data_factory/<str:pk>', sk_api.get_employee_data_factory, name="get_employee_data_factory"),    # 20210708:加入pk, 分公司
    path('get_director_data_factory/<str:pk>', sk_api.get_director_data_factory, name="get_director_data_factory"),    # 20210708:加入pk, 分公司
    path('get_common_udc/<str:pk>', sk_api.get_common_udc, name="get_common_udc"),                                     #20210707取得udc資料 pk:topic_code

    #app:skill
    path('update_session/<int:select_dept>', sk_api.update_session, name="update_session"),    #
    path('update_session_pdca/<str:select_work_code>/<str:select_chi_name>', sk_api.update_session_pdca, name="update_session_pdca"),    #

    path('gen_matrix_master/<str:pk>', sk_api.gen_matrix_master, name="gen_matrix_master"),    #

    path('matrix_score/', sk_api.matrix_score, name="matrix_score"),
    path('matrix_score/<str:pk1>/<str:pk2>', sk_api.matrix_score, name="matrix_score"),

    path('update_tabs_datagrid_rows', sk_api.update_tabs_datagrid_rows.as_view(), name="update_tabs_datagrid_rows"),  # 更新職能評核結果
    path('export_matrix_detail', sk_api.export_matrix_detail.as_view(), name="export_matrix_detail"),  # 技能盤點明細匯出

    path('get_last_job_code/<str:job_code_l2>', sk_api.get_last_job_code, name="get_last_job_code"),
    path('get_last_skill_code/<str:skill_class>', sk_api.get_last_skill_code, name="get_last_skill_code"),
    path('get_job_title_l3', sk_api.get_job_title_l3, name="get_job_title_l3"),
    path('employee_title', sk_api.employee_title, name="employee_title"),

    path('matrix_master_director', sk_api.matrix_master_director, name="matrix_master_director"),
    path('matrix_master_employee', sk_api.matrix_master_employee, name="matrix_master_employee"),
    path('matrix_master_employee/<str:direct_supv>/<str:dept>/<str:year>/<str:month>/<str:bpm>', sk_api.matrix_master_employee, name="matrix_master_employee"),
    path('supv_work_code_title/<str:direct_supv>/<str:dept_udc>', sk_api.supv_work_code_title, name="supv_work_code_title"),
    path('get_work_code_direct_supv/<str:work_code>', sk_api.get_work_code_direct_supv, name="get_work_code_direct_supv"),
    path('pdca_export_data_count/<int:master_id>', sk_api.pdca_export_data_count, name="pdca_export_data_count"),

    path('download_pdf/<str:url>', sk_api.download_pdf, name="download_pdf"),

    path('get_pdca_subs_data', sk_api.get_pdca_subs_data, name="get_pdca_subs_data"),
    path('get_pdca_subs_data/<str:pk1>', sk_api.get_pdca_subs_data, name="get_pdca_subs_data"),

    path('get_job_tiitle_skill_order_number/<str:job_title>', sk_api.get_job_tiitle_skill_order_number, name="get_job_tiitle_skill_order_number"),
    path('valid_employee_title_skill/<str:job_title>', sk_api.valid_employee_title_skill, name="valid_employee_title_skill"),

    path('pdca_detail_import', sk_api.pdca_detail_import, name="pdca_detail_import"),
    path('pdca_master', sk_api.pdca_master, name="pdca_master"),
    path('pdca_detail/<str:job_title>/<str:userId>/<str:add_version>', sk_api.pdca_detail, name="pdca_detail"),
    path('update_tabs_datagrid_rows_pdca', sk_api.update_tabs_datagrid_rows_pdca.as_view(), name="update_tabs_datagrid_rows_pdca"),    # 更新工作事項填寫


    path('set_language_code/<str:choice_language>', sk_api.set_language_code, name="set_language_code"),

    # 報表 : api_skill_report
    path('submit_bpm', sk_api_r.submit_bpm.as_view(), name="submit_bpm"),  # 更新bpm資料
    path('submit_bpm_pdca', sk_api_r.submit_bpm_pdca.as_view(), name="submit_bpm_pdca"),  # 更新bpm資料
]