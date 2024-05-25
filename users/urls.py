from django.urls import path

from users.apps import UsersConfig
from users.views import LoginView, LogoutView, RegisterView, UserAllListView, UserDetailView, UserUpdateView, \
    UserDeleteView, UserFriendshipListView, UserRejectedListView, UserRequestsListView, UserReceiversListView, \
    RedirectToCurrentUserProfile

app_name = UsersConfig.name

urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('register/', RegisterView.as_view(), name='register'),

    path('', UserAllListView.as_view(), name='user_list'),
    path('friends/', UserFriendshipListView.as_view(), name='user_friendship_list'),
    path('subscribers/', UserRejectedListView.as_view(), name='user_rejected_list'),
    path('requests/', UserRequestsListView.as_view(), name='user_requests_list'),
    path('receivers/', UserReceiversListView.as_view(), name='user_receivers_list'),
    path('<int:pk>/', UserDetailView.as_view(), name='user_detail'),
    path('edit/<int:pk>/', UserUpdateView.as_view(), name='user_edit'),
    path('delete/<int:pk>/', UserDeleteView.as_view(), name='user_delete'),
    path('redirect_to_profile/', RedirectToCurrentUserProfile.as_view(), name='redirect_to_profile')
]
