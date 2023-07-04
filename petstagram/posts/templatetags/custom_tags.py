from django import template
from users_pet.models import Profile

register = template.Library()

@register.simple_tag
def is_subscribed(profile, user):
    profilee = Profile.objects.get(user = user.user)
    if profile in profilee.subscribed.all():
        return True
    return False