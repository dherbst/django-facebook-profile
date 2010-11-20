django-facebook-profile
====

This app is designed to be used on Google AppEngine with the django helper to use facebook for the authentication method instead of Google Accounts or Google's Oauth.  

In settings.py in the MIDDLEWARE_CLASSES do not use

#    'django.contrib.auth.middleware.AuthenticationMiddleware',
instead use 
    'django_facebook_profile.middleware.FBProfileMiddleware',


and add 'django_facebook_profile' to your INSTALLED_APPS

For best results, you will want to use the modified version of the helper here: https://github.com/dherbst/google-app-engine-django



