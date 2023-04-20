from django.http import JsonResponse
from django.core.cache import cache
from django.conf import settings
from django.utils import translation

from system.models import Program, Factory
from .models import UserDefCode


#google_translate : 方法1
from googletrans import Translator

#google_translate : 方法2
from django.http import HttpResponse
import os
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "D:/webapps/virtualenv\google-translation-api/google_cloud_key/corded-actor-354708-4d38d67d2016.json"


# TODO: Less Coupling

def system_tree(request):
    factory = request.session['factory']['id']
    # TODO: Less Coupling
    user = request.user
    # 取得樹狀最頂層
    tree_data = cache.get('tree')
    if tree_data:
        return JsonResponse(tree_data, safe=False)
    head = Program.objects.filter(parent=None)
    tree = _get_system_tree(head, factory, user)
    # print("="*150)
    # print(head,factory,user)
    # print(tree)
    # print("="*150)
    # cache.set('tree', tree, 1)       # 將tree緩存在'tree'中, 1秒過期
    # cache.set('tree', tree, 600)       # 將tree緩存在'tree'中, 600秒過期
    # JsonResponse傳遞的data : 必需為dict, 若非dict, safe=false-->JsonResponse會強制轉換為dictT
    return JsonResponse(tree, safe=False)


def _get_system_tree(nodes, factory, user):
    branch = []
    # 樹枝
    for node in nodes:
        # 取出每個節點
        child = node.child.all()
        has_sub_folder = True if len(child) else False

        # 判斷是否有子節點
        # 如果有， 資料夾設定為開啟，並繼續呼叫遞迴函式
        if has_sub_folder:
            children = _get_system_tree(child, factory, user)
            if len(children):
                if (node.enable):        # enable=true....才新增( 可以使用/但不顯示 )
                    leaf = {
                        "id": node.program_id,
                        "text": node.program_name,
                        "state": "open",
                        "children": children,
                    }
                    branch.append(leaf)
        else:
            factory_auth = node.factory.filter(factory_id=factory)
            if len(factory_auth):
                if factory_auth[0].auth.filter(user=user).exists():
                    if (node.enable):      # enable=true....才新增( 可以使用/但不顯示 )
                        leaf = {
                            "id": node.program_id,
                            "text": '%s - %s' % (node.program_id.upper(), node.program_name),
                            "attributes": {
                                "url": node.url(),
                                "code": node.program_id,
                                # 寫在 Program Model
                            },
                        }
                        branch.append(leaf)
    return branch


def _set(request):
    factory = str(request.POST.get('factory'))
    request.session['factory'] = Factory.objects.get(id=factory).to_dict()
    # TODO: Less Coupling
    cache.clear()
    return JsonResponse({'status': 200, 'success': True})


# def set_language_code(request):
#     factory = str(request.POST.get('factory'))
#     request.session['factory'] = Factory.objects.get(id=factory).to_dict()
#     # TODO: Less Coupling
#     cache.clear()
#     return JsonResponse({'status': 200, 'success': True})


def set_language_code(request):
    settings.LANGUAGE_CODE = 'vi'
    translation.activate('vi')
    print("\n"*5)
    print("*"*230)
    print("-"*230)
    print(request)
    print('vi')
    print("="*230)
    print("*"*230)
    print("\n"*5)
    return JsonResponse({'status': 200, 'success': True})


