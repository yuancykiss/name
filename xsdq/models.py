from django.db import models

# Create your models here.


class Surname(models.Model):
    class Meta:
        db_table = 'surname'

    id = models.IntegerField(primary_key=True, null=False)
    url = models.CharField(max_length=1024, null=True)
    surname = models.CharField(max_length=20, null=True)


class Name(models.Model):
    class Meta:
        db_table = 'name_copy'

    id = models.IntegerField(primary_key=True, null=False)
    name = models.CharField(max_length=50, null=True, unique=True)
    sex_girl = models.FloatField(null=True)
    sex_boy = models.FloatField(null=True)
    five_lines = models.CharField(max_length=50, null=True)
    three_talents = models.CharField(max_length=50, null=True)
    nums = models.IntegerField(null=True)
    sky = models.IntegerField(null=True)
    earth = models.IntegerField(null=True)
    human = models.IntegerField(null=True)
    total = models.IntegerField(null=True)
    wai = models.IntegerField(null=True)
    sky_parse = models.CharField(max_length=255, null=True)
    earth_parse = models.CharField(max_length=255, null=True)
    human_parse = models.CharField(max_length=255, null=True)
    total_parse = models.CharField(max_length=255, null=True)
    wai_parse = models.CharField(max_length=255, null=True)
