from django.contrib import admin

from services.departments.models import Course, Department, Facility


class DepartmentAdmin(admin.ModelAdmin):
    list_display = ('name', 'is_lab')


class CourseAdmin(admin.ModelAdmin):
    model = Course
    list_display = ('name', 'start_year', 'end_year', 'duration')


class FacilityAdmin(admin.ModelAdmin):
    model = Facility
    list_display = ('name',)


admin.site.register(Department, DepartmentAdmin)
admin.site.register(Course, CourseAdmin)
admin.site.register(Facility, FacilityAdmin)
