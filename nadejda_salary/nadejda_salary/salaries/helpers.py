import math


def worker_month_calc(worker, current_month):
    worker.gross = worker.worker.salary + worker.insurance

    worker.equivalent_hours = math.ceil(worker.work_hours / 8) * 8
    worker.unpaid_hours = worker.equivalent_hours - worker.work_hours
    worker.equivalent_days = worker.equivalent_hours / 8
    worker.salary_earned = (worker.work_hours / (current_month.work_days * 8)) * worker.worker.salary

    worker.sick_days_sum = worker.sick_days_firm * 35

    worker.vacation_calc = current_month.work_days \
                           - worker.sick_days_firm \
                           - worker.sick_days_noi \
                           - worker.vacation_used \
                           - worker.equivalent_days
    worker.vacation_calc = 0 if worker.vacation_calc < 0 else worker.vacation_calc
    worker.vacation_sum = worker.vacation_used + worker.vacation_calc
    worker.pay_for_vacation = worker.vacation_sum * 50

    worker.total = worker.salary_earned + worker.sick_days_sum + worker.pay_for_vacation

    worker.unpaid_hours_euro = worker.insurance / current_month.work_days / 8 * worker.unpaid_hours
    worker.rest = worker.total \
                  - float(worker.unpaid_hours_euro) \
                  - float(worker.paid_by_bank) \
                  - float(worker.paid_by_cash) \
                  - float(worker.mobile) \
                  - float(worker.voucher)
    worker.total_paid = worker.rest \
                        + float(worker.unpaid_hours_euro) \
                        + float(worker.paid_by_bank) \
                        + float(worker.paid_by_cash) \
                        + float(worker.mobile) \
                        + float(worker.voucher)

    return worker
