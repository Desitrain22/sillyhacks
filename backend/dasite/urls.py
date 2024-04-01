from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("create_user", views.create_user, name="create_user"),
    path("create_room", views.create_room, name="create_room"),
    path("check_room", views.check_room, name="check_room"),
    path(
        "get_users_status_for_room",
        views.get_users_status_for_room,
        name="get_users_status_for_room",
    ),
    path("get_total_unloadable", views.get_total_unloadable, name="get_total_unloadable"),
    path("get_leaderboard", views.get_leaderboard, name="get_leaderboard"),
    path("get_dong_history", views.get_dong_history, name="get_dong_history"),
    path("dong_by_api", views.dong_by_api, name="dong_by_api"),
    path("check_if_at_bell", views.check_if_at_bell, name="check_if_at_bell"),
    path("get_loaded_dongs", views.get_loaded_dongs, name="get_loaded_dongs"),
    path("taco_entry_event", views.taco_entry_event, name="taco_entry_event")
]
