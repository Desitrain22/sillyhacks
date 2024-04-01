from django.db import models


class Room(models.Model):
    room_id = models.CharField(max_length=100, primary_key=True)
    room_name = models.CharField(max_length=100)


class User(models.Model):
    user_id = models.CharField(max_length=100, primary_key=True)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)


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

    def get_available_dongs(self, donger: User, dongee: User):
        dongs = Dong.objects.filter(donger=donger, dongee=dongee)
        sum_dong_type = dongs.aggregate(total_dong_type=models.Sum("dong_type"))[
            "total_dong_type"
        ]
        return sum_dong_type if type(sum_dong_type) == int else 0

    def get_dong_count_for_user(self, donger: User):
        dongs = Dong.objects.filter(donger=donger, dong_type=1)
        return dongs.count()

    def get_total_unloadable_dongs(self, donger: User):
        dongs = Dong.objects.filter(donger=donger)
        sum_dong_type = dongs.aggregate(total_dong_type=models.Sum("dong_type"))[
            "total_dong_type"
        ]
        return sum_dong_type

    def get_dong_history(self, donger: User):
        # get a history of claimed dongs
        dongs = Dong.objects.filter(donger=donger, dong_type=1)
        dong_list = []
        for dong in dongs:
            dong_list.append(
                {
                    "donger": dong.donger.user_id,
                    "dongee": dong.dongee.user_id,
                    "dong_time": dong.dong_time,
                    "dong_type": dong.dong_type,
                    "location": dong.location.address,
                }
            )
        return dong_list

class TacoEntryEvent(models.Model):
    location = models.ForeignKey(Location, on_delete=models.CASCADE)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    time = models.DateTimeField(auto_now_add=True)
    status = models.IntegerField(default=0)  # 0 for entering, 1 for leaving

    def get_recent_events(self, room: Room):
        # Get the most recent entries
        events = TacoEntryEvent.objects.filter(room=room)
        events = events.order_by("time")
        users = User.objects.filter(room=room)
        return [events.filter(user=user).last() for user in users]
    
    def get_last_user_entry(self, user: User):
        return TacoEntryEvent.objects.filter(user=user).order_by("time").last()