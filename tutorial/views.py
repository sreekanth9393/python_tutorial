from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from tutorial.authhelper import get_signin_url
from tutorial.outlookservice import get_me
from tutorial.authhelper import get_signin_url, get_token_from_code, get_access_token
from tutorial.outlookservice import get_me, get_my_messages
from tutorial.outlookservice import get_my_events
from tutorial.outlookservice import get_my_contacts


# Create your views here.
def home(request):
  return HttpResponse("Welcome to the tutorial.")
  redirect_uri = request.build_absolute_uri(reverse('tutorial:gettoken'))
  sign_in_url = get_signin_url(redirect_uri)
  context = {'signin_url': sign_in_url}
  return render(request,'home.html', context)

def gettoken(request):
  auth_code = request.GET['code']
  redirect_uri = request.build_absolute_uri(reverse('tutorial:gettoken'))
  token = get_token_from_code(auth_code, redirect_uri)
  access_token = token['access_token']
  user = get_me(access_token)
  refresh_token = token['refresh_token']
  expires_in = token['expires_in']
  expiration = int(time.time()) + expires_in - 300
  request.session['access_token'] = access_token
  request.session['refresh_token'] = refresh_token
  request.session['token_expires'] = expiration
  return HttpResponseRedirect(reverse('tutorial:mail'))

def events(request):
  access_token = get_access_token(request, request.build_absolute_uri(reverse('tutorial:gettoken')))
  if not access_token:
    return HttpResponseRedirect(reverse('tutorial:home'))
  else:
    events = get_my_events(access_token)
    context = { 'events': events['value'] }
    return render(request, 'events.html', context)

def mail(request):
  access_token = get_access_token(request, request.build_absolute_uri(reverse('tutorial:gettoken')))
  if not access_token:
    return HttpResponseRedirect(reverse('tutorial:home'))
  else:
    messages = get_my_messages(access_token)
    context = {'messages': messages['value']}
    return render(request, 'mail.html', context)

def contacts(request):
  access_token = get_access_token(request, request.build_absolute_uri(reverse('tutorial:gettoken')))
  if not access_token:
    return HttpResponseRedirect(reverse('tutorial:home'))
  else:
    contacts = get_my_contacts(access_token)
    context = { 'contacts': contacts['value'] }
    return render(request, 'contacts.html', context)












