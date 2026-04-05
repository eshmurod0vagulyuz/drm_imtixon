from django.urls import path, include

app_name = 'v1'

urlpatterns = [
    path('users/', include('apps.users.urls.v1', namespace='users')),
    path('posts/', include('apps.posts.urls.v1', namespace='posts')),
    path('comments/', include('apps.comments.urls.v1', namespace='comments')),
]

