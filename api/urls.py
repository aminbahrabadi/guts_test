from django.urls import path
from . import views

app_name = 'api'

urlpatterns = [
    path('bulk-seating/', views.BulkSeatingApiView.as_view(), name='api_bulk_seating'),
    path('retrieve-seats/', views.SeatsRetrieveApi.as_view(), name='api_retrieve_seats'),
    path('retrieve-single-seat/', views.SingleSeatRetrieveApi.as_view(),
         name='api_retrieve_single_seat'),
    path('retrieve-sections/', views.SectionsRetrieveApi.as_view(), name='api_retrieve_sections'),
]
