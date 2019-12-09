from django import forms
from django.core.exceptions import ValidationError

from crm import models


class RegForm(forms.ModelForm):
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

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for filed in self.fields.values():
            filed.widget.attrs.update({'class': 'form-control'})

    def clean(self):
        pwd = self.cleaned_data.get('password')
        re_pwd = self.cleaned_data.get('re_password')

        if pwd == re_pwd:
            return self.cleaned_data
        self.add_error('re_password', '两次密码不一致')
        raise ValidationError('两次秘密不一致')

# 客户form
class CustomerForm(forms.ModelForm):

    class Meta:
        model =  models.Customer
        fields='__all__'
        widgets ={
            'course':forms.widgets.SelectMultiple,
            'birthday':forms.widgets.DateInput
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for filed in self.fields.values():
            filed.widget.attrs.update({'class': 'form-control'})