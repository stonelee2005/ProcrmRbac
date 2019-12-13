"""crm URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
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
from django.urls import path, re_path
from django.conf.urls import include, url

from crm import views

urlpatterns = [
    #公户
    #path('customer_list', views.customer_list,name='customer'),
    re_path(r'customer_list/', views.CustomerList.as_view(),name='customer'),
    # 私户
    #path('my_customer', views.customer_list, name='my_customer'),
    re_path(r'my_customer/', views.CustomerList.as_view(),name='my_customer'),
    #增加客户
    # path('customer/add/', views.add_customer, name='add_customer'),
    # path('customer/edit/<int:edit_id>', views.edit_customer, name='edit_customer'),
    #编辑客户
    # re_path(r'customer/edit/(\d+)', views.edit_customer, name='edit_customer')
    path('customer/add/', views.customer, name='add_customer'),
    re_path(r'customer/edit/(\d+)', views.customer, name='edit_customer'),
    #展示跟进记录
    re_path(r'consult_record_list/(\d+)', views.ConsultRecord.as_view(), name='consult_record'),
    #添加跟进记录
    re_path(r'consult_record/add/', views.consult_record, name='add_consult_record'),
    # 修改跟进记录
    re_path(r'consult_record/edit/(\d+)', views.consult_record, name='edit_consult_record'),
    # 展示报名记录
    re_path(r'enrollment_list/(?P<customer_id>\d+)', views.EnrollmentList.as_view(), name='enrollment'),
    # 添加报名记录
    re_path(r'enrollment/add/(?P<customer_id>\d+)', views.enrollment, name='add_enrollment'),
    # 编辑报名记录
    re_path(r'enrollment/edit/(?P<edit_id>\d+)', views.enrollment, name='edit_enrollment'),
]
