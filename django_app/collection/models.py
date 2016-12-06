import boto
from io import BytesIO
from boto.s3.connection import S3Connection
from django.db import models
from member.models import MyUser
from saytalk.models import SayTalk
from django.utils import timezone
from resizeimage import resizeimage
from urllib.request import urlopen
from PIL import Image as Image_PIL

from django.conf import settings

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

        rtn = super(Image, self).save(*args, **kwargs)
        _img_url = self.img_file.url

        _img_url = _img_url[_img_url.index('.com/')+5: len(_img_url)]

        print(self.img_file.url)
        print(_img_url.replace('/img/','/small/'))

        fp = urlopen(self.img_file.url)

        img = BytesIO(fp.read())
        im = Image_PIL.open(img)
        im2 = im.resize((100, 100), Image_PIL.NEAREST)
        out_im2 = BytesIO()
        im2.save(out_im2, 'PNG')

        conn = S3Connection(settings.AWS_ACCESS_KEY_ID, settings.AWS_SECRET_ACCESS_KEY)
        b = conn.get_bucket(settings.AWS_STORAGE_BUCKET_NAME)

        k = b.new_key(_img_url.replace('/img/','/small/'))
        k.set_contents_from_string(out_im2.getvalue())

        return rtn



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




