# Create your views here.
#HP Django stuff
from django import forms
from django.shortcuts import render_to_response, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.template import RequestContext
from django.core.mail import send_mail
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.db.models import Q
from django.core.mail import EmailMessage

#HP app-specific stuff
from app.models import *
from app.forms import *
import settings, urls
import urllib
import urllib2
import re

#HP everything else (these are usually useful)
import os, sys, datetime, json
from datetime import date
# from bootstrap.forms import BootstrapModelForm, Fieldset

#HP:
def hackpackify(request, context):
  '''
  Updates a view's context to include variables expected in base.html
  Intended to make boilerplate info conveyance and menu bars quick and easy.
  and returns a RequestContext of the resulting dict (which is usually better).

  CHANGE EVERYTHING IN THIS!
  '''
  pages = []
  for urlpat in urls.urlpatterns:
    if urlpat.__dict__.__contains__('name'):
      if '(' not in urlpat.regex.pattern:
        pages.append({'name':urlpat.name, 'url':urlpat.regex.pattern.replace('^','/').replace('$','')})

  #HP project_name is used in navbar, copyright (footer), about page, and <title>
  project_name = "WiCS @ UPenn"

  #HP project_description is used in <meta name="description"> and the about page.
  project_description = "Women in Computer Science Organization at the University of Pennsylvania."

  #HP Founder information is in popups linked from the footers, the about page, and <meta name="author">
  hackpack_context = {
      'pages': pages,
      'project_name': project_name,
      'project_description': project_description,
      }
  if not context.__contains__('hackpack'):
    #HP add the hackpack dict to the page's context
    context['hackpack'] = hackpack_context

  return RequestContext(request, context) #HP RequestContext is good practice. (I think).

def index(request):
  context = {
    'thispage': 'Home', #HP necessary to know which page we're on (for nav). Always spell the same as the 'Name' field in hackpackify()'s `pages` variable
  }
  return render_to_response('index.html', hackpackify(request, context))

def about(request):
  context = {
    'thispage':'About', #HP necessary to know which page we're on (for nav). Always spell the same as the 'Name' field in hackpackify()'s `pages` variable
  }
  return render_to_response('about.html', hackpackify(request, context))

def calendar(request):
  access='345148995606822|DZwQeXvfbnXR9PaNczKW2b-HNaY'
  events = Event.objects.all()
  list_events = []
  for e in events:
    txt = e.fb_url
    re1='.*?'	# Non-greedy match on filler
    re2='(\\d+)'	# Integer Number 1
    rg = re.compile(re1+re2,re.IGNORECASE|re.DOTALL)
    m = rg.search(txt)
    if m:
      url=m.group(1)
      params = urllib.urlencode({'access_token':access})
      f4=urllib.urlopen("https://graph.facebook.com/%s?%s" % (url, params))
      js = json.loads(f4.read())
      event = {'name' : js['name'],
        'description' : " ".join(js['description'].split()),
        'start_time' : js['start_time'].replace('T', ' '),
        'location' : js['location'],
        'url' : e.fb_url
      }
      if 'end_time' in js:
        event['end_time'] = js['end_time'].replace('T', ' ')
      list_events.append(event)
  context= {
      'thispage':'Events',
      'events':list_events,
  }
  return render_to_response('events.html', hackpackify(request, context))

def career(request):
  today = datetime.date.today()
  q = Opportunity.objects.filter(type_opp='INTERN')
  q = q.filter(Q(due__gt = today) | Q(due__isnull=True))
  q = q.order_by('-due')
  interns = q
  q = Opportunity.objects.filter(type_opp='FULL')
  q = q.filter(Q(due__gt = today) | Q(due__isnull=True))
  q = q.order_by('-due')
  full = q
  q = Opportunity.objects.filter(type_opp='SCHOLARSHIP')
  q = q.filter(Q(due__gt = today) | Q(due__isnull=True))
  q = q.order_by('-due')
  scholars = q
  q = Opportunity.objects.filter(type_opp='CONFERENCE')
  q = q.filter(Q(due__gt = today) | Q(due__isnull=True))
  q = q.order_by('-due')
  conf = q
  context = {
      'thispage' : 'Career',
      'internship' : interns,
      'full' : full,
      'scholars' : scholars,
      'conf' : conf,
  }
  return render_to_response('career.html', hackpackify(request, context))

def contact(request):
  if request.method == 'POST':
    form = ContactForm(request.POST)
    if form.is_valid():
      cd = form.cleaned_data
      message = ('Message: '+cd['message']+"\n"+
        "Company: "+ cd['company'] + "\n" +
        "URL: " + cd['url'])
      email = EmailMessage(
        cd['subject'],
        message,
        cd['email'],
        ['s.clara.wu@gmail.com', 'snehak@wharton.upenn.edu', 'johanna.m.martens@gmail.com'],
      )
      email.send()
      return HttpResponse('success')
  else:
    form = ContactForm(
      initial={}
    )
  context={
      'thispage':'Contact us',
      'form' : form,
  }
  return render_to_response('contact.html', hackpackify(request, context))

def photos(request):
  access='345148995606822|DZwQeXvfbnXR9PaNczKW2b-HNaY'
  params = urllib.urlencode({'limit':50, 'access_token':access})
  f=urllib.urlopen("https://graph.facebook.com/wicsatpenn/albums?%s" % params)
  js = json.loads(f.read())
  dictionary = js['data']
  list_albums = []
  for album in dictionary:
    params2 = urllib.urlencode({'access_token' : access})
    f2 = urllib.urlopen("https://graph.facebook.com/%s?%s" % (album['cover_photo'], params2))
    ph = json.loads(f2.read())
    info = {'id' : album['id'],
      'name' : album['name'],
      'photo' : ph['source'],
      'time' : album['updated_time'],
    }
    list_albums.append(info)
  context={
      'thispage':'Photos',
      'album' : list_albums,
  }
  return render_to_response('photos.html', hackpackify(request, context))

def photos_all(request, album_id):
  access='345148995606822|DZwQeXvfbnXR9PaNczKW2b-HNaY'
  id_album = album_id.strip()
  string = "https://graph.facebook.com/%s" % id_album
  f3 = urllib.urlopen(string + "/photos?access_token=%s" % access)
  allp = json.loads(f3.read())
  eachp = []
  dictionary2 = allp['data']
  for e in dictionary2:
    info2 = {
      'icon': e['images'][5]['source'],
      'source':e['source'],
    }
    eachp.append(info2)
  context={
      'thispage': 'Photos',
      'photos' : eachp,
  }
  return render_to_response('albums.html', hackpackify(request, context))

