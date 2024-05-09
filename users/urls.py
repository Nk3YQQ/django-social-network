from django.urls import path

from users.apps import UsersConfig
from users.views import LoginView, LogoutView, RegisterView, UserListView, UserDetailView, UserUpdateView, \
    UserDeleteView, create_friendship_between_users, cancel_application, UserFriendshipListView, has_been_friend

app_name = UsersConfig.name

urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('register/', RegisterView.as_view(), name='register'),

    path('', UserListView.as_view(), name='user_list'),
    path('friends/', UserFriendshipListView.as_view(), name='user_friendship_list'),
    path('<int:pk>/', UserDetailView.as_view(), name='user_detail'),
    path('edit/<int:pk>/', UserUpdateView.as_view(), name='user_edit'),
    path('delete/<int:pk>/', UserDeleteView.as_view(), name='user_delete'),

    path('make_a_friendship/<int:pk>', create_friendship_between_users, name='create_friendship_between_users'),
    path('cancel_application/<int:pk>', cancel_application, name='cancel_application'),
    path('has_been_friend/', has_been_friend, name='has_been_friend')
]
