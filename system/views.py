from django.shortcuts import render,redirect,HttpResponseRedirect
from django.http import HttpResponseForbidden, HttpResponseServerError
from django.core.cache import cache
from django.db.models import F

from components.views import SingleView
from system.forms import *
from system.urls import *

from .models import (Factory, ProgramAuth, User)
from apps.kpi.models import WorkingYM
from ldap_auth.views import LoginView as AuthLoginView
from django.conf import settings

from common.site import urls
from django.urls import path,include,re_path
from common.context_processors import set_language_code


class SY110(SingleView):
    main_model = User
    form_param = {}
    form_class = UserDataForm
    template_name = 'system/sy110.html'
    title = '使用者資料管理'

    main_fields = [
          'username',
          'name',
    ]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["main_dg_config"]["source_url"] = '/api/user_data'
        return context


class SY120(SingleView):
    main_model = ProgramAuth
    form_param = {}
    form_class = ProgramUserForm
    main_sort = 'user'
    template_name = 'system/sy120.html'
    title = '程式使用權限設定'

    """下面 GRID 資料"""
    main_fields = [
        'user',
        'create',
        'delete',
        'update',
        'read',
        'self_data',
        'all_data'
    ]

    """form 資料"""

    def get(self, request, *args, **kwargs):
        self.form_param.update({'factory': request.session['factory']})
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['all_user'] = list(
            User.objects.filter(factory__factory_id=self.request.session['factory']['id'])\
                        .values(user_id=F('username'), user=F('name'))
        )

        context['main_dg_config']['source_url'] = '/api/program_auth'  # prpcess center's datas...add/del/update/show

        #right side's grid     model : FactoryProgram
        context.update({
            "program_dg_config": {
                "display_fields": [
                    {'name': 'id', 'verbose_name': 'ID'},
                    {'name': 'program_id', 'verbose_name': '程式編號'},
                    {'name': 'program', 'verbose_name': '程式名稱'},
                ],
                "model": None,
                "source_url": reverse_lazy(
                    'model_handler', kwargs={'model': 'factory_program'}),
            }
        })
        return context


class SY130(SingleView):
    main_model = ProgramAuth
    form_param = {}
    form_class = AuthFormUser
    main_sort = 'program'
    template_name = 'system/sy130.html'
    title = '使用者權限設定'

    """GRID 資料"""
    main_fields = [
        'program',
        'create',
        'delete',
        'update',
        'read',
        'self_data',
        'all_data'
    ]

    """form 資料"""
    def get(self, request, *args, **kwargs):
        self.form_param.update({'factory': request.session['factory']})
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        all_programs = Program.objects.filter(factory__factory_id=self.request.session['factory']['id'])\
                                      .values_list('factory__pk', 'program_id','program_name')
        all_program_lst = [dict(program_id=program[0], program=program[1]+" "+program[2]) for program in all_programs]
        context['all_program'] = all_program_lst
        context['main_dg_config']['source_url'] = '/api/program_auth'
        context.update({
            "user_dg_config": {
                "display_fields": [
                    {'name': 'user_id', 'verbose_name':'工號'},
                    {'name': 'user', 'verbose_name':'姓名'},
                ],
                "model": None,
                "source_url": reverse_lazy('model_handler', kwargs={'model': 'factory_auth'}),
            }
        })

        return context


class SY011(SingleView):
    main_model = Program
    form_param = {}
    form_class = ProgramFactoryForm
    template_name = 'system/sy011.html'
    title = '工廠程式設定'

    """ GRID 資料 """
    main_fields = [
          'program_id',
          'program_name',
    ]


    def get_context_data(self , **kwargs):
        context = super().get_context_data(**kwargs)
        context['main_dg_config']['source_url'] = '/api/program_factory'
        return context


class LoginView(AuthLoginView):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        language = settings.LANGUAGES
        language_choices = language[1:len(language)]
        context['choice_language']= language_choices
        return context

    def form_valid(self, form):
        cache.clear()
        factory = form.cleaned_data['factory']
        language = form.cleaned_data['language']
        self.request.session['factory'] = \
            Factory.objects.get(id=factory).to_dict()
        self.request.session['choice_language'] = language

        YM = WorkingYM.objects.values_list('date_yyyy','date_mm').get(id=1)
        self.request.session['workingYear'] = YM[0]
        self.request.session['workingMonth'] = YM[1]
        quarter = int(YM[1]/3)
        self.request.session['workingQuarter'] = 12 if quarter==0 else quarter

        return super().form_valid(form)
