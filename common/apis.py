from django.db import models
from .models import UserDefCode

from django.http import JsonResponse
from django.core.cache import cache

from system.models import Program, Factory
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
    # cache.set('tree', tree, 600)
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
