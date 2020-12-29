from django.urls import reverse, resolve


class TestUrls:
    def test_register_url(self):
        path = reverse("register")
        assert resolve(path).view_name == "register"

    def test_login_url(self):
        path = reverse("login")
        assert resolve(path).view_name == "login"