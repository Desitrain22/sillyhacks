from django.db import models


class Room(models.Model):
    room_id = models.CharField(max_length=100, primary_key=True)
    room_name = models.CharField(max_length=100)


class User(models.Model):
    user_id = models.CharField(max_length=100, primary_key=True)
    room_id = models.ForeignKey(Room, on_delete=models.CASCADE)


class Location(models.Model):
    id = models.AutoField(primary_key=True)
    address = models.CharField(max_length=100)
    longitude = models.FloatField()
    latitude = models.FloatField()


class Dong(models.Model):
    donger = models.ForeignKey(User, related_name="donger", on_delete=models.CASCADE)
    dongee = models.ForeignKey(User, related_name="dongee", on_delete=models.CASCADE)
    dong_time = models.DateTimeField(auto_now_add=True)
    dong_type = models.IntegerField(default=1)  # 1 for earned dong, -1 for used dong
    location = models.ForeignKey(Location, on_delete=models.CASCADE)

    def get_available_dongs(self, donger: str, dongee: str):
        donger = User.objects.get(user_id=donger)
        dongee = User.objects.get(user_id=dongee)
        dongs = Dong.objects.filter(donger=donger, dongee=dongee)
        sum_dong_type = dongs.aggregate(total_dong_type=models.Sum("dong_type"))[
            "total_dong_type"
        ]
        return sum_dong_type


class TacoEntrance(models.Model):
    location = models.ForeignKey(Location, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    time = models.DateTimeField(auto_now_add=True)
    status = models.IntegerField(default=0)  # 0 for entering, 1 for leaving

    def get_current_dongable(self):
        # Retrieve the most recent entry for each unique user
        most_recent_entries = (
            TacoEntrance.objects.filter(user_id=self.user_id)
            .order_by("-time")
            .distinct("user_id")
        )
        most_recent_entries = most_recent_entries.filter(status=0)
        return most_recent_entries
