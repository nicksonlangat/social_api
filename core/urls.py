from rest_framework.routers import DefaultRouter

from . import views

router = DefaultRouter()
router.register(r"", views.PostsViewset, basename="posts")

urlpatterns = router.urls
