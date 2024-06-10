from django.db.models import Q


class FriendshipHandler:
    def __init__(self, friendship_model, current_user, user_model, pk):
        self.friendship_model = friendship_model
        self.current_user = current_user
        self.other_user = user_model.objects.get(pk=pk)

    def create_friendship(self):
        friendship = self.friendship_model.objects.filter(
            Q(user_1=self.current_user, user_2=self.other_user) | Q(user_1=self.other_user, user_2=self.current_user)
        )

        if not friendship:
            friendship = self.friendship_model.objects.create(user_1=self.current_user, user_2=self.other_user)
            friendship.status = "pending"
            friendship.save()

    def cancel_friendship(self):
        friendship = self.friendship_model.objects.filter(
            Q(user_1=self.current_user, user_2=self.other_user) | Q(user_1=self.other_user, user_2=self.current_user)
        ).first()

        if friendship:
            friendship.delete()

    def accept_friendship(self):
        friendship = self.friendship_model.objects.filter(
            Q(user_1=self.current_user, user_2=self.other_user) | Q(user_1=self.other_user, user_2=self.current_user)
        ).first()

        if friendship:
            friendship.status = "accepted"
            friendship.save()

    def reject_friendship(self):
        friendship = self.friendship_model.objects.filter(
            Q(user_1=self.current_user, user_2=self.other_user) | Q(user_1=self.other_user, user_2=self.current_user)
        ).first()

        if friendship:
            friendship.status = "rejected"
            friendship.save()
