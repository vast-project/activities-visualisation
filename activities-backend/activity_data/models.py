import hashlib
import urllib.parse
import uuid

import qrcode
from django.conf import settings
from django.contrib.auth.models import Group
from django.db import models

## RDF Graph...
from vast_rdf.vast_repository import RDFStoreVAST


class AutoUpdateTimeFields(models.Model):
    uuid              = models.UUIDField(default = uuid.uuid4, editable = False)
    created           = models.DateTimeField(auto_now_add=True, null=True)
    updated           = models.DateTimeField(auto_now=True, null=True)
    created_by        = models.ForeignKey(settings.AUTH_USER_MODEL, null=False, blank=False, on_delete=models.CASCADE)

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        ## Save the object in the django database...
        super().save(*args, **kwargs)
        ## Save the object in RDF Graph...
        rdf = RDFStoreVAST()
        rdf.save(type(self).__name__, self)
        del rdf

    def delete(self, *args, **kwargs):
        ## Delete the object from the RDF Graph...
        rdf = RDFStoreVAST()
        rdf.delete(type(self).__name__, self)
        del rdf
        super().delete(*args, **kwargs)


class VASTObject(AutoUpdateTimeFields):
    uuid              = models.UUIDField(default = uuid.uuid4, editable = False)
    name              = models.CharField(max_length=255, default=None)
    name_md5          = models.CharField(max_length=64,  default=None, null=True, blank=True, editable=False)
    description       = models.CharField(max_length=255, default=None, null=True, blank=True)
    name_local        = models.CharField(max_length=255, default=None, null=True, blank=True)
    description_local = models.CharField(max_length=255, default=None, null=True, blank=True)
    language_local    = models.ForeignKey('Language', on_delete=models.CASCADE, default=None, null=True, blank=True)
    created           = models.DateTimeField(auto_now_add=True, null=True)
    updated           = models.DateTimeField(auto_now=True, null=True)
    created_by        = models.ForeignKey(settings.AUTH_USER_MODEL, null=False, blank=False, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.name}'

    class Meta(AutoUpdateTimeFields.Meta):
        abstract = True

    def save(self, *args, **kwargs):
        if self.name and not self.name_md5:
            self.name_md5 = hashlib.md5(self.name.encode('utf-8')).hexdigest()
        super().save(*args, **kwargs)

class VASTObject_NameUnique(VASTObject):
    name              = models.CharField(max_length=255, default=None, unique=True, null=False, blank=False)
    class Meta(VASTObject.Meta):
        abstract = True

class VASTObject_NameUserGroupUnique(VASTObject):
    class Meta(VASTObject.Meta):
        abstract = True
        # Enforce a policy for the name to be unique (for each user)
        unique_together = [["name", "created_by"]]

class Language(AutoUpdateTimeFields):
    code              = models.CharField(max_length=6,   default=None, unique=True, null=False, blank=False)
    name              = models.CharField(max_length=255, default=None, unique=True, null=False, blank=False)
    description       = models.CharField(max_length=255, default=None, null=True, blank=True)
    def __str__(self):
        return f'{self.name}'

## Organisations...
class OrganisationType(VASTObject_NameUnique):
    pass

class Organisation(VASTObject_NameUserGroupUnique):
    type              = models.ForeignKey('OrganisationType', on_delete=models.CASCADE, null=False, blank=False)
    subtype           = models.ForeignKey('OrganisationType', on_delete=models.CASCADE, related_name='subtype', null=True, blank=True)
    location          = models.CharField(max_length=255, default=None, null=True, blank=True)
    # is_visitor        = models.CharField(max_length=3, choices=[('Yes','Yes'),('No','No')], default='Yes', null=False, blank=False)

class Class(VASTObject_NameUnique):
    pass

## Contexts...
class Context(VASTObject_NameUserGroupUnique):
    pass

## Activities...
class Nature(VASTObject_NameUnique):
    pass

class Activity(VASTObject_NameUserGroupUnique):
    class Meta(VASTObject_NameUserGroupUnique.Meta):
        verbose_name_plural = 'Activities'

class Stimulus(VASTObject_NameUserGroupUnique):
    uriref            = models.URLField(max_length=512, default=None, null=True, blank=True)
    stimulus_type     = models.CharField(max_length=16, choices=[('Document','Document'),('Segment','Segment'),('Image','Image'),('Audio','Audio'),('Video','Video'),('Tool','Tool')], null=False, blank=False)

    class Meta(VASTObject_NameUserGroupUnique.Meta):
        verbose_name_plural = 'Stimuli'

