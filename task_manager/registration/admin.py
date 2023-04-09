from django.contrib import admin

from registration.models import *

class TaskAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name', )}

class HabitAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name', )}

# Register your models here.
admin.site.register(CustomUser)
admin.site.register(Category)
admin.site.register(Achievement)
admin.site.register(Task, TaskAdmin)
admin.site.register(Habit, HabitAdmin)
