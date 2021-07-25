from django.contrib import admin
from .models import Todo, Image


class TodoAdmin(admin.ModelAdmin):
    readonly_fields = ('created',)
    list_display = ['title', 'datecompleted', 'user']


class ImageAdmin(admin.ModelAdmin):
    list_display = ['photo', 'date','user']


admin.site.register(Todo, TodoAdmin)
admin.site.register(Image, ImageAdmin)
