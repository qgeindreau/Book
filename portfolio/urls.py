from django.contrib import admin
from django.urls import path, include
from .views import (
    homePage,
    projetsPage,
    projectDetail,
    search,
    handler404,
)

from django.conf import settings
from django.conf.urls.static import static


handler404 = handler404

urlpatterns = [

    path('', homePage, name='homePage'),
    path('projets/', projetsPage, name='projetsPage'),
    path('projets/<str:slug>/', projectDetail, name='projetDetail'),
    path('search/', search, name='search'),

    path('dashboard/', include('dashboard.urls')),
    path('admin/', admin.site.urls),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
