from django.urls import path
from events.views import event_list,navbar, event_details, events_by_category,create_event,update_event, delete_event, create_category, participants_list, update_category, delete_category, rsvp_event, organizer_dashboard,category_details 

urlpatterns = [
    path('event-list/', event_list, name="event-list"),
    path('navbar/', navbar, name="navbar"),
    path('event-details/<int:event_id>/', event_details, name="event-details"),
    path('events-by-category/',events_by_category, name='events-by-category'),
    path('create-event/',create_event, name='create-event' ),
    path('update-event/<int:event_id>/',update_event, name='update-event' ),
    path('delete-event/<int:event_id>/',delete_event, name='delete-event' ),
    path('create-category/', create_category, name='create-category'),
    path('category-details/<int:cat_id>/', category_details, name='category-details'),
    path('update-category/<int:category_id>/', update_category, name='update-category'),
    path('delete-category/<int:cat_id>/', delete_category, name='delete-category'),
    path('participants-list/', participants_list, name='participants-list'),
    path('rsvp-event/<int:event_id>', rsvp_event, name='rsvp-event'),
    path('organizer-dashboard/', organizer_dashboard, name='organizer-dashboard'),




]