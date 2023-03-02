# import admin
from django.contrib     import admin

# import needed model/s
from . models           import Task, Note

# register the Task model to admin interface
@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    # list the fields to display
    list_display = ('title', 'description', 'status', 'is_active')

@admin.register(Note)
class NoteAdmin(admin.ModelAdmin):
    list_display = ('title', 'description', 'created', 'modified')
