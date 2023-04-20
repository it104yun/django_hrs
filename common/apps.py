from django.apps import AppConfig
from django.contrib.admin import ModelAdmin

class CommonConfig(AppConfig):
    name = 'common'


class MyModelAdmin(ModelAdmin):
    list_per_page = 10
    save_on_top = True
    list_max_show_all = False      # 不顯示『顯示全部』的按紐
    save_on_top = True
    # list_max_show_all = 10

