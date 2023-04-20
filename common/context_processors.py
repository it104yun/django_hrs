from django.forms.models import model_to_dict
from system.models import Factory, FactoryAuth
from apps.kpi.models import EmployeeInfoEasy
from common.models import UserDefCode,GoogleLanguage
from django.conf import settings
from django.utils import translation



def factory(request):
    director_instance = None
    is_director = None
    eval_class = None
    if request.user.is_anonymous:
        factories = Factory.objects.values('id', 'name').all()
    else:
        factories = FactoryAuth.objects.values('factory__id', 'factory__name')\
                                .filter(user=request.user).distinct()
        try:
            EmployeeInfo = EmployeeInfoEasy.objects.\
                values_list('director','eval_class').get(work_code=request.user.username)    # 找出director_id
        except:
            pass
        else:
            director_instance = EmployeeInfoEasy.objects.get(work_code=EmployeeInfo[0]) if EmployeeInfo[0] else None
            eval_class = UserDefCode.objects.get(id=EmployeeInfo[1]).desc1 if EmployeeInfo[1] else None
            is_director = True if EmployeeInfoEasy.objects.filter(director=request.user.username).count()>0 else False
            # 還要再加上『下屬』做判斷

    all_factory = Factory.objects.all()
    all_lang =  GoogleLanguage.objects.values_list('lang_code').all()
    google_lang = ""
    for x in all_lang:
        google_lang += x[0]+","

    kwargs = {
        'factory': request.session.get('factory', None),
        'factories': factories,
        'all_factory': all_factory,
        # 'all_lang' : google_lang,
        'all_lang' : settings.LANGUAGES,
        'workingYear': request.session.get('workingYear', None),
        'workingMonth': request.session.get('workingMonth', None),
        'workingQuarter': request.session.get('workingQuarter', None),
        'eval_class': eval_class,                          #評核KPI/BSC
        'director': director_instance,
        'is_director': is_director,
        # 'skill_class':skillClassList,                     #app : skill_pdca 技能成熟度"盤點"時使用
    }
    return kwargs



def set_language_code(request):
    # browser_language = request.LANGUAGE_CODE                     #網頁語系(瀏覽器設定的語系), 中文是"zh-hant"
    choice_language = request.session.get('choice_language')       #取得"登入"時, 選擇的語系(system.forms存在session)
    settings.LANGUAGE_CODE = choice_language
    translation.activate(choice_language)
    return choice_language
