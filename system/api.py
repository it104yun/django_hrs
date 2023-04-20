from django.templatetags.static import static

from django.db.models import F, Q
from django.http import JsonResponse
from django.urls import reverse, reverse_lazy
from django.utils import timezone
from django.views import View
import logging

from apps.kpi.models import *
from apps.kpi.forms import *

from common.views import DoubleView, SingleView
from components.easyui_components import DataGrid
from system.forms import *
from ldap_auth.extensions import ldap_user_info

from .models import (Program,FactoryAuth, FactoryProgram, ProgramAuth,  # model rename
                     User, UserData)

logger = logging.getLogger('debug')
tracer = logging.getLogger('trace')


def program_auth_handle(request, pk=None):
    def _serialize(obj, related=True):
        datas = [
            dict(
                id= o.pk,
                program_id = o.program_id,
                program = o.program.__str__(),
                user_id = o.user_id,
                user = o.user.__str__(),
                create= 'V' if o.create else '',
                delete= 'V' if o.delete else '',
                update= 'V' if o.update else '',
                read= 'V' if o.read else '',
                self_data= 'V' if o.self_data else '',
                all_data= 'V' if o.all_data else '',
            ) for o in obj
        ]
        return datas

    if request.method == 'POST':
        post_param = request.POST
        # factory_id = post_param.get('factory_id')
        user_id = post_param.get('user_id', None)
        program_id = post_param.get('program_id', None)
        data = {k: True if v=='true' else False for k, v in post_param.items()} 
        data.pop('user_id')
        data.pop('program_id')
        # data.pop('program')
        if pk:
            tracer.info('Update program auth')
            data.update({
                'create_time': timezone.now(),
                'creator': request.user.username,
                'change_time': timezone.now(),
                'changer': request.user.username
            })
            try:
                ProgramAuth.objects.filter(pk=pk).update(**data)
            except Exception as e:
                logger.debug(e)
                return JsonResponse({"success": False})
            return JsonResponse({"success": True})
        else:
            tracer.info('Create program auth')
            data['program'] = FactoryProgram.objects.get(pk=program_id)
            data['user'] = User.objects.get(username=user_id)
            data.update({
                'change_time': timezone.now(),
                'changer': request.user.username
            })
            try:
                ProgramAuth.objects.create(**data)
            except Exception as e:
                logger.debug(e)
                return JsonResponse({"success": False})
            else:
                return JsonResponse({"success": True})
    else:
        if pk:
            tracer.info('delete program auth')
            ProgramAuth.objects.filter(pk=pk).delete()
            return JsonResponse({"success": True})
        else:
            tracer.info('get program auth')
            get_param = request.GET
            factory_id = get_param.get('factory_id')
            user_id = get_param.get('user_id', None)
            program_id = get_param.get('program_id', None)
            query = Q(program__factory_id=factory_id)
            if user_id:
                query &= Q(user_id=user_id)
            else:
                query &= Q(program__program_id=program_id)
            data = ProgramAuth.objects.filter(query)
            dict_data = _serialize(data, True)
            return JsonResponse(dict_data, safe=False)


