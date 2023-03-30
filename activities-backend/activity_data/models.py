from django.db import models
from datetime import datetime

class AutoUpdateTimeFields(models.Model):
    created     = models.DateTimeField(auto_now_add=True)
    updated     = models.DateTimeField(auto_now=True)
    class Meta:
        abstract = True


class VASTObject(AutoUpdateTimeFields):
    name              = models.CharField(max_length=255, default=None)
    description       = models.CharField(max_length=255, default=None, null=True, blank=True)
    name_local        = models.CharField(max_length=255, default=None, blank=True)
    description_local = models.CharField(max_length=255, default=None, blank=True)
    language_local    = models.ForeignKey('Language', on_delete=models.DO_NOTHING, default=None, null=True, blank=True)

    created     = models.DateTimeField(auto_now_add=True)
    updated     = models.DateTimeField(auto_now=True)
    def __str__(self):
        return f'{self.name}'

    class Meta:
        abstract = True

## Organisations...
class OrganisationType(VASTObject):
    pass

class Organisation(VASTObject):
    type      = models.ForeignKey('OrganisationType', on_delete=models.DO_NOTHING)
    subtype   = models.ForeignKey('OrganisationType', on_delete=models.DO_NOTHING, related_name='subtype', null=True, blank=True)
    location  = models.CharField(max_length=255, default=None)

class Class(VASTObject):
    pass

class Event(VASTObject):
    pass

class Stimulus(VASTObject):
    class Meta:
        verbose_name_plural = 'Stimuli'

class Product(VASTObject):
    pass

class Context(VASTObject):
    pass

class Language(AutoUpdateTimeFields):
    code              = models.CharField(max_length=6,   default=None)
    name              = models.CharField(max_length=255, default=None)
    description       = models.CharField(max_length=255, default=None)
    def __str__(self):
        return f'{self.name}'

class Age(VASTObject):
    pass

class Gender(VASTObject):
    pass

class Education(VASTObject):
    pass

class Nationality(VASTObject):
    pass

class Nature(VASTObject):
    pass

class ActivityStep(VASTObject):
    stimulus    = models.ForeignKey('Stimulus',     on_delete=models.DO_NOTHING)
    product     = models.ForeignKey('Product',      on_delete=models.DO_NOTHING)

class Activity(VASTObject):
    event       = models.ForeignKey('Event',        on_delete=models.DO_NOTHING)
    date        = models.DateTimeField()
    step        = models.ForeignKey('ActivityStep', on_delete=models.DO_NOTHING)
    context     = models.ForeignKey('Context',      on_delete=models.DO_NOTHING)
    language    = models.ForeignKey('Language',     on_delete=models.DO_NOTHING, related_name='activity_language')
    nature      = models.ForeignKey('Nature',       on_delete=models.DO_NOTHING)
    class Meta:
        verbose_name_plural = 'Activities'

# Users...
class UserType(VASTObject):
    pass

class User(AutoUpdateTimeFields):
    type            = models.ForeignKey('UserType', on_delete=models.DO_NOTHING)
    name            = models.CharField(max_length=255, default=None, null=True, blank=True)
    useid           = models.CharField(max_length=255, default=None, null=True, blank=True)
    age             = models.ForeignKey('Age', on_delete=models.DO_NOTHING, default=None, null=True, blank=True)
    gender          = models.ForeignKey('Gender', on_delete=models.DO_NOTHING, default=None, null=True, blank=True)
    education       = models.ForeignKey('Education', on_delete=models.DO_NOTHING, default=None, null=True, blank=True)
    nationality     = models.ForeignKey('Nationality', on_delete=models.DO_NOTHING, default=None, null=True, blank=True)
    motherLanguage  = models.ForeignKey('Language', on_delete=models.DO_NOTHING, default=None, null=True, blank=True)
    activity        = models.ForeignKey('Activity', on_delete=models.DO_NOTHING, default=None, null=True, blank=True)
    group           = models.ForeignKey('Group', on_delete=models.DO_NOTHING, default=None, null=True, blank=True)

class Group(VASTObject):
    organisation    = models.ForeignKey('Organisation', on_delete=models.DO_NOTHING, default=None, null=True, blank=True)
    age             = models.ForeignKey('Age', on_delete=models.DO_NOTHING, default=None, null=True, blank=True)
