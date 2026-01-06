from django.db import models
from nadejda_salary.salaries.choices import WorkshopChoices, YearChoices, MonthChoices, WorkDaysChoices
from django.core.validators import MinValueValidator, MaxValueValidator

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
    )

    total_vacation = models.PositiveSmallIntegerField(
        null=True,
    )

    contract = models.BooleanField(
        default=True,
    )


    def __str__(self):
        return self.name


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

    pay_per_day_vacation = models.PositiveSmallIntegerField()

    pay_per_day_sick = models.PositiveSmallIntegerField()

    worker = models.ForeignKey(
        to=Workers,
        on_delete=models.DO_NOTHING,
        related_name='vacations'
    )

    def __str__(self):
        return self.year


class Month(models.Model):
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

    def __str__(self):
        return self.month

    def __total_sick_days__(self):
        total = self.sick_days_noi + self.sick_days_firm
        return total









