from rest_framework.viewsets import ModelViewSet

from services.departments.models import Course, Department
from services.departments.serializers import CourseSerializer, DepartmentSerializer
from services.feeds.serializers import FeedSerializer
from services.institutes.models import InstituteDepartment
from services.institutes.serializers import InstituteDepartmentSerializer
from services.utils.mixins import ActionRatingFeedMixin


class DepartmentViewSet(ActionRatingFeedMixin, ModelViewSet):
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer
    self_class = Department
    serializer_action_classes = {'feeds': FeedSerializer}
    
    def get_queryset(self):
        queryset = self.queryset
        if self.kwargs.get('id'):
            queryset = queryset.filter(institute__id=self.kwargs.get('id')).order_by('-updated_at')
        return queryset


class CourseViewSet(ActionRatingFeedMixin, ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    self_class = Course
    serializer_action_classes = {'feeds': FeedSerializer}


class InstituteDepartmentViewSet(ActionRatingFeedMixin, ModelViewSet):
    queryset = InstituteDepartment.objects.all()
    serializer_class = InstituteDepartmentSerializer
    self_class = InstituteDepartment
    serializer_action_classes = {'feeds': FeedSerializer}
    
    def get_queryset(self):
        queryset = self.queryset
        if self.kwargs.get('id'):
            queryset = queryset.filter(institute__id=self.kwargs.get('id')).order_by('-updated_at')
        return queryset
