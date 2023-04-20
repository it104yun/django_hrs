# from django.contrib import admin
# from django.utils.translation import gettext_lazy as _
#
# from .models import *
# from common.apps import MyModelAdmin
#
#
# @admin.register(EmployeeInfo)
# class EmployeeInfoAdmin(MyModelAdmin,admin.ModelAdmin):
#     list_display = (
#         'id_card_num', 'gender_id',
#         'chi_name','eng_name','birth_date','mug_shot',
#         'height', 'weight', 'blood_type', 'marrige_id',
#         'siblings','sons','daughters',
#         'ht_province','ht_city',
#         'reg_postcode','reg_address',
#         'mail_postcode','mail_address',
#         'reg_phone','mail_phone','mobile_phone',
#         'transport1', 'trans1_licnum', 'trans1_exhaust',
#         'transport2', 'trans2_licnum', 'trans2_exhaust',
#         'educ_id', 'major',
#         'work_code', 'card_code','dl_idl',
#         'corp_id','dept_id','director_id','factory_id','pos_id',
#         'arrival_date','insurance_date',
#         'intr_chi_name','intr_ship','intr_dept_id','intr_pos_id',
#         'labor_pension_yn','labor_pension_p','labor_pension_sd', 'labor_pension_ed',
#         'expat_will', 'expat_country',
#         'meals_partner','depend_nums',
#         'legal_case','memo_line')
#
#
#     fieldsets =(
#         (_('Employee base data'),{
#             'fields':(
#                 ('id_card_num', 'gender_id'),
#                 ('chi_name','eng_name','birth_date','mug_shot'),
#                 ('height', 'weight', 'blood_type', 'marrige_id'),
#                 ( 'siblings','sons','daughters'),
#             ),}),
#         (_('Employee communications data'),{
#             'fields':(
#                 ('ht_province','ht_city'),
#                 ('reg_postcode','reg_address'),
#                 ('mail_postcode','mail_address' ),
#                 ('reg_phone','mail_phone','mobile_phone'),
#             ),}),
#         (_('Employee transport data'), {
#             'fields': (
#                 ('transport1', 'trans1_licnum', 'trans1_exhaust'),
#                 ('transport2', 'trans2_licnum', 'trans2_exhaust'),
#             ),}),
#         (_('Employee highest education'),{'fields':('educ_id', 'major'),}),
#         (_('Introducer Information'),{
#             'fields':(
#                 ('intr_chi_name',  'intr_ship'),
#                 ('intr_dept_id', 'intr_pos_id'),
#             ),}),
#         (_('Basic job information'),{
#             'fields':(
#                 ('work_code','card_code', 'dl_idl'),
#                 ('corp_id','dept_id','director_id','factory_id','pos_id'),
#                 ('arrival_date','insurance_date'),
#             ),}),
#         (_('Willingness to mention'),{
#             'fields':(
#                 ('labor_pension_yn','labor_pension_p'),
#                 ('labor_pension_sd', 'labor_pension_ed'),
#             ),}),
#         (_('Willingness to go abroad'), {'fields': (('expat_will', 'expat_country')), }),
#         (_('Others'),{'fields':('meals_partner','depend_nums'),}),
#         (_('Law/Case'),{'fields':('legal_case','memo_line'),}),
#     )
#
#     list_filter = ('chi_name','corp_id','dept_id','factory_id','arrival_date','gender_id','labor_pension_yn')
#
#
# @admin.register(EducBackground)
# class EducBackgroundAdmin(MyModelAdmin,admin.ModelAdmin):
#     list_display = ('id','employee','school_name','educ_sys','major_degree','major_years','major_sd','major_ed','grad_status',)
#     list_display_links = ('id',)
#     # list_editable = ('employee','school_name','educ_sys','major_degree','major_years','major_sd','major_ed','grad_status',)
#     list_filter = ('employee','school_name','educ_sys','major_degree','major_years','major_sd','major_ed','grad_status', )
#
#
# @admin.register(CertificateLicense)
# class CertificateLicenseAdmin(MyModelAdmin,admin.ModelAdmin):
#     list_display = ('id','employee','license_code','license_name','license_sd','license_ed')
#     list_display_links = ('id',)
#     # list_editable = ('employee','license_code','license_name','license_sd','license_ed')
#     list_filter = ('employee','license_code','license_name','license_sd','license_ed')
#
#
# @admin.register(ExpertiseSkill)
# class ExpertiseSkillAdmin(MyModelAdmin,admin.ModelAdmin):
#     list_display = ('id','employee','expert_type','expert_name')
#     list_display_links = ('id',)
#     # list_editable = ('employee','expert_type','expert_name')
#     list_filter = ('employee','expert_type','expert_name')
#
#
# @admin.register(WorkExperience)
# class WorkExperienceAdmin(MyModelAdmin,admin.ModelAdmin):
#     list_display = ('id','employee','comp_name','pos_name','rsn_lvg','salary','employed_sd','employed_ed')
#     list_display_links = ('id',)
#     # list_editable = ('employee','comp_name','pos_name','rsn_lvg','salary','employed_sd','employed_ed')
#     list_filter = ('employee','comp_name','pos_name','rsn_lvg','salary','employed_sd','employed_ed')
#
#
# @admin.register(FamilyStauts)
# class FamilyStauts(MyModelAdmin,admin.ModelAdmin):
#     list_display = ('id','employee','ship','name','status')
#     list_display_links = ('id',)
#     # list_editable = ('employee','ship','name','status')
#     list_filter = ('employee','ship','name','status')
#
#
# @admin.register(Dependent_NHI)
# class Dependent_NHI(MyModelAdmin,admin.ModelAdmin):
#     list_display = ('id','employee','ship','name','birth_date','id_card_num')
#     list_display_links = ('id',)
#     # list_editable = ('employee','ship','name','birth_date','id_card_num')
#     list_filter = ('employee','ship','name','birth_date','id_card_num')
#
#
# @admin.register(EmergencyContact)
# class EmergencyContactAdmin(MyModelAdmin,admin.ModelAdmin):
#     list_display = ('id','employee','ship','name','mail_address','mail_phone','sector','position')
#     list_display_links = ('id',)
#     # list_editable = ('employee','ship','name','mail_address','mail_phone','sector','position')
#     list_filter = ('employee','ship','name','mail_address','mail_phone','sector','position')


