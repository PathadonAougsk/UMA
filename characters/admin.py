from django.contrib import admin

from .models import character, playable, skill, skill_assignment, support

# Register your models here.
# admin.site.unregister(character)
admin.site.register(playable)
admin.site.register(support)
admin.site.register(skill)
admin.site.register(skill_assignment)
