from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("room", views.room, name="room"),
    path("check_user", views.check_user, name="check_user"),
    path(
        "get_actively_dongable",
        views.get_actively_dongable,
        name="get_actively_dongable",
    ),
    path("get_unloadable", views.get_unloadable, name="get_unloadable"),
    path("get_leaderboard", views.get_leaderboard, name="get_leaderboard"),
    path("get_dong_history", views.get_dong_history, name="get_dong_history"),
    path("set_dongable", views.set_dongable, name="set_dongable"),
    path("dong_by_api", views.dong_by_api, name="dong_by_api"),
    path("check_if_at_bell", views.check_if_at_bell, name="check_if_at_bell"),
]
