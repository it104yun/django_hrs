import inspect
import importlib
import logging

from django.apps import apps
from django.db.utils import ProgrammingError
from django.urls import path

from .views import main
from apps.kpi.views import *
from apps.skill_pdca.views import *


# from django.views.i18n import JavaScriptCatalog

debuger = logging.getLogger('debug')



def urls():
    urlpatterns = [
        path('', main, name="main"),
    ]
    try:
        from django.db.migrations.recorder import MigrationRecorder
        MigrationRecorder.Migration.objects.all()
    except ProgrammingError as e:
        pass
    else:
        program_model = apps.get_model('system', 'Program')
        programs = program_model.objects.filter(child=None)
        # 取得最底層的程式(非資料夾的意思)  child:related name
        for pg in programs:
            url = '%s/%s' % (pg.module.module_id, pg.program_id)
            print('%s.views' % pg.module.module_id)
            print(url)
            try:
                root_app = pg.module.module_id
                if (root_app=='system' or root_app=='common'):
                    # from system.views import sy011,sy110,sy120..........
                    module = importlib.import_module('%s.views' % pg.module.module_id)
                else:
                    # from apps.kpi.views import hr01,hr02,hr03......
                    module = importlib.import_module('apps.%s.views' % pg.module.module_id)
                # dynamic import
            except Exception as e:
                print(e)
                print('%s.views' % pg.module.module_id)

            try:
                related_view = getattr(module, pg.program_id.upper())    # view的class名稱, 一律大寫
            except Exception as e:
                print(e)
                pass
            else:
                # view = related_view.as_view() if inspect.isclass(related_view) else related_view
                if inspect.isclass(related_view):
                    view = related_view.as_view()
                else:
                    view = related_view
                # view 為 CBV 或 FBV 有不同方式
                urlpatterns.append(
                    path(url, view, name=pg.program_id)
                )
        return urlpatterns, 'hrs', 'hrs'


# def i18n_javascript(self, request, extra_context=None):
#     """
#     Display the i18n JavaScript that the Django admin requires.
#
#     `extra_context` is unused but present for consistency with the other
#     admin views.
#     """
#     return JavaScriptCatalog.as_view(packages=['django.contrib.admin'])(request)