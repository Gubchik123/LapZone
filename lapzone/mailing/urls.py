from django.urls import path

from . import views


app_name = "mailing"
urlpatterns = [
    path("create/", views.MailingCreateView.as_view(), name="create")
]
