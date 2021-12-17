from django.urls import path, include
from rest_framework import routers
from app import views

router = routers.DefaultRouter()
router.register("users", views.UserViewSet)
router.register("profile", views.ProfileViewSet)
router.register("plans", views.PlanViewSet, basename="plans")
router.register("subscribe", views.SubscriptionViewSet, basename="subscriptions")


urlpatterns = [
    path("api/", include(router.urls)),
    path("api-auth/", include("rest_framework.urls")),
    # path("api/plan", views.PlanView.as_view()),
]