class ActivityStep(VASTObject_NameUserGroupUnique):
    activity          = models.ForeignKey('Activity',     on_delete=models.CASCADE, default=None, null=False, blank=False)
    stimulus          = models.ForeignKey('Stimulus',     on_delete=models.CASCADE, default=None, null=False, blank=False)

## Events...
class Event(VASTObject_NameUserGroupUnique):
    activity          = models.ForeignKey('Activity',     on_delete=models.CASCADE, null=False, blank=False)
    date              = models.DateTimeField(default=None, null=True, blank=True)
    date_from         = models.DateTimeField(default=None, null=True, blank=True)
    date_to           = models.DateTimeField(default=None, null=True, blank=True)
    context           = models.ForeignKey('Context',      on_delete=models.CASCADE, null=False, blank=False)
    host_organisation = models.ForeignKey('Organisation', on_delete=models.CASCADE, default=None, null=False, blank=False)
    language          = models.ForeignKey('Language',     on_delete=models.CASCADE, null=True, blank=True, related_name='event_language')
    nature            = models.ForeignKey('Nature',       on_delete=models.CASCADE, default=None, null=True, blank=True)
    education         = models.ForeignKey('Education',    on_delete=models.CASCADE, default=None, null=True, blank=True)

## Visitor fields...
class Age(VASTObject_NameUnique):
    pass
       
class Education(VASTObject_NameUserGroupUnique):
    pass

class Gender(VASTObject_NameUnique):
    pass

class Nationality(VASTObject_NameUnique):
    class Meta(VASTObject_NameUnique.Meta):
        verbose_name_plural = 'Nationalities'

# Visitors...
class VisitorGroup(VASTObject_NameUserGroupUnique):
    composition          = models.IntegerField(default=None, null=True, blank=True)
    event                = models.ForeignKey('Event',        on_delete=models.CASCADE, default=None, null=False, blank=False)
    education            = models.ForeignKey('Education',    on_delete=models.CASCADE, default=None, null=True,  blank=True)
    nationality          = models.ForeignKey('Nationality',  on_delete=models.CASCADE, default=None, null=True,  blank=True)
    mother_language      = models.ForeignKey('Language',     on_delete=models.CASCADE, default=None, null=True,  blank=True, related_name='visitor_group_language')
    visitor_organisation = models.ForeignKey('Organisation', on_delete=models.CASCADE, default=None, null=True,  blank=True)
    age                  = models.ForeignKey('Age',          on_delete=models.CASCADE, default=None, null=True,  blank=True)

class Visitor(VASTObject):
    userid               = models.CharField(max_length=255,  default=None, null=True, blank=True)
    age                  = models.ForeignKey('Age',          on_delete=models.CASCADE, default=None, null=True, blank=True)
    gender               = models.ForeignKey('Gender',       on_delete=models.CASCADE, default=None, null=True, blank=True)
    date_of_visit        = models.DateTimeField(default=None, null=True, blank=True)
    education            = models.ForeignKey('Education',    on_delete=models.CASCADE, default=None, null=True, blank=True)
    nationality          = models.ForeignKey('Nationality',  on_delete=models.CASCADE, default=None, null=True, blank=True)
    mother_language      = models.ForeignKey('Language',     on_delete=models.CASCADE, default=None, null=True, blank=True, related_name='mother_language')
    activity             = models.ForeignKey('Activity',     on_delete=models.CASCADE, default=None, null=False, blank=False)
    visitor_group        = models.ForeignKey('VisitorGroup', on_delete=models.CASCADE, default=None, null=False, blank=False)

## Products...
class ProductType(VASTObject_NameUnique):
    pass

class Product(VASTObject_NameUserGroupUnique):
    product_type         = models.ForeignKey('ProductType',  on_delete=models.CASCADE, default=None, null=False, blank=False)
    visitor              = models.ForeignKey('Visitor',      on_delete=models.CASCADE, default=None, null=False, blank=False)
    activity_step        = models.ForeignKey('ActivityStep', on_delete=models.CASCADE, default=None, null=False, blank=False)

    # We must generate a "unique" name
    def save(self, *args, **kwargs):
        if not self.name:
            self.name = ".".join([self.product_type.name, str(self.visitor.id), self.activity_step.name])
        super().save(*args, **kwargs)

