import fnmatch

from django.shortcuts import render
from django.template import Engine
from django.views import View

from ..settings import app_settings


class HomeView(View):
    def get(self, request, *args, **kwargs):
        engine = Engine.get_default()

        dirs = []
        for dir in engine.dirs:
            if fnmatch.fnmatch(dir, app_settings.MATCH_PATH):
                dirs.append(dir)

        return render(request, 'templates_debugger/index.html', context={
            'dirs': dirs
        })
