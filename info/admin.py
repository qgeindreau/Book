from django.contrib import admin
from .models import Project, Message, Information


admin.site.register(Information)
admin.site.register(Project)
admin.site.register(Message)
