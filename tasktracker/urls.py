from django.urls import path
from . import views

urlpatterns = [
    path('', views.IndexApi.as_view(), name="index"),
    path('register/', views.UserRegistrationView.as_view(), name="register"),
    path('userlist/', views.UserListView.as_view(), name="userlist"),
    path('teamlist/', views.TeamListView.as_view(), name="teamlist"),
    path('createteam/', views.CreateTeamView.as_view(), name="createteam"),
    path('addmember/', views.AddMemberView.as_view(), name="addmember"),
    path('removemember/', views.RemoveMemberView.as_view(), name="removemember"),
    path('allot_task/', views.AllotTaskView.as_view(), name="allot_task"),
    path('task_list/', views.TaskListView.as_view(), name="task_list"),
    path('task_status/', views.TaskStatusView.as_view(), name="task_status"),
]