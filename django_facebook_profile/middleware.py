# middleware to connect a fb user with django.contrib.auth.models.User
import logging
from django.contrib.auth.models import AnonymousUser, User
from django_facebook_profile.models import FacebookProfile
import settings
import facebook # requires the facebook/python-sdk

FACEBOOK_APP_ID = settings.FACEBOOK_APP_ID
FACEBOOK_APP_SECRET = settings.FACEBOOK_APP_SECRET

class LazyUser(object):
    def __get__(self, request, obj_type=None):
        if not hasattr(request, "_cached_user"):
            if settings.DEBUG:
                if request.session.get('logindebug',False):
                    self._cached_user = User.get("ag1tdXNpY2thbGVuZGFycgoLEgRVc2VyGAIM")
                else:
                    self._cached_user = AnonymousUser()
                return self._cached_user

            request._cached_user = FacebookProfile.get_djangouser(request)

        return request._cached_user


class FBProfileMiddleware(object):
    """
    Checks to see if the facebook user is logged in, if so performs the connection.
    """
    def process_request(self, request):
        request.__class__.user = LazyUser()
        return None
