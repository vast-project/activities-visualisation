from django.test import TestCase

from django.test.utils import setup_test_environment

from django.contrib.auth.models import User

from django.test import Client
client = Client()

# import logging
# logger = logging.getLogger("RDFStoreVAST")
# logging.disable(logging.NOTSET)
# logger.setLevel(logging.DEBUG)
# 
# from unittest.mock import patch


class ProductModelTests(TestCase):
    def setUp(self):
        user = User.objects.create_superuser("admin", password="admin123")

    def post(self, url, data):
        response = client.post(url, content_type="application/json", data=data)
        print("POST:", url, "Response:", response.status_code, response.headers, "Content:", response.content)
        location = response.headers.get("Location", None)
        if (location):
            r = client.get(location)
            print("GET:", location, "Response:", response.status_code, "Content:", response.content)
            print()
        self.assertIs(response.status_code < 400, True)
        return response

    def login(self):
        self.assertIs(client.login(username="admin", password="admin123"), True)

    def setUp_language_add(self):
        self.login()
        response = self.post("/rest/languages/", data={
            "code": "en",
            "name": "English",
            "description": "Language: English"
        })
        response = self.post("/rest/languages/", data={
            "code": "el",
            "name": "Greek",
            "description": "Language: Greek"
        })
        response = self.post("/rest/languages/", data={
            "code": "it",
            "name": "Italian",
            "description": "Language: Italian"
        })
        response = self.post("/rest/languages/", data={
            "code": "pt",
            "name": "Portuguese",
            "description": "Language: Portuguese"
        })

    def setUp_organisation_type_add(self):
        response = self.post("/rest/organisation_types/", data={
            "name": "Host Organisation",
            "description": "An organisation that organises an event",
            "name_local": "Host Organisation",
            "description_local": "An organisation that organises an event",
            "language_local": "/rest/languages/1/",  # English
        })
        response = self.post("/rest/organisation_types/", data={
            "name": "School",
            "description": "A school",
        })

    def setUp_organisation_add(self):
        response = self.post("/rest/organisations/", data={
            "name": "Museo Galileo",
            "description": "Museo Galileo - Instituto e Museo di Storia della Scienza",
            "name_local": "Museo Galileo",
            "description_local": "Museo Galileo - Instituto e Museo di Storia della Scienza",
            "language_local": "/rest/languages/3/",  # Italian
            "type": "/rest/organisation_types/1/",   # Host Organisation
            "location": "Florence",
            "is_visitor": "No"
        })
        response = self.post("/rest/organisations/", data={
            "name": "School in Florence",
            "description": "A school from Florence",
            "type": "/rest/organisation_types/2/",   # School
            "location": "Florence",
            "is_visitor": "Yes"
        })

    def setUp_event_add(self):
        response = self.post("/rest/events/", data={
            "name": "Museo Galileo Event",
            "description": "An event by Museo Galileo",
            "name_local": "Museo Galileo Event",
            "description_local": "An event by Museo Galileo in Italian",
            "language_local": "/rest/languages/3/",          # Italian
            "host_organisation": "/rest/organisations/1/",   # Museo Galileo
        })

    def setUp_context_add(self):
        response = self.post("/rest/contexts/", data={
            "name": "Museo Galileo VAST Participation",
            "description": "A context for running activities in Museo Galileo",
            "name_local": "Museo Galileo VAST Participation",
            "description_local": "A context for running activities in Museo Galileo in Italian",
            "language_local": "/rest/languages/3/" # Italian
        })

    def setUp_nature_add(self):
        response = self.post("/rest/natures/", data={
            "name": "In Person",
        })
        response = self.post("/rest/natures/", data={
            "name": "On-site",
        })
        response = self.post("/rest/natures/", data={
            "name": "Online",
        })

    def setUp_education_add(self):
        response = self.post("/rest/educations/", data={
            "name": "Secondary School",
            "name_local": "Scuola secondaria di secondo grado",
            "language_local": "/rest/languages/3/" # Italian
        })

    def setUp_activity_add(self):
        response = self.post("/rest/activities/", data={
            "name": "Museo Galileo Default Activity",
            "description": "A default activity in Museo Galileo",
            "name_local": "Museo Galileo Default Activity",
            "description_local": "A default activity in Museo Galileo in Italian",
            "language_local": "/rest/languages/3/", # Italian
            "event": "/rest/events/1/",             # Museo Galileo Event
            "context": "/rest/contexts/1/",         # Museo Galileo VAST Participation
            "language": "/rest/languages/3/",       # Italian
            "nature": "/rest/natures/2/",           # On-site
            "education": "/rest/educations/1/",     # Secondary School
            "date_from": "2020-12-01T00:00:00",
            "date_to":   "2024-02-24T23:59:59"
        })

    def setUp_stimulus_add(self):
        response = self.post("/rest/stimuli/", data={
            "name": "Video",
            "description": "A performance in Museo Galileo",
            "uriref": "https://www.youtube.com/channel/UC2oyweCFfvyP66hmsaU1aUA",
            "stimulus_type": "Video"
        })

    def setUp_activity_step_add(self):
        response = self.post("/rest/activity_steps/", data={
            "name": "Default Activity Step",
            "description": "The only activity step in activity",
            "activity": "/rest/activities/1/",
            "stimulus": "/rest/stimuli/1/"
        })

    def setUp_age_add(self):
        response = self.post("/rest/ages/", data={
            "name": "18-99",
        })
        response = self.post("/rest/ages/", data={
            "name": "5-17",
        })

    def setUp_gender_add(self):
        response = self.post("/rest/genders/", data={
            "name": "Male",
        })
        response = self.post("/rest/genders/", data={
            "name": "Female",
        })

    def setUp_nationality_add(self):
        response = self.post("/rest/nationalities/", data={
            "name": "Greek",
        })
        response = self.post("/rest/nationalities/", data={
            "name": "Italian",
        })

    def setUp_visitor_group_add(self):
        response = self.post("/rest/visitor_groups/", data={
            "name": "Group for Activity",
            "composition": 30,
            "age":  "/rest/ages/1/",
            "education": "/rest/educations/1/",
            "nationality": "/rest/nationalities/2/",
            "mother_language": "/rest/languages/3/",
            "visitor_organisation": "/rest/organisations/2/"
        })

    def setUp_visitor_add(self):
        response = self.post("/rest/visitors/", data={
            "name": "Georgios Petasis",
            "age":  "/rest/ages/1/",
            "gender": "/rest/genders/1/",
            "date_of_visit": "2023-01-01T09:45",
            "nationality": "/rest/nationalities/2/",
            "mother_language": "/rest/languages/3/",
            "activity": "/rest/activities/1/",
            "group": "/rest/visitor_groups/1/",
            "school": "1st School in Florence",
        })

    def setUp_product_type_add(self):
        response = self.post("/rest/product_types/", data={
            "name": "MindMap",
        })

    def setUp_product_add(self):
        response = self.post("/rest/products/", data={
            "product_type": "/rest/product_types/1/",
            "visitor": "/rest/visitors/1/",
            "activity_step": "/rest/activity_steps/1/",
        })

    def setUp_concept_add(self):
        response = self.post("/rest/concepts/", data={
            "name": "value 1",
            "name_local": "italian value 1",
            "language_local": "/rest/languages/3/", # Italian
        })
        response = self.post("/rest/concepts/", data={
            "name": "value 2",
            "name_local": "italian value 2",
            "language_local": "/rest/languages/3/", # Italian
        })

    def setUp_predicate_add(self):
        response = self.post("/rest/predicates/", data={
            "name": "equivalent",
        })
        response = self.post("/rest/predicates/", data={
            "name": "concequence",
        })

    def setUp_statement_add(self):
        response = self.post("/rest/statements/", data={
            "product": "/rest/products/1/",
            "subject": "/rest/concepts/1/",
            "predicate": "/rest/predicates/1/",
            "object": "/rest/concepts/2/",
        })

    def test_1(self):
        self.setUp_language_add()
        self.setUp_organisation_type_add()
        self.setUp_organisation_add()
        self.setUp_event_add()
        self.setUp_context_add()
        self.setUp_nature_add()
        self.setUp_education_add()
        self.setUp_activity_add()
        self.setUp_stimulus_add()
        self.setUp_activity_step_add()
        self.setUp_age_add()
        self.setUp_gender_add()
        self.setUp_nationality_add()
        self.setUp_visitor_group_add()
        self.setUp_visitor_add()
        self.setUp_product_type_add()
        self.setUp_product_add()
        self.setUp_concept_add()
        self.setUp_predicate_add()
        self.setUp_statement_add()
