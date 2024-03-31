from django.db import models


class User(models.Model):
    user_id = models.CharField(max_length=100, primary_key=True)
    room_id = models.CharField(max_length=100)

class Location(models.Model):
    id = models.AutoField(primary_key=True)
    address = models.CharField(max_length=100)
    longitude = models.FloatField()
    latitude = models.FloatField()

class Dong(models.Model):
    donger = models.ForeignKey(User, related_name='donger', on_delete=models.CASCADE)
    #donger = models.ForeignKey(User, on_delete=models.CASCADE)
    dongee = models.ForeignKey(User, related_name='dongee', on_delete=models.CASCADE)
    dong_time = models.DateTimeField(auto_now_add=True)
    dong_type = models.IntegerField(default=0)
    location = models.ForeignKey(Location, on_delete=models.CASCADE)

class TacoEntrance(models.Model):
    location = models.ForeignKey(Location, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    time = models.DateTimeField(auto_now_add=True)
    status = models.IntegerField(default=0) #0 for entering, 1 for leaving