from django.urls import path
from . import views

app_name = 'tickets'

urlpatterns = [
    path('', views.PortalIndexTemplateView.as_view(), name='portal_index'),
    path('section/create/', views.PortalSectionCreateView.as_view(),
         name='portal_section_create'),
    path('section/update/<int:section_id>/', views.PortalSectionUpdateView.as_view(),
         name='portal_section_update'),
    path('section/create-seats/', views.PortalSectionSeatsFormView.as_view(),
         name='portal_section_equal_seats_create'),
    path('section/create-seats-by-row/', views.PortalSectionSeatsByRowsFormView.as_view(),
         name='portal_section_seats_by_row'),
    path('customer/create/', views.PortalCustomerCreateView.as_view(),
         name='portal_customer_create'),
    path('section/bulk-seating/', views.PortalCustomerBulkSeatingView.as_view(),
         name='portal_customer_bulk_seating'),
    path('seats/list/', views.PortalSeatsManageListView.as_view(),
         name='portal_seats_manage'),
    path('seats/update/<int:seat_id>/', views.PortalSeatUpdateView.as_view(),
         name='portal_seat_update'),
    path('section/list/', views.PortalSectionsManageListView.as_view(),
         name='portal_sections_manage'),
    path('section/delete/<int:section_id>/', views.PortalSectionDeleteView.as_view(),
         name='portal_section_delete'),

]
