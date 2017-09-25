import random

from django.contrib.contenttypes.models import ContentType
from django.template.loader import render_to_string

from celery.app import shared_task

from services.departments.models import Department
from services.events.models import Events
from services.feeds.models import Feed
from services.institutes.models import Institute
from users.models import UserProfile


@shared_task
def add_institute_child_feed():
    content = ContentType.objects.get(model='institute')
    message = render_to_string('review_data.html')
    feed_objs = Feed.objects.all()
    # child feed
    for inst_id in Institute.objects.values_list('id', flat=True)[:50]:
        print(inst_id,)
        for user in UserProfile.objects.all()[:random.randrange(0, 30)]:
            feed = [Feed(from_user=user, content_type=content, object_id=inst_id, message=message, parent=feed) for feed in feed_objs for i in range(10)]
    Feed.objects.bulk_create(feed)
    feed = Feed.objects.all()


@shared_task
def add_institute_feed():
    content = ContentType.objects.get(model='institute')
    message = render_to_string('review_data.html')
    feed_objs = []
    # parent feed
    for inst_id in Institute.objects.values_list('id', flat=True)[:50]:
        print(inst_id,)
        for user in UserProfile.objects.all()[:random.randrange(0, 30)]:
            feed_objs.append(Feed(from_user=user, content_type=content,
                                  object_id=inst_id, message=message))

    Feed.objects.bulk_create(feed_objs)
    add_institute_child_feed.delay()


@shared_task
def add_department_child_feed():
    content = ContentType.objects.get(model='department')
    message = render_to_string('review_data.html')
    feed_objs = Feed.objects.filter(content_type=content)
    # child feed
    for depart_id in Department.objects.values_list('id', flat=True)[:50]:
        print(depart_id,)
        for user in UserProfile.objects.all()[:random.randrange(0, 30)]:
            feed = [Feed(from_user=user, content_type=content, object_id=depart_id, message=message, parent=feed) for feed in feed_objs for i in range(10)]
    Feed.objects.bulk_create(feed)


@shared_task
def add_department_feed():
    content = ContentType.objects.get(model='department')
    message = render_to_string('review_data.html')
    feed_objs = []
    # parent feed
    for depart_id in Department.objects.values_list('id', flat=True)[:50]:
        print(depart_id,)
        for user in UserProfile.objects.all()[:random.randrange(0, 30)]:
            feed_objs.append(Feed(from_user=user, content_type=content,
                                  object_id=depart_id, message=message))

    Feed.objects.bulk_create(feed_objs)
    add_department_child_feed.delay()


@shared_task
def add_event_child_feed():
    content = ContentType.objects.get(model='events')
    message = render_to_string('review_data.html')
    feed_objs = Feed.objects.filter(content_type=content)
    # child feed
    for event_id in Events.objects.values_list('id', flat=True)[:50]:
        print(event_id,)
        for user in UserProfile.objects.all()[:random.randrange(0, 30)]:
            feed = [Feed(from_user=user, content_type=content, object_id=event_id, message=message, parent=feed) for feed in feed_objs for i in range(10)]
    Feed.objects.bulk_create(feed)


@shared_task
def add_event_feed():
    content = ContentType.objects.get(model='events')
    message = render_to_string('review_data.html')
    feed_objs = []
    # parent feed
    for event_id in Events.objects.values_list('id', flat=True)[:50]:
        print(event_id,)
        for user in UserProfile.objects.all()[:random.randrange(0, 30)]:
            feed_objs.append(Feed(from_user=user, content_type=content,
                                  object_id=event_id, message=message))

    Feed.objects.bulk_create(feed_objs)
    add_event_child_feed.delay()


def add_feed():
    add_institute_feed.delay()
    add_department_feed.delay()
    add_event_feed.delay()
