from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model


User = get_user_model()


class PasswordChangeTests(TestCase):
	def setUp(self):
		self.user = User.objects.create(
			username='tester',
			email='tester@example.com',
			first_name='Test',
			last_name='User',
		)
		self.user.set_password('oldpassword123')
		self.user.save()

	def test_password_change_success(self):
		self.client.force_login(self.user)
		url = reverse('profile_update', args=[self.user.pk])
		data = {
			'username': self.user.username,
			'first_name': self.user.first_name,
			'last_name': self.user.last_name,
			'email': self.user.email,
			'current_password': 'oldpassword123',
			'new_password1': 'NewStrongPass123',
			'new_password2': 'NewStrongPass123',
		}
		resp = self.client.post(url, data)
		self.user.refresh_from_db()
		self.assertTrue(self.user.check_password('NewStrongPass123'))

	def test_password_change_wrong_current(self):
		self.client.force_login(self.user)
		url = reverse('profile_update', args=[self.user.pk])
		data = {
			'username': self.user.username,
			'first_name': self.user.first_name,
			'last_name': self.user.last_name,
			'email': self.user.email,
			'current_password': 'wrongpassword',
			'new_password1': 'NewStrongPass123',
			'new_password2': 'NewStrongPass123',
		}
		resp = self.client.post(url, data)
		self.user.refresh_from_db()
		# password should remain unchanged
		self.assertTrue(self.user.check_password('oldpassword123'))
		self.assertContains(resp, 'Current password is incorrect.')

	def test_password_mismatch(self):
		self.client.force_login(self.user)
		url = reverse('profile_update', args=[self.user.pk])
		data = {
			'username': self.user.username,
			'first_name': self.user.first_name,
			'last_name': self.user.last_name,
			'email': self.user.email,
			'current_password': 'oldpassword123',
			'new_password1': 'NewStrongPass123',
			'new_password2': 'DifferentPass456',
		}
		resp = self.client.post(url, data)
		self.user.refresh_from_db()
		self.assertTrue(self.user.check_password('oldpassword123'))
		# HTML will escape the apostrophe as &#39; in the rendered template
		self.assertContains(resp, "didn&#39;t match")

	def test_leave_blank_keeps_password(self):
		self.client.force_login(self.user)
		url = reverse('profile_update', args=[self.user.pk])
		data = {
			'username': self.user.username,
			'first_name': self.user.first_name,
			'last_name': self.user.last_name,
			'email': self.user.email,
			# no password fields
		}
		resp = self.client.post(url, data)
		self.user.refresh_from_db()
		self.assertTrue(self.user.check_password('oldpassword123'))
