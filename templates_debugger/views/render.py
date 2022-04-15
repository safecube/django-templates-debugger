import os
import os.path

from django.shortcuts import render
from django.template.base import VariableNode
from django.template.loader import get_template
from django.template.loader_tags import IncludeNode
from django.views import View


class RenderView(View):
    def get(self, request, path: str, *args, **kwargs):
        template = get_template(path)
        variables = template.template.nodelist.get_nodes_by_type(VariableNode)
        includes = template.template.nodelist.get_nodes_by_type(IncludeNode)
        return render(request, path, context={
            'templates_debugger_enabled': True
        })
