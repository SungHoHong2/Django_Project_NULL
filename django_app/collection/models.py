from django.db import models
from member.models import MyUser
from saytalk.models import SayTalk
from django.utils import timezone

# Create your models here.

class Image(models.Model):
    member = models.ForeignKey(MyUser, blank=True, null=True)
    say_talk = models.ForeignKey(SayTalk, blank=True, null=True)
    created_by = models.CharField(max_length=28)
    modified_by = models.CharField(max_length=28)
    created_date = models.DateTimeField(editable=False)
    modified_date = models.DateTimeField()
    img_order = models.IntegerField(default=1)
    img_file = models.ImageField(upload_to= 'img', blank=True, null=True)

    def save(self, *args, **kwargs):
        if not self.id:
            self.created_date = timezone.now()
        self.modified_date = timezone.now()
        return super(Image, self).save(*args, **kwargs)



class Hash_Tag(models.Model):
    created_by = models.CharField(max_length=28)
    modified_by = models.CharField(max_length=28)
    created_date = models.DateTimeField(editable=False)
    modified_date = models.DateTimeField()
    tag_name = models.CharField(max_length=28)
    flag = models.BooleanField(default=True)

    hash_relation_user = models.ManyToManyField(MyUser, symmetrical=False
                                        , related_name='hash_set_users'
                                        , through='Hash_Relationship')

    hash_relation_say = models.ManyToManyField(SayTalk, symmetrical=False
                                        , related_name='hash_set_say'
                                        , through='Hash_Relationship')

    def save(self, *args, **kwargs):
        if not self.id:
            self.created_date = timezone.now()
        self.modified_date = timezone.now()
        return super(Hash_Tag, self).save(*args, **kwargs)



class Hash_Relationship(models.Model):
    member = models.ForeignKey(MyUser, blank=True, null=True)
    hash_tag = models.ForeignKey(Hash_Tag, blank=True, null=True)
    say_talk = models.ForeignKey(SayTalk, blank= True, null=True)
    flag = models.BooleanField(default=True)




