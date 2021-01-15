from django.urls import reverse, resolve


class TestUrls:
    def test_label_url(self):
        path = reverse("manage-labels")
        assert resolve(path).view_name == "manage-labels"

    def test_specific_label_url(self):
        path = reverse("manage-label", args=[1])
        assert resolve(path).view_name == "manage-label"
