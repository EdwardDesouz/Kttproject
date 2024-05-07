from django.db import models

class InNonImporter(models.Model):
    Code =  models.CharField(max_length=500)
    Name =  models.CharField(max_length=500)
    Name1 =  models.CharField(max_length=500)
    CRUEI =  models.CharField(max_length=500)
    TouchUser =  models.CharField(max_length=500)
    TouchTime =  models.CharField(max_length=500)
    Status =  models.CharField(max_length=500)

    class Meta:
        db_table = 'InNonImporter'
        managed = True