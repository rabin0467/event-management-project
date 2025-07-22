from django.urls import path
from events.views import event_list,navbar, participants_list, event_details, events_by_category,create_event,update_event, delete_event

urlpatterns = [
    path('event-list/', event_list, name="event-list"),
    path('navbar/', navbar, name="navbar"),
    path('participants-list/', participants_list, name="participants-list"),
    path('event-details/<int:event_id>/', event_details, name="event-details"),
    path('events-by-category/<int:category_id>/',events_by_category, name='events-by-category'),
    path('create-event/',create_event, name='create-event' ),
    path('update-event/<int:event_id>/',update_event, name='update-event' ),
    path('delete-event/<int:event_id>/',delete_event, name='delete-event' )

]