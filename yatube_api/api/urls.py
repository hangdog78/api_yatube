from django.urls import include, path
from rest_framework import routers
from rest_framework.authtoken import views

from .views import GroupViewSet, PostViewSet, CommentsViewSet

router = routers.DefaultRouter()

router.register(r'api/v1/posts/(?P<post_id>\d+)/comments',
                CommentsViewSet,
                basename='comments'
                )

router.register('api/v1/posts', PostViewSet)
router.register('api/v1/groups', GroupViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('api/v1/api-token-auth/', views.obtain_auth_token),
]
