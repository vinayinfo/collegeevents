from django.contrib.contenttypes.models import ContentType
from django.core.urlresolvers import reverse
from django.http.response import Http404
from django.shortcuts import get_object_or_404

from sorl.thumbnail.shortcuts import get_thumbnail

from services.commons.models import UserParticipate
from services.feeds.models import Feed
# from services.multiuploader.models import MultiuploaderFileMapping
from users.models import UserProfile


def get_object_or_none(queryset, *filter_args, **filter_kwargs):
    """
    Same as Django's standard shortcut, but make sure to also raise 404
    if the filter_kwargs don't match the required types.
    """
    try:
        return get_object_or_404(queryset, *filter_args, **filter_kwargs)
    except (Http404, TypeError, ValueError):
        return None


def get_content_type_by_name(model):
    return get_object_or_none(ContentType, model=model)


def get_content_type(obj):
    return get_object_or_none(ContentType, model=obj.__class__.__name__.lower())


def join_count(obj):
    content_type = get_content_type(obj)
    return UserParticipate.objects.filter(content_type=content_type, object_id=obj.id).count()


def join_status(obj, user):
    content_type = get_content_type(obj)
    status = None
    if user:
        status = get_object_or_none(UserParticipate, content_type=content_type, object_id=obj.id, user=user)
        if status:
            status = status.status
    return status


def rate_instance(request, user, instance, score):
    if instance and score<=5 and score >=0:
        instance.rating.add(score=score, user=user, ip_address=request.META.get('REMOTE_ADDR'))
        return True
    return False


def get_avg_rating_and_total_feed(obj, rating):
    return ((obj.avg_rating*obj.total_feed)+int(rating))/(obj.total_feed+1), obj.total_feed+1


def get_all_feeds(obj):
    content_type = get_content_type(obj)
    return Feed.objects.filter(content_type=content_type, object_id=obj.id).order_by('-updated_at')


def get_all_users(obj):
    content_type = get_object_or_none(ContentType, model=obj.__class__.__name__.lower())
    user_ids = UserParticipate.objects.filter(content_type=content_type, object_id=obj.id).values_list('user_id', flat=True)
    return UserProfile.objects.filter(id__in=user_ids)


def get_join(user, obj, status):
    content_type = get_object_or_none(ContentType, model=obj.__class__.__name__.lower())
    class_name = content_type.model_class()
    obj = get_object_or_none(class_name, id=obj.id)
    data = {'user': user, 'event': obj, 'status': status}
    return data


def get_static_data(obj):
    content_type = ContentType.objects.get(model=obj.__class__.__name__.lower())
    data = {
            'rating': int(obj.avg_rating),
            'review_count': Feed.objects.filter(content_type=content_type, object_id=obj.id).count(),
            'student_count': get_all_users(obj).filter(user_role__name='student').count(),
            'teacher_count': get_all_users(obj).filter(user_role__name='teacher').count(),
            'department_count': obj.institutedepartment_set.all().count(),
            'course_count': obj.institutedepartment_set.count(),
            'event_count': obj.events_set.count(),
            'event_participant_count': get_all_users(obj).count()
            }
    return data


def get_address(obj_address):
    return obj_address.formatted


def get_short_address(obj_address, json_address=None):
    city = state = country = ''
    if json_address:
        return {k: None if v == '' else v for k, v in obj_address.as_dict().items()}
    try:
        city = obj_address.locality.name
    except:
        pass
    try:
        state = obj_address.locality.state.name
    except:
        pass
    try:
        country = obj_address.locality.state.country.code
    except:
        pass
    address = city + ' ' + state + ' ' + country

    return address.strip()


def add_media(media_ids, instance, category=None, user=None):
    for media_id in media_ids:
        kwargs = {
                  'media_id': media_id,
                  'user_id': user.id if user.id else None,
                  'category': category,
                  'content_type': get_content_type(instance),
                  'object_id': instance.id
                  }
        MultiuploaderFileMapping.objects.create(**kwargs)


def add_rating(instance, user, category, data):
    from faker import Faker
    faker = Faker()
    instance.rating.add(data.get('rating'), data.get('user'), ip_address=faker.ipv4())
    content_object = instance.content_object
    content_object.avg_rating, content_object.total_feed = get_avg_rating_and_total_feed(content_object, data.get('rating'))
    content_object.save()
    add_media(data.get('media_ids'), instance, category=category, user=user)


def search_data(modle_name, **kwargs):
    return modle_name.objects.filter(**kwargs).distinct('name')


def participant(queryset, **kwargs):
    return get_object_or_none(queryset, **kwargs)


def get_profile_media(content_type, object_id):
    media_obj = get_object_or_none(MultiuploaderFileMapping, content_type_id=content_type, object_id=object_id)
    if media_obj:
        fl = media_obj.media
        result = {"files":  [{"id": str(fl.id),
                              "name": fl.filename,
                              "url": reverse('multiuploader_file_link', args=[fl.pk]),
                              "thumbnailUrl": get_thumbnail(fl.file, "180x100", quality=80).url,
                              "deleteUrl": reverse('multiuploader_file_link', args=[fl.pk]),
                              "deleteType":"DELETE", }]
                  }
        return result
