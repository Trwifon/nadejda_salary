from django.urls import path
from .views import WorkerCreateView, MonthCreateView, DataFillView, \
    WorkerUpdateView, DataListView, DataUpdateView, CloseMonthView, DetailsWorkerMonthView

urlpatterns = [
    path('create-worker/', WorkerCreateView.as_view(), name='create_worker'),
    path('create-month/', MonthCreateView.as_view(), name='create_month'),
    path('data/<int:index>/', DataFillView.as_view(), name='data'),
    path('update-worker/<int:index>/', WorkerUpdateView.as_view(), name='update_worker'),
    path('list-data/', DataListView.as_view(), name='list_data'),
    path('details-worker-month/<int:pk>/', DetailsWorkerMonthView.as_view(), name='details_worker_month'),
    path('update-data/<int:pk>/', DataUpdateView.as_view(), name='update_data'),
    path('close-month/<int:pk>/', CloseMonthView.as_view(), name='close_month'),
]
