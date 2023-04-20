
from django.urls import reverse
from django.views.generic import TemplateView
from django.shortcuts import render

from common.forms import (
                      SearchForm,
                      ComplexSearchForm,
                      CustomSearchForm,
                      CustomComplexSearchForm
                          )
from common.context_processors import set_language_code

from common.forms import TopicOfUdcForm,UserDefCodeForm,GoogleLanguageForm

from common.models import (
                            TopicOfUdc,
                            UserDefCode,
                            ProcessOptionsTxtDef,
                            RegActRules,
                            GoogleLanguage
                            )
from django.conf import settings
from django.utils import translation

#定義左邊的menu tree
class BaseLayoutView(TemplateView):
    title = None

    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'system_tree_config': dict(
                source_url=reverse('system_tree')
            ),
            "title": self.title
        })

        return context


#定義Button
class ManipulateBaseView(BaseLayoutView):
    form_class = None
    form_param = {}

    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'new_btn_config': dict(
                text="建立新資料",
                node_id="new_btn",
                css_class="btn btn-sm btn-info"
            ),
            'create_btn_config': dict(
                text="新增",
                node_id="create_btn",
                css_class="btn btn-sm btn-info"
            ),
            'update_btn_config': dict(
                text="儲存更新",
                node_id="update_btn",
                css_class="btn btn-sm btn-info"
            ),
            'delete_btn_config': dict(
                text="刪除",
                node_id="delete_btn",
                css_class="btn btn-sm btn-disabled"
            ),
            'cancel_btn_config': dict(
                text="取消",
                node_id="cancel_btn",
                css_class="btn btn-sm btn-secondary"
            ),
            "form": self.form_class(**self.form_param),
        })

        return context


#定義dialog(及其內部的Button)
class SingleView(ManipulateBaseView):
    main_model = None
    main_fields = []
    main_sort = None

    custom_model = None
    custom_fields = []
    custom_sort = None

    def get_context_data(self, **kwargs):
        pk_name = self.main_model._meta.pk.name
        context = super().get_context_data(**kwargs)
        context.update({
            "main_dg_config": {
                'display_fields': self.main_fields,
                'key': pk_name,
                'sort_order': 'desc',
                'model': self.main_model,
                'sort': self.main_sort if self.main_sort else pk_name,
            },
            "mono_search_btn_config": dict(
                text="單一條件搜尋",
                node_id='main_mono_search_btn',
                css_class="btn btn-sm btn-outline-secondary"
            ),
            "complex_search_btn_config": dict(
                text="多條件搜尋",
                node_id="main_cpx_search_btn",
                css_class="btn btn-sm btn-outline-secondary"
            ),
            "mono_search_dlg_config": {
                "form": SearchForm(
                    model_class=self.main_model,
                    display_fields=self.main_fields,
                    ukey='main'
                )
            },
            "complex_search_dlg_config": {
                # 'node_id': 'cpx_search_dlg',
                # 'title': '多條件搜尋',
                'cpx_model': self.main_model,
                'cpx_fields': self.main_fields,
                'cpx_ukey': 'cpx',
            },
            "mono_search_custom_btn_config": dict(
                text="單一條件搜尋",
                node_id='custom_mono_search_btn',
                css_class="btn btn-sm btn-outline-secondary"
            ),
            "complex_search_custom_btn_config": dict(
                text="多條件搜尋",
                node_id="custom_cpx_search_btn",
                css_class="btn btn-sm btn-outline-secondary"
            ),
            "custom_mono_search_dlg_config": {
                "form": CustomSearchForm(
                    model_class=self.custom_model,
                    display_fields=self.custom_fields,
                    ukey='custom'
                )
            },
            "custom_complex_search_dlg_config": {
                'cpx_model': self.custom_model,
                'cpx_fields': self.custom_fields,
                'cpx_ukey': 'c_cpx',
            },
            "column_order": self.main_fields,
            "custom_column_order": self.custom_fields,
        })
        return context


class DoubleView(SingleView):
    detail_model = None
    detail_fields = []
    detail_sort = 'pk'

    def get(self, request, *args, **kwargs):
        self.form_param.update({'user': request.user})
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        pk_name = self.detail_model._meta.pk.name
        context = super().get_context_data(**kwargs)
        context.update({
            "detail_dg_config": {
                'display_fields': self.detail_fields,
                # 'node_id': 'detail_dg',
                'key': pk_name,
                'model': self.detail_model,
                'sort': pk_name if pk_name else self.detail_sort,
                'uneditable': []
            },
        })

        return context


def main(request):
    # factory = 1000
    system_tree_config = dict(
        source_url=reverse('system_tree')
    )
    # locals() 這個內建函數將會回傳一個字典，以區域變數的名稱為鍵(字串形式)，區域變數的值為值
    django_lang_code = set_language_code(request)
    return render(request, 'hrs/main.html', locals())  #common/templates/hrs




class CM002(SingleView):
    main_model = TopicOfUdc
    form_param = {}
    form_class = TopicOfUdcForm
    template_name = 'common/cm002.html'
    title = '員工簡易資料'

    """ GRID 資料 """
    main_fields = [
        'topic_code',
        'topic_name',
        'app_model',
    ]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["main_dg_config"]["source_url"] = '/api/data/topic_of_UDC'
        return context


class CM004(SingleView):
    main_model = UserDefCode
    form_param = {}
    form_class = UserDefCodeForm
    template_name = 'common/cm004.html'
    title = '員工簡易資料'

    """ GRID 資料 """
    main_fields = [
        # 'parent',
        'id',
        'topic_code',
        'udc',
        'desc1',
        'desc2',
    ]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["main_dg_config"]["source_url"] = '/api/data/user_def_code'
        return context


#可用語系設定
class CM006(SingleView):
    main_model = GoogleLanguage
    form_param = {}
    form_class = GoogleLanguageForm
    template_name = 'common/cm006.html'
    title = 'Google語系選擇'

    """ GRID 資料 """
    main_fields = [
        'lang_code',
        'lang_desc',
    ]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["main_dg_config"]["source_url"] = '/api/data/google_language'
        return context
