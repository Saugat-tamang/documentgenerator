import sys
from django.apps import AppConfig
from django.dispatch import receiver
from django.db.models.signals import post_migrate
from django.contrib.auth.models import Group, Permission

class UserConfig(AppConfig):
    name = 'user'
    def ready(self):
            from .roles_config import ROLES_CONFIG

            @receiver(post_migrate)
            def create_roles_and_permissions(sender, **kwargs):
                # Only run after all migrations, not just 'accounts'
                if 'migrate' not in sys.argv:
                    return
                for role_name, perms in ROLES_CONFIG.items():
                    group, _ = Group.objects.get_or_create(name=role_name)
                    for perm_codename in perms:
                        perm = Permission.objects.filter(codename=perm_codename).first()
                        if perm:
                            group.permissions.add(perm)
                        else:
                            print(f"Permission {perm_codename} does not exist yet.")