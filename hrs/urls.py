"""hrs URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.contrib import admin

from django.urls import path,include,re_path
from django.conf.urls.static import static #圖片連結使用
from django.views.decorators.cache import  cache_page          # "i18n" 2022/07/15 ADD
from django.views.i18n import JavaScriptCatalog,JSONCatalog    # "i18n" deliver to JS which can use gettext(),ngettext()2022/07/15 ADD


from common.site import urls
# from common import api as common_api
from common.api import set_language_code
from system.views import LoginView
from ldap_auth.views import LogoutView


urlpatterns = [
    path('admin/', admin.site.urls),
    path('',urls()),
    path('login',LoginView.as_view(),name='login'),
    path('logout',LogoutView.as_view(),name='logout'),
    path('api/',include('hrs.api_urls_kpi')),
    path('sk_api/',include('hrs.api_urls_skill')),
    path('jsi18n/', JavaScriptCatalog.as_view(),name='javascript-catalog'),    # "i18n" deliver to JS which can use gettext(),ngettext() 2022/07/15 ADD
    path('jsi18n/', JavaScriptCatalog.as_view(),name='json-catalog'),          # "i18n" deliver to JS which can use gettext(),ngettext()2022/07/15 ADD
    path('set_language_code',set_language_code, name='set_language_code'),
]

if 'rosetta' in settings.INSTALLED_APPS:
    urlpatterns += [
        re_path('rosetta/', include('rosetta.urls'))
    ]


# 增加圖片連結顯示的路徑(如此才不會有錯誤)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


