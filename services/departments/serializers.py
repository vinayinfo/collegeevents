from rest_framework import serializers

from services.departments.models import Course, Department, DepartmentCourse, Facility


class DepartmentCourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = DepartmentCourse
        fields = ('department', 'course')

    def create(self, validated_data):
        """
        Create and return a new `Snippet` instance, given the validated data.
        """
        return DepartmentCourse.objects.create(**validated_data)


class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = ('id', 'name', 'year',)

    def create(self, validated_data):
        """
        Create and return a new `Snippet` instance, given the validated data.
        """
        return Course.objects.create(**validated_data)


class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = ('id', 'name', 'is_lab',)

    def create(self, validated_data):
        """
        Create and return a new `Snippet` instance, given the validated data.
        """
        return Department.objects.create(**validated_data)


class FacilitySerializer(serializers.ModelSerializer):
    """
    """
    class Meta:
        model = Facility

    def create(self, validated_data):
        """
        Create and return a new `Snippet` instance, given the validated data.
        """
        return Facility.objects.create(**validated_data)
