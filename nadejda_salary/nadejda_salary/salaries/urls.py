from django.urls import path, include
from .views import WorkerCreateView, MonthCreateView, DataFillView


urlpatterns = [
    path('create-worker/', WorkerCreateView.as_view(), name='create_worker'),
    path('create-month/', MonthCreateView.as_view(), name='create_month'),
    path('data/', DataFillView.as_view(), name='data'),

    # path('show-report/', ReportShowView.as_view(), name='show_report'),
    # path('cash-report/', CashShowView.as_view(), name='cash_report'),
    # path('partner-create/', PartnerCreateView.as_view(), name='partner_create'),
    # path('errors-test/', ErrorTestView.as_view(), name='errors_test'),
    # path('<int:partner_pk>/create/', RecordCreateView.as_view(), name='record_create'),
    # path('<int:record_pk>/', include([
    #     path('update/', RecordUpdateView.as_view(), name='record_update'),
    #     path('delete/', RecordGlassDeleteView.as_view(), name='record_glass_delete'),
    # ])),
]