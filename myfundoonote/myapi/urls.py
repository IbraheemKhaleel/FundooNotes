from django.urls import include, path
from rest_framework import routers
from . import views

router = routers.DefaultRouter()
router.register(r'allusers', views.AccountView)

urlpatterns = [
    path('', include(router.urls)),
    path('accounts/' , include("django.contrib.auth.urls")),
    path('dashboard/' , views.dashboard , name ="dashboard"),
    path('register/', views.register , name ="register"),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
]