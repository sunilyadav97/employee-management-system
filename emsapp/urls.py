from django.urls import path
from .views import (
    DepartmentListView, DepartmentCreateView, DepartmentUpdateView, DepartmentDeleteView,
    EmployeeListView, EmployeeCreateView, EmployeeUpdateView, EmployeeDeleteView,
    PayRollListView, PayRollCreateView, PayRollUpdateView, PayRollDeleteView,
    AttendanceListView, AttendanceCreateView, AttendanceUpdateView, AttendanceDeleteView,
    LeaveListView, LeaveCreateView, LeaveUpdateView, LeaveDeleteView,
    PerformanceListView, PerformanceCreateView, PerformanceUpdateView, PerformanceDeleteView, DashboardView
)
app_name = "emsapp"
urlpatterns = [
    path("", DashboardView.as_view(), name="dashboard"),
    path('departments/', DepartmentListView.as_view(), name='department_list'),
    path('departments/new/', DepartmentCreateView.as_view(), name='department_create'),
    path('departments/<int:pk>/edit/', DepartmentUpdateView.as_view(), name='department_update'),
    path('departments/<int:pk>/delete/', DepartmentDeleteView.as_view(), name='department_delete'),

    path('employees/', EmployeeListView.as_view(), name='employee_list'),
    path('employees/new/', EmployeeCreateView.as_view(), name='employee_create'),
    path('employees/<int:pk>/edit/', EmployeeUpdateView.as_view(), name='employee_update'),
    path('employees/<int:pk>/delete/', EmployeeDeleteView.as_view(), name='employee_delete'),

    path('payrolls/', PayRollListView.as_view(), name='payroll_list'),
    path('payrolls/new/', PayRollCreateView.as_view(), name='payroll_create'),
    path('payrolls/<int:pk>/edit/', PayRollUpdateView.as_view(), name='payroll_update'),
    path('payrolls/<int:pk>/delete/', PayRollDeleteView.as_view(), name='payroll_delete'),

    path('attendances/', AttendanceListView.as_view(), name='attendance_list'),
]