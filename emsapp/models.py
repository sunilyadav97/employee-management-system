from django.contrib.auth.models import User
from django.db import models


class TimeStampedModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Role(TimeStampedModel):
    name = models.CharField(max_length=50, unique=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class Department(TimeStampedModel):
    name = models.CharField(max_length=100)
    description = models.TextField()

    def __str__(self):
        return self.name


class Employee(TimeStampedModel):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.ForeignKey(Role, on_delete=models.SET_NULL, null=True)
    mobile_no = models.CharField(max_length=100, null=True, blank=True)
    dob = models.DateField()
    position = models.CharField(max_length=100, null=True, blank=True)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    address = models.TextField(null=True, blank=True)

    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.user.get_full_name() if self.user.get_full_name() else self.user.username


class PayRoll(TimeStampedModel):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    basic_salary = models.DecimalField(max_digits=10, decimal_places=2)
    bonuses = models.DecimalField(max_digits=10, decimal_places=2)
    deductions = models.DecimalField(max_digits=10, decimal_places=2)
    net_salary = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

    is_active = models.BooleanField(default=True)

    def __str__(self):
        return str(self.employee.user.get_full_name() if self.employee.user.get_full_name() else self.employee.user)

    @property
    def get_net_salary(self):
        return self.basic_salary + self.bonuses - self.deductions

    def save(self, *args, **kwargs):
        # Automatically calculate net salary before saving
        self.net_salary = self.get_net_salary
        super().save(*args, **kwargs)


class Attendance(TimeStampedModel):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    date = models.DateField()
    is_present = models.BooleanField(default=False)

    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['-date']

    def __str__(self):
        return str(self.date)


class Leave(TimeStampedModel):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    leave_type = models.CharField(max_length=100)
    from_date = models.DateField()
    to_date = models.DateField()
    reason = models.TextField()
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.leave_type


class Performance(TimeStampedModel):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    rating = models.DecimalField(max_digits=10, decimal_places=2)
    comments = models.TextField()
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.employee.user.get_full_name()
