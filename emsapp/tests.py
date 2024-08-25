from django.test import TestCase

from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Role, Department, Employee, PayRoll


class EMSAppViewsTestCase(TestCase):

    def setUp(self):
        # Create a test user and role
        self.role = Role.objects.create(name="Admin", is_active=True)
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.employee = Employee.objects.create(user=self.user, role=self.role, is_active=True)

        # Login the user
        self.client = Client()
        self.client.login(username='testuser', password='12345')

    def test_dashboard_view(self):
        response = self.client.get(reverse('emsapp:dashboard'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'emsapp/dashboard.html')

    def test_profile_view(self):
        response = self.client.get(reverse('emsapp:profile', args=[self.employee.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'emsapp/profile.html')

    def test_profile_view_invalid_access(self):
        another_employee = Employee.objects.create(
            user=User.objects.create_user(username='otheruser', password='12345'), role=self.role)
        response = self.client.get(reverse('emsapp:profile', args=[another_employee.id]))
        self.assertRedirects(response, reverse('emsapp:dashboard'))
        messages = list(response.wsgi_request._messages)
        self.assertEqual(str(messages[0]), "Invalid access!")

    def test_role_list_view(self):
        response = self.client.get(reverse('emsapp:role_list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'emsapp/role_list.html')

    def test_role_create_view(self):
        response = self.client.post(reverse('emsapp:role_create'), {
            'name': 'Manager',
            'is_active': True
        })
        self.assertRedirects(response, reverse('emsapp:role_list'))
        messages = list(response.wsgi_request._messages)
        self.assertEqual(str(messages[0]), 'Role successfully created.')

    def test_role_update_view(self):
        response = self.client.post(reverse('emsapp:role_update', args=[self.role.id]), {
            'name': 'Updated Role',
            'is_active': True
        })
        self.assertRedirects(response, reverse('emsapp:role_list'))
        self.role.refresh_from_db()
        self.assertEqual(self.role.name, 'Updated Role')
        messages = list(response.wsgi_request._messages)
        self.assertEqual(str(messages[0]), 'Role successfully updated.')

    def test_role_delete_view(self):
        response = self.client.post(reverse('emsapp:role_delete', args=[self.role.id]))
        self.assertRedirects(response, reverse('emsapp:role_list'))
        with self.assertRaises(Role.DoesNotExist):
            self.role.refresh_from_db()
        messages = list(response.wsgi_request._messages)
        self.assertEqual(str(messages[0]), 'Role successfully deleted.')

    def test_department_list_view(self):
        response = self.client.get(reverse('emsapp:department_list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'emsapp/department_list.html')

    def test_department_create_view(self):
        response = self.client.post(reverse('emsapp:department_create'), {
            'name': 'HR',
            'description': 'Human Resources'
        })
        self.assertRedirects(response, reverse('emsapp:department_list'))
        messages = list(response.wsgi_request._messages)
        self.assertEqual(str(messages[0]), 'Department successfully created.')

    def test_department_update_view(self):
        department = Department.objects.create(name="Finance", description="Finance Department")
        response = self.client.post(reverse('emsapp:department_update', args=[department.id]), {
            'name': 'Updated Department',
            'description': 'Updated Description'
        })
        self.assertRedirects(response, reverse('emsapp:department_list'))
        department.refresh_from_db()
        self.assertEqual(department.name, 'Updated Department')
        messages = list(response.wsgi_request._messages)
        self.assertEqual(str(messages[0]), 'Department successfully updated.')

    def test_department_delete_view(self):
        department = Department.objects.create(name="Marketing", description="Marketing Department")
        response = self.client.post(reverse('emsapp:department_delete', args=[department.id]))
        self.assertRedirects(response, reverse('emsapp:department_list'))
        with self.assertRaises(Department.DoesNotExist):
            department.refresh_from_db()
        messages = list(response.wsgi_request._messages)
        self.assertEqual(str(messages[0]), 'Department successfully deleted!')

    def test_user_employee_create_view(self):
        response = self.client.post(reverse('emsapp:useremployee_create'), {
            'username': 'newuser',
            'password': 'newpassword123',
            'email': 'newuser@example.com',
            'first_name': 'New',
            'last_name': 'User',
            'mobile_no': '1234567890',
            'dob': '1990-01-01',
            'position': 'Developer',
            'department': 'IT',
            'address': '123 Main St'
        })
        self.assertRedirects(response, reverse('emsapp:employee_list'))
        self.assertTrue(User.objects.filter(username='newuser').exists())
        messages = list(response.wsgi_request._messages)
        self.assertEqual(str(messages[0]), 'Employee successfully created.')

    def test_user_employee_update_view(self):
        response = self.client.post(reverse('emsapp:useremployee_update', args=[self.employee.id]), {
            'username': 'updateduser',
            'email': 'updateduser@example.com',
            'first_name': 'Updated',
            'last_name': 'User',
            'mobile_no': '0987654321',
            'dob': '1985-05-05',
            'position': 'Manager',
            'department': 'Sales',
            'address': '456 Other St'
        })
        self.assertRedirects(response, reverse('emsapp:employee_list'))
        self.user.refresh_from_db()
        self.assertEqual(self.user.username, 'updateduser')
        messages = list(response.wsgi_request._messages)
        self.assertEqual(str(messages[0]), 'Employee successfully updated.')

    def test_employee_list_view(self):
        response = self.client.get(reverse('emsapp:employee_list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'emsapp/employee_list.html')

    def test_employee_detail_view(self):
        response = self.client.get(reverse('emsapp:employee_detail', args=[self.employee.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'emsapp/employee_detail.html')

    def test_employee_delete_view(self):
        response = self.client.post(reverse('emsapp:employee_delete', args=[self.employee.id]))
        self.assertRedirects(response, reverse('emsapp:employee_list'))
        with self.assertRaises(Employee.DoesNotExist):
            self.employee.refresh_from_db()
        messages = list(response.wsgi_request._messages)
        self.assertEqual(str(messages[0]), 'Employee successfully deleted!')

    def test_payroll_list_view(self):
        response = self.client.get(reverse('emsapp:payroll_list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'emsapp/payroll_list.html')

    def test_payroll_create_view(self):
        response = self.client.post(reverse('emsapp:payroll_create'), {
            'employee': self.employee.id,
            'basic_salary': 5000,
            'bonuses': 500,
            'deductions': 200
        })
        self.assertRedirects(response, reverse('emsapp:payroll_list'))
        self.assertTrue(PayRoll.objects.filter(employee=self.employee).exists())
        messages = list(response.wsgi_request._messages)
        self.assertEqual(str(messages[0]), 'Payroll successfully created.')

    def test_payroll_update_view(self):
        payroll = PayRoll.objects.create(employee=self.employee, basic_salary=5000, bonuses=500, deductions=200)
        response = self.client.post(reverse('emsapp:payroll_update', args=[payroll.id]), {
            'basic_salary': 6000,
            'bonuses': 600,
            'deductions': 250
        })
        self.assertRedirects(response, reverse('emsapp:payroll_list'))
        payroll.refresh_from_db()
        self.assertEqual(payroll.basic_salary, 6000)
        messages = list(response.wsgi_request._messages)
        self.assertEqual(str(messages[0]), 'Payroll successfully updated.')

    def test_payroll_delete_view(self):
        payroll = PayRoll.objects.create(employee=self.employee, basic_salary=5000, bonuses=500, deductions=200)
        response = self.client.post(reverse('emsapp:payroll_delete', args=[payroll.id]))
        self.assertRedirects(response, reverse('emsapp:payroll_list'))
        with self.assertRaises(PayRoll.DoesNotExist):
            payroll.refresh_from_db()
        messages = list(response.wsgi_request._messages)
        self.assertEqual(str(messages[0]), 'Payroll successfully deleted.')

