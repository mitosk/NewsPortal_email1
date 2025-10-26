from django.contrib.auth.models import Group, User
from django.db.models.signals import post_save
from django.dispatch import receiver

@receiver(post_save, sender=User)
def add_user_to_common(sender, instance, created, **kwargs):
    if created:
        group, _ = Group.objects.get_or_create(name='common')
        instance.groups.add(group)
