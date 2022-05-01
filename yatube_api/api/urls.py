from django.urls import include, path
from rest_framework import routers
from rest_framework.authtoken import views

from .views import GroupViewSet, PostViewSet, CommentsViewSet

api_v1_router = routers.DefaultRouter()

api_v1_router.register(r'posts/(?P<post_id>\d+)/comments',
                       CommentsViewSet,
                       basename='comments'
                       )

api_v1_router.register('posts', PostViewSet)
api_v1_router.register('groups', GroupViewSet)

urlpatterns = [
    path('v1/', include(api_v1_router.urls)),
    path('v1/api-token-auth/', views.obtain_auth_token),
]
