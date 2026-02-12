from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin
from django.contrib.auth.models import User

from .models import Profile, App, Review


class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False
    extra = 0


class UserAdmin(DjangoUserAdmin):
    inlines = [ProfileInline]
    list_display = ("username", "email", "is_staff", "is_active", "get_role")

    @admin.display(description="Role")
    def get_role(self, obj):
        return getattr(obj.profile, "role", "")

class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'role')

class AppAdmin(admin.ModelAdmin):
    list_display = ('name', 'developer', 'category', 'version', 'status')
    list_filter = ('category',)
    search_fields = ('name', 'developer__username')

class ReviewAdmin(admin.ModelAdmin):
    list_display = ('app', 'user', 'rating')

admin.site.unregister(User)
admin.site.register(User, UserAdmin)
admin.site.register(Profile, ProfileAdmin)
admin.site.register(App, AppAdmin)
admin.site.register(Review, ReviewAdmin)

