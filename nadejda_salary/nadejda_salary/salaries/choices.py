from django.db import models


class WorkshopChoices(models.TextChoices):
    ANTON = 'AN', 'Антон'
    ALUMIN = 'A', 'Алуминий'
    GLASSES = 'G', 'Стъклопакети'
    PVC = 'P', 'PVC'
    INSTALLER = 'I', 'Монтажник'
    LABOURER = 'L', 'Общ работник'


class YearChoices(models.IntegerChoices):
    YEAR_FOUR = 2024, '2024'
    YEAR_FIVE = 2025, '2025'
    YEAR_SIX = 2026, '2026'
    YEAR_SEVEN = 2027, '2027'
    YEAR_EIGHT = 2028, '2028'
    YEAR_NINE = 2029, '2029'
    YEAR_TEN = 2030, '2030'
    YEAR_ONE = 2031, '2031'
    YEAR_TWO = 2032, '2032'
    YEAR_THREE = 2033, '2033'


class MonthChoices(models.IntegerChoices):
    JANUARY = 1, 'Януари'
    FEBRUARY = 2, 'Февруари'
    MARCH = 3, 'Март'
    APRIL = 4, 'Април'
    MAY = 5, 'Май'
    JUNE = 6, 'Юни'
    JULY = 7, 'Юли'
    AUGUST = 8, 'Август'
    SEPTEMBER = 9, 'Септември'
    OCTOBER = 10, 'Октомври'
    NOVEMBER = 11, 'Ноември'
    DECEMBER = 12, 'Декември'


class WorkDaysChoices(models.IntegerChoices):
    EIGHTEEN = 18, '18'
    NINETEEN = 19, '19'
    TWENTY = 20, '20'
    TWENTY_ONE = 21, '21'
    TWENTY_TWO = 22, '22'
    TWENTY_THREE = 23, '23'


