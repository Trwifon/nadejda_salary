from django.urls import path
from nadejda_salary.common.views import Dashboard

urlpatterns = [
    path('', Dashboard.as_view(), name='dashboard'),
]
