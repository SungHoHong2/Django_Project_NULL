from django.utils import timezone
from django.db import models
from django.contrib.auth.models import AbstractUser, UserManager



# Create your models here.
class MyUserManager(UserManager):
    pass


class MyUser(AbstractUser):
    created_date = models.DateTimeField(editable=False)
    modified_date = models.DateTimeField()
    nickname = models.CharField(max_length=28)
    google_location = models.CharField(max_length=100)
    auth_token = models.CharField(max_length=100)

    # like relation
    like_relation = models.ManyToManyField('self', symmetrical=False
                                        , related_name='follower_set_users'
                                        , through='Like_Relationship')

    # image - connected with the collecion.image class
    # hashtag - connected with the collection.hash_tag class


    def save(self, *args, **kwargs):
        if not self.id:
            self.created_date = timezone.now()
        self.modified_date = timezone.now()
        return super(MyUser, self).save(*args, **kwargs)


    def __str__(self):
        return self.get_full_name()



class Like_Relationship(models.Model):
    follower = models.ForeignKey(MyUser, related_name='relationship_follower')
    followee = models.ForeignKey(MyUser, related_name='relationship_followee')
    created_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('follower','followee')

    def __str__(self):
        return '{follower} {followee}'.format(followee=self.followee.get_full_name(), follower = self.follower.get_full_name())

