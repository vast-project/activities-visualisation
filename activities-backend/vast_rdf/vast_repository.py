from rdflib import Graph, URIRef, Literal
from rdflib.namespace import RDF, RDFS, XSD, FOAF
from rdflib import Namespace
from rdflib.graph import DATASET_DEFAULT_GRAPH_ID
from rdflib.plugins.stores.sparqlstore import SPARQLUpdateStore
import rdflib
from dataclasses import dataclass
import hashlib
from dotenv import dotenv_values
import os

from pprint import pprint

import logging
logger = logging.getLogger('RDFStoreVAST')


NAMESPACE_VAST                   = Namespace("https://www.vast-project.eu/vast#")
VAST_GRAPH_OWNER: URIRef         = URIRef(f"{NAMESPACE_VAST.vastGraphObjectOwner}/digitisation_tool")
GRAPH_ID_ELLOGON_ANNOTATION_TOOL = URIRef("https://www.vast-project.eu/vastOntology/DigitisationTools")

@dataclass
class RDFStoreObject:
    T:                     URIRef  = None
    id:                    URIRef  = None
    name:                  Literal = None
    comment:               Literal = None
    created_at:            Literal = None
    updated_at:            Literal = None
    created_by:            URIRef  = None
    updated_by:            URIRef  = None

    # Organisation
    type:                  URIRef  = None
    subtype:               URIRef  = None
    location:              Literal = None
    is_visitor:            Literal = None

    # Activity
    event:                 URIRef  = None
    
    # Strimulus
    uriref:                URIRef  = None
    stimulus_type:         URIRef  = None

    # ActivityStep
    activity:              URIRef  = None
    stimulus:              URIRef  = None

    # Event
    event_activity:        URIRef  = None
    host_organisation:     URIRef  = None
    date:                  Literal = None
    date_from:             Literal = None
    date_to:               Literal = None
    context:               URIRef  = None
    language:              URIRef  = None
    nature:                Literal = None
    education:             Literal = None

    # VisitorGroup
    composition:           Literal = None
    nationality:           URIRef  = None
    #education -> also on Event
    mother_language:       URIRef  = None
    visitor_organisation:  URIRef  = None
    age:                   Literal = None

    # Visitor
    userid:                Literal = None
    #age -> also in VisitorGroup
    gender:                Literal = None
    date_of_visit:         Literal = None
    #education -> also on activity, visitor group
    #nationality -> also visitor group
    #mother_language -> also on visitor group
    visitor_activity:      URIRef  = None
    group:                 URIRef  = None
    #school:                Literal = None

    # Product
    product_type:          URIRef  = None
    visitor:               URIRef  = None
    activity_step:         URIRef  = None

    # Statement/ProductStatement
    subject:               URIRef  = None
    object:                URIRef  = None
    predicate:             URIRef  = None


    rdf_graph_owner:    Literal = VAST_GRAPH_OWNER

    def add(self, graph):
        if (self.id == None):
            return
        #if (self.rdf_graph_owner):   graph.add((self.id, NAMESPACE_VAST.vastGraphObjectOwner,  self.rdf_graph_owner))
        if (self.T):                    graph.add((self.id, RDF.type,  self.T))
        if (self.name):                 graph.add((self.id, FOAF.name, self.name))
        if (self.comment):              graph.add((self.id, RDFS.comment, self.comment))
        if (self.created_at):           graph.add((self.id, NAMESPACE_VAST.vastCreatedAt, self.created_at))
        if (self.updated_at):           graph.add((self.id, NAMESPACE_VAST.vastUpdatedAt, self.updated_at))
        if (self.created_by):           graph.add((self.id, NAMESPACE_VAST.vastCreatedBy, self.created_by))
        if (self.updated_by):           graph.add((self.id, NAMESPACE_VAST.vastUpdatedBy, self.updated_by))

        # Organisation
        if (self.type):                 graph.add((self.id, NAMESPACE_VAST.vastOrganisationType, self.type))
        if (self.subtype):              graph.add((self.id, NAMESPACE_VAST.vastOrganisationSubtype, self.subtype))
        if (self.location):             graph.add((self.id, NAMESPACE_VAST.vastLocation, self.location))
        if (self.is_visitor):           graph.add((self.id, NAMESPACE_VAST.vastIsVisitor, self.is_visitor))

        # Activity
        if (self.event):                graph.add((self.id, NAMESPACE_VAST.vastAssociatedEvent, self.event))

        # stimulus
        if (self.stimulus_type):        graph.add((self.id, RDF.type, self.stimulus_type))
        if (self.uriref):               graph.add((self.id, NAMESPACE_VAST.vastURIRef, self.uriref))

        # ActivityStep
        if (self.activity):             graph.add((self.activity, NAMESPACE_VAST.vastStep, self.id))
        if (self.stimulus):             graph.add((self.id, NAMESPACE_VAST.vastStimulus, self.stimulus))

        # Event
        if (self.event_activity):
                                        graph.add((self.id, NAMESPACE_VAST.vastAssociatedActivity, self.event_activity))
                                        graph.add((self.event_activity, NAMESPACE_VAST.vastAssociatedEvent, self.id))
        if (self.host_organisation):    graph.add((self.id, NAMESPACE_VAST.vastHostOrganisation, self.host_organisation))
        if (self.date):                 graph.add((self.id, NAMESPACE_VAST.vastDate, self.date))
        if (self.date_from):            graph.add((self.id, NAMESPACE_VAST.vastDateFrom, self.date_from))
        if (self.date_to):              graph.add((self.id, NAMESPACE_VAST.vastDateTo, self.date_to))
        if (self.context):              graph.add((self.id, NAMESPACE_VAST.vastInContext, self.context))
        if (self.language):             graph.add((self.id, NAMESPACE_VAST.vastTongue, self.language))
        if (self.nature):               graph.add((self.id, NAMESPACE_VAST.vastNature, self.nature))
        if (self.education):            graph.add((self.id, NAMESPACE_VAST.vastEducation, self.education))

        # VisitorGroup
        if (self.composition):          pass
        if (self.nationality):          graph.add((self.id, NAMESPACE_VAST.vastNationality, self.nationality))
        if (self.mother_language):      graph.add((self.id, NAMESPACE_VAST.vastMotherTongue, self.mother_language))
        if (self.visitor_organisation): graph.add((self.id, NAMESPACE_VAST.vastVisitorOrganisation, self.visitor_organisation))
        if (self.age):                  graph.add((self.id, NAMESPACE_VAST.vastAge, self.age))

        # Visitor
        if (self.userid):               graph.add((self.id, NAMESPACE_VAST.vastUserId, self.userid))
        if (self.gender):               graph.add((self.id, NAMESPACE_VAST.vastGender, self.gender))
        if (self.date_of_visit):        graph.add((self.id, NAMESPACE_VAST.vastVisitDate, self.date_of_visit))
        if (self.visitor_activity):     graph.add((self.id, NAMESPACE_VAST.vastParticipatesIn, self.visitor_activity))
        if (self.group):                graph.add((self.id, NAMESPACE_VAST.vastMemberOf, self.group))
        #if (self.school):               graph.add((self.id, NAMESPACE_VAST.vastShool, self.school))

        # Product
        if (self.product_type):         graph.add((self.id, RDF.type, self.product_type))
        if (self.visitor):              graph.add((self.id, NAMESPACE_VAST.vastMadeBy, self.visitor))
        if (self.activity_step):        graph.add((self.activity_step, NAMESPACE_VAST.vastProduces, self.id))

        # Statement/ProductStatement
        if (self.subject):              graph.add((self.id, RDF.subject, self.subject))
        if (self.object):               graph.add((self.id, RDF.object, self.object))
        if (self.predicate):            graph.add((self.id, RDF.predicate, self.predicate))

