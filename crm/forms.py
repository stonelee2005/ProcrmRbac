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


# 客户form
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