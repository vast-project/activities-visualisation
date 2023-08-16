import hashlib
import urllib.parse
import uuid

import qrcode
from django.conf import settings
from django.contrib.auth.models import User, Group
from django.db import models
from django.utils.html import mark_safe
import os

## RDF Graph...
from vast_rdf.vast_repository import RDFStoreVAST, NAMESPACE_VAST, RDF, GRAPH_ID_SURVEY_DATA
## For saving images in DAM...
from vast_rdf.vast_dam import DAMStoreVAST
from PIL import Image

import logging
logger = logging.getLogger('VASTModel')

##
## DAM Image
##
class VASTDAMImage:
    def save(self, *args, **kwargs):
        logger.info(f"{self.__class__.__name__}: save():", *args, **kwargs)
        ## If we have a prior resource in DAM, delete it...
        self.delete_image_resource()
        ## Try to save image in DAM...
        self.create_image_resource()
        return super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        logger.info(f"{self.__class__.__name__}: delete():", *args, **kwargs)
        ## Delete the image from the DAM...
        self.delete_image_resource()
        return super().delete(*args, **kwargs)

    def create_image_resource(self):
        if self.image:
            path = self.image.path
            url  = self.image.url
            logger.info(f"{self.__class__.__name__}: create_image_resource(): Image url:  {url}  (exists: {os.path.exists(path)})")
            logger.info(f"{self.__class__.__name__}: create_image_resource(): Image path: {path} (exists: {os.path.exists(path)})")
            delete_tmp_image = False
            # if not os.path.exists(path):
            #     # Image not found at this path. Look into product_images...
            #     head_tail = os.path.split(path)
            #     path = os.path.join(head_tail[0], 'product_images', head_tail[1])
            #     logger.info(f"Product: save(): Trying new Image path: {path} (exists: {os.path.exists(path)})")
            #     if os.path.exists(path):
            #         head_tail = os.path.split(url)
            #         url = os.path.join(head_tail[0], 'product_images', head_tail[1])
            #         logger.info(f"Product: save(): Trying new Image url:  {url}  (exists: {os.path.exists(path)})")
            if not os.path.exists(path):
                ## Try to save the image in a temporary file...
                path = self.image.path
                logger.info(f"{self.__class__.__name__}: create_image_resource(): Saving Temp Image: {path}")
                # Open the image using PIL
                img = Image.open(self.image)
                img.save(path)
                delete_tmp_image = True
            if os.path.exists(path):
                dam = DAMStoreVAST()
                logger.info(f"{self.__class__.__name__}: create_image_resource(): Creating Image resource...")
                self.image_resource_id = dam.create_resource(self.image.url, {
                    'description': f'{type(self).__name__}: {self.name}',
                })
                logger.info(f"{self.__class__.__name__}: create_image_resource(): Image Resource: {self.image_resource_id}")
                json_data = dam.get_resource(self.image_resource_id)
                self.image_uriref = dam.get_size(json_data)['url']
                logger.info(f"{self.__class__.__name__}: create_image_resource(): Image url: {self.image_uriref}")
                del dam
                if delete_tmp_image:
                    logger.info(f"{self.__class__.__name__}: create_image_resource(): Deleting Temp Image: {path}")
                    os.remove(path)
            else:
                self.image_resource_id = None
                self.image_uriref      = None

    def delete_image_resource(self):
        ## Do we have a resoule id?
        if self.image_resource_id:
            dam = DAMStoreVAST()
            logger.info(f"{self.__class__.__name__}: delete_image_resource(): Deleting DAM resource with id: {self.image_resource_id}")
            dam.delete_resource(self.image_resource_id)
            self.image_resource_id = None
            del dam

