from django.template import Library

register = Library()

@register.inclusion_tag("profiles/profile_item.html")
def show_profile(profile):
    return {"profile": profile}