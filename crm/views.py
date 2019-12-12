import copy

from django.http import HttpResponse, QueryDict
from django.shortcuts import render, redirect, reverse
from django.contrib import auth
from django.utils.safestring import mark_safe
from django.views import View

from crm import models
from crm.forms import RegForm, CustomerForm, ClassRecordForm
from utils.pagination import Pagination
from django.db.models import Q


# Create your views here.

def login(request):
    err_msg = ''
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        obj = auth.authenticate(request, username=username, password=password)
        if obj:
            auth.login(request, obj)
            return redirect(reverse('my_customer'))
        err_msg = '用户名或密码错误'
    return render(request, 'login.html', {'err_msg': err_msg})


def reg(request):
    form_obj = RegForm()
    if request.method == 'POST':
        form_obj = RegForm(request.POST)
        if form_obj.is_valid():
            # form_obj.cleaned_data.pop('re_password')
            # models.UserProfile.objects.create_user(**form_obj.cleaned_data)
            # return redirect('/login/')
            obj = form_obj.save()
            obj.set_password(obj.password)
            obj.save()
            return redirect('/login/')
    return render(request, 'reg.html', {'form_obj': form_obj})


# 展示客户列表
def customer_list(request):
    print(request.POST)

    if request.path_info == reverse('customer'):
        # 公户
        all_customer = models.Customer.objects.filter(consultant__isnull=True)
    else:
        # 私户
        all_customer = models.Customer.objects.filter(consultant=request.user)

    page = Pagination(request, all_customer.count(), per_num=5)
    return render(request, 'crm/customer_list.html',
                  # {'all_customer': all_customer}
                  {'all_customer': all_customer[page.start:page.end], 'pagination': page.show_li}
                  )


# 展示客户列表CBV
class CustomerList(View):

    def get(self, request):

        q = self.get_search_condition(['qq', 'name', 'class_type'])

        if request.path_info == reverse('customer'):
            # 公户
            all_customer = models.Customer.objects.filter(q, consultant__isnull=True)
        else:
            # 私户
            all_customer = models.Customer.objects.filter(q, consultant=request.user)

        # 分页保留搜索条件
        print(request.GET.urlencode())
        # query_params = copy.deepcopy(request.GET)
        query_params = request.GET.copy()
        # _mutable改为True，就可以修改URL
        # query_params._mutable = True
        # query_params['page']=1

        page = Pagination(request, all_customer.count(), query_params, per_num=2)

        # 生成按钮
        add_btn, query_params = self.get_add_btn()

        return render(request, 'crm/customer_list.html',
                      # {'all_customer': all_customer}
                      {'all_customer': all_customer[page.start:page.end], 'pagination': page.show_li,
                       'add_btn': add_btn, 'query_params': query_params}
                      )

    def post(self, request):
        # 处理Post的action动作
        print(request.POST)
        action = request.POST.get('action')

        if not hasattr(self, action):
            return HttpResponse('非法操作')

        ret = getattr(self, action)()

        if ret:
            return request
        return self.get(request)

    def multi_apply(self):
        # 公户变私户

        ids = self.request.POST.getlist('id')
        # 方法1
        # models.Customer.objects.filter(id__in=ids).update(consultant=self.request.user)

        # 方法2
        self.request.user.customers.add(*models.Customer.objects.filter(id__in=ids))

    def multi_pub(self):
        # 私户变公户
        ids = self.request.POST.getlist('id')
        # 方法1
        # models.Customer.objects.filter(id__in=ids).update(consultant=None)

        # 方法2
        self.request.user.customers.remove(*models.Customer.objects.filter(id__in=ids))

    def get_search_condition(self, query_list):
        print(self.request.GET)
        query = self.request.GET.get('query', '')
        q = Q()
        q.connector = 'OR'
        for i in query_list:
            q.children.append(Q(('{}__contains'.format(i), query)))
        return q

    def get_add_btn(self):
        url = self.request.get_full_path()
        qd = QueryDict()
        qd._mutable = True
        qd['next'] = url
        query_params = qd.urlencode()
        # add_btn='<a href="{}?next={}" class="btn btn-primary btn-sm ">添加</a>'.format(reverse('add_customer'),url)
        add_btn = '<a href="{}?{}" class="btn btn-primary btn-sm ">添加</a>'.format(reverse('add_customer'), query_params)
        print('add_btn', add_btn)
        return mark_safe(add_btn), query_params


