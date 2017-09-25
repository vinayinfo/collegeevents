# CELERY SETTINGS
CELERY_IMPORTS = (
                  "services.celerytasks.institutes",
                  "services.celerytasks.events",
                  "services.utils.tasks",
                  )
BROKER_URL = 'redis://localhost:6379/0'
CELERY_ACCEPT_CONTENT = ['json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
