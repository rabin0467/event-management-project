
from django.contrib import admin
from django.urls import path, include
from debug_toolbar.toolbar import debug_toolbar_urls
from django.shortcuts import redirect

urlpatterns = [
    path('admin/', admin.site.urls),
    path('events/', include("events.urls")),
    path("", lambda request:redirect("events/event-list/"))
]+debug_toolbar_urls()
