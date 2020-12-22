from django.urls import path
from . import views

urlpatterns = [
    path('label/', views.LabelsView.as_view(), name = 'label_create_retrieve'),
    path('label-update/<int:pk>/', views.LabelView.as_view(), name = 'label_put_delete')
    ]