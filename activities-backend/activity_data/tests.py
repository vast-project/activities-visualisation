from django.test import TestCase

from django.test.utils import setup_test_environment
#setup_test_environment()

from django.contrib.auth.models import User
#my_admin = User.objects.create_superuser("admin", password="admin123")

from django.test import Client
client = Client()
#client.login(username="admin", password="praxis")

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
            "language_local": "/languages/1/",  # English
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
            "language_local": "/languages/3/",  # Italian
            "type": "/organisation_types/1/",   # Host Organisation
            "location": "Florence",
            "is_visitor": "No"
        })
        response = self.post("/rest/organisations/", data={
            "name": "School in Florence",
            "description": "A school from Florence",
            "type": "/organisation_types/2/",   # School
            "location": "Florence",
            "is_visitor": "Yes"
        })

    def setUp_event_add(self):
        response = self.post("/rest/events/", data={
            "name": "Museo Galileo Event",
            "description": "An event by Museo Galileo",
            "name_local": "Museo Galileo Event",
            "description_local": "An event by Museo Galileo in Italian",
            "language_local": "/languages/3/",          # Italian
            "host_organisation": "/organisations/1/",   # Museo Galileo
        })

    def setUp_context_add(self):
        response = self.post("/rest/contexts/", data={
            "name": "Museo Galileo VAST Participation",
            "description": "A context for running activities in Museo Galileo",
            "name_local": "Museo Galileo VAST Participation",
            "description_local": "A context for running activities in Museo Galileo in Italian",
            "language_local": "/languages/3/" # Italian
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
            "language_local": "/languages/3/" # Italian
        })

    def setUp_activity_add(self):
        response = self.post("/rest/activities/", data={
            "name": "Museo Galileo Default Activity",
            "description": "A default activity in Museo Galileo",
            "name_local": "Museo Galileo Default Activity",
            "description_local": "A default activity in Museo Galileo in Italian",
            "language_local": "/languages/3/", # Italian
            "event": "/events/1/",             # Museo Galileo Event
            "context": "/contexts/1/",         # Museo Galileo VAST Participation
            "language": "/languages/3/",       # Italian
            "nature": "/natures/2/",           # On-site
            "education": "/educations/1/",     # Secondary School
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
            "activity": "/activities/1/",
            "stimulus": "/stimuli/1/"
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
            "age":  "/ages/1/",
            "education": "/educations/1/",
            "nationality": "/nationalities/2/",
            "mother_language": "/languages/3/",
            "visitor_organisation": "/organisations/2/"
        })

    def setUp_visitor_add(self):
        response = self.post("/rest/visitors/", data={
            "name": "Georgios Petasis",
            "age":  "/ages/1/",
            "gender": "/genders/1/",
            "date_of_visit": "2023-01-01T09:45",
            "mother_language": "/languages/3/",
            "activity": "/activities/1/",
            "group": "/visitor_groups/1/",
            "school": "1st School in Florence",
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

#    def test_20_create_new_product(self):
#        response = client.post("/api/products", content_type="application/json", data={
#            "name":              "IMSS Web App Product",
#            "name_local":        None,
#            "created_by":        2,
#            "description":       None,
#            "description_local": None,
#            "activity_step":     2,
#            "date" : "2023-02-24 20:50:00",
#            "visitor": 2,
#            "data": {"consequence1": "wd",
#                     "consequence2": "wewd",
#                     "consequence3": "dd",
#                     "opposite1":    "ds",
#                     "opposite2":    "s",
#                     "opposite3":    "s",
#                     "equivalent1":  "v",
#                     "equivalent2":  "v",
#                     "equivalent3":  "v",
#                     }
#            }
#        )
#        print("--->", response.status_code)