## Statements...
class Concept(VASTObject_NameUnique):
    pass

class Predicate(VASTObject_NameUnique):
    pass

class Statement(VASTObject_NameUserGroupUnique):
    product              = models.ForeignKey('Product',   on_delete=models.CASCADE, default=None, null=False, blank=False)
    subject              = models.ForeignKey('Concept',   on_delete=models.CASCADE, default=None, null=False, blank=False, related_name='subject')
    predicate            = models.ForeignKey('Predicate', on_delete=models.CASCADE, default=None, null=False, blank=False)
    object               = models.ForeignKey('Concept',   on_delete=models.CASCADE, default=None, null=False, blank=False, related_name='object')
     # We must generate a "unique" name
    def save(self, *args, **kwargs):
        if not self.name:
            self.name = ".".join([self.product.name, self.subject.name, self.predicate.name, self.object.name])
        super().save(*args, **kwargs)

class ProductStatement(VASTObject_NameUserGroupUnique):
    subject              = models.ForeignKey('Product',   on_delete=models.CASCADE, default=None, null=False, blank=False, related_name='ps_subject')
    predicate            = models.ForeignKey('Predicate', on_delete=models.CASCADE, default=None, null=False, blank=False, related_name='ps_predicate')
    object               = models.ForeignKey('Concept',   on_delete=models.CASCADE, default=None, null=False, blank=False, related_name='ps_object')
     # We must generate a "unique" name
    def save(self, *args, **kwargs):
        if not self.name:
            self.name = ".".join([self.subject.name, self.subject.name, self.predicate.name, self.object.name])
        super().save(*args, **kwargs)

## QR Codes...
class DigitisationApplication(VASTObject_NameUserGroupUnique):
    uriref               = models.URLField(max_length=255, null=False, blank=False)

class VisitorGroupQRCode(VASTObject):
    event                = models.ForeignKey('Event',        on_delete=models.CASCADE, default=None, null=False, blank=False)
    activity             = models.ForeignKey('Activity',     on_delete=models.CASCADE, default=None, null=False, blank=False)
    activity_step        = models.ForeignKey('ActivityStep', on_delete=models.CASCADE, default=None, null=False, blank=False)
    visitor_group        = models.ForeignKey('VisitorGroup', on_delete=models.CASCADE, default=None, null=False, blank=False)
    application          = models.ForeignKey('DigitisationApplication', on_delete=models.CASCADE, default=None, null=False, blank=False)
    qr_code              = models.ImageField(upload_to='qr_codes', default=None, null=True, blank=True)
    uriref               = models.URLField(max_length=255, null=True, blank=True)

    def save(self, *args, **kwargs):
        frontend_url = self.application.uriref # No need for check, this will be checked during application object creation...
        query = {
            'school':         self.visitor_group.visitor_organisation.name if self.visitor_group.visitor_organisation and self.visitor_group.visitor_organisation.name else None,
            'edulevel':       self.visitor_group.education.name            if self.visitor_group.education and self.visitor_group.education.name else None,
            'age':            self.visitor_group.age.name                  if self.visitor_group.age and self.visitor_group.age.name else None,
            'nationality':    self.visitor_group.nationality.name          if self.visitor_group.nationality and self.visitor_group.nationality.name else None,
            'language':       self.visitor_group.mother_language.name      if self.visitor_group.mother_language and self.visitor_group.mother_language.name else None,
            'eventid':        str(self.event.id),
            'activityid':     str(self.activity.id),
            'activitystepid': str(self.activity_step.id),
            'vgroupid':       str(self.visitor_group.id),
            'username':       str(self.created_by.username),
        }

        # Remove "None" values from query
        query = {k: v for k, v in query.items() if v is not None}

        self.uriref = urllib.parse.urljoin(frontend_url, '?' + urllib.parse.urlencode(query))
        if self.name and not self.name_md5:
            self.name_md5 = hashlib.md5(self.name.encode('utf-8')).hexdigest()
        qrcode_img = qrcode.make(self.uriref, version=1, box_size=4)
        self.qr_code.name = f'qr_codes/qr_code-{self.name_md5}.png'
        qrcode_img.save(self.qr_code.path)
        super().save(*args, **kwargs)
