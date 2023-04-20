from django.contrib import admin

from common.apps import MyModelAdmin
from .models import *


@admin.register(JobTitle)
class JobTitleAdmin(MyModelAdmin, admin.ModelAdmin):
    list_display = ('job_code','job_name','job_desc','level_number','job_parent',)
    list_display_links = ('job_code',)
    list_filter =('job_code','job_name','job_desc','level_number','job_parent',)
    search_fields = ('job_code','job_name','job_desc','level_number','job_parent',)


@admin.register(JobTitleForeign)
class JobTitleForeignAdmin(MyModelAdmin, admin.ModelAdmin):
    list_display = ('job_code','lang_code','job_name',)
    list_display_links = ('job_code',)
    list_filter = ('job_code','lang_code','job_name',)
    search_fields = ('job_code','lang_code','job_name',)


@admin.register(PdcaDefinition)
class PdcaDefinitionAdmin(MyModelAdmin, admin.ModelAdmin):
    list_display = ('order_number','pdca_choice','pdca_desc','enable',)
    list_display_links = ('order_number',)
    list_filter = ('order_number','pdca_choice','pdca_desc','enable',)
    search_fields = ('order_number','pdca_choice','pdca_desc','enable',)


@admin.register(PdcaDefinitionForeign)
class PdcaDefinitionForeignAdmin(MyModelAdmin, admin.ModelAdmin):
    list_display = ('pdca_id','lang_code','pdca_desc',)
    list_display_links = ('pdca_id',)
    list_filter = ('pdca_id','lang_code','pdca_desc',)
    search_fields = ('pdca_id','lang_code','pdca_desc',)


@admin.register(FlowDefinition)
class FlowDefinitionAdmin(MyModelAdmin, admin.ModelAdmin):
    list_display = ('order_number','flow_desc','enable',)
    list_display_links = ('order_number',)
    list_filter = ('order_number','flow_desc','enable',)
    search_fields = ('order_number','flow_desc','enable',)


@admin.register(FlowDefinitionForeign)
class FlowDefinitionForeignAdmin(MyModelAdmin, admin.ModelAdmin):
    list_display = ('flow_id','lang_code','flow_desc',)
    list_display_links = ('flow_id',)
    list_filter = ('flow_id','lang_code','flow_desc',)
    search_fields = ('flow_id','lang_code','flow_desc',)


@admin.register(CycleDefinition)
class CycleDefinitionAdmin(MyModelAdmin, admin.ModelAdmin):
    list_display = ('order_number','cycle_desc','basic','months','enable',)
    list_display_links = ('order_number',)
    list_filter = ('order_number','cycle_desc','basic','months','enable',)
    search_fields = ('order_number','cycle_desc','basic','months','enable',)


@admin.register(CycleDefinitionForeign)
class CycleDefinitionForeignAdmin(MyModelAdmin, admin.ModelAdmin):
    list_display = ('cycle_id','lang_code','cycle_desc',)
    list_display_links = ('cycle_id',)
    list_filter = ('cycle_id','lang_code','cycle_desc',)
    search_fields = ('cycle_id','lang_code','cycle_desc',)