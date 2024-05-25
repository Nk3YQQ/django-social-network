def filter_users_in_friendship_list(friendship_list, current_user):
    return list(
        friendship.user_2 if friendship.user_1 == current_user else friendship.user_1
        for friendship in friendship_list
    )[:3]
