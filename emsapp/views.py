from django.contrib import messages
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, TemplateView, DetailView, View, FormView
from .models import Department, Employee, PayRoll, Attendance, Leave, Performance, Role
from .forms import DepartmentForm, EmployeeForm, PayRollForm, AttendanceForm, LeaveForm, PerformanceForm, \
    UserEmployeeForm


class DashboardView(TemplateView):
    template_name = "emsapp/dashboard.html"


class ProfileView(DetailView):
    model = Employee
    template_name = "emsapp/profile.html"

    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        if request.user.employee == self.object:
            return super().dispatch(request, *args, **kwargs)
        else:
            messages.warning(request, "Invalid access!")
            return redirect("emsapp:dashboard")


class RoleListView(ListView):
    model = Role
    template_name = 'emsapp/role_list.html'


class RoleCreateView(CreateView):
    model = Role
    template_name = 'emsapp/role_form.html'
    fields = ['name', 'is_active']

    def get_success_url(self):
        messages.success(self.request, 'Role successfully created.')
        return reverse("emsapp:role_list")


class RoleUpdateView(UpdateView):
    model = Role
    template_name = 'emsapp/role_form.html'
    fields = ['name', 'is_active']

    def get_success_url(self):
        messages.success(self.request, 'Role successfully updated.')
        return reverse("emsapp:role_list")


class RoleDeleteView(DeleteView):
    model = Role
    template_name = "utils/delete_confirmation.html"

    def get_success_url(self):
        messages.success(self.request, 'Role successfully deleted.')
        return reverse("emsapp:role_list")


class DepartmentListView(ListView):
    model = Department
    template_name = 'emsapp/department_list.html'
    context_object_name = 'departments'


class DepartmentCreateView(CreateView):
    model = Department
    form_class = DepartmentForm
    template_name = 'emsapp/department_form.html'

    def get_success_url(self):
        messages.success(self.request, 'Department successfully created.')
        return reverse("emsapp:department_list")


class DepartmentUpdateView(UpdateView):
    model = Department
    form_class = DepartmentForm
    template_name = 'emsapp/department_form.html'

    def get_success_url(self):
        messages.success(self.request, 'Department successfully updated.')
        return reverse("emsapp:department_list")


class DepartmentDeleteView(DeleteView):
    model = Department
    template_name = 'utils/delete_confirmation.html'

    def get_success_url(self):
        messages.success(self.request, 'Department successfully deleted!')
        return reverse("emsapp:department_list")


class UserListView(ListView):
    model = User
    template_name = 'emsapp/user_list.html'


class UserEmployeeCreateView(FormView):
    form_class = UserEmployeeForm
    template_name = 'emsapp/employee_form.html'

    def form_valid(self, form):
        username = form.cleaned_data.get('username')
        if User.objects.filter(username=username).exists():
            form.errors['username'] = ['Username already registered.']
            return self.form_invalid(form)
        email = form.cleaned_data.get('email')
        first_name = form.cleaned_data.get('first_name')
        last_name = form.cleaned_data.get('last_name')
        password = form.cleaned_data.get('password')
        user_instance = User.objects.create_user(
            username=username, email=email, password=password, first_name=first_name, last_name=last_name
        )
        if user_instance and not Employee.objects.filter(user=user_instance).exists():
            employee_object = form.save(commit=False)
            employee_object.user = user_instance
            employee_object.save()
        else:
            messages.error(self.request, 'This user has already employee profile.')
        return super().form_valid(form)

    def get_success_url(self):
        messages.success(self.request, 'Employee successfully created.')
        return reverse("emsapp:employee_list")


class UserEmployeeUpdateView(UpdateView):
    form_class = UserEmployeeForm
    model = Employee
    template_name = 'emsapp/employee_form.html'

    def form_valid(self, form):
        self.object = self.get_object()
        username = form.cleaned_data.get('username')
        email = form.cleaned_data.get('email')
        first_name = form.cleaned_data.get('first_name')
        last_name = form.cleaned_data.get('last_name')

        user_instance = self.object.user
        if user_instance.username != username:
            if User.objects.filter(username=username).exists():
                form.errors['username'] = ['Username already registered.']
                return self.form_invalid(form)
            else:
                user_instance.username = username
        user_instance.email = email
        user_instance.first_name = first_name
        user_instance.last_name = last_name
        user_instance.save()
        return super().form_valid(form)

    def get_success_url(self):
        messages.success(self.request, 'Employee successfully updated.')
        return reverse("emsapp:employee_list")


class EmployeeListView(ListView):
    model = Employee
    template_name = 'emsapp/employee_list.html'
    context_object_name = 'employees'

    def get_queryset(self):
        queryset = super().get_queryset()
        name = self.request.GET.get('name')
        email = self.request.GET.get('email')
        mobile_no = self.request.GET.get('mobile_no')
        if name:
            queryset = queryset.filter(user__first_name__icontains=name)

        if email:
            queryset = queryset.filter(user__email__icontains=email)

        if mobile_no:
            queryset = queryset.filter(mobile_no__icontains=mobile_no)
        return queryset


