from django.http import HttpResponse
from django.contrib.auth import login

from social.apps.django_app.utils import psa

from .tools import get_access_token

# When we send a third party access token to that view
# as a GET request with access_token parameter,
# python social auth communicate with
# the third party and request the user info to register or
# sign in the user. Magic. Yeah.
@psa('social:complete')
def register_by_access_token(request, backend):

    #try:
        token = request.GET.get('access_token')
        if backend == 'twitter':
            secret = request.GET.get('access_secret')
            token = {
               'oauth_token': token,
               'oauth_token_secret': secret
            }
        print token
        # here comes the magic
        user = request.backend.do_auth(token)
        if user:
            login(request, user)
            # that function will return our own
            # OAuth2 token as JSON
            return get_access_token(user)
        else:
            # If there was an error... you decide what you do here
            return HttpResponse("error")

    #except Exception as e:
        #return HttpResponse("Error: " + str(e))

