from django.contrib import admin

from django.contrib import admin
from .models import Department, Employee, PayRoll, Attendance, Performance


@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ['name']
    search_fields = ('name',)


@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ('user', 'department', 'dob', 'address', 'position')
    search_fields = ('user__username', 'department__name', 'position')
    list_filter = ('department', 'position')


@admin.register(PayRoll)
class PayrollAdmin(admin.ModelAdmin):
    list_display = ('employee', 'basic_salary', 'bonuses', 'deductions', 'net_salary')
    search_fields = ('employee__user__username',)
    list_filter = ('employee__department',)


@admin.register(Attendance)
class AttendanceAdmin(admin.ModelAdmin):
    list_display = ('employee', 'date', 'is_present')
    search_fields = ['employee__user__username']
    list_filter = ('is_present', 'date')


@admin.register(Performance)
class PerformanceAdmin(admin.ModelAdmin):
    list_display = ('id', 'employee', 'rating')
    search_fields = ('employee__user__username', 'rating')
    list_filter = ('rating',)
