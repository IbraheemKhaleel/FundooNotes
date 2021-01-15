from django.urls import path
from . import views

urlpatterns = [
    path('manage-labels/', views.ManageLabel.as_view(), name='manage-labels'),
    path('manage-labels/<int:pk>/', views.ManageLabel.as_view(), name='manage-label'),
]