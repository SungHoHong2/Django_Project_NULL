from django.db import models
from django.utils import timezone
# Create your models here.

class SayTalk(models.Model):
    created_by = models.CharField(max_length=28)
    modified_by = models.CharField(max_length=28)
    created_date = models.DateTimeField(editable=False)
    modified_date = models.DateTimeField()
    title = models.CharField(max_length=100)
    content = models.TextField()
    is_parent = models.BooleanField(default=True)
    is_chat = models.BooleanField(default=False)
    flag = models.BooleanField(default=True)

    # like relation
    talk_relation = models.ManyToManyField('self', symmetrical=False
                                        , related_name='talk_set_relationship'
                                        , through='Talk_Relationship')

    def save(self, *args, **kwargs):
        if not self.id:
            self.created_date = timezone.now()
        self.modified_date = timezone.now()
        return super(SayTalk, self).save(*args, **kwargs)



class Talk_Relationship(models.Model):
    follower = models.ForeignKey(SayTalk, related_name='talk_follower')
    followee = models.ForeignKey(SayTalk, related_name='talk_followee')
    created_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('follower','followee')



class SayHistory(models.Model):
    say_talk = models.ForeignKey(SayTalk)
    content = models.TextField()
    created_by = models.CharField(max_length=28)
    created_date = models.DateTimeField(editable=False)
    requested_to = models.CharField(max_length=28)
    unopen_flag = models.BooleanField(default=True)
    flag = models.BooleanField(default=True)

    def save(self, *args, **kwargs):
        if not self.id:
            self.created_date = timezone.now()
        self.modified_date = timezone.now()
        return super(SayHistory, self).save(*args, **kwargs)