def user_data_handle(request, pk=None):
    if request.method == 'POST':
        post_param = request.POST
        username = post_param.get('username', None)
        name = post_param.get('name', None)
        factories = post_param.getlist('factory[]', [])
        section_manager = post_param.get('section_manager', '')
        director = post_param.get('director', '')
        if pk:
            tracer.info('Update user data')
            user = User.objects.get(username=username)
            # user.name = name     #由ldap抓取, 不得變更
            user.change_time=timezone.now()
            user.changer=request.user.username
            user.save()
            try:
                user_data = user.data
            except:
                UserData.objects.create(
                    user=user,
                    section_manager=section_manager,
                    director=director,
                )
            else:
                user_data.section_manager = section_manager
                user_data.director = director
                user_data.save()
            current_factory_set = set(
                FactoryAuth.objects.values_list('factory__id', flat=True)\
                                   .filter(user=user))
            new_factory_set = set(factories)
            create = new_factory_set - current_factory_set
            delete = current_factory_set - new_factory_set
            bulk = [
                FactoryAuth(
                    user=user, factory_id=id,
                    create_time=timezone.now(),
                    creator=request.user.username,
                    change_time=timezone.now(),
                    changer=request.user.username
                ) for id in create]
            FactoryAuth.objects.bulk_create(bulk)
            FactoryAuth.objects.filter(Q(factory_id__in=delete) & Q(user_id=username)).delete()
        else:
            tracer.info('Create user data')
            result = ldap_user_info(username, 'cn')

            if result:
                name = result['cn'][0].decode('utf8')
                try:
                    user = User.objects.create(
                        username=username, name=name,
                        create_time=timezone.now(),
                        creator=request.user.username,
                        change_time=timezone.now(),
                        changer=request.user.username
                    )
                    UserData.objects.create(
                        user=user,
                        section_manager=section_manager,
                        director=director,
                    )
                except Exception as e:
                    logger.error(e)
                    return JsonResponse({"success": False})
                else:
                    bulk_data = [
                        FactoryAuth(
                            factory_id=factory, user=user,
                            create_time=timezone.now(),
                            creator=request.user.username,
                            change_time=timezone.now(),
                            changer=request.user.username
                        ) for factory in factories]
                    FactoryAuth.objects.bulk_create(bulk_data)
            else:
                return JsonResponse({"success": False, "msg": "錯誤的工號"})
        return JsonResponse({"success": True})
    else:
        if pk:
            tracer.info('Delete user data')
            try:
                User.objects.get(pk=pk).delete()
            except Exception as e:
                logger.debug(e)
                return JsonResponse({"success": False})
            return JsonResponse({"success": True})
        else:
            tracer.info('Get user data')

            users = User.objects.all()
            datas = []

            for user in users:
                try:
                    user_data = user.data
                except:
                    section_manager = ''
                    director = ''
                else:
                    section_manager = user_data.section_manager
                    director = user_data.director
                datas.append({
                    'username': user.username,
                    'name': user.name,
                    'section_manager': section_manager,
                    'director': director,
                    'factories': [factory.factory_id for factory in user.factory.all()]
                })
            return JsonResponse(datas, safe=False)


def program_factory_handler(request, pk=None):
    if request.method == 'POST':
        if pk:
            tracer.info('Update program factory')
            post_param = request.POST
            factory_list = post_param.getlist('factory[]', [])
            try:
                current_factory_set = set(
                    FactoryProgram.objects.values_list('factory__id', flat=True)\
                                          .filter(program_id=pk)
                )
                new_factory_set = set(factory_list)
                create = new_factory_set - current_factory_set
                delete = current_factory_set - new_factory_set
                bulk = [FactoryProgram(program_id=pk, factory_id=id) for id in create]
                FactoryProgram.objects.bulk_create(bulk)
                FactoryProgram.objects.filter(
                    Q(program_id=pk) & Q(factory_id__in=delete)).delete()
            except Exception as e:
                logger.debug(e)
                return JsonResponse({"success": False})
            return JsonResponse({"success": True})
    else:
        tracer.info('Get program factory')
        try:
            programs = Program.objects.filter(child=None)
        except Exception as e:
            logger.debug(e)
            return JsonResponse('')
        else:
            datas = []
            for program in programs:
                datas.append({
                    "program_id": program.program_id,
                    "program_name": program.program_name,
                    "factory": [pf.factory_id for pf in program.factory.all()]
                })
            return JsonResponse(datas, safe=False)


def get_factory_program_id(request,pk1=None,pk2=None):
    if pk2=='ProgramID':
        fieldList = [
            'program_id',
            'program_id__program_name'
        ]
        results = FactoryProgram.objects.values_list(*fieldList).filter(factory_id=pk1).order_by('program_id')
    dataList = []
    for dataTuple in results:
        value_str = dataTuple[0] if dataTuple[0] else ''
        text_str = dataTuple[1] if dataTuple[1] else ''
        dataList.append({
            'value': value_str,
            'text': value_str+" "+text_str,
        })
    return JsonResponse(dataList,safe=False)


def get_factory_auth_user(request,pk1=None):
    fieldList = [
        'user_id',
        'user__name'
    ]
    results = FactoryAuth.objects.values_list(*fieldList).filter(factory_id=pk1).order_by('user_id').distinct('user_id')
    dataList = []
    for dataTuple in results:
        value_str = dataTuple[0] if dataTuple[0] else ''
        text_str = dataTuple[1] if dataTuple[1] else ''
        dataList.append({
            'value': value_str,
            'text': value_str+" "+text_str,
        })
    return JsonResponse(dataList,safe=False)


def get_factorys(request):
    pass
    return