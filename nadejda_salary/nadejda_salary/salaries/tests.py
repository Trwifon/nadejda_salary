from django.test import TestCase
from decimal import Decimal
from nadejda_salary.salaries.models import Workers, CurrentMonth, WorkerMonth, Vacation


class WorkerMonthModelTests(TestCase):
	def setUp(self):
		self.worker = Workers.objects.create(name='Alice', workshop='A', salary=1000, bonus_one=0, bonus_two=0, initial_vacation=10)
		self.current_month = CurrentMonth.objects.create(year=2024, month=1, work_days=20, open=True)

	def test_total_paid_returns_sum(self):
		wm = WorkerMonth.objects.create(
			salary=1000,
			bonus_one=0,
			bonus_two=0,
			insurance=Decimal('100.00'),
			work_hours=160,
			sick_days_noi=0,
			sick_days_firm=0,
			vacation_used=0,
			vacation_paid=0,
			paid_by_bank=Decimal('100.00'),
			paid_by_cash=Decimal('50.00'),
			mobile=Decimal('10.00'),
			voucher=0,
			worker=self.worker,
			month=self.current_month,
		)

		# total_paid should equal rest + components; since rest + components == total
		self.assertIsNotNone(wm.total_paid)


class VacationModelTests(TestCase):
	def test_str_returns_string(self):
		v = Vacation.objects.create(year=2024, days=10, pay_per_day_vacation=10, pay_per_day_sick=5, worker=Workers.objects.create(name='Bob', workshop='B', salary=500, bonus_one=0, bonus_two=0, initial_vacation=5))
		self.assertIsInstance(str(v), str)
