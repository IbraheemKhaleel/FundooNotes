from django.urls import path
from . import views

urlpatterns = [
    path('label/', views.Labels.as_view()),
    path('label-update/<int:pk>/', views.UpdateLabel.as_view())
    ]