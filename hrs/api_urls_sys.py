from django.urls import path

import system.api as sapi
from common.api import system_tree, _set



urlpatterns = [
    #app:system data handle
    path('program_auth', sapi.program_auth_handle),
    path('program_auth/<int:pk>', sapi.program_auth_handle),
    path('user_data', sapi.user_data_handle),
    path('user_data/<str:pk>', sapi.user_data_handle),
    path('program_factory', sapi.program_factory_handler),
    path('program_factory/<str:pk>', sapi.program_factory_handler),
    #app:system login's tree
    path('set', _set, name="_set"),
    path('system_tree', system_tree, name="system_tree"),
]
