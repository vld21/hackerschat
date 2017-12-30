from __future__ import absolute_import, unicode_literals
import os
from celery import Celery, shared_task
from django.core.cache import cache
from django.conf import settings

# set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'boredhackers.settings')

app = Celery('boredhackers', broker=os.environ['redis_url'])

# Using a string here means the worker don't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object('django.conf:settings', namespace='CELERY')

# Load task modules from all registered Django app configs.
app.autodiscover_tasks()

@app.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    sender.add_periodic_task(settings.CELERY_TASK_INTERVAL, prune_redis_user_list.s(), name="Prune user list", expires=settings.CELERY_TASK_EXPIRES)
    sender.add_periodic_task(settings.CELERY_TASK_INTERVAL, broadcast_presence.s(), name="Broadcast presence", expires=settings.CELERY_TASK_EXPIRES)

@app.task
def prune_redis_user_list():
    import time
    user_list = cache.get('user_list')
    if user_list == None:
        user_list = list()
        cache.set('user_list', user_list)
    else:
        for item in user_list:
            if time.time() - item['last_seen'] > settings.LAST_SEEN_LIMIT :
                user_list.remove(item)
        cache.set('user_list', user_list)

@app.task
def broadcast_presence():
    from channels import Group
    import json
    user_list = cache.get('user_list')
    topic_users = {}
    topic_anon_count = {}
    topics = set()
    for user in user_list:
        topic_name = user['topic']
        topics.add(topic_name)
        if topic_name not in topic_users:
            topic_users[topic_name] = set()
        if user['username'] != None:
            topic_users[topic_name].add(user['username'])

        if topic_name not in topic_anon_count:
            topic_anon_count[topic_name] = 0
        if user['username'] == None:
            topic_anon_count[topic_name] += 1

    for topic_name in topics:
        Group(topic_name).send({
            'text': json.dumps({
                'type': 'presence',
                'payload': {
                    'channel_name': topic_name,
                    'members': list(topic_users[topic_name]),
                    'lurkers': topic_anon_count[topic_name],
                }
            })
        })