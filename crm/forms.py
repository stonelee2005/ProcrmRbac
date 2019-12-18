from django import forms
from django.core.exceptions import ValidationError

from crm import models

class BaseForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for filed in self.fields.values():
            filed.widget.attrs.update({'class': 'form-control'})


class RegForm(BaseForm):

    password = forms.CharField(
        label="密码",
        widget=forms.widgets.PasswordInput(),
        min_length=6,
        error_messages={'min_length': '最小长度为6'},
    )

    re_password = forms.CharField(
        label="确认密码",
        widget=forms.widgets.PasswordInput(),
    )

    class Meta:
        model = models.UserProfile
        fields = ['username', 'password', 're_password', 'name', 'department']
        widgets = {
            'username': forms.widgets.EmailInput(attrs={"placeholder": "Email"}),
            'password': forms.widgets.PasswordInput(attrs={"placeholder": "Password"}),

        }

        labels = {
            'username': '用户名',
            'password': '密码',
            'name': '姓名',
            'department': '部门',
        }

        error_messages = {
            'password': {
                'required': '密码不能空',
            }
        }

    def clean(self):
        pwd = self.cleaned_data.get('password')
        re_pwd = self.cleaned_data.get('re_password')

        if pwd == re_pwd:
            return self.cleaned_data
        self.add_error('re_password', '两次密码不一致')
        raise ValidationError('两次秘密不一致')

# 客户form
class CustomerForm(BaseForm):

    class Meta:
        model =  models.Customer
        fields='__all__'
        widgets ={
            'course':forms.widgets.SelectMultiple,
            'birthday':forms.widgets.DateInput
        }


# 跟进记录form
class ClassRecordForm(BaseForm):

    class Meta:
        model =  models.ConsultRecord
        exclude=['delete_status']

        # widgets={
        #     'customer':forms.widgets.Select(choices=((1,'xxx')))
        # }

    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        customer_choices=[ (i.id,i) for i in self.instance.consultant.customers.all()]
        customer_choices.insert(0,('','----------'))
        consultant_choices=[ (self.instance.consultant.id, self.instance.consultant)]
        self.fields['customer'].widget.choices=customer_choices
        self.fields['consultant'].widget.choices = consultant_choices

# 跟进记录form
# class EnrollmentForm(BaseForm):
#
#     class Meta:
#         model =  models.Enrollment
#         exclude=['delete_status','contract_approved']
#
#
#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         # 限制当前的客户只能是传的id对应的客户
#         self.fields['customer'].widget.choices = [(self.instance.customer.id, self.instance.customer), ]
#         # 限制当前可报名班级是当前客户的意向班级
#         self.fields['enrolment_class'].widget.choices= [(i.id,i) for i in self.instance.customer.class_list.all()]


# 报名表Form
class EnrollmentForm(BaseForm):
    class Meta:
        model = models.Enrollment
        exclude = ['delete_status', 'contract_approved']
        labels = {}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for filed in self.fields.values():
            filed.widget.attrs.update({'class': 'form-control'})

        # 限制当前的客户只能是传的id对应的客户
        self.fields['customer'].widget.choices = [(self.instance.customer_id, self.instance.customer), ]
        # 限制当前可报名的班级是当前客户的意向班级
        self.fields['enrolment_class'].widget.choices = [(i.id, i) for i in self.instance.customer.class_list.all()]


#班级Form
class ClassForm(BaseForm):
    forms.DateField(label='日期', )
    class Meta:
        model=models.ClassList
        fields='__all__'

    start_date = forms.DateField(
        label="开班日期",
        widget=forms.DateInput(attrs={'type': 'date'})
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for filed in self.fields.values():
            filed.widget.attrs.update({'class': 'form-control'})

class CourseForm(BaseForm):

    class Meta:
        model=models.CourseRecord
        fields='__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # 限制当前的客户只能是传的id对应的客户
        self.fields['re_class'].widget.choices = [(self.instance.re_class_id, self.instance.re_class)]
        # 限制当前可报名的班级是当前客户的意向班级
        self.fields['teacher'].widget.choices = [(self.instance.teacher_id, self.instance.teacher)]

class StudyRecordForm(BaseForm):

    class Meta:
        model=models.StudyRecord
        fields=['attendance','score','homework_note','student']
