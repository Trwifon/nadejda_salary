from django.test import SimpleTestCase
from django.conf import settings


class SettingsSmokeTest(SimpleTestCase):
	def test_static_root_set(self):
		# STATIC_ROOT should be defined (used by collectstatic in prod)
		self.assertTrue(hasattr(settings, 'STATIC_ROOT'))

	def test_secret_key_from_env_or_default(self):
		# In development the default fallback is allowed, but ensure the setting exists
		self.assertTrue(hasattr(settings, 'SECRET_KEY'))
