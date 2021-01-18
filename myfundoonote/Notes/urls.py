from django.urls import path
from . import views

urlpatterns = [
    path('', views.NotesOverview.as_view()),
    path('notes/archived-notes/', views.ManageArchivedNote.as_view(), name='archived-notes'),
    path('note/archived-note/<int:pk>/', views.ManageArchivedNote.as_view(), name='manage-specific-archived'),
    path('note/trashed-note/<int:pk>/',views.ManageTrashedNotes.as_view(),name ='manage-specific-trashed-notes'),
    path('notes/trashed-notes/',views.ManageTrashedNotes.as_view(),name = 'trashed-notes'),
    path('note/pinned-note/<int:pk>/',views.ManagePinnedNotes.as_view(),name = 'manage-specific-pinned-notes'),
    path('notes/pinned-notes/',views.ManagePinnedNotes.as_view(),name = 'pinned-notes'),
    path('notes/', views.ManageNotes.as_view(), name='manage-notes'),
    path('note/<int:pk>/', views.ManageNotes.as_view(), name='manage-specific-notes'),
    path('notes/search-notes/', views.SearchNote.as_view(), name='search-notes')
]