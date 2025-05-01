from django.contrib import admin
from .models import Material, Stock, Project, MaterialHistory, UserProfile

admin.site.register(Material)
admin.site.register(Stock)
admin.site.register(Project)
admin.site.register(MaterialHistory)
admin.site.register(UserProfile)