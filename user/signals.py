from django.dispatch import receiver
from .roles_config import ROLES_CONFIG
from django.db.models.signals import post_migrate
from django.contrib.auth.models import Group, Permission

@receiver(post_migrate)
def create_roles_and_permissions(sender, **kwargs):
    for role_name, perms in ROLES_CONFIG.items():
        group, _ = Group.objects.get_or_create(name=role_name)
        for perm_codename in perms:
            perm = Permission.objects.filter(codename=perm_codename).first()
            if perm:
                group.permissions.add(perm)
