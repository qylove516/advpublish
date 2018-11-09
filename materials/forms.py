from django import forms
from django.core.exceptions import ValidationError
from materials import models


class RegForm(forms.Form):
    username = forms.CharField(
        max_length=16,
        label="用户名",
        error_messages={
            "max_length": "用户名最长为16位",
            "required": "用户名不能为空"
        },
        widget=forms.TextInput(
            attrs={"class": "form-control"}
        )
    )
    company = forms.CharField(
        max_length=16,
        label="公司",
        error_messages={
            "max_length": "公司最长为16位",
            "required": "公司不能为空"
        },
        widget=forms.TextInput(
            attrs={"class": "form-control"}
        )
    )
    address = forms.CharField(
        max_length=16,
        label="地址",
        error_messages={
            "max_length": "最长为64位",
            "required": "不能为空"
        },
        widget=forms.TextInput(
            attrs={"class": "form-control"}
        )
    )
    password = forms.CharField(
        min_length=6,
        label="密码",
        widget=forms.PasswordInput(
            attrs={"class": "form-control"},
            render_value=True,
        ),
        error_messages={
            "min_length": "密码至少要6位",
            "required": "密码不能为空",
        }
    )
    re_password = forms.CharField(
        min_length=6,
        label="确认密码",
        widget=forms.PasswordInput(
            attrs={"class": "form-control"},
            render_value=True,
        ),
        error_messages={
            "min_length": "确认密码至少要6位",
            "required": "确认密码不能为空",
        }
    )
    email = forms.EmailField(
        label="邮箱",
        widget=forms.EmailInput(
            attrs={"class": "form-control"},
        ),
        error_messages={
            "invalid": "邮箱格式不正确！",
            "required": "邮箱不能为空",
        }
    )
    tel = forms.CharField(
        label="电话",
        widget=forms.TextInput(
            attrs={"class": "form-control"},
        ),
        error_messages={
            "invalid": "格式不正确！",
            "required": "电话不能为空",
        }
    )

    # 重写username字段的局部钩子
    def clean_username(self):
        username = self.cleaned_data.get("username")
        is_exist = models.UserInfo.objects.filter(username=username)
        if is_exist:
            # 表示用户名已注册
            self.add_error("username", ValidationError("用户名已存在"))
        else:
            return username

    def clean_company(self):
        company = self.cleaned_data.get("company")
        return company

    def clean_address(self):
        address = self.cleaned_data.get("address")
        return address

    def clean_tel(self):
        tel = self.cleaned_data.get("tel")
        is_exist = models.UserInfo.objects.filter(username=tel)
        if is_exist:
            # 表示用户名已注册
            self.add_error("tel", ValidationError("电话已存在"))
        else:
            return tel

    # 重写email字段的局部钩子
    def clean_email(self):
        email = self.cleaned_data.get("email")
        is_exist = models.UserInfo.objects.filter(email=email)
        if is_exist:
            # 表示邮箱已注册
            self.add_error("email", ValidationError("邮箱已被注册"))
        else:
            return email

    def clean(self):
        password = self.cleaned_data.get("password")
        re_password = self.cleaned_data.get("re_password")

        if re_password and re_password != password:
            self.add_error("re_password", ValidationError("再次密码不一致！"))
        else:
            return self.cleaned_data
