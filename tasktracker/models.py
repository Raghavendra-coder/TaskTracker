from django.db import models
import uuid
from django.contrib.auth.models import AbstractUser
import string, random
from django.conf import settings
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token
# Create your models here.

ROLES = [
    ('L', 'Leader'),
    ('M', 'Member'),
]

class CustomUser(AbstractUser):
    uuid = models.UUIDField(primary_key=True, max_length=36, default=uuid.uuid4, editable=False)

    def __str__(self):
        return self.username



@receiver(post_save, sender=CustomUser)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)


class Team(models.Model):
    uuid = models.UUIDField(max_length=36, default=uuid.uuid4, primary_key=True, editable=False)
    name = models.CharField(max_length=25)
    leader = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="team_leader", null=True, blank=True)
    team_members = models.ManyToManyField(CustomUser, related_name="team_member", null=True, blank=True)

    def __str__(self):
        return self.name


class Task(models.Model):
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, max_length=36, editable=False)
    team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name="task")
    task_name = models.CharField(max_length=200)
    task_user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="user_task")
    status = models.CharField(max_length=200, null=True, blank=True)
    started_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_completed = models.BooleanField(default=False)
    completed_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.task_name


class UserRole(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="UserRole_user")
    team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name="UserRole_team")
    role = models.CharField(max_length=1, choices=ROLES)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['user', 'team', 'role'], name='A User can only have one role in a Team')
        ]


    def __str__(self):
        return f'{self.user}  has  {self.role} role in {self.team} team'




