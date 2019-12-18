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

from crm.views import teacher,consultant

urlpatterns = [
    #公户
    #path('customer_list', views.customer_list,name='customer'),
    re_path(r'customer_list/', consultant.CustomerList.as_view(),name='customer'),
    # 私户
    #path('my_customer', views.customer_list, name='my_customer'),
    re_path(r'my_customer/', consultant.CustomerList.as_view(),name='my_customer'),
    #增加客户
    # path('customer/add/', views.add_customer, name='add_customer'),
    # path('customer/edit/<int:edit_id>', views.edit_customer, name='edit_customer'),
    #编辑客户
    # re_path(r'customer/edit/(\d+)', views.edit_customer, name='edit_customer')
    path('customer/add/', consultant.customer, name='add_customer'),
    re_path(r'customer/edit/(\d+)', consultant.customer, name='edit_customer'),
    #展示跟进记录
    re_path(r'consult_record_list/(\d+)', consultant.ConsultRecord.as_view(), name='consult_record'),
    #添加跟进记录
    re_path(r'consult_record/add/', consultant.consult_record, name='add_consult_record'),
    # 修改跟进记录
    re_path(r'consult_record/edit/(\d+)', consultant.consult_record, name='edit_consult_record'),
    # 展示报名记录
    re_path(r'enrollment_list/(?P<customer_id>\d+)', consultant.EnrollmentList.as_view(), name='enrollment'),
    # 添加报名记录
    re_path(r'enrollment/add/(?P<customer_id>\d+)', consultant.enrollment, name='add_enrollment'),
    # 编辑报名记录
    re_path(r'enrollment/edit/(?P<edit_id>\d+)', consultant.enrollment, name='edit_enrollment'),

    # 展示班级列表
    re_path(r'class_list/', teacher.ClassList.as_view(), name='class_list'),
    # 添加班级
    re_path(r'class/add/', teacher.classes, name='add_class'),
    # 编辑班级
    re_path(r'class/edit/(\d+)/', teacher.classes, name='edit_class'),
    # 展示某个班级的课程记录
    re_path(r'course_list/(?P<class_id>\d+)', teacher.CourseList.as_view(), name='course_list'),

    # 添加某个班级的课程记录
    re_path(r'course/add/(?P<class_id>\d+)/', teacher.courses, name='add_course'),
    # 编辑某个班级的课程记录
    re_path(r'course/edit/(?P<edit_id>\d+)/', teacher.courses, name='edit_course'),
    # 展示学习记录
    re_path(r'study_record_list/(?P<course_id>\d+)', teacher.study_record, name='study_record_list'),

]
