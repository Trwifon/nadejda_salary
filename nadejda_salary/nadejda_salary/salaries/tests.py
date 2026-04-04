from django.test import TestCase
from decimal import Decimal
from datetime import date
from nadejda_salary.salaries.models import Workers, CurrentMonth, WorkerMonth


class WorkerMonthModelTests(TestCase):
	def setUp(self):
		self.current_month = CurrentMonth.objects.create(year=2026, month=4, work_days=20, open=True)

	def _create_worker(self, name, start_date=None, end_date=None):
		return Workers.objects.create(
			name=name,
			workshop='A',
			bonus_boss=0,
			bonus_constant=0,
			bonus_variable=0,
			total_vacation=20,
			initial_vacation=Decimal('10.0'),
			start_date=start_date,
			end_date=end_date,
			contract=True,
		)

	def _create_worker_month(self, worker, work_hours=160):
		return WorkerMonth.objects.create(
			bonus_boss=0,
			bonus_constant=0,
			bonus_variable=0,
			insurance=Decimal('100.00'),
			work_hours=work_hours,
			sick_days_noi=0,
			sick_days_firm=2,
			vacation_used=3,
			vacation_paid=0,
			paid_by_bank=Decimal('100.00'),
			paid_by_cash=Decimal('50.00'),
			mobile=Decimal('10.00'),
			voucher=Decimal('0.00'),
			worker=worker,
			month=self.current_month,
		)

	def test_vacation_calc_is_zero_when_start_date_is_in_current_month(self):
		worker = self._create_worker(name='Alice', start_date=date(2026, 4, 10))
		worker_month = self._create_worker_month(worker)
		self.assertEqual(0, worker_month.vacation_calc)

	def test_vacation_calc_is_zero_when_end_date_is_in_current_month(self):
		worker = self._create_worker(name='Bob', end_date=date(2026, 4, 25))
		worker_month = self._create_worker_month(worker)
		self.assertEqual(0, worker_month.vacation_calc)

	def test_vacation_calc_uses_formula_when_dates_are_outside_current_month(self):
		worker = self._create_worker(name='Charlie', start_date=date(2026, 3, 1), end_date=date(2026, 5, 1))
		worker_month = self._create_worker_month(worker, work_hours=96)
		self.assertEqual(3, worker_month.vacation_calc)
