from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import ugettext_lazy as _

from users.forms import UserProfileChangeForm, UserProfileCreationForm
from users.models import UserProfile, UserRole


class UserProfileAdmin(UserAdmin):
    # The forms to add and change user instances

    # The fields to be used in displaying the User model.
    # These override the definitions on the base UserAdmin
    # that reference the removed 'username' field
    fieldsets = (
        (_('Login info'), {'fields': ('email', 'password')}),
        (_('Personal info'), {'fields': ('first_name', 'last_name', 'user_role',
                                         'gender', 'phone_number', 'address',)}),
        (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser',
                                       'groups', 'user_permissions')}),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2')}
        ),
    )
    form = UserProfileChangeForm
    add_form = UserProfileCreationForm
    list_display = ('id', 'email', 'first_name', 'last_name', 'user_role', 'is_staff')
    search_fields = ('id', 'email',)
#     inlines = (ImageInlineAdmin,)
    ordering = ('email',)

    def user_role(self, obj):
        if obj.user_role:
            return obj.user_role.name
        return None



class UserRoleAdmin(admin.ModelAdmin):
    fieldsets = (
        (_('User Role'), {'fields': ('name',)}),
    )

admin.site.register(UserProfile, UserProfileAdmin)
admin.site.register(UserRole, UserRoleAdmin)
