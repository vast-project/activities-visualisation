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
    T:                  URIRef  = None
    id:                 URIRef  = None
    name:               Literal = None
    comment:            Literal = None
    created_at:         Literal = None
    updated_at:         Literal = None
    created_by:         URIRef  = None
    updated_by:         URIRef  = None

    type:               URIRef  = None
    subtype:            URIRef  = None
    event:              URIRef  = None
    date_from:          URIRef  = None
    date_to:            URIRef  = None
    host_organisation:  URIRef  = None
    
    activity:           URIRef  = None
    activity_step:      URIRef  = None
    context:            URIRef  = None
    language:           URIRef  = None
    nature:             URIRef  = None
    education:          URIRef  = None
    visitor:            URIRef  = None

    location:           Literal = None
    is_visitor:         Literal = None

    stimulus:           URIRef  = None
    stimulus_type:      URIRef  = None
    uriref:             URIRef  = None

    userid:             Literal = None
    rdf_graph_owner:    Literal = VAST_GRAPH_OWNER
    age:                Literal = None
    gender:             Literal = None
    date_of_visit:      Literal = None
    education:          URIRef  = None
    nationality:        URIRef  = None
    motherLanguage:     URIRef  = None
    participates_in:    URIRef  = None
    group:              URIRef  = None
    school:             Literal = None

    def add(self, graph):
        if (self.id == None):
            return
        #if (self.rdf_graph_owner):   graph.add((self.id, NAMESPACE_VAST.vastGraphObjectOwner,  self.rdf_graph_owner))
        if (self.T):                 graph.add((self.id, RDF.type,  self.T))
        if (self.name):              graph.add((self.id, FOAF.name, self.name))
        if (self.comment):           graph.add((self.id, RDFS.comment, self.comment))
        if (self.created_at):        graph.add((self.id, NAMESPACE_VAST.vastCreatedAt, self.created_at))
        if (self.updated_at):        graph.add((self.id, NAMESPACE_VAST.vastUpdatedAt, self.updated_at))
        if (self.created_by):        graph.add((self.id, NAMESPACE_VAST.vastCreatedBy, self.created_by))
        if (self.updated_by):        graph.add((self.id, NAMESPACE_VAST.vastUpdatedBy, self.updated_by))

        if (self.type):              graph.add((self.id, NAMESPACE_VAST.vastOrganisationType, self.type))
        if (self.subtype):           graph.add((self.id, NAMESPACE_VAST.vastOrganisationSubtype, self.subtype))
        if (self.event):             graph.add((self.id, NAMESPACE_VAST.vastAssociatedEvent, self.event))
        if (self.date_from):         graph.add((self.id, NAMESPACE_VAST.vastDateFrom, self.date_from))
        if (self.date_to):           graph.add((self.id, NAMESPACE_VAST.vastDateTo, self.date_to))
        if (self.host_organisation): graph.add((self.id, NAMESPACE_VAST.vastHostOrganisation, self.host_organisation))

        if (self.activity):          graph.add((self.activity, NAMESPACE_VAST.vastStep, self.id))
        #if (self.activity_step):     graph.add((self.id, NAMESPACE_VAST.vast, self.activity_step))
        if (self.context):           graph.add((self.id, NAMESPACE_VAST.vastInContext, self.context))
        if (self.language):          graph.add((self.id, NAMESPACE_VAST.vastTongue, self.language))
        if (self.nature):            graph.add((self.id, NAMESPACE_VAST.vastNature, self.nature))
        if (self.education):         graph.add((self.id, NAMESPACE_VAST.vastEducation, self.education))
        #if (self.visitor):           graph.add((self.id, NAMESPACE_VAST.vast, self.visitor))

        if (self.location):          graph.add((self.id, NAMESPACE_VAST.vastLocation, self.location))
        if (self.is_visitor):        graph.add((self.id, NAMESPACE_VAST.vastIsVisitor, self.is_visitor))
        if (self.stimulus):          graph.add((self.id, NAMESPACE_VAST.vastStimulus, self.stimulus))
        if (self.stimulus_type):     graph.add((self.id, RDF.type, self.stimulus_type))
        if (self.uriref):            graph.add((self.id, NAMESPACE_VAST.vastURIRef, self.uriref))

        if (self.age):               graph.add((self.id, NAMESPACE_VAST.vastAge, self.age))
        if (self.gender):            graph.add((self.id, NAMESPACE_VAST.vastGender, self.gender))
        if (self.date_of_visit):     graph.add((self.id, NAMESPACE_VAST.vastVisitDate, self.date_of_visit))
        if (self.nationality):       graph.add((self.id, NAMESPACE_VAST.vastNationality, self.nationality))
        if (self.motherLanguage):    graph.add((self.id, NAMESPACE_VAST.vastMotherTongue, self.motherLanguage))
        if (self.group):             graph.add((self.id, NAMESPACE_VAST.vast, self.group))
        if (self.school):            graph.add((self.id, NAMESPACE_VAST.vast, self.school))
        if (self.participates_in):   graph.add((self.id, NAMESPACE_VAST.vastParticipatesIn, self.participates_in))
        # if (self.):               graph.add((self.id, NAMESPACE_VAST.vast, self.))
        # if (self.):               graph.add((self.id, NAMESPACE_VAST.vast, self.))
        # if (self.):               graph.add((self.id, NAMESPACE_VAST.vast, self.))
        # if (self.):               graph.add((self.id, NAMESPACE_VAST.vast, self.))
        # if (self.):               graph.add((self.id, NAMESPACE_VAST.vast, self.))
        # if (self.):               graph.add((self.id, NAMESPACE_VAST.vast, self.))
        # if (self.):               graph.add((self.id, NAMESPACE_VAST.vast, self.))

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
            logger.info(f"RDFStoreVAST(): removeObject(): Removing: {triple}")
            self.g.remove(triple)
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
        return Literal(dt, datatype=XSD.dateTime)

    def AutoUpdateTimeFields(self, obj, robj):
        robj.created_at=self.serialiseDateTime(obj.created)
        robj.updated_at=self.serialiseDateTime(obj.updated)

    def VASTObject(self, obj, robj, lang="en"):
        self.AutoUpdateTimeFields(obj, robj)
        robj.name=Literal(obj.name, lang=lang)
        robj.comment=Literal(obj.description, lang=lang)
        robj.add(self.g)
        if obj.language_local:
            robj.name=Literal(obj.name_local, lang=obj.language_local.code)
            robj.comment=Literal(obj.description_local, lang=obj.language_local.code)
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

    def Language(self, obj):
        pass ;# Nothing to do here...

    def OrganisationType(self, obj):
        # pprint(vars(obj))
        robj = self.createVASTObject(obj, self.vast.vastOrganisationType)

    def Organisation(self, obj):
        # pprint(vars(obj))
        # pprint(vars(obj.type))
        robj = self.createVASTObject(obj, self.vast.vastOrganisation)
        robj.type       = self.getURIRef(self.vast.vastOrganisationType, obj.type)
        robj.subtype    = self.getURIRef(self.vast.vastOrganisationType, obj.subtype)
        robj.location   = Literal(obj.location, lang="en")
        robj.is_visitor = Literal(obj.is_visitor, lang="en")
        robj.add(self.g)

    def Event(self, obj):
        robj = self.createVASTObject(obj, self.vast.vastEvent)
        robj.host_organisation = self.getURIRef(self.vast.vastOrganisation, obj.host_organisation)
        robj.add(self.g)

    def Context(self, obj):
        robj = self.createVASTObject(obj, self.vast.vastContext)

    # Nature does not need to be RDF-serialised, we are going to use strings in Activities
    # def Nature(self, obj):
    #     robj = self.createVASTObject(obj, self.vast.vastNature)

    def Activity(self, obj):
        robj = self.createVASTObject(obj, self.vast.vastActivity)
        robj.event       = self.getURIRef(self.vast.vastEvent, obj.event)
        robj.context     = self.getURIRef(self.vast.vastContext, obj.context)
        robj.nature      = self.getURIRef(self.vast.vastNature, obj.nature)
        robj.education   = self.getURIRef(self.vast.vastEducation, obj.education)
        robj.language    = Literal(obj.language, lang="en")
        robj.add(self.g)

    def Stimulus(self, obj):
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
        robj.uriref        = URIRef(obj.uriref)
        robj.add(self.g)

    def ActivityStep(self, obj):
        robj = self.createVASTObject(obj, self.vast.vastActivityStep)
        robj.activity = self.getURIRef(self.vast.vastActivity, obj.activity)
        robj.stimulus = self.getURIRef(self.vast.vastStimulus, obj.stimulus)
        robj.add(self.g)

