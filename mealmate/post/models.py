from django.db import models

class Post(models.Model):
    owner = models.TextField(blank=True, null=True)
    ownerName = models.CharField(max_length=30, null=False, blank=False, default="")
    where = models.TextField(blank=True, null=True)
    when = models.TextField(default='2024-04-09 12:08:00', blank=True, null=True)
    Note = models.TextField(default = "", blank=True, null=True)
    current_user_number = models.IntegerField(default=1, blank=True, null=True)
    current_users = models.TextField(default = [], blank=True, null=True)
    max_user_num = models.IntegerField(blank=True, null=True)

    class Meta:
        db_table = 'post'