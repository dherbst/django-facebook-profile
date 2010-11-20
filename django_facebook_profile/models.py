from django.contrib.auth.models import User
from google.appengine.ext import db
from appengine_django.models import BaseModel
from django.contrib.auth.models import AnonymousUser, User
import settings
import facebook
import logging

FACEBOOK_APP_ID = settings.FACEBOOK_APP_ID
FACEBOOK_APP_SECRET = settings.FACEBOOK_APP_SECRET


class FacebookProfile(BaseModel):
    """
    Links the django.contrib.auth.user with a facebook profile.
    """
    
    user = db.ReferenceProperty(User, required=True)
    uid = db.StringProperty(required=True)

    class Meta:
        db_table = "djfbp_facebook_profile"
        ordering = ('user', )

    def __unicode__(self):
        return u"%s - %s" % (user.username, uid)

    @classmethod
    def get_djangouser(cls, request):
        """
        Given the facebook uid, return the django user
        """
        # check to see if the user is logged into Facebook for this site
        cookie = facebook.get_user_from_cookie(request.COOKIES, FACEBOOK_APP_ID, FACEBOOK_APP_SECRET)
        logging.info("FacebookProfile.get_djangouser cookie=%s" % cookie)
        if cookie:
            uid = cookie['uid']
            logging.info("FacebookProfile.get_djangouser cookie[uid]=%s" % uid)
            fbprofile = cls.all().filter("uid =", uid).get()
            if fbprofile is None:
                # we have not see this user before, connect them to a django user
                user = User()
                user.save()
                fbprofile = FacebookProfile(uid=uid, user=user)
                fbprofile.save()
            return fbprofile.user

        else:
            return AnonymousUser()
