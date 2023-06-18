from django.db import models
from datetime import datetime
from django.conf import settings
import qrcode
from io import BytesIO
from django.core.files import File
from PIL import Image, ImageDraw
from django.contrib.auth.models import Group
import uuid
import hashlib

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

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        if self.name and not self.name_md5:
            self.name_md5 = hashlib.md5(self.name.encode('utf-8')).hexdigest()
        super().save(*args, **kwargs)

class VASTObject_NameUnique(VASTObject):
    name              = models.CharField(max_length=255, default=None, unique=True)
    class Meta:
        abstract = True

class VASTObject_NameUserGroupUnique(VASTObject):
    class Meta:
        abstract = True
        # Enforce a policy for the name to be unique (for each user)
        unique_together = [["name", "created_by"]]

class Language(AutoUpdateTimeFields):
    code              = models.CharField(max_length=6,   default=None, unique=True)
    name              = models.CharField(max_length=255, default=None, unique=True)
    description       = models.CharField(max_length=255, default=None)
    def __str__(self):
        return f'{self.name}'

## Organisations...
class OrganisationType(VASTObject_NameUnique):
    pass

class Organisation(VASTObject_NameUserGroupUnique):
    type              = models.ForeignKey('OrganisationType', on_delete=models.CASCADE)
    subtype           = models.ForeignKey('OrganisationType', on_delete=models.CASCADE, related_name='subtype', null=True, blank=True)
    location          = models.CharField(max_length=255, default=None)
    is_visitor        = models.CharField(max_length=3, choices=[('Yes','Yes'),('No','No')], default='Yes')

class Class(VASTObject_NameUnique):
    pass

##Activities - Data
class Event(VASTObject_NameUserGroupUnique):
    host_organisation = models.ForeignKey('Organisation', on_delete=models.CASCADE, default=None)

class Context(VASTObject_NameUserGroupUnique):
    pass

class Age(VASTObject_NameUnique):
    pass

class Gender(VASTObject_NameUnique):
    pass
         
class Education(VASTObject_NameUserGroupUnique):
    pass

class Nationality(VASTObject_NameUnique):
    class Meta:
        verbose_name_plural = 'Nationalities'

class Nature(VASTObject_NameUnique):
    pass

class Activity(VASTObject_NameUserGroupUnique):
    event             = models.ForeignKey('Event',        on_delete=models.CASCADE)
    date              = models.DateTimeField(default=None, null=True, blank=True)
    date_from         = models.DateTimeField(default=None, null=True, blank=True)
    date_to           = models.DateTimeField(default=None, null=True, blank=True)
    context           = models.ForeignKey('Context',      on_delete=models.CASCADE)
    language          = models.ForeignKey('Language',     on_delete=models.CASCADE, related_name='activity_language')
    nature            = models.ForeignKey('Nature',       on_delete=models.CASCADE)
    education         = models.ForeignKey('Education',    on_delete=models.CASCADE, default=None, null=True, blank=True)

    class Meta:
        verbose_name_plural = 'Activities'

class Stimulus(VASTObject_NameUserGroupUnique):
    uriref            = models.CharField(max_length=512, default=None, null=True, blank=True)
    stimulus_type     = models.CharField(max_length=16, choices=[('Document','Document'),('Segment','Segment'),('Image','Image'),('Audio','Audio'),('Video','Video'),('Tool','Tool')])

    class Meta:
        verbose_name_plural = 'Stimuli'

class ActivityStep(VASTObject_NameUserGroupUnique):
    activity          = models.ForeignKey('Activity',     on_delete=models.CASCADE, default=None)
    stimulus          = models.ForeignKey('Stimulus',     on_delete=models.CASCADE, default=None)

# Visitors...
class VisitorGroup(VASTObject_NameUserGroupUnique):
    composition          = models.IntegerField(default=None, null=True, blank=True)
    event                = models.ForeignKey('Event',        on_delete=models.CASCADE, default=None, null=True, blank=True)
    education            = models.ForeignKey('Education',    on_delete=models.CASCADE, default=None, null=True, blank=True)
    nationality          = models.ForeignKey('Nationality',  on_delete=models.CASCADE, default=None, null=True, blank=True)
    mother_language      = models.ForeignKey('Language',     on_delete=models.CASCADE, default=None, null=True, blank=True, related_name='visitor_group_language')
    visitor_organisation = models.ForeignKey('Organisation', on_delete=models.CASCADE, default=None, null=True, blank=True)
    age                  = models.ForeignKey('Age',          on_delete=models.CASCADE, default=None, null=True, blank=True)