class RDFStoreConfig:

    def __init__(self, env=os.path.dirname(os.path.realpath(__file__))+"/.env"):
        self.config = {
            **dotenv_values(env),  # load sensitive variables from .env file
            **os.environ,          # override loaded values with environment variables
        }

class RDFStoreVAST:

    def __init__(self, config=None, identifier=GRAPH_ID_ELLOGON_ANNOTATION_TOOL, store=None):
        self.default_config(config)
        # logger.debug(f"RDFStoreVAST(): config: {self.config.config}")
        self.default_store(store)
        self.g = Graph(store=self.store, identifier=identifier)
        self.vast = NAMESPACE_VAST
        self.g.bind("vast", self.vast)

        #self.owner = RDFStoreObject(T=self.vast.vastGraphObjectOwner,
        #                            id=VAST_GRAPH_OWNER)
        #self.owner.add(self.g)
        self.commit()

    def default_config(self, config):
        if not config:
            config = RDFStoreConfig()
        self.config = config

    def default_store(self, store):
        if not store and self.config:
            store = SPARQLUpdateStore(query_endpoint=self.config.config["GRAPHDB_QUERY_ENDPOINT"],
                                      update_endpoint=self.config.config["GRAPHDB_UPDATE_ENDPOINT"],
                                      auth=(self.config.config["GRAPHDB_AUTH_USER"],
                                            self.config.config["GRAPHDB_AUTH_PASS"]),
                                      autocommit=False,
                                      context_aware=True,
                                      postAsEncoded=False
                                     )
            # Default is 'GET'. We want to send 'POST' requests in this instance.
            store.method = 'POST'
        self.store = store

    def commit(self):
        if self.store:
            self.store.commit()

    def queryObject(self, id):
        if not self.store:
            return []
        return self.g.triples( (id, None, None),  )

    def removeObject(self, id):
        for triple in self.queryObject(id):
            # logger.info(f"RDFStoreVAST(): removeObject(): Removing: {triple}")
            self.g.remove(triple)
        self.commit()

    def delete(self, class_name, obj):
        logger.info(f"RDFStoreVAST(): delete(): class: {class_name}, obj: {obj}")
        match class_name:
            case "Language":
                T = None
            case "OrganisationType":
                T = self.vast.vastOrganisationType
            case "Organisation":
                T = self.vast.vastOrganisation
            case "Event":
                T = self.vast.vastEvent
            case "Context":
                T = self.vast.vastContext
            case "Activity":
                T = self.vast.vastActivity
            case "Stimulus":
                T = self.vast.vastStimulus
            case "ActivityStep":
                T = self.vast.vastActivityStep
            case "Age":
                T = self.vast.vastAge
            case "Education":
                T = self.vast.vastEducation
            case "Gender":
                T = self.vast.vastGender
            case "Nationality":
                T = self.vast.vastNationality
            case "VisitorGroup":
                T = self.vast.vastGroup
            case "Visitor":
                T = self.vast.vastNonExpert
            case "ProductType":
                T = None
            case "Product":
                T = self.vast.vastProduct
            case "Concept":
                T = self.vast.vastConcept
            case "Predicate":
                T = self.vast.vastPredicate
            case "Statement" | "ProductStatement":
                T = self.vast.vastStatement
            case _:
                T = None
        if T:
            robj = RDFStoreObject(T=T, id=URIRef(f"{T}/{obj.name_md5}"))
            self.removeObject(robj.id)
            self.commit()

    def save(self, class_name, obj):
        logger.info(f"RDFStoreVAST(): save(): class: {class_name}, obj: {obj}")
        method = getattr(self, class_name, None)
        logger.info(f"RDFStoreVAST(): save(): method: {method}")
        if method:
            method(obj)
            self.commit()

    def hash(self, string):
        return hashlib.md5(string.encode('utf-8')).hexdigest()

    def serialiseDateTime(self, dt):
        if dt:
            return Literal(dt, datatype=XSD.dateTime)
        return None

    def AutoUpdateTimeFields(self, obj, robj):
        robj.created_at=self.serialiseDateTime(obj.created)
        robj.updated_at=self.serialiseDateTime(obj.updated)

    def VASTObject(self, obj, robj, lang="en"):
        self.AutoUpdateTimeFields(obj, robj)
        if obj.name:        robj.name=Literal(obj.name, lang=lang)
        if obj.description: robj.comment=Literal(obj.description, lang=lang)
        robj.add(self.g)
        if obj.language_local:
            if obj.name_local:        robj.name=Literal(obj.name_local, lang=obj.language_local.code)
            if obj.description_local: robj.comment=Literal(obj.description_local, lang=obj.language_local.code)
            robj.add(self.g)

    def createVASTObject(self, obj, T):
        robj = RDFStoreObject(T=T,
                              #id=URIRef(f"{self.vast.vastOrganisationType}/{obj.uuid}"),
                              id=URIRef(f"{T}/{obj.name_md5}"),
                              )
        self.removeObject(robj.id)
        self.VASTObject(obj, robj)
        robj.add(self.g)
        return robj

    def getURIRef(self, T, obj):
        if obj:
            return URIRef(f"{T}/{obj.name_md5}")
        return None

    def getLiteral(self, obj, lang="en"):
        if obj and obj.name:
            return Literal(obj.name, lang=lang)
        return None

    def Language(self, obj):
        pass ;# Nothing to do here...

    def OrganisationType(self, obj):
        # pprint(vars(obj))
        robj = self.createVASTObject(obj, self.vast.vastOrganisationType)

    def Organisation(self, obj): # RDF checked
        # pprint(vars(obj))
        # pprint(vars(obj.type))
        robj = self.createVASTObject(obj, self.vast.vastOrganisation)
        robj.type       = self.getURIRef(self.vast.vastOrganisationType, obj.type)
        robj.subtype    = self.getURIRef(self.vast.vastOrganisationType, obj.subtype)
        robj.location   = Literal(obj.location, lang="en")
        robj.is_visitor = Literal(obj.is_visitor, lang="en")
        robj.add(self.g)

    def Context(self, obj): # RDF Checked
        robj = self.createVASTObject(obj, self.vast.vastContext)

    # Nature does not need to be RDF-serialised, we are going to use strings in Activities
    # def Nature(self, obj):
    #     robj = self.createVASTObject(obj, self.vast.vastNature)

    def Activity(self, obj):
        robj = self.createVASTObject(obj, self.vast.vastActivity)

    def Stimulus(self, obj): # RDF Checked
        robj = self.createVASTObject(obj, self.vast.vastStimulus)
        match obj.stimulus_type:
            case "Document":
                robj.stimulus_type = URIRef(NAMESPACE_VAST.vastDocument)
            case "Segment":
                robj.stimulus_type = URIRef(NAMESPACE_VAST.vastSegment)
            case "Image":
                robj.stimulus_type = URIRef(NAMESPACE_VAST.vastImage)
            case "Video":
                robj.stimulus_type = URIRef(NAMESPACE_VAST.vastVideo)
            case "Tool":
                robj.stimulus_type = URIRef(NAMESPACE_VAST.vastTool)
        if obj.uriref:
            robj.uriref = URIRef(obj.uriref)
        robj.add(self.g)

    def ActivityStep(self, obj): # RDF Checked
        robj = self.createVASTObject(obj, self.vast.vastActivityStep)
        robj.activity = self.getURIRef(self.vast.vastActivity, obj.activity)
        robj.stimulus = self.getURIRef(self.vast.vastStimulus, obj.stimulus)
        robj.add(self.g)
    
    def Age(self, obj): # RDF Checked
        robj = self.createVASTObject(obj, self.vast.vastAge)

    def Education(self, obj): # RDF Checked
        robj = self.createVASTObject(obj, self.vast.vastEducation)

    def Event(self, obj): # RDF Checked
        robj = self.createVASTObject(obj, self.vast.vastEvent)
        robj.host_organisation = self.getURIRef(self.vast.vastOrganisation, obj.host_organisation)
        robj.event_activity    = self.getURIRef(self.vast.vastActivity, obj.activity)
        robj.date              = self.serialiseDateTime(obj.date)
        robj.date_from         = self.serialiseDateTime(obj.date_from)
        robj.date_to           = self.serialiseDateTime(obj.date_to)
        robj.context           = self.getURIRef(self.vast.vastContext, obj.context)
        robj.language          = Literal(obj.language, lang="en")
        robj.nature            = self.getLiteral(obj.nature)
        robj.education         = self.getLiteral(obj.education)
        robj.add(self.g)

    def Gender(self, obj): # RDF Checked
        robj = self.createVASTObject(obj, self.vast.vastGender)

    def Nationality(self, obj): # RDF Checked
        robj = self.createVASTObject(obj, self.vast.vastNationality)

    def VisitorGroup(self, obj): # RDF Checked
        robj = self.createVASTObject(obj, self.vast.vastGroup)
        robj.composition            = Literal(obj.composition, lang="en")
        robj.age                    = self.getURIRef(self.vast.vastAge, obj.age)
        robj.education              = self.getURIRef(self.vast.vastEducation, obj.education)
        robj.nationality            = self.getURIRef(self.vast.vastNationality, obj.nationality)
        robj.mother_language        = Literal(obj.mother_language, lang="en")
        robj.visitor_organisation   = self.getURIRef(self.vast.vastOrganisation, obj.visitor_organisation)
        robj.add(self.g)
        
    def Visitor(self, obj): # RDF Checked
        robj = self.createVASTObject(obj, self.vast.vastNonExpert)
        robj.userid             = Literal(obj.userid, lang="en")
        robj.age                = self.getURIRef(self.vast.vastAge, obj.age)
        robj.gender             = self.getURIRef(self.vast.vastGender, obj.gender)
        robj.date_of_visit      = self.serialiseDateTime(obj.date_of_visit)
        robj.education          = self.getURIRef(self.vast.vastEducation, obj.education)
        robj.nationality        = self.getURIRef(self.vast.vastNationality, obj.nationality)
        robj.mother_language    = Literal(obj.mother_language, lang="en")
        robj.visitor_activity   = self.getURIRef(self.vast.vastActivity, obj.activity)
        robj.group              = self.getURIRef(self.vast.vastGroup, obj.visitor_group)
        #robj.school             = Literal(obj.school, lang="en")
        robj.add(self.g)

    # Product types are converted to class references in Product
    def ProductType(self, obj):
        pass

    def Product(self, obj): # RDF Checked
        robj = self.createVASTObject(obj, self.vast.vastProduct)
        match obj.product_type.name.lower():
            case "MindMap":
                robj.product_type = URIRef(NAMESPACE_VAST.vastMindMap)
            case "Annotation":
                robj.product_type = URIRef(NAMESPACE_VAST.vastAnnotation)
            case "Questionnaire":
                robj.product_type = URIRef(NAMESPACE_VAST.vastQuestionnaire)
            case "Interview":
                robj.product_type = URIRef(NAMESPACE_VAST.vastInterview)
            case _:
                robj.product_type = URIRef(getattr(NAMESPACE_VAST, "vast" + obj.product_type.name.title().replace(" ", "")))

        robj.visitor       = self.getURIRef(self.vast.vastVisitor, obj.visitor)
        robj.activity_step = self.getURIRef(self.vast.vastActivityStep, obj.activity_step)
        robj.add(self.g)
    
    def Concept(self, obj): # RDF Checked
        robj = self.createVASTObject(obj, self.vast.vastConcept)

    def Predicate(self, obj): # RDF Checked
        robj = self.createVASTObject(obj, self.vast.vastPredicate)

    def Statement(self, obj): # RDF Checked
        robj = self.createVASTObject(obj, self.vast.vastStatement)
        robj.product    = self.getURIRef(self.vast.vastProduct,   obj.product)
        robj.subject    = self.getURIRef(self.vast.vastConcept,   obj.subject)
        robj.predicate  = self.getURIRef(self.vast.vastPredicate, obj.predicate)
        robj.object     = self.getURIRef(self.vast.vastConcept,   obj.object)
        robj.add(self.g)

    def ProductStatement(self, obj): # RDF Checked
        robj = self.createVASTObject(obj, self.vast.vastStatement)
        robj.subject    = self.getURIRef(self.vast.vastProduct,   obj.subject)
        robj.predicate  = self.getURIRef(self.vast.vastPredicate, obj.predicate)
        robj.object     = self.getURIRef(self.vast.vastConcept,   obj.object)
        robj.add(self.g)
