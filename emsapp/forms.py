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


class UserEmployeeCreateForm(forms.ModelForm):
    username = forms.CharField(max_length=150, required=True)
    email = forms.EmailField(required=True)
    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=30, required=True)
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

    def save(self, commit=True):
        user = User(
            username=self.cleaned_data['username'],
            email=self.cleaned_data['email'],
            first_name=self.cleaned_data['first_name'],
            last_name=self.cleaned_data['last_name'],
        )
        user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()

        employee = super().save(commit=False)
        employee.user = user
        if commit:
            employee.save()

        return user, employee


class UserEmployeeUpdateForm(forms.ModelForm):
    email = forms.EmailField(required=True)
    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=30, required=True)

    class Meta:
        model = Employee
        fields = ['role', 'mobile_no', 'dob', 'position', 'department', 'address', 'is_active']

    def __init__(self, *args, **kwargs):
        self.user_instance = kwargs.pop('user_instance', None)
        super().__init__(*args, **kwargs)
        if self.user_instance:
            self.fields['email'].initial = self.user_instance.email
            self.fields['first_name'].initial = self.user_instance.first_name
            self.fields['last_name'].initial = self.user_instance.last_name

    def save(self, commit=True):
        user = self.user_instance
        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        if commit:
            user.save()

        employee = super().save(commit=False)
        if commit:
            employee.save()

        return user, employee


class EmployeeForm(forms.ModelForm):
    dob = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}), label="Date of birth")

    class Meta:
        model = Employee
        fields = ['user', 'role', 'mobile_no', 'dob', 'position', 'department', 'address']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['role'].empty_label = 'Select Role'
        self.fields['department'].empty_label = 'Select Department'


class UserEmployeeForm(forms.Form):
    user = forms.ModelChoiceField(queryset=User.objects.all(), required=False, widget=forms.HiddenInput())
    username = forms.CharField(max_length=150)
    first_name = forms.CharField(max_length=30)
    last_name = forms.CharField(max_length=30)
    email = forms.EmailField()
    mobile_no = forms.CharField(max_length=100, required=False)

    role = forms.ModelChoiceField(queryset=Role.objects.filter(is_active=True))

    department = forms.ModelChoiceField(queryset=Department.objects.all())
    position = forms.CharField(max_length=100, required=False)
    dob = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}), )
    address = forms.CharField(widget=forms.Textarea, required=False)

    password = forms.CharField(widget=forms.PasswordInput(), required=False)
    is_active = forms.BooleanField(required=False)

    def __init__(self, *args, **kwargs):
        user_instance = kwargs.pop('user_instance', None)
        employee_instance = kwargs.pop('employee_instance', None)
        super().__init__(*args, **kwargs)

        self.fields['role'].empty_label = 'Select Role'
        self.fields['department'].empty_label = 'Select Department'

        if user_instance:
            self.fields['username'].initial = user_instance.username
            self.fields['email'].initial = user_instance.email
            self.fields['first_name'].initial = user_instance.first_name
            self.fields['last_name'].initial = user_instance.last_name

        if employee_instance:
            self.fields['role'].initial = employee_instance.role
            self.fields['mobile_no'].initial = employee_instance.mobile_no
            self.fields['dob'].initial = employee_instance.dob
            self.fields['position'].initial = employee_instance.position
            self.fields['department'].initial = employee_instance.department
            self.fields['address'].initial = employee_instance.address
            self.fields['is_active'].initial = employee_instance.is_active

    def save(self, commit=True):
        user_instance = self.cleaned_data.get('user')
        if not user_instance:
            user_instance = User(
                username=self.cleaned_data['username'],
                email=self.cleaned_data['email'],
                first_name=self.cleaned_data['first_name'],
                last_name=self.cleaned_data['last_name']
            )
            if self.cleaned_data['password']:
                user_instance.set_password(self.cleaned_data['password'])
            if commit:
                user_instance.save()
        else:
            user_instance.username = self.cleaned_data['username']
            user_instance.email = self.cleaned_data['email']
            user_instance.first_name = self.cleaned_data['first_name']
            user_instance.last_name = self.cleaned_data['last_name']
            if self.cleaned_data['password']:
                user_instance.set_password(self.cleaned_data['password'])
            if commit:
                user_instance.save()

        employee_instance = Employee(
            user=user_instance,
            role=self.cleaned_data['role'],
            mobile_no=self.cleaned_data['mobile_no'],
            dob=self.cleaned_data['dob'],
            position=self.cleaned_data['position'],
            department=self.cleaned_data['department'],
            address=self.cleaned_data['address'],
            is_active=self.cleaned_data['is_active']
        )
        if commit:
            employee_instance.save()

        return user_instance, employee_instance


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
        fields = ['employee', 'rating', 'comments']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['employee'].empty_label = 'Select Employee'
