from django.urls import reverse, resolve


class TestUrls:
    def test_note_url(self):
        path = reverse("manage-labels")
        assert resolve(path).view_name == "manage-labels"

    def test_specific_note_url(self):
        path = reverse("manage-label", args=[1])
        assert resolve(path).view_name == "manage-label"

    def test_archived_notes_url(self):
        path = reverse("archived-notes")
        assert resolve(path).view_name == "archived-notes"

    def test_specific_archived_note_url(self):
        path = reverse("manage-specific-archived", args=[1])
        assert resolve(path).view_name == "manage-specific-archived"

    def test_pinned_notes_url(self):
        path = reverse("pinned-notes")
        assert resolve(path).view_name == "pinned-notes"

    def test_specific_pinned_note_url(self):
        path = reverse("manage-specific-pinned-notes", args=[1])
        assert resolve(path).view_name == "manage-specific-pinned-notes"

    def test_trashed_notes_url(self):
        path = reverse("trashed-notes")
        assert resolve(path).view_name == "trashed-notes"

    def test_specific_trashed_note_url(self):
        path = reverse("manage-specific-trashed-notes", args=[1])
        assert resolve(path).view_name == "manage-specific-trashed-notes"

    def test_search_note_url(self):
        path = reverse("search-notes")
        assert resolve(path).view_name == "search-notes"