class AutoUpdateTimeFields(models.Model):
    uuid              = models.UUIDField(default = uuid.uuid4, editable = False)
    created           = models.DateTimeField(auto_now_add=True, null=True)
    updated           = models.DateTimeField(auto_now=True, null=True)
    created_by        = models.ForeignKey(settings.AUTH_USER_MODEL, null=False, blank=False, on_delete=models.CASCADE)

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        ## Save the object in the django database...
        result = super().save(*args, **kwargs)
        ## Save the object in RDF Graph...
        rdf = RDFStoreVAST()
        rdf.save(type(self).__name__, self)
        del rdf
        return result

    def delete(self, *args, **kwargs):
        ## Delete the object from the RDF Graph...
        rdf = RDFStoreVAST()
        rdf.delete(type(self).__name__, self)
        del rdf
        return super().delete(*args, **kwargs)


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

    @classmethod
    def set_fields_verbose_names(cls):
        cls._meta.get_field('name').verbose_name= f"{cls.__name__} Name"
        #field = cls.get_field('name')
        #_meta.get_field('name')
        #field.verbose_name = f"{self.__class__.__name__} Name"

    def __str__(self):
        return f'{self.name}'

    class Meta(AutoUpdateTimeFields.Meta):
        abstract = True
        ordering = ["name",]

    def save(self, *args, **kwargs):
        if self.name and not self.name_md5:
            self.name_md5 = hashlib.md5(self.name.encode('utf-8')).hexdigest()
        return super().save(*args, **kwargs)

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
    @classmethod
    def set_fields_verbose_names(cls):
        cls._meta.get_field('name').verbose_name= f"{cls.__name__} Name"
    def __str__(self):
        return f'{self.name}'
    class Meta:
        ordering = ["name",]

## Organisations...
class OrganisationType(VASTObject_NameUnique):
    pass

class Organisation(VASTObject_NameUserGroupUnique):
    type              = models.ForeignKey('OrganisationType', on_delete=models.CASCADE, null=False, blank=False)
    subtype           = models.ForeignKey('OrganisationType', on_delete=models.CASCADE, related_name='subtype', null=True, blank=True)
    location          = models.CharField(max_length=255, default=None, null=True, blank=True)
    # is_visitor        = models.CharField(max_length=3, choices=[('Yes','Yes'),('No','No')], default='Yes', null=False, blank=False)

class Class(VASTObject_NameUnique):
    class Meta(VASTObject_NameUserGroupUnique.Meta):
        verbose_name_plural = 'Classes'

## Contexts...
class Context(VASTObject_NameUserGroupUnique):
    pass

## Activities...
class Nature(VASTObject_NameUnique):
    pass

class Activity(VASTObject_NameUserGroupUnique):
    class Meta(VASTObject_NameUserGroupUnique.Meta):
        verbose_name_plural = 'Activities'

class Stimulus(VASTDAMImage, VASTObject_NameUserGroupUnique):
    stimulus_type        = models.CharField(max_length=32, choices=[('Document','Document'),('Segment','Segment'),('Image','Image'),('Audio','Audio'),('Video','Video'),('Tool','Tool'), ('Questionnaire','Questionnaire')], null=False, blank=False)
    uriref               = models.URLField(max_length=512, default=None, null=True, blank=True)
    text                 = models.TextField(default=None, null=True, blank=True)
    image                = models.ImageField(upload_to='stimulus_images/', default=None, null=True, blank=True)
    image_resource_id    = models.IntegerField(default=None, null=True, blank=True)
    image_uriref         = models.URLField(max_length=512, null=True, blank=True)
    questionnaire        = models.CharField(max_length=512, choices=[('','---------')], null=True, blank=True)

    def image_preview(self):
        if self.image:
            return mark_safe(f'<img src = "{self.image.url}" width = "300"/>')
        else:
            return '(No image)'

    @classmethod
    def get_questionnaires(cls):
        stimulus    = NAMESPACE_VAST.vastStimulus
        description = NAMESPACE_VAST.vastDescription
        rdf = RDFStoreVAST(identifier=GRAPH_ID_SURVEY_DATA)
        sparql = f'SELECT ?s ?d WHERE {{ ?s rdf:type <{stimulus}> . ?s <{description}> ?d }}'
        logger.info(f"{cls.__name__}: get_questionnaires(): SPARQL: '{sparql}'")
        results = rdf.querySPARQL(sparql)
        logger.info(f"{cls.__name__}: get_questionnaires(): result: (len: {len(results)})")
        del rdf
        choices = [('', '---------')]
        for row in results:
            # logger.info(f"{cls.__name__}: get_questionnaires(): row: '{row.s}' '{row.d}'")
            choices.append((row.s, row.d))
        return choices

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
    image                = models.ImageField(upload_to='product_images/', default=None, null=True, blank=True)
    image_resource_id    = models.IntegerField(default=None, null=True, blank=True)
    image_uriref         = models.URLField(max_length=512, null=True, blank=True)

    def image_preview(self):
        if self.image:
            return mark_safe(f'<img src = "{self.image.url}" width = "300"/>')
        else:
            return '(No image)'

    def save(self, *args, **kwargs):
        logger.info(f"Product: save():", *args, **kwargs)
        # We must generate a "unique" name
        if not self.name:
            self.name = ".".join([self.product_type.name, str(self.visitor.id), self.activity_step.name])
        self.delete_image_resource()
        ## Try to save image in DAM...
        self.create_image_resource()
        return super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        ## Delete the image from the DAM...
        self.delete_image_resource()
        return super().delete(*args, **kwargs)

    def create_image_resource(self):
        if self.image:
            path = self.image.path
            url  = self.image.url
            logger.info(f"Product: save(): Image url:  {url}  (exists: {os.path.exists(path)})")
            logger.info(f"Product: save(): Image path: {path} (exists: {os.path.exists(path)})")
            delete_tmp_image = False
            if not os.path.exists(path):
                # Image not found at this path. Look into product_images...
                head_tail = os.path.split(path)
                path = os.path.join(head_tail[0], 'product_images', head_tail[1])
                logger.info(f"Product: save(): Trying new Image path: {path} (exists: {os.path.exists(path)})")
                if os.path.exists(path):
                    head_tail = os.path.split(url)
                    url = os.path.join(head_tail[0], 'product_images', head_tail[1])
                    logger.info(f"Product: save(): Trying new Image url:  {url}  (exists: {os.path.exists(path)})")
            if not os.path.exists(path):
                ## Try to save the image in a temporary file...
                path = self.image.path
                logger.info(f"Product: save(): Saving Temp Image: {path}")
                # Open the image using PIL
                img = Image.open(self.image)
                img.save(path)
                delete_tmp_image = True
            if os.path.exists(path):
                dam = DAMStoreVAST()
                logger.info(f"Product: save(): Creating Image resource...")
                self.image_resource_id = dam.create_resource(self.image.url, {
                    'description': f'{type(self).__name__}: {self.name}',
                })
                logger.info(f"Product: save(): Image Resource: {self.image_resource_id}")
                json_data = dam.get_resource(self.image_resource_id)
                self.image_uriref = dam.get_size(json_data)['url']
                logger.info(f"Product: save(): Image url: {self.image_uriref}")
                del dam
                if delete_tmp_image:
                    logger.info(f"Product: save(): Deleting Temp Image: {path}")
                    os.remove(path)
            else:
                self.image_resource_id = None
                self.image_uriref      = None

    def delete_image_resource(self):
        ## Do we have a resoule id?
        if self.image_resource_id:
            dam = DAMStoreVAST()
            logger.info(f"Product: save(): Deleting DAM resource with id: {self.image_resource_id}")
            dam.delete_resource(self.image_resource_id)
            self.image_resource_id = None
            del dam


