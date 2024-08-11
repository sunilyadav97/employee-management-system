from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from .models import Department, Employee, PayRoll, Attendance, Leave, Performance


class DepartmentForm(forms.ModelForm):
    class Meta:
        model = Department
        fields = ['name', 'description']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class EmployeeForm(forms.ModelForm):
    dob = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}), label="Date of birth")

    class Meta:
        model = Employee
        fields = ['user', 'mobile_no', 'dob', 'position', 'department', 'address']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['user'].empty_label = 'Select User'


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
        fields = ['employee', 'date', 'is_present', 'is_active']

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
        fields = ['employee', 'rating', 'comments', 'is_active']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
