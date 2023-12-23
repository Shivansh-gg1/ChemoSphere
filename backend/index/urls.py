from django.contrib import admin
from django.urls import path, include
import home.views as homeViews
from .router import router

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls))
]
