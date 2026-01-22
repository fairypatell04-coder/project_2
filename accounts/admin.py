from django.contrib import admin
from .models import Profile

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'bio', 'image')  # fields in the Profile model
    search_fields = ('user__username',)      # must be a tuple/list
    list_filter = ()                         # no extra fields yet
