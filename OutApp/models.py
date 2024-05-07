from django.db import models

class OutExporter(models.Model):
    Id = models.CharField(max_length=500)
    OutUserCode = models.CharField(max_length=500)
    OutUserName = models.CharField(max_length=500)
    OutUserName1 = models.CharField(max_length=500)
    OutUserCRUEI = models.CharField(max_length=500)
    OutUserAddress = models.CharField(max_length=500)
    OutUserAddress1 = models.CharField(max_length=500)
    OutUserCity = models.CharField(max_length=500)
    OutUserSubCode = models.CharField(max_length=500)
    OutUserSub = models.CharField(max_length=500)
    OutUserPostal = models.CharField(max_length=500)
    OutUserCountry = models.CharField(max_length=500)
    TouchUser = models.CharField(max_length=500)
    TouchTime = models.CharField(max_length=500)
    Status = models.CharField(max_length=500)

    class Meta:
        db_table = 'OutExporter'