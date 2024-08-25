from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Div
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from .models import Department, Employee, PayRoll, Attendance, Leave, Performance, Role


class DepartmentForm(forms.ModelForm):
    class Meta:
        model = Department
        fields = ['name', 'description']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class UserEmployeeForm(forms.ModelForm):
    username = forms.CharField(max_length=150, required=True)
    email = forms.EmailField(required=True)
    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=30, required=False)
    dob = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}), label="Date of birth")
    password = forms.CharField(widget=forms.PasswordInput())
    address = forms.CharField(widget=forms.Textarea(attrs={'rows': 2, 'cols': 30}), label="Address")

    class Meta:
        model = Employee
        fields = ['role', 'mobile_no', 'dob', 'position', 'department', 'address', 'is_active']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['role'].empty_label = 'Select Role'
        self.fields['department'].empty_label = 'Select Department'
        if self.instance and self.initial:
            self.fields['username'].initial = self.instance.user.username
            self.fields['email'].initial = self.instance.user.email
            self.fields['first_name'].initial = self.instance.user.first_name
            self.fields['last_name'].initial = self.instance.user.last_name
            self.fields.pop('password')
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Div(
                Div('username', css_class='col-md-6'),
                Div('first_name', css_class='col-md-6'),
                Div('last_name', css_class='col-md-6'),
                Div('email', css_class='col-md-6'),
                Div('mobile_no', css_class='col-md-6'),
                Div('role', css_class='col-md-6'),
                Div('department', css_class='col-md-6'),
                Div('position', css_class='col-md-6'),
                Div('dob', css_class='col-md-6'),
                Div('password', css_class='col-md-6'),
                Div('address', css_class='col-md-12'),
                Div('is_active', css_class='col-md-6'),
                css_class='row',
            ),
        )
        self.helper.form_tag = False
        self.helper.disable_csrf = True


class EmployeeForm(forms.ModelForm):
    dob = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}), label="Date of birth")

    class Meta:
        model = Employee
        fields = ['user', 'role', 'mobile_no', 'dob', 'position', 'department', 'address']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['role'].empty_label = 'Select Role'
        self.fields['department'].empty_label = 'Select Department'


class PayRollForm(forms.ModelForm):
    class Meta:
        model = PayRoll
        fields = ['employee', 'basic_salary', 'bonuses', 'deductions', 'net_salary', 'is_active']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['employee'].empty_label = 'Select Employee'


class AttendanceForm(forms.ModelForm):
    date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}), label="Date")

    class Meta:
        model = Attendance
        fields = ['employee', 'date', 'is_present']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['employee'].empty_label = 'Select Employee'


class LeaveForm(forms.ModelForm):
    LEAVE_TYPE_CHOICES = [
        ('', 'Select Leave Type'),
        ('sick', 'Sick Leave'),
        ('vacation', 'Vacation Leave'),
        ('casual', 'Casual Leave'),
        ('maternity', 'Maternity Leave'),
        ('paternity', 'Paternity Leave'),
    ]

    leave_type = forms.ChoiceField(choices=LEAVE_TYPE_CHOICES, label='Select Leave Type', required=True)
    from_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}), label="From Date")
    to_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}), label="To Date")

    class Meta:
        model = Leave
        fields = ['employee', 'leave_type', 'from_date', 'to_date', 'reason']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['employee'].empty_label = 'Select Employee'


class PerformanceForm(forms.ModelForm):
    class Meta:
        model = Performance
        fields = ['employee', 'rating', 'comments']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['employee'].empty_label = 'Select Employee'
