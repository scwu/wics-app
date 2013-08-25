from django.db import models
from datetime import date
from django.forms.fields import DateField

# Create your models here.

class Event(models.Model):
  fb_url = models.URLField(verbose_name='Facebook Event Link')
  added = models.DateTimeField(auto_now_add=True)

  def __unicode__(self):
        return u'%s' % (self.fb_url)


class Opportunity(models.Model):
  name = models.CharField(max_length=500, verbose_name='Opportunity name')
  link = models.URLField()
  INTERN = 'INTERN'
  FULL = 'FULL'
  SCHOLARSHIP = 'SCHOLARSHIP'
  CONFERENCE = 'CONFERENCE'
  TYPE_OPP = (
    (INTERN, 'Internship'),
    (FULL, 'Full-time'),
    (SCHOLARSHIP, 'Scholarship'),
    (CONFERENCE, 'Conference'),
  )
  type_opp = models.CharField(max_length=20, choices=TYPE_OPP, default=INTERN)
  Y = 'Y'
  N = 'N'
  NA = 'NA'
  PAID = (
    (Y, 'Yes'),
    (N, 'No'),
    (NA, 'Not Applicable'),
  )
  paid = models.CharField(max_length=2, choices=PAID, default=Y)
  description = models.TextField()
  due = models.DateField(null=True, blank=True, verbose_name="Due Date", help_text=('Enter Date Format CCYY-MM-DD'))
  
  def __unicode__(self):
    return u'%s' % (self.name)

  def is_valid(self):
    date = self.cleaned_data['due']
    if date <= date.today():
      raise models.ValidationError("The date cannot be in the past")
    return date
