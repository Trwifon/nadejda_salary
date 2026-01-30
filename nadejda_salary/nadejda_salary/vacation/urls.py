from django.urls import path

from .views import VacationListView

urlpatterns = [
    path('list-vacation/', VacationListView.as_view(), name='list_vacation'),
    # path('display-vacation/', VacationDsiplayView.as_view(), name='display_vacation'),
]