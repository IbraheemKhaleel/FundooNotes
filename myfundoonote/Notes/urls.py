from django.urls import path
from . import views

urlpatterns = [
    path('', views.NotesOverview.as_view()),
    path('manage-notes/archived-notes/', views.ManageArchivedNote.as_view(), name='archived-notes'),
    path('manage-notes/archived-notes/<int:pk>/', views.ManageArchivedNote.as_view(), name='manage-specific-archived'),
    path('manage-notes/trashed-notes/<int:pk>/',views.ManageTrashedNotes.as_view(),name ='manage-specific-trashed-notes'),
    path('manage-notes/trashed-notes/',views.ManageTrashedNotes.as_view(),name = 'trashed-notes'),
    path('manage-notes/pinned-notes/<int:pk>/',views.ManagePinnedNotes.as_view(),name = 'manage-specific-pinned-notes'),
    path('manage-notes/pinned-notes/',views.ManagePinnedNotes.as_view(),name = 'pinned-notes'),
    path('manage-notes/', views.ManageNotes.as_view(), name='manage-notes'),
    path('manage-notes/<int:pk>/', views.ManageNotes.as_view(), name='manage-specific-notes'),
    path('manage-notes/search-notes/', views.SearchNote.as_view(), name='search-notes')
]