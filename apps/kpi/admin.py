from django.contrib import admin

from .models import *
from  common.models import *
from common.apps import MyModelAdmin

# @admin.register(EmployeeInfoEasy)
# class EmployeeInfoEasyAdmin(MyModelAdmin,admin.ModelAdmin):
#     list_display = ('work_code','chi_name','corp','dept','pos','director','arrival_date','resign_date')
#     list_display_links = ('work_code',)
#     list_filter = ('work_code','chi_name','corp','dept','pos','director','arrival_date','resign_date')


# @admin.register(MetricsSetup)
# class MetricsSetupAdmin(MyModelAdmin,admin.ModelAdmin):
#     list_display = ('work_code','metrics_type','metrics_content','allocation')
#     list_display_links = ('work_code',)
#     list_filter =  ('work_code','metrics_type','metrics_content','allocation')
#
#
# @admin.register(MetricsCalc)
# class MetricsCalcAdmin(MyModelAdmin,admin.ModelAdmin):
#     list_display = ('metrics','calc_content','score')
#     list_display_links = ('metrics',)
#     list_filter = ('metrics','calc_content','score')


