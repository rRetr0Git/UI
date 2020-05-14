"""UI URL Configuration

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
from django.contrib import admin
from django.urls import path,re_path
from django.views.generic.base import TemplateView
from backend import views

urlpatterns = [
    # path('admin/', admin.site.urls),
    path(r'admin/', admin.site.urls),
    path(r'demo/', TemplateView.as_view(template_name="index.html")),
    re_path(r'^demo/view1/', TemplateView.as_view(template_name="index.html")),
    re_path(r'^demo/view2/', TemplateView.as_view(template_name="index.html")),
    re_path(r'^api/alert/',views.get_api_alert),
    re_path(r'^api/graph/',views.get_api_graph),
    re_path(r'^api/overview/',views.get_api_overview),
    re_path(r'^api/pe/',views.get_api_pe),
    re_path(r'^api/pe_interface_stats/',views.get_api_pe_interface_stats),
    re_path(r'^api/te_1/',views.get_api_te_1),
    re_path(r'^api/te_if_state/',views.get_api_te_if_state),
    re_path(r'^api/tenant_te_traffic/',views.get_api_tenant_te_traffic),
    re_path(r'^api/top_10_if/',views.get_api_top_10_if),
    re_path(r'^api/traffic/',views.get_api_traffic),
]
