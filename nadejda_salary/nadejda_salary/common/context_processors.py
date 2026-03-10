from django.db import DatabaseError

from nadejda_salary.salaries.models import CurrentMonth


def current_month(request):
    """Add `current_month` to every template context.

    Returns the open CurrentMonth instance or False when none found or database
    isn't available (e.g. during initial migrations).
    """
    try:
        open_month = CurrentMonth.objects.filter(open=True)
        if open_month:
            month = open_month[0]
            # working hours for the month (work_days * 8)
            hours = month.work_days * 8 if month.work_days is not None else None
            return {'current_month': month, 'current_month_hours': hours}
    except DatabaseError:
        # Database may not be ready during migrate/collectstatic.
        pass
    return {'current_month': False}
