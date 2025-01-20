

# Create your models here.
from django.db import models

# Create your models here.
class Users_Publication(models.Model):
    user_name = models.CharField(max_length=100, default='')
    user_email = models.CharField(max_length=100, unique=True,default='')
    user_password = models.CharField(max_length=100, default='')
    user_category = models.CharField(max_length=50, default='')

    


class Publication(models.Model):
    main_author = models.CharField(max_length=255)
    title = models.CharField(max_length=500)
    year = models.IntegerField()
    cited_by = models.IntegerField()
    co_author = models.TextField()
    conference_journal = models.CharField(max_length=255, null=True, blank=True)
    domains = models.TextField()
    download_links = models.TextField()
