from django.urls import path

from .views import VacationListView, VacationDisplayView

urlpatterns = [
    path('list-vacation/', VacationListView.as_view(), name='list_vacation'),
    path('display-vacation/<int:pk>/', VacationDisplayView.as_view(), name='display_vacation'),
]