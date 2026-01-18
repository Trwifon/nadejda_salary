from django.urls import path
from .views import WorkerCreateView, MonthCreateView, DataFillView, WorkerUpdateView


urlpatterns = [
    path('create-worker/', WorkerCreateView.as_view(), name='create_worker'),
    path('create-month/', MonthCreateView.as_view(), name='create_month'),
    path('data/<int:index>/', DataFillView.as_view(), name='data'),
    path('update-worker/<int:index>/', WorkerUpdateView.as_view(), name='update_worker'),
    # path('update-data/<int:index>/', DataFillView.as_view(), name='update_data'),
]
