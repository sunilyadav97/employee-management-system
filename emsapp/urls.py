from django.contrib.auth.decorators import login_required
from django.urls import path
from .views import (
    DepartmentListView, DepartmentCreateView, DepartmentUpdateView, DepartmentDeleteView,
    EmployeeListView, EmployeeDeleteView,
    PayRollListView, PayRollCreateView, PayRollUpdateView, PayRollDeleteView,
    AttendanceListView, AttendanceCreateView, AttendanceUpdateView, AttendanceDeleteView,
    LeaveListView, LeaveCreateView, LeaveUpdateView, LeaveDeleteView,
    PerformanceListView, PerformanceCreateView, PerformanceUpdateView, PerformanceDeleteView, DashboardView,
    RoleListView, RoleCreateView, RoleUpdateView, RoleDeleteView, EmployeeDetailView, UserListView,
    UserEmployeeCreateView, UserEmployeeUpdateView, ProfileView, emp_apply_leave_view
)

app_name = "emsapp"
urlpatterns = [
    path("", login_required(DashboardView.as_view()), name="dashboard"),
    path("profile/<int:pk>/", login_required(ProfileView.as_view()), name="profile"),
    path('roles/', RoleListView.as_view(), name='role_list'),
    path('role/new/', RoleCreateView.as_view(), name='role_create'),
    path('role/<int:pk>/update/', RoleUpdateView.as_view(), name='role_update'),
    path('role/<int:pk>/delete/', RoleDeleteView.as_view(), name='role_delete'),

    path('departments/', login_required(DepartmentListView.as_view()), name='department_list'),
    path('department/new/', login_required(DepartmentCreateView.as_view()), name='department_create'),
    path('department/<int:pk>/edit/', login_required(DepartmentUpdateView.as_view()), name='department_update'),
    path('department/<int:pk>/delete/', login_required(DepartmentDeleteView.as_view()), name='department_delete'),

    path('users/', UserListView.as_view(), name='user_list'),
    path('employee/new/', UserEmployeeCreateView.as_view(), name='employee_create'),
    path('employee/<int:pk>/edit/', UserEmployeeUpdateView.as_view(), name='employee_update'),

    path('employees/', login_required(EmployeeListView.as_view()), name='employee_list'),
    path('employee/<int:pk>/', login_required(EmployeeDetailView.as_view()), name='employee_detail'),
    path('employee/<int:pk>/delete/', login_required(EmployeeDeleteView.as_view()), name='employee_delete'),

    path('payrolls/', login_required(PayRollListView.as_view()), name='payroll_list'),
    path('payroll/new/', login_required(PayRollCreateView.as_view()), name='payroll_create'),
    path('payroll/<int:pk>/edit/', login_required(PayRollUpdateView.as_view()), name='payroll_update'),
    path('payroll/<int:pk>/delete/', login_required(PayRollDeleteView.as_view()), name='payroll_delete'),

    path('attendances/', login_required(AttendanceListView.as_view()), name='attendance_list'),
    path('attendance/new/', login_required(AttendanceCreateView.as_view()), name='attendance_create'),
    path('attendance/<int:pk>/edit/', login_required(AttendanceUpdateView.as_view()), name='attendance_update'),
    path('attendance/<int:pk>/delete/', login_required(AttendanceDeleteView.as_view()), name='attendance_delete'),
]

urlpatterns += [
    path("leaves/", login_required(LeaveListView.as_view()), name="leave_list"),
    path("leave/request/", login_required(LeaveCreateView.as_view()), name="leave_create"),
    path("leave/<int:pk>/edit/", login_required(LeaveUpdateView.as_view()), name="leave_update"),
    path("leaves/<int:pk>/delete/", login_required(LeaveDeleteView.as_view()), name="leave_delete"),

    path("performances/", login_required(PerformanceListView.as_view()), name="performance_list"),
    path("performance/new/", login_required(PerformanceCreateView.as_view()), name="performance_create"),
    path("performance/<int:pk>/", login_required(PerformanceUpdateView.as_view()), name="performance_update"),
    path("performance/<int:pk>/delete/", login_required(PerformanceDeleteView.as_view()), name="performance_delete"),
]

urlpatterns += [
    path("employee/<int:pk>/apply-leave/", login_required(emp_apply_leave_view), name="emp_apply_leave"),
]
