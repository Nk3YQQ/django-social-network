from django.urls import path

from friendship.apps import FriendshipConfig
from friendship.views import (AcceptApplicationListView, AcceptApplicationOnPageView, CancelApplicationListView,
                              CancelApplicationOnPageView, CreateFriendshipListView, CreateFriendshipOnPageView,
                              RejectApplicationListView, RejectApplicationOnPageView)

app_name = FriendshipConfig.name

urlpatterns = [
    # List
    path("create_list/<int:pk>/", CreateFriendshipListView.as_view(), name="create_friendship_list"),
    path("cancel_list/<int:pk>/", CancelApplicationListView.as_view(), name="cancel_friendship_list"),
    path("accept_list/<int:pk>/", AcceptApplicationListView.as_view(), name="accept_friendship_list"),
    path("reject_list/<int:pk>/", RejectApplicationListView.as_view(), name="reject_friendship_list"),
    # Page
    path("create/<int:pk>/", CreateFriendshipOnPageView.as_view(), name="create_friendship_on_page"),
    path("cancel/<int:pk>/", CancelApplicationOnPageView.as_view(), name="cancel_application_on_page"),
    path("accept/<int:pk>/", AcceptApplicationOnPageView.as_view(), name="accept_application_on_page"),
    path("reject/<int:pk>/", RejectApplicationOnPageView.as_view(), name="reject_application_on_page"),
]
