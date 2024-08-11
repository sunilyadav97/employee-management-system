from django.contrib import messages
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, TemplateView
from .models import Department, Employee, PayRoll, Attendance, Leave, Performance
from .forms import DepartmentForm, EmployeeForm, PayRollForm, AttendanceForm, LeaveForm, PerformanceForm


class DashboardView(TemplateView):
    template_name = "emsapp/dashboard.html"


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


class EmployeeListView(ListView):
    model = Employee
    template_name = 'emsapp/employee_list.html'
    context_object_name = 'employees'


class EmployeeCreateView(CreateView):
    model = Employee
    form_class = EmployeeForm
    template_name = 'emsapp/employee_form.html'
    success_url = reverse_lazy('employee_list')

    def get_success_url(self):
        messages.success(self.request, 'Employee successfully created.')
        return reverse("emsapp:employee_list")


class EmployeeUpdateView(UpdateView):
    model = Employee
    form_class = EmployeeForm
    template_name = 'emsapp/employee_form.html'

    def get_success_url(self):
        messages.success(self.request, 'Employee successfully updated!')
        return reverse("emsapp:employee_list")


class EmployeeDeleteView(DeleteView):
    model = Employee
    template_name = 'utils/delete_confirmation.html'

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
    context_object_name = 'performances'


class PerformanceCreateView(CreateView):
    model = Performance
    form_class = PerformanceForm
    template_name = 'emsapp/performance_form.html'
    success_url = reverse_lazy('performance_list')


class PerformanceUpdateView(UpdateView):
    model = Performance
    form_class = PerformanceForm
    template_name = 'emsapp/performance_form.html'
    success_url = reverse_lazy('performance_list')


class PerformanceDeleteView(DeleteView):
    model = Performance
    template_name = 'emsapp/performance_confirm_delete.html'
    success_url = reverse_lazy('performance_list')
