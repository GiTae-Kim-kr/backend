from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, Club

class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ('email', 'student_id', 'department', 'phone', 'name', 'is_staff', 'is_active')
    list_filter = ('is_staff', 'is_active')
    fieldsets = (
        (None, {'fields': ('email', 'student_id', 'department', 'phone', 'name', 'password')}),
        ('Permissions', {'fields': ('is_staff', 'is_active', 'is_superuser', 'groups', 'user_permissions')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'student_id', 'department', 'phone','name', 'password1', 'password2', 'is_staff', 'is_active')}
        ),
    )
    search_fields = ('email',)
    ordering = ('email',)

admin.site.register(CustomUser, CustomUserAdmin)

@admin.register(Club)
class ClubAdmin(admin.ModelAdmin):
    list_display = ('name', 'leader', 'advisor', 'max_members', 'current_members')
    search_fields = ('name', 'leader__email', 'advisor')
    list_filter = ('advisor',)
