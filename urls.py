from django.contrib import admin
from django.urls import path

from accounts.views import login_view, registration_view, user_view
from drawings.views import omission_view, participant_view, drawing_view, drawings_view

urlpatterns = [
    path("admin/", admin.site.urls),
    path("login/", login_view),
    path("register/", registration_view),
    path("drawing/<str:id>", drawing_view),
    path("drawings/", drawings_view),
    path("participant/", participant_view),
    path("me/", user_view),
    path("omissions", omission_view),
]
