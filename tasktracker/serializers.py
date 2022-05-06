from .models import *
from rest_framework import serializers
from rest_framework.serializers import SerializerMethodField
from rest_framework.authtoken.models import Token


class UserRegistrationSerializer(serializers.ModelSerializer):
    token = SerializerMethodField()
    class Meta:
        model = CustomUser
        fields = ('uuid', 'token', 'username', 'first_name', 'last_name')

    def get_token(self, obj):
        user_token = Token.objects.filter(user=obj).first()
        return user_token.key


class TeamSerializer(serializers.ModelSerializer):
    team_leader = serializers.ReadOnlyField(source='leader.username')
    members = SerializerMethodField()

    class Meta:
        model = Team
        fields = ('uuid', 'name', 'team_leader', 'members')

    def get_members(self, obj):
        return [i.username for i in obj.team_members.all()]


class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = "__all__"

