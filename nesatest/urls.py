from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from ninja import NinjaAPI
from .utils.auth import UserAuth
from user.views import user_api
from task.views import task_api
from dashboard import urls as dashboard_urls

api_v1 = NinjaAPI(version='1.0', auth=UserAuth())

api_v1.add_router('/user/', user_api)
api_v1.add_router('/tasks/', task_api)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', api_v1.urls),
    path('', include(dashboard_urls))
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)