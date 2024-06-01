from django import template

register = template.Library()

@register.filter
def active_count(videos):
    return videos.filter(status='active').count()