class Visitor(VASTObject):
    userid            = models.CharField(max_length=255,  default=None, null=True, blank=True)
    age               = models.ForeignKey('Age',          on_delete=models.CASCADE, default=None, null=True, blank=True)
    gender            = models.ForeignKey('Gender',       on_delete=models.CASCADE, default=None, null=True, blank=True)
    date_of_visit     = models.DateTimeField(default=None, null=True, blank=True)
    education         = models.ForeignKey('Education',    on_delete=models.CASCADE, default=None, null=True, blank=True)
    nationality       = models.ForeignKey('Nationality',  on_delete=models.CASCADE, default=None, null=True, blank=True)
    mother_language   = models.ForeignKey('Language',     on_delete=models.CASCADE, default=None, null=True, blank=True, related_name='mother_language')
    activity          = models.ForeignKey('Activity',     on_delete=models.CASCADE, default=None, null=True, blank=True)
    group             = models.ForeignKey('VisitorGroup', on_delete=models.CASCADE, default=None, null=True, blank=True)
    school            = models.CharField(max_length=255,  default=None, null=True, blank=True)

class ProductType(VASTObject_NameUnique):
    pass

class Product(VASTObject_NameUserGroupUnique):
    product_type      = models.ForeignKey('ProductType',  on_delete=models.CASCADE, default=None)
    visitor           = models.ForeignKey('Visitor',      on_delete=models.CASCADE, default=None)
    activity_step     = models.ForeignKey('ActivityStep', on_delete=models.CASCADE, default=None)

    # We must generate a "unique" name
    def save(self, *args, **kwargs):
        if not self.name:
            self.name = ".".join([self.product_type.name, str(self.visitor.id), self.activity_step.name])
        super().save(*args, **kwargs)

class Concept(VASTObject_NameUnique):
    pass

class Predicate(VASTObject_NameUnique):
    pass

class Statement(VASTObject_NameUserGroupUnique):
    product           = models.ForeignKey('Product',   on_delete=models.CASCADE, default=None)
    subject           = models.ForeignKey('Concept',   on_delete=models.CASCADE, default=None, related_name='subject')
    predicate         = models.ForeignKey('Predicate', on_delete=models.CASCADE, default=None)
    object            = models.ForeignKey('Concept',   on_delete=models.CASCADE, default=None, related_name='object')
     # We must generate a "unique" name
    def save(self, *args, **kwargs):
        if not self.name:
            self.name = ".".join([self.product.name, self.subject.name, self.predicate.name, self.object.name])
        super().save(*args, **kwargs)


class VisitorGroupQRCode(VASTObject):
    event             = models.ForeignKey('Event', on_delete=models.CASCADE, default=None)
    activity          = models.ForeignKey('Activity',     on_delete=models.CASCADE, default=None)
    activity_step     = models.ForeignKey('ActivityStep', on_delete=models.CASCADE, default=None, null=False, blank=False)
    visitor_group     = models.ForeignKey('VisitorGroup', on_delete=models.CASCADE, default=None)
    url               = models.CharField(max_length=255, default=None)
    qr_code           = models.ImageField(upload_to='qr_codes', default=None, null=True, blank=True)

    def save(self, *args, **kwargs):
        vgroup = self.visitor_group
        vgroupid = vgroup.id
        event = self.event
        school = vgroup.visitor_organisation
        try:
            schoolname = school.name
        except AttributeError:
            schoolname = "null"
        event = self.event
        try:
            eventid = event.id
        except AttributeError:
            eventid = "null"
        activity = self.activity
        try:
            activityid = activity.id
        except AttributeError:
            activityid = "null"
        activitystep = self.activity_step
        try:
            activitystepid = activitystep.id
        except AttributeError:
            activitystepid = "null"
        museum = event.host_organisation
        try:
            museumname = museum.name
        except AttributeError:
            museumname = "null"
        educlevel = vgroup.education
        try:
            educlevelname = educlevel.name
        except AttributeError:
            educlevelname = "null"
        age = vgroup.age
        try:
            agename = age.name
        except AttributeError:
            agename = "null"
        frontend_url = self.url
        url = frontend_url+'/?school='+schoolname+'&museum='+museumname+'&edulevel='+educlevelname+'&age='+agename+'&eventid='+str(eventid)+'&activityid='+str(activityid)+'&activitystepid='+str(activitystepid)+'&vgroupid='+str(vgroupid)+'}'
        qrcode_img = qrcode.make(url, version=1, box_size=4)
        canvas = Image.new('RGB',(400, 400), 'white')
        draw = ImageDraw.Draw(canvas)
        canvas.paste(qrcode_img)
        fname = f'qr_code-{self.name}.png'
        buffer = BytesIO()
        canvas.save(buffer, 'PNG')
        self.qr_code.save(fname, File(buffer), save=False)
        canvas.close()
        super().save(*args, **kwargs)

