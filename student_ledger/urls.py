from django.urls import path

from . import views

urlpatterns = [
    path('', views.BillListView.as_view(), name='home'),
    path('settings/', views.settings_view, name='settings'),

    path('students/', views.StudentListView.as_view(), name='students'),
    path('students/create/', views.StudentCreateView.as_view(), name='student-create'),
    path('students/<int:pk>/detail/', views.StudentDetailView.as_view(), name='student-detail'),
    path('students/<int:pk>/update/', views.StudentUpdateView.as_view(), name='student-update'),
    path('students/<int:pk>/delete/', views.StudentDeleteView.as_view(), name='student-delete'),

    path('bill/<int:pk>/detail/', views.BillDetailView.as_view(), name='bill-detail'),
    path('bill/create/', views.BillCreateView.as_view(), name='bill-create'),
    path('bill/generate/', views.BillGenerateView.as_view(), name='bill-generate'),
     path('bill/<int:pk>/update/', views.BillUpdateView.as_view(), name='bill-update'),
    path('bill/<int:pk>/delete/', views.BillDeleteView.as_view(), name='bill-delete'),

    path('payment/<int:pk>/delete/', views.PaymentDeleteView.as_view(), name='payment-delete'),


    path('bill/<int:pk>/pay/', views.BillPay.as_view(), name='bill-payment'),
]
