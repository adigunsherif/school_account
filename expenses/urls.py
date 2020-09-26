from django.urls import path

from . import views

urlpatterns = [
    path('', views.ExpenseView.as_view(), name='expenses'),
    path('create/', views.ExpenseCreateView.as_view(), name='expenses-create'),
    path('<int:pk>/update/', views.ExpenseUpdateView.as_view(), name='expenses-update'),
    path('<int:pk>/delete/', views.ExpenseDeleteView.as_view(), name='expenses-delete'),
]
