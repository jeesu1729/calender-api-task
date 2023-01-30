from django.urls import path

from api.views import *

urlpatterns = [
    path('', HomeView.as_view(), name='homeview'),
    path('GoogleCalendarInitView/', GoogleCalendarInitView.as_view(), name='googlecalendarinitview'),
    path('GoogleCalendarRedirectView/', GoogleCalendarRedirectView.as_view(), name='googlecalendarredirectview'),
]