from django.contrib import admin

from .models import User, Location, Dong, TacoEntrance

admin.site.register(User)
admin.site.register(Location)
admin.site.register(Dong)
admin.site.register(TacoEntrance)