class ConsultRecord(View):
    def get(self, request,customer_id):
        if customer_id=='0':
            all_consult_record = models.ConsultRecord.objects.filter(delete_status=False)
        else:
            all_consult_record = models.ConsultRecord.objects.filter(customer_id=customer_id,delete_status=False)
        return render(request, 'crm/consult_record_list.html', {'all_consult_record': all_consult_record})


def add_consult_record(request):
    obj = models.ConsultRecord(consultant=request.user)
    form_obj = ClassRecordForm(instance=obj)

    if request.method == 'POST':
        print('*' * 30)
        form_obj = ClassRecordForm(request.POST)
        if form_obj.is_valid():
            form_obj.save()
            return redirect(reverse('consult_record'))

    return render(request, 'crm/add_consult_record.html', {'form_obj': form_obj})


def edit_consult_record(request, edit_id):
    obj = models.ConsultRecord.objects.filter(id=edit_id).first()
    form_obj = ClassRecordForm(instance=obj)
    if request.method == 'POST':
        print('*' * 30)
        form_obj = ClassRecordForm(request.POST, instance=obj)
        if form_obj.is_valid():
            form_obj.save()
            return redirect(reverse('consult_record',args=(0,)))

    return render(request, 'crm/edit_consult_record.html', {'form_obj': form_obj})

#新增和修改跟进记录
def consult_record(request, edit_id=None):
    obj = models.ConsultRecord.objects.filter(id=edit_id).first() or models.ConsultRecord(consultant=request.user)
    form_obj = ClassRecordForm(instance=obj)
    if request.method == 'POST':
        print('*' * 30)
        form_obj = ClassRecordForm(request.POST, instance=obj)
        if form_obj.is_valid():
            form_obj.save()
            return redirect(reverse('consult_record',args=(0,)))

    return render(request, 'crm/edit_consult_record.html', {'form_obj': form_obj})
# 增加客户
# def add_customer(request):
#     # 实例化一个空的form对象
#     from_obj = CustomerForm()
#     if request.method == 'POST':
#         # 实例化一个提交数据的form
#         form_obj = CustomerForm(request.POST)
#         # 对提交数据进行校验
#         if form_obj.is_valid():
#             # 创建对象
#             form_obj.save()
#             return redirect(reverse('customer'))
#     return render(request, 'crm/add_customer.html', {"from_obj": from_obj})


# 增加客户
def add_customer(request):
    # 实例化一个空的form对象
    form_obj = CustomerForm()
    if request.method == 'POST':
        # 实例化一个带提交数据的form对象
        form_obj = CustomerForm(request.POST)
        # 对提交数据进行校验
        if form_obj.is_valid():
            # 创建对象
            form_obj.save()
            return redirect(reverse('customer'))

    return render(request, 'crm/add_customer.html', {"form_obj": form_obj})


users = [{'name': 'alex{}'.format(i), 'pwd': 'alexsd{}'.format(i)} for i in range(1, 302)]


# def edit_customer(request,edit_id):
#
#     obj = models.Customer.objects.filter(id=edit_id).first()
#     form_obj=CustomerForm(instance=obj)
#     return render(request, 'crm/edit_customer.html', {"form_obj": form_obj})


# 编辑客户
def edit_customer(request, edit_id):
    # 根据ID查出所需要编辑的客户对象
    obj = models.Customer.objects.filter(id=edit_id).first()
    form_obj = CustomerForm(instance=obj)
    if request.method == 'POST':
        # 将提交的数据和要修改的实例交给form对象
        form_obj = CustomerForm(request.POST, instance=obj)
        if form_obj.is_valid():
            form_obj.save()
            return redirect(reverse('customer'))

    return render(request, 'crm/edit_customer.html', {"form_obj": form_obj})


# 整合新增编辑客户
def customer(request, edit_id=None):
    # 根据ID查出所需要编辑的客户对象
    obj = models.Customer.objects.filter(id=edit_id).first()
    form_obj = CustomerForm(instance=obj)
    if request.method == 'POST':
        # 将提交的数据和要修改的实例交给form对象
        form_obj = CustomerForm(request.POST, instance=obj)
        if form_obj.is_valid():
            form_obj.save()
            next = request.GET.get('next')
            if next:
                return redirect(next)
            return redirect(reverse('customer'))

    return render(request, 'crm/customer.html', {"form_obj": form_obj, "edit_id": edit_id})


# 测试分页:分页之封装成类及使用

def user_list(request):
    page = Pagination(request, len(users))
    return render(request, 'user_list.html', {'data': users[page.start:page.end],
                                              # 'total_num': range(page_start, page_end + 1)
                                              'html_str': page.show_li
                                              })
