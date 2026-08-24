from ..salaries.models import WorkerMonth, CurrentMonth


def vacation_calc(current_worker):
    initial_vacation = current_worker.initial_vacation
    vacation_for_take = float(initial_vacation)

    vacation_total = 0

    current_vacations_data = []
    vacation_months = WorkerMonth.objects.filter(worker=current_worker.pk)

    current_worker_vacation_data = {'data': current_vacations_data, 'current_worker': current_worker}

    for month in vacation_months:
        current_month = {'year': month.month.year,
                         'month': month.month.month,
                         'vacation_used': month.vacation_used,
                         'vacation_calc': month.vacation_calc,
                         'vacation_paid': month.vacation_paid,
                         }

        vacation_spent = month.vacation_used + month.vacation_calc + month.vacation_paid
        current_month['vacation_spent'] = vacation_spent
        vacation_total += vacation_spent
        current_month['vacation_total'] = vacation_total

        if current_month['month'] in (11, 12):
            vacation_to_add = 1.5
        else:
            vacation_to_add = 1.7

        current_month['vacation_to_add'] = vacation_to_add

        vacation_for_take += vacation_to_add
        current_month['vacation_for_take'] = vacation_for_take

        vacation_left = vacation_for_take - vacation_total
        current_month['vacation_left'] = vacation_left

        current_vacations_data.append(current_month)

    return current_worker_vacation_data


def sync_worker_with_current_month(worker):
    current_month = CurrentMonth.objects.filter(open=True).first()

    if not current_month:
        return

    worker_month = WorkerMonth.objects.filter(
        worker=worker,
        month=current_month
    ).first()

    if not worker_month:
        return

    worker_month.bonus_boss = worker.bonus_boss
    worker_month.bonus_constant = worker.bonus_constant
    worker_month.bonus_variable = worker.bonus_variable

    worker_month.save(
        update_fields=[
            'bonus_boss',
            'bonus_constant',
            'bonus_variable',
        ]
    )