from rest_framework import routers

from notion.views import PageViewSet

router = routers.SimpleRouter()
router.register(r'pages', PageViewSet,basename='notion')