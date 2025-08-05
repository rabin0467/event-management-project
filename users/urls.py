from django.urls import path
from users.views import sign_up, sign_in, sign_out, activate_user, admin_dashboard, assign_role, create_group, group_list,delete_group, delete_participants, rsvp_dashboard

urlpatterns = [
    path('sign-up/',sign_up, name='sign-up'),
    path('sign-in/',sign_in, name="sign-in"),
    path('sign-out/', sign_out, name='sign-out'),
    path('activate/<int:user_id>/<str:token>/', activate_user),
    path('admin/dashboard/', admin_dashboard, name="admin-dashboard"),
    path('admin/assign-role/<int:user_id>', assign_role, name="assign-role"),
    path('admin/create-group/', create_group, name='create-group'),
    path('admin/group-list/', group_list, name='group-list'),
    path('admin/delete-group/<int:group_id>/',delete_group, name='delete-group'),
    path('admin/delete-participant/<int:user_id>/', delete_participants, name='delete-participant'),
    path('user/rsvp-dashboard/', rsvp_dashboard, name='rsvp-dashboard')
]
