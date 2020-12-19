from django.urls import path
from . import views


urlpatterns = [
    path('', views.NotesOverview.as_view()),
    path('note/', views.Notes.as_view()),
    path('note-update/<int:pk>/', views.UpdateNote.as_view())
    ]