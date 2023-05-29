from admin.settings import *
import mongomock
import mongoengine

# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'djongo',
        'NAME': 'quiz_app',
        'ENFORCE_SCHEMA': False,
        'CLIENT': {
            'host': "mongodb://localhost:27017/"
        }
    }
}

mongoengine.register_connection(alias='default', name='quiz_app',
                                host='mongodb://localhost:27017/',
                                mongo_client_class=mongomock.MongoClient)
