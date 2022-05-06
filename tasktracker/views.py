from django.shortcuts import render
from django.http import JsonResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from .serializers import *
from .models import *
from datetime import datetime

from django.db.models import Q

# Create your views here.


class IndexApi(APIView):
    def get(self, request):
        response = {
            "message": "Welcome To Project"
        }
        return Response(response)


class UserRegistrationView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            response = serializer.data
        else:
            response = serializer.errors
        return Response(response)


class UserListView(APIView):

    permission_classes = [AllowAny]

    def get(self, request):
        uuid = request.GET.get('uuid')
        if uuid:
            user = CustomUser.objects.filter(uuid=uuid).first()
            serializer = UserRegistrationSerializer(user)
            response = serializer.data
        else:
            user = CustomUser.objects.all()
            serializer = UserRegistrationSerializer(user, many=True)
            if user:
                response = serializer.data
            else:
                response = serializer.errors
        return Response(response)


class TeamListView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        uuid = request.GET.get('uuid')
        if uuid:
            team = Team.objects.filter(uuid=uuid).first()
            serializer = TeamSerializer(team)
        else:
            team = Team.objects.all()
            serializer = TeamSerializer(team, many=True)
        return Response(serializer.data)


class CreateTeamView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        data = request.data
        user = request.user
        user_role = list()
        try:
            name = data['name']
            while True:
                if not Team.objects.filter(name=name):
                    break
                else:
                    response = {
                        "status": "False",
                        "message": "This Name is Occupied. Try Another"
                    }
                    return Response(response)
            team = Team.objects.create(name=name, leader=user)
            user_role.append(UserRole(user=user, team=team, role="L"))
        except:
            response = {
                "status": "False",
                "message": "<name> field is required"
            }
            return Response(response)
        try:
            team_member = data['members']
            for i in team_member:
                member_user = CustomUser.objects.filter(username=i).first()
                team.team_members.add(member_user)
                user_role.append(UserRole(user=member_user, team=team, role="M"))
                team.save()
            response = {
                "status": "True",
                "messgae": f"team --> {team} is created with leader --> {request.user} and members --> {str(team_member)[1:-1]}"
            }

        except:
            response = {
                "status": "True",
                "messgae": f"team --> {team} is created with leader --> {request.user} and NO MEMBERS ARE ADDED"
            }
        bulk_user_create = UserRole.objects.bulk_create(user_role)
        return JsonResponse(response, safe=False)


class AddMemberView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        data = request.data
        not_members = []
        available_members = []
        try:
            team_name = data['team_name']
            members = data['members']
            print(team_name, members)
            team = Team.objects.filter(name=team_name, leader=request.user).first()
            if not team:
                response = {
                    "state": "False",
                    "message": "You are not the leader of this team"
                }
                return Response(response)
            else:
                for i in members:
                    user_members = CustomUser.objects.filter(username=i).first()
                    if user_members:
                        team.team_members.add(user_members)
                        available_members.append(i)
                    else:
                        not_members.append(i)
                response = {
                    "status": "True",
                    "data": f"{str(available_members)[1:-1]} has been added in team and {str(not_members)[1:-1]} are not present in database"
                }
                return Response(response)

        except:
            response = {
                "state": "False",
                "message": "field name <team_name> or <members> is empty"
            }
            return Response(response)


class RemoveMemberView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        data = request.data
        not_members = []
        available_members = []
        try:
            team_name = data['team_name']
            members = data['members']
            print(team_name, members)
            team = Team.objects.filter(name=team_name, leader=request.user).first()
            if not team:
                response = {
                    "state": "False",
                    "message": "You are not the leader of this team"
                }
                return Response(response)
            else:
                for i in members:
                    user_members = CustomUser.objects.filter(username=i).first()
                    if user_members:
                        team.team_members.remove(user_members)
                        available_members.append(i)
                    else:
                        not_members.append(i)
                response = {
                    "status": "True",
                    "data": f"{str(available_members)[1:-1]} has been removed in team and {str(not_members)[1:-1]} are not present in database"
                }
                return Response(response)

        except:
            response = {
                "state": "False",
                "message": "field name <team_name> or <members> is empty"
            }
            return Response(response)


class AllotTaskView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        data = request.data
        try:
            team_name = data['team_name']
            member = data['member']
            task_name = data['task']
            print(team_name, member)
            team = Team.objects.filter(name=team_name, leader=request.user).first()
            if not team:
                response = {
                    "state": "False",
                    "message": "You are not the leader of this team"
                }
                # return Response(response)
            else:
                user_member = CustomUser.objects.filter(username=member).first()
                if user_member:
                    if user_member not in team.team_members.all():
                        response = {
                            "status": "False",
                            "message": f"{member} is not in the team"
                        }
                    else:
                        old_task = Task.objects.filter(team=team, task_name=task_name, task_user=user_member).first()
                        if old_task:
                            response = {
                                "status": "True",
                                "message": f"{task_name} has already been assigned to {user_member}"
                            }
                            return Response(response)
                        else:
                            task = Task.objects.create(team=team, task_name=task_name, task_user=user_member)
                            response = {
                                "status": "True",
                                "message": f"{task_name} has been assigned to {user_member}"
                            }
                else:
                    response = {
                        "status": "True",
                        "data": f"can't find a user with username {member}"
                    }

        except:
            response = {
                "state": "False",
                "message": "missing field name <team> or <member> or <task>"
            }
        return Response(response)


class TaskListView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        user = request.user
        data = request.data
        try:
            team_name = data['team']
            team = Team.objects.filter(name=team_name).first()
            if not team:
                response = {
                    "status": "False",
                    "message": f"NO team with the name {team_name} found"
                }
                return Response(response)
            elif team and team.leader == user or user in team.team_members.all():
                task = Task.objects.filter(team=team)
                serializer = TaskSerializer(task, many=True)
                resposne = serializer.data
                return Response(resposne)
            else:
                response = {
                    "status": "False",
                    "message": f"You don't have permissions to look at task list"
                }
                return Response(response)
        except:
            response = {
                "status": "False",
                "message": "missing keyword <team>"
            }
            return Response(response)


class TaskStatusView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        data = request.data
        try:
            team_name = data['team_name']
            task_name = data['task']
            status = data['status']
            is_completed = data['is_completed']
            # team = Team.objects.filter(name=team_name, leader=request.user).first()

            task = Task.objects.filter(team__name=team_name, task_name=task_name, task_user=request.user).first()
            if task:
                task.status = status
                if is_completed == "True":
                    task.completed_at = datetime.now()
                    task.is_completed = True
                task.save()
                response = {
                    "state": "True",
                    "message": "Your Task status has been update"
                }
                return Response(response)

            else:
                response = {
                    "state": "False",
                    "message": "No Task Found"
                }

        except:
            response = {
                "state": "False",
                "message": "missing field name <team_name> or <task> or <status> or <is_completed>"
            }
        return Response(response)





