from django import template
import json

register = template.Library()

@register.inclusion_tag('includes/values_wheel.html')
def values_wheel(*args, **kwargs):
    # Define the values and their colors
    values = (
        {"name": "Self-direction",    "color": "#f00"},
        {"name": "Stimulation",       "color": "#f80"},
        {"name": "Hedonism",          "color": "#ff0"},
        {"name": "Achievement",       "color": "#8f0"},
        {"name": "Power",             "color": "#0f0"},
        {"name": "Security",          "color": "#0f8"},
        {"name": "Conformity",        "color": "#0ff"},
        {"name": "Tradition",         "color": "#08f"},
        {"name": "Benevolence",       "color": "#00f"},
        {"name": "Universalism",      "color": "#80f"}
    )
    context = {'values': json.dumps(values)}
    for arg in args:
        context.update(arg)

    context.update(kwargs)
    return context
