from django.contrib import admin
from django.core import serializers
from django.http import HttpResponse
from django.contrib.contenttypes.models import ContentType
from django.contrib.messages import constants as messages
from django.http import HttpResponseRedirect
from django.utils.translation import ngettext,gettext_lazy as _

from .models import *
from .apps import MyModelAdmin


# 增加『動作』: 動作是指新增、刪除、修改............................begin
def export_as_json(modeladmin, request, queryset):
    response = HttpResponse(content_type="application/json")
    serializers.serialize("json", queryset, stream=response)
    return response


def export_selected_objects(modeladmin, request, queryset):
    selected = queryset.values_list('pk', flat=True)
    ct = ContentType.objects.get_for_model(queryset.model)
    return HttpResponseRedirect('/export/?ct=%s&ids=%s' % (
        ct.pk,
        ','.join(str(pk) for pk in selected),
    ))

def make_published(self, request, queryset):
    updated = queryset.update(status='p')
    self.message_user(request, ngettext(
        '%d story was successfully marked as published.',
        '%d stories were successfully marked as published.',
        updated,
    ) % updated, messages.SUCCESS)

admin.site.add_action(export_as_json, _('export as json'))
admin.site.add_action(export_selected_objects, _('export_selected'))
admin.site.add_action(make_published, _('make_published'))
# 增加『動作』: 動作是指新增、刪除、修改............................ending

@admin.register(TopicOfUdc)
class TopicOfUdcAdmin(MyModelAdmin,admin.ModelAdmin):
    list_display = ('topic_code','topic_name','app_model')
    list_display_links = ('topic_code',)
    list_filter = ('topic_code','topic_name','app_model')
    search_fields = ('topic_code','topic_name','app_model')


@admin.register(UserDefCode)
class UserDefCodeAdmin(MyModelAdmin,admin.ModelAdmin):
    list_display = ('id','parent','topic_code','udc','desc1','desc2','shc1','shc1_desc','shc2','shc2_desc','shc3','shc3_desc','description',)
    list_display_links = ('id',)
    list_filter = ('id','parent','topic_code','udc','desc1','desc2','shc1','shc1_desc','shc2','shc2_desc','shc3','shc3_desc','description',)
    search_fields = ('udc','desc1','desc2','shc1','shc1_desc','shc2','shc2_desc','shc3','shc3_desc','description',)


@admin.register(ReportInformation)
class ReportInformationAdmin(MyModelAdmin,admin.ModelAdmin):
    list_display =  ('app_model','view_code','view_name','report_code','report_name','report_version','report_size','report_orientation','report_title','enable_date','disable_date',)
    list_display_links =  ('app_model','view_code','view_name','report_code','report_name','report_version','report_size','report_orientation','report_title','enable_date','disable_date',)
    list_filter = ('app_model','view_code','view_name','report_code','report_name','report_version','report_size','report_orientation','report_title','enable_date','disable_date',)
    search_fields = ('app_model','view_code','view_name','report_code','report_name','report_version','report_size','report_orientation','report_title','enable_date','disable_date',)


@admin.register(ReportSign)
class ReportSignAdmin(MyModelAdmin,admin.ModelAdmin):
    list_display = ('report_info','order_number','sign_title','sign_space',)
    list_display_links = ('report_info','order_number',)
    list_filter = ('report_info','order_number','sign_title','sign_space',)
    search_fields = ('report_info','order_number','sign_title','sign_space',)


@admin.register(ReportSignForeign)
class ReportSignForeignAdmin(MyModelAdmin,admin.ModelAdmin):
    list_display = ('report_sign','lang_code','sign_title','sign_space',)
    list_display_links = ('report_sign','lang_code',)
    list_filter = ('report_sign','lang_code','sign_title','sign_space',)
    search_fields = ('report_sign','lang_code','sign_title','sign_space',)