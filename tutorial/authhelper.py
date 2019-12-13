import requests
from urllib.parse import quote, urlencode
import base64
import json
import time


client_id = '68c64aa5-153d-418a-ab53-3129899577a1'
client_secret = 'B-AP=v:zUjitZ5GZ:j6E8V3c5qAaKovl'
authority = 'https://login.microsoftonline.com'
authorize_url = '{0}{1}'.format(authority, '/common/oauth2/v2.0/authorize?{0}')
token_url = '{0}{1}'.format(authority, '/common/oauth2/v2.0/token')
scopes = [ 'openid',
           'offline_access',
           'User.Read',
           'Mail.Read',
           'Contacts.Read' ]

def get_signin_url(redirect_uri):
  params = { 'client_id':'68c64aa5-153d-418a-ab53-3129899577a1',
             'redirect_uri': redirect_uri,
             'response_type': 'code',
             'scope': ' '.join(str(i) for i in scopes)
            }
  signin_url = authorize_url.format(urlencode(params))
  return signin_url


def get_token_from_code(auth_code, redirect_uri):
  post_data = { 'grant_type': 'authorization_code',
                'code': auth_code,
                'redirect_uri': redirect_uri,
                'scope': ' '.join(str(i) for i in scopes),
                'client_id': client_id,
                'client_secret': client_secret
              }
  r = requests.post(token_url, data = post_data)
  try:
    return r.json()
  except:
    return 'Error retrieving token: {0} - {1}'.format(r.status_code, r.text)

def get_token_from_refresh_token(refresh_token, redirect_uri):
  post_data = { 'grant_type': 'refresh_token',
                'refresh_token': refresh_token,
                'redirect_uri': redirect_uri,
                'scope': ' '.join(str(i) for i in scopes),
                'client_id': client_id,
                'client_secret': client_secret
              }
  r = requests.post(token_url, data = post_data)
  try:
    return r.json()
  except:
    return 'Error retrieving token: {0} - {1}'.format(r.status_code, r.text)

def get_access_token(request, redirect_uri):
    current_token = request.session['access_token']
    expiration = request.session['token_expires']
    now = int(time.time())
    if (current_token and now < expiration):
        return current_token
    else:
        refresh_token = request.session['refresh_token']
        new_tokens = get_token_from_refresh_token(refresh_token, redirect_uri)
        expiration = int(time.time()) + new_tokens['expires_in'] - 300
        request.session['access_token'] = new_tokens['access_token']
        request.session['refresh_token'] = new_tokens['refresh_token']
        request.session['token_expires'] = expiration
        return new_tokens['access_token']