## Statements...
class ConceptType(VASTObject_NameUnique):
    @classmethod
    def get_default_pk(cls):
        ct, created = cls.objects.get_or_create(
            name='Concept', 
            defaults=dict(description='The default Concept type', created_by=User.objects.get(username='admin')),
        )
        return ct.pk

class Concept(VASTObject):
    concept_type         = models.ForeignKey('ConceptType',  on_delete=models.CASCADE, default=ConceptType.get_default_pk, null=False, blank=False)
    class Meta(VASTObject.Meta):
        # Enforce a policy for the name to be unique (for each user)
        unique_together = [["name", "concept_type"]]

    def save(self, *args, **kwargs):
        if self.name and self.concept_type and not self.name_md5:
            self.name_md5 = hashlib.md5((self.name + self.concept_type.name).encode('utf-8')).hexdigest()
        return super().save(*args, **kwargs)

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
        return super().save(*args, **kwargs)

class ProductStatement(VASTObject_NameUserGroupUnique):
    subject              = models.ForeignKey('Product',   on_delete=models.CASCADE, default=None, null=False, blank=False, related_name='ps_subject')
    predicate            = models.ForeignKey('Predicate', on_delete=models.CASCADE, default=None, null=False, blank=False, related_name='ps_predicate')
    object               = models.ForeignKey('Concept',   on_delete=models.CASCADE, default=None, null=False, blank=False, related_name='ps_object')
     # We must generate a "unique" name
    def save(self, *args, **kwargs):
        if not self.name:
            self.name = ".".join([self.subject.name, self.subject.name, self.predicate.name, self.object.name])
        return super().save(*args, **kwargs)

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

    def image_preview(self):
        if self.qr_code:
            return mark_safe(f'<img src = "{self.qr_code.url}" width = "300"/>')
        else:
            return '(No image)'

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
        # Make sure the path can be written
        dirname = os.path.dirname(self.qr_code.path)
        if not os.path.exists(dirname):
            os.makedirs(dirname)
        qrcode_img.save(self.qr_code.path)
        return super().save(*args, **kwargs)
