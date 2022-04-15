import os
import os.path

from django.apps import apps
from django.shortcuts import render
from django.views import View


class DirsView(View):
    def get(self, request, path: str, *args, **kwargs):
        parts = path.split("/")
        app = ".".join(parts[:-1])
        dir_name = parts[-1]
        app_config = next(filter(lambda c: c.name == app, apps.app_configs.values()))
        app_root = app_config.path
        template_dir = os.path.join(app_root, dir_name)

        template_list = []
        for base_dir, dirnames, filenames in os.walk(template_dir):
            for filename in filenames:
                template_list.append(os.path.join(base_dir, filename))

        return render(request, 'templates_debugger/dirs.html', context={
            'files': template_list
        })
