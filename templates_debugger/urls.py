from django.urls import path

from .views.dirs import DirsView
from .views.home import HomeView
from .views.render import RenderView

app_name = "templates_debugger"

urlpatterns = [
    path('', HomeView.as_view()),
    path('dirs/<path:path>', DirsView.as_view(), name='dirs'),
    path('render/<path:path>', RenderView.as_view(), name='render'),
]
