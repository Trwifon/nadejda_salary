import math
from django.db import models
from .choices import WorkshopChoices, YearChoices, MonthChoices, WorkDaysChoices
from django.core.validators import MinValueValidator, MaxValueValidator


PAY_PER_SICK = 20.67
PAY_PER_VACATION = 29.50


class Workers(models.Model):
    name = models.CharField(
        max_length=50,
        unique=True,
    )

    workshop = models.CharField(
        max_length=20,
        choices=WorkshopChoices.choices,
    )

    salary = models.IntegerField(
        null=True,
        default=0,
    )

    bonus_one = models.IntegerField(
        null=True,
        default=0,
    )

    bonus_two = models.IntegerField(
        null=True,
        default=0,
    )

    total_vacation = models.PositiveSmallIntegerField(
        null=True,
    )

    initial_vacation = models.PositiveSmallIntegerField()

    start_date = models.DateField(
        blank=True,
        null=True,
    )

    end_date = models.DateField(
        blank=True,
        null=True,
    )

    contract = models.BooleanField(
        default=True,
    )

    @property
    def total_salary(self):
        return self.salary + self.bonus_one + self.bonus_two


class CurrentMonth(models.Model):
    year = models.PositiveSmallIntegerField(
        validators=[
            MinValueValidator(2024),
            MaxValueValidator(2044),
        ],
        choices=YearChoices.choices,
    )

    month = models.PositiveSmallIntegerField(
        validators=[
            MinValueValidator(1),
            MaxValueValidator(12),
        ],
        choices=MonthChoices.choices,
    )

    work_days = models.PositiveSmallIntegerField(
        validators=[
            MinValueValidator(18),
            MaxValueValidator(23),
        ],
        choices=WorkDaysChoices.choices,
    )

    open = models.BooleanField(
        default=True,
    )


class WorkerMonth(models.Model):
    salary = models.PositiveSmallIntegerField(
        default=0,
    )

    bonus_one = models.PositiveSmallIntegerField(
        default=0,
    )

    bonus_two = models.PositiveSmallIntegerField(
        default=0,
    )

    insurance = models.DecimalField(
        max_digits=6,
        decimal_places=2,
        validators=[MinValueValidator(0)],
    )

    work_hours = models.PositiveSmallIntegerField()

    sick_days_noi = models.PositiveSmallIntegerField()

    sick_days_firm = models.PositiveSmallIntegerField()

    vacation_used = models.PositiveSmallIntegerField()

    vacation_paid = models.PositiveSmallIntegerField()

    paid_by_bank = models.DecimalField(
        max_digits=6,
        decimal_places=2,
    )

    paid_by_cash = models.DecimalField(
        max_digits=6,
        decimal_places=2,
    )

    mobile = models.DecimalField(
        max_digits=6,
        decimal_places=2,
    )

    voucher = models.SmallIntegerField(
        default=0,
    )

    worker = models.ForeignKey(
        to=Workers,
        on_delete=models.DO_NOTHING,
        related_name='worker'
    )

    month = models.ForeignKey(
        to=CurrentMonth,
        on_delete=models.DO_NOTHING,
        related_name='current_month'
    )

    @property
    def total_salary(self):
        return self.salary + self.bonus_one + self.bonus_two

    @property
    def gross(self):
        return self.total_salary + self.insurance

    @property
    def equivalent_hours(self):
        result = math.ceil(self.work_hours / 8) * 8
        return result

    @property
    def unpaid_hours(self):
        result = self.equivalent_hours - self.work_hours
        return result

    @property
    def equivalent_days(self):
        result = self.equivalent_hours / 8
        return result

    @property
    def salary_earned(self):
        result = (self.work_hours / (self.month.work_days * 8)) * self.total_salary
        return result

    @property
    def sick_days_sum(self):
        result = self.sick_days_firm * PAY_PER_SICK
        return result

    @property
    def vacation_calc(self):
        result = self.month.work_days \
           - self.sick_days_firm \
           - self.sick_days_noi \
           - self.vacation_used \
           - self.equivalent_days
        result = 0 if result < 0 else result
        return result

    @property
    def vacation_sum(self):
        result = self.vacation_used + self.vacation_calc
        return result

    @property
    def pay_for_vacation(self):
        result = self.vacation_sum * PAY_PER_VACATION
        return result

    @property
    def total(self):
        result = self.salary_earned + self.sick_days_sum + self.pay_for_vacation
        return result

    @property
    def unpaid_hours_euro(self):
        result = self.insurance / self.month.work_days / 8 * self.unpaid_hours
        return result

    @property
    def rest(self):
        result = self.total \
            - float(self.unpaid_hours_euro) \
            - float(self.paid_by_bank) \
            - float(self.paid_by_cash) \
            - float(self.mobile) \
            - float(self.voucher)
        return result

    @property
    def total_paid(self):
        result = self.rest \
            + float(self.unpaid_hours_euro) \
            + float(self.paid_by_bank) \
            + float(self.paid_by_cash) \
            + float(self.mobile) \
            + float(self.voucher)
        return result


class Vacation(models.Model):
    year = models.PositiveSmallIntegerField(
        validators=[
            MinValueValidator(2024),
            MaxValueValidator(2044),
        ],
        choices=YearChoices.choices,
    )

    days = models.PositiveIntegerField(
        validators=[
            MinValueValidator(0),
            MaxValueValidator(20),
        ],
    )

    used_days = models.PositiveIntegerField(
        validators=[
            MinValueValidator(0),
            MaxValueValidator(20),
        ],
        default=0
    )

    pay_per_day_vacation = models.PositiveSmallIntegerField()

    pay_per_day_sick = models.PositiveSmallIntegerField()

    worker = models.ForeignKey(
        to=Workers,
        on_delete=models.DO_NOTHING,
        related_name='vacations'
    )

    def __str__(self):
        return str(self.year)












