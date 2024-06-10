from friendship.models import Friendship


def friend_request(request):
    """ Обработчик показывает, сколько друзей у пользователя """

    current_user = request.user

    if current_user.is_authenticated:
        friend_requests_count = Friendship.objects.filter(user_2=current_user, status="pending").count()

    else:
        friend_requests_count = 0

    return {'friend_requests_count': friend_requests_count}
