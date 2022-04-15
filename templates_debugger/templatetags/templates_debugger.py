import json

from django import template
from django.template import Node
from faker import Faker
from django.apps import apps

register = template.Library()


def _is_enabled(context):
    for ctx_dict in context.dicts:
        if 'templates_debugger_enabled' in ctx_dict:
            return True
    return False


@register.simple_tag(takes_context=True)
def faked_var(context, var_name: str, generator: str):
    if not _is_enabled(context):
        return ''

    fake = Faker()
    context.dicts[0][var_name] = fake.__getattr__(generator)()
    return ''


@register.simple_tag(takes_context=True)
def faked_obj(context, var_name: str, json_obj: str):
    if not _is_enabled(context):
        return ''

    python_obj = json.loads(json_obj)
    context.dicts[0][var_name] = python_obj
    return ''


@register.simple_tag(takes_context=True)
def faked_queryset(context, var_name: str, queryset: str):
    if not _is_enabled(context):
        return ''

    parts = queryset.split(".")
    model_cls = apps.get_model(parts[0], parts[1])
    queryset = ".".join(parts[1:])

    lcl = locals()
    lcl[model_cls._meta.object_name] = model_cls
    exec(f"data = {queryset}")

    context.dicts[0][var_name] = lcl['data']
    return ''


class FakedVariableNode(Node):
    def __init__(self, var_name: str, generator_name: str):
        self.var_name = var_name
        self.generator_name = generator_name

    def render(self, context):
        if not _is_enabled(context):
            return ''

        fake = Faker()
        context.dicts[0][self.var_name] = fake.__getattr__(self.generator_name)()
        return ''
