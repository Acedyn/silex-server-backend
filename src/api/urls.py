from rest_framework import routers
from api import views

router = routers.DefaultRouter()
router.register(r"users", views.UserViewSet)
router.register(r"groups", views.GroupViewSet)
router.register(r"projects", views.ProjectViewSet)
router.register(r"sequences", views.SequenceViewSet)
router.register(r"shots", views.ShotViewSet)
router.register(r"frames", views.FrameViewSet)
router.register(r"assets", views.AssetViewSet)
router.register(r"tasks", views.TaskViewSet)
