from django.contrib import admin

from registration.models import *

class TaskAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name', )}

class HabitAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name', )}


admin.site.register(CustomUser)
admin.site.register(Category)
admin.site.register(Reward)
admin.site.register(Task, TaskAdmin)
admin.site.register(Habit, HabitAdmin)
