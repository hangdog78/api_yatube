from django.urls import include, path
from rest_framework import routers
from rest_framework.authtoken import views

from .views import GroupViewSet, PostViewSet, api_comments, api_comments_detail

router = routers.DefaultRouter()
'''
router.register(r'api/v1/posts/(?P<post_id>\\d+)/comments',
                CommentsViewSet,
                basename='comments'
                )
#router.register(r'api/v1/posts/(?P<post_id>\\d+)/comments/(?P<comment_id>\\d+)',
                CommentViewSet,
                basename='comments'
                )
'''
router.register('api/v1/posts', PostViewSet)
router.register('api/v1/groups', GroupViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('api/v1/posts/<int:post_id>/comments/',
         api_comments),
    path('api/v1/posts/<int:post_id>/comments/<int:comment_id>/',
         api_comments_detail),
    path('api/v1/api-token-auth/', views.obtain_auth_token),
]