class EmployeeDetailView(DetailView):
    model = Employee
    template_name = 'emsapp/employee_detail.html'


class EmployeeDeleteView(DeleteView):
    model = Employee
    template_name = 'utils/delete_confirmation.html'

    def form_valid(self, form):
        object = self.get_object()
        object.user.delete()
        return super().form_valid(form)

    def get_success_url(self):
        messages.success(self.request, 'Employee successfully deleted!')
        return reverse("emsapp:employee_list")


class PayRollListView(ListView):
    model = PayRoll
    template_name = 'emsapp/payroll_list.html'


class PayRollCreateView(CreateView):
    model = PayRoll
    form_class = PayRollForm
    template_name = 'emsapp/payroll_form.html'

    def get_success_url(self):
        messages.success(self.request, 'Payroll successfully created.')
        return reverse("emsapp:payroll_list")


class PayRollUpdateView(UpdateView):
    model = PayRoll
    form_class = PayRollForm
    template_name = 'emsapp/payroll_form.html'

    def get_success_url(self):
        messages.success(self.request, 'Payroll successfully updated.')
        return reverse("emsapp:payroll_list")


class PayRollDeleteView(DeleteView):
    model = PayRoll
    template_name = "utils/delete_confirmation.html"

    def get_success_url(self):
        messages.success(self.request, 'Payroll successfully deleted.')
        return reverse("emsapp:payroll_list")


class AttendanceListView(ListView):
    model = Attendance
    template_name = 'emsapp/attendance_list.html'

    def get_queryset(self):
        queryset = super().get_queryset()
        if self.request.user.employee.role.name == "Employee":
            queryset = queryset.filter(employee=self.request.user.employee)
        return queryset


class AttendanceCreateView(CreateView):
    model = Attendance
    form_class = AttendanceForm
    template_name = 'emsapp/attendance_form.html'

    def get_success_url(self):
        messages.success(self.request, 'Attendance successfully created.')
        return reverse("emsapp:attendance_list")


class AttendanceUpdateView(UpdateView):
    model = Attendance
    form_class = AttendanceForm
    template_name = 'emsapp/attendance_form.html'

    def get_success_url(self):
        messages.success(self.request, 'Attendance successfully Updated.')
        return reverse("emsapp:attendance_list")


class AttendanceDeleteView(DeleteView):
    model = Attendance
    template_name = "utils/delete_confirmation.html"

    def get_success_url(self):
        messages.success(self.request, 'Attendance successfully created.')
        return reverse("emsapp:attendance_list")


class LeaveListView(ListView):
    model = Leave
    template_name = 'emsapp/leave_list.html'

    def get_queryset(self):
        queryset = super().get_queryset()
        if self.request.user.employee.role.name == "Employee":
            queryset = queryset.filter(employee=self.request.user.employee)

        name = self.request.GET.get('name')
        email = self.request.GET.get('email')
        from_date = self.request.GET.get('from_date')
        to_date = self.request.GET.get('to_date')

        if name:
            queryset = queryset.filter(employee__user__first_name__icontains=name)

        if email:
            queryset = queryset.filter(employee__user__first_email__icontains=email)

        if from_date and to_date:
            queryset = queryset.filter(from_date=from_date, to_date=to_date)
        return queryset


class LeaveCreateView(CreateView):
    model = Leave
    form_class = LeaveForm
    template_name = 'emsapp/leave_form.html'

    def get_success_url(self):
        messages.success(self.request, 'Successfully added!')
        return reverse("emsapp:leave_list")


class LeaveUpdateView(UpdateView):
    model = Leave
    form_class = LeaveForm
    template_name = 'emsapp/leave_form.html'

    def get_success_url(self):
        messages.success(self.request, 'Successfully Updated!')
        return reverse("emsapp:leave_list")


class LeaveDeleteView(DeleteView):
    model = Leave
    template_name = "utils/delete_confirmation.html"

    def get_success_url(self):
        messages.success(self.request, 'Deleted successfully!')
        return reverse("emsapp:leave_list")


class PerformanceListView(ListView):
    model = Performance
    template_name = 'emsapp/performance_list.html'


class PerformanceCreateView(CreateView):
    model = Performance
    form_class = PerformanceForm
    template_name = 'emsapp/performance_form.html'

    def get_success_url(self):
        messages.success(self.request, 'Performance given successfully!')
        return reverse("emsapp:performance_list")


class PerformanceUpdateView(UpdateView):
    model = Performance
    form_class = PerformanceForm
    template_name = 'emsapp/performance_form.html'

    def get_success_url(self):
        messages.success(self.request, 'Performance updated successfully!')
        return reverse("emsapp:performance_list")


class PerformanceDeleteView(DeleteView):
    model = Performance
    template_name = "utils/delete_confirmation.html"

    def get_success_url(self):
        messages.success(self.request, 'Performance deleted successfully!')
        return reverse("emsapp:performance_list")


# Employee Section

class EMPLeaveListView(ListView):
    model = Leave
    template_name = "emsapp/employee/leave_list.html"
