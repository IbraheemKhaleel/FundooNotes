from django.urls import path
from . import views

urlpatterns = [
    path('', views.NotesOverview.as_view()),
    path('note-list/', views.NotesList.as_view()),
    path('note-detail/<int:pk>/', views.NotesDetail.as_view()),
    path('note-create/', views.CreateNote.as_view()),
    path('note-update/<int:pk>/', views.UpdateNote.as_view()),
    path('note-delete/<int:pk>/', views.DeleteNote.as_view()),
    path('label-list/', views.LabelList.as_view()),
    path('label-create/', views.CreateLabel.as_view()),
    path('label-update/<int:pk>/', views.UpdateLabel.as_view()),
    path('label-delete/<int:pk>/', views.DeleteLabel.as_view()), 
    ]