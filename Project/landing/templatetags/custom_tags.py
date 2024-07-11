from django import template
from social.models import Notification

register = template.Library()

@register.inclusion_tag('social/show_notifications.html', takes_context=True)
def show_notifications(context):
    request_user = context['request'].user
    if request_user.is_authenticated:
        notifications = Notification.objects.filter(to_user=request_user).exclude(user_has_seen=True).order_by('-date')
    else:
        notifications = []
    return {'notifications': notifications}
