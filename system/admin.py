from django.contrib import admin

from common.apps import MyModelAdmin
from .models import *


# @admin.register(Category)
# class CategoryAdmin(MyModelAdmin, admin.ModelAdmin):
#     list_display = ('id','name','title','slug','slug_u1','slug_u2','slug_char','slug_char_u1','slug_char_u2','parent_category')
#     list_display_links = ('id','name')
#     list_filter = ('name','title','slug','slug_u1','slug_u2','slug_char','slug_char_u1','slug_char_u2','parent_category')


@admin.register(Module)
class ModuleAdmin(MyModelAdmin,admin.ModelAdmin):
    list_display = ('id','module_name','module_id')
    list_display_links = ('id','module_name')
    # list_editable = ('module_name','module_id')
    list_filter = ('module_name','module_id')
    search_fields = ('module_name','module_id')


@admin.register(Program)
class ProgramAdmin(MyModelAdmin, admin.ModelAdmin):
    list_display = ('enable','module','parent','sequence','program_id','program_name','enable',)
    list_display_links = ('sequence','program_id',)
    # list_editable = ('enable','sequence','module','parent','program_name')
    list_filter = ('enable','sequence','module','parent','program_name')
    ordering = ('enable','module','parent','sequence','program_id','program_name','enable',)
    search_fields = ('enable','module','parent','sequence','program_id','program_name','enable',)


@admin.register(Factory)
class FactoryAdmin(MyModelAdmin, admin.ModelAdmin):
    list_display = ('id','name','code','description','nat',)
    list_display_links = ('id',)
    list_filter =  ('name','code','description','nat',)
    search_fields = ('name','code','description','nat',)


@admin.register(FactoryProgram)
class FactoryProgramAdmin(MyModelAdmin, admin.ModelAdmin):
    list_display = ('factory','program',)
    list_display_links = ('factory',)
    list_filter = ('factory','program',)
    search_fields = ('factory','program',)

@admin.register(User)
class UserAdmin(MyModelAdmin, admin.ModelAdmin):
    list_display = ('username','name','last_login','is_admin_site',)
    list_display_links = ('username',)
    list_filter = ('username','name','last_login','is_admin_site')
    search_fields = ('username','name','last_login','is_admin_site')


@admin.register(FactoryAuth)
class FactoryAuth(MyModelAdmin, admin.ModelAdmin):
    list_display = ('user','factory')
    list_display_links = ('user',)
    list_filter = ('user','factory')
    search_fields = ('user','factory')


@admin.register(ProgramAuth)
class ProgramAuthAdmin(MyModelAdmin,admin.ModelAdmin):
    list_display = ('program','user','create','delete','read','update','read','self_data','all_data')
    list_display_links = ('program',)
    list_filter = ('program','user','create','delete','read','update','read','self_data','all_data')
    search_fields = ('program','user','create','delete','read','update','read','self_data','all_data')