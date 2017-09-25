from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from services.commons.models import UserParticipate
from services.commons.serializers import UserParticipateSerializer
from services.utils.utils import get_content_type_by_name, participant


class UserParticipateView(ModelViewSet):
    queryset = UserParticipate.objects.all()
    serializer_class = UserParticipateSerializer

    def list(self, request, *args, **kwargs):
        content_type = get_content_type_by_name(request.query_params.get('content_type')) 
        object_id = request.query_params.get('object_id')
        if content_type and object_id:
            data = {'user_id': request.user.id, 'content_type': content_type, 'object_id': object_id}
            serializer = self.get_serializer(participant(self.queryset, **data))
            return Response(serializer.data)
        return super(UserParticipateView, self).list(self, request, *args, **kwargs)
