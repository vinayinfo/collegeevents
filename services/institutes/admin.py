from django.contrib import admin

from services.institutes.models import Institute, InstituteType


class InstituteFacilityInlineAdmin(admin.TabularInline):
    model = Institute.facility.through


class InstituteDepartmentInlineAdmin(admin.TabularInline):
    model = Institute.department.through 



class InstituteTypeAdmin(admin.ModelAdmin):
    model = InstituteType
    list_display = ('name',)


class InstituteAdmin(admin.ModelAdmin):
    list_display = ('name', 'parent_name', 'city')
    inlines = (InstituteDepartmentInlineAdmin, InstituteFacilityInlineAdmin,)

    def parent_name(self, obj):
        if obj.parent:
            return obj.parent.name

    def city(self, obj):
        if obj.address:
            return obj.address

admin.site.register(InstituteType, InstituteTypeAdmin)
admin.site.register(Institute, InstituteAdmin)
