import requests
import urllib.parse
import argparse
import os
import sys

# Initialize parser
parser = argparse.ArgumentParser()

# Adding optional argument
parser.add_argument("-l", "--local", help="Enable local server (http://127.0.0.1:8000)", action=argparse.BooleanOptionalAction)
parser.set_defaults(local=False)

# Read arguments from command line
args = parser.parse_args()
# print(args)

if args.local:
    API          = "http://127.0.0.1:8000"
    PASSWORD     = os.environ.get('DJANGO_SUPERUSER_PASSWORD')
else:
    API          = "https://activities-backend.vast-project.eu"
    PASSWORD     = os.environ.get('DJANGO_SUPERUSER_PASSWORD')

if not PASSWORD:
    sys.exit("environmental variable DJANGO_SUPERUSER_PASSWORD undefined")

class Client:
    API          = API
    object_cache = {}
    client       = requests.session()

    def delete(self, url):
        if 'csrftoken' in self.client.cookies:
            csrftoken = self.client.cookies['csrftoken']
        else:
            csrftoken = None

        response = self.client.delete(url, headers={'Referer': url, 'X-CSRFTOKEN': csrftoken})
        assert response.status_code < 400
        return response

    def get(self, url):
        return self.client.get(self.API + url)

    def post(self, url, data):
        ## Check if the object is already in the database...
        objs = self.find(url, data)
        if len(objs):
            print("OBJECTS EXIST:", len(objs), objs)
            return self.cache(objs[0])
        if 'csrftoken' in self.client.cookies:
            csrftoken = self.client.cookies['csrftoken']
        else:
            csrftoken = None
        data['csrfmiddlewaretoken'] = csrftoken
        URL = self.API + url
        response = self.client.post(URL, headers=dict(Referer=URL), data=data)
        print("POST:", url, "Response:", response.status_code)#, response.headers)#, "Content:", response.content)
        # print("HEADERS:", response.headers)
        location = response.headers.get("Location", None)
        if (location):
            r = client.client.get(location)
            print("GET:", location, "Response:", r.status_code, "Content:", r.content)
            print()
            if r.status_code < 400:
                ## Add object to our cache...
                self.cache(r.json())
        if response.status_code >= 400:
            print("POST DATA:", data)
            print("Content:", response.content)
        assert response.status_code < 400
        return response

    def cache(self, data):
        self.object_cache[data["name"]] = data["url"]
        return data["url"]

    def url(self, name):
        return self.object_cache[name]

    def find(self, url, data):
        if not "name" in data:
            return []
        if "concept_type" in data:
            concept_type = data.get("concept_type")
            concept_type = concept_type.rstrip('/').split('/')[-1]
            #print("++++++++", data.get("name"), concept_type, data.get("concept_type"))
            response = self.get(url + "?name=" + urllib.parse.quote(data.get("name")) + "&concept_type=" + urllib.parse.quote(concept_type))
        else:
            ## Find if an object already exists, based on "name"
            response = self.get(url + "?name=" + urllib.parse.quote(data.get("name")))
        if response.status_code >= 400:
            return []
        return response.json()

    def login(self, username="admin", password=None):
        self.get("/api-auth/login/")
        self.post("/api-auth/login/", {'username': username, 'password': password})

client = Client()
client.login(password=PASSWORD)

## Declare some languages...
response = client.post("/rest/languages/", data={
    "code": "en",
    "name": "English",
    "description": "Language: English"
})
response = client.post("/rest/languages/", data={
    "code": "el",
    "name": "Greek",
    "description": "Language: Greek"
})
response = client.post("/rest/languages/", data={
    "code": "it",
    "name": "Italian",
    "description": "Language: Italian"
})
response = client.post("/rest/languages/", data={
    "code": "pt",
    "name": "Portuguese",
    "description": "Language: Portuguese"
})
response = client.post("/rest/languages/", data={
    "code": "sl",
    "name": "Slovene",
    "description": "Language: Slovene"
})

## Declare some ages...
for value in (
    '18-24', '25-34', '35-44', '45-54', '55-64', '65+',
    'Any',
    'Minor',
    'Adult'
    ):
    response = client.post("/rest/ages/", data={
        "name": value,
        "description": f"Age Range: {value}"
    })

## Declare some nationalities...
for nationality in (
    'Any',
    'Austrian',
    'Belgian',
    'Bulgarian',
    'Croatian',
    'Cypriot',
    'Czech',
    'Danish',
    'Estonian',
    'Finnish',
    'French',
    'German',
    'Greek',
    'Hungarian',
    'Irish',
    'Italian',
    'Latvian',
    'Lithuanian',
    'Luxembourgish',
    'Maltese',
    'Dutch',
    'Polish',
    'Portuguese',
    'Romanian',
    'Slovak',
    'Slovenian',
    'Spanish',
    'Swedish',
    'Unknown',):
    response = client.post("/rest/nationalities/", data={
        "name": nationality,
        "description": f"Nationality: {nationality}"
    })

## Declare some organisation types...
response = client.post("/rest/organisation_types/", data={
    "name": "Event Host Organisation",
    "description": "A Host Organisation (that organises an Event based on an Activity"
})
response = client.post("/rest/organisation_types/", data={
    "name": "Event Participant",
    "description": "An organisation visiting an Event",
})

## Declare a context
response = client.post("/rest/contexts/", data={
    "name": "Generic Context",
    "description": "A generic context for running VAST activities",
})

## Declare some natures...
response = client.post("/rest/natures/", data={
    "name": "In Person",
})
response = client.post("/rest/natures/", data={
    "name": "On-site",
})
response = client.post("/rest/natures/", data={
    "name": "Online",
})

## Declare some education levels...
for value in (
    'Preschool',
    'Elementary school',
    'Middle school',
    'High school',
    'Primary school',
    'Secondary school',
    'Unknown',
    'Any Level',
    ):
    response = client.post("/rest/educations/", data={
        "name": value,
        "description": f"Education Level: {value}"
    })

## Declare some genders...
response = client.post("/rest/genders/", data={
    "name": "Male",
})
response = client.post("/rest/genders/", data={
    "name": "Female",
})

## Declare some groups...
for value in (
    'Aylon Lyceum',
    'Fairy Tales Museum',
    'Museo Galileo - Istituto e Museo di Storia della Scienza',
    'Athens Epidaurus Festival',
    'Common Data Group',
    ):
    response = client.post("/rest/groups/", data={
        "name": value,
        "description": f"Group: {value}"
    })

## Declare some applications...
response = client.post("/rest/applications/", data={
    "name": "IMSS MindMap",
    "uriref": "https://imss-activity.vast-project.eu/"
})

## Declare some sidebar menu items...
# response = client.post("/rest/sidebar_menu_items/", data={
#     "title": "Add Event",
#     "url":   "activity-event-visitorgroup-wizard"
# })
# response = client.post("/rest/sidebar_menu_items/", data={
#     "title": "Add QR Code",
#     "url":   "visitorgroupqrcode-wizard"
# })

## Declare some Product Types...
for value in (
    'MindMap',
    'Annotation',
    'Questionnaire',
    'Interview',
    'Document',
    'Segment',
    'Image',
    'Audio',
    'Video',
    'Tool',
    ):
    response = client.post("/rest/product_types/", data={
        "name": value,
        "description": f"Product Type: {value}"
    })

## Concepts...
for value in (
    {'name': 'Concept', 'description': 'The default Concept type'},
    {'name': 'Higher Order Value', 'description': 'A Schwartz\'s Higher Order Value'},
    {'name': 'Original Value', 'description': 'A Schwartz\'s value from the 10 Original Values'},
    {'name': 'Narrowly Defined Value', 'description': 'A Schwartz\'s value from the 19 Narrowly Defined Values'},
    {'name': 'VAST Keyword', 'description': 'A VAST Keyword (used to annotate in the past of values)'},
    {'name': 'Non-expert Keyword', 'description': 'A user provided Keyword (used to annotate in the present of values)'},
    ):
    response = client.post("/rest/concept_types/", data=value)

for value in (
    {'name': 'Self-transcendence', 'concept_type': client.url('Higher Order Value')},
        {'name': 'Benevolence', 'concept_type': client.url('Original Value')},
            {'name': 'Benevolence-Dependability', 'concept_type': client.url('Narrowly Defined Value')},
            {'name': 'Benevolence-Caring', 'concept_type': client.url('Narrowly Defined Value')},
        {'name': 'Universalism', 'concept_type': client.url('Original Value')},
            {'name': 'Universalism-Tolerance', 'concept_type': client.url('Narrowly Defined Value')},
            {'name': 'Universalism-Concern', 'concept_type': client.url('Narrowly Defined Value')},
            {'name': 'Universalism-Nature', 'concept_type': client.url('Narrowly Defined Value')},
            {'name': 'Humility', 'concept_type': client.url('Narrowly Defined Value')},
    {'name': 'Conservation', 'concept_type': client.url('Higher Order Value')},
        {'name': 'Conformity', 'concept_type': client.url('Original Value')},
            {'name': 'Conformity-Interpersonal', 'concept_type': client.url('Narrowly Defined Value')},
            {'name': 'Conformity-Rules', 'concept_type': client.url('Narrowly Defined Value')},
        {'name': 'Tradition (O)', 'concept_type': client.url('Original Value')},
            {'name': 'Tradition', 'concept_type': client.url('Narrowly Defined Value')},
        {'name': 'Security', 'concept_type': client.url('Original Value')},
            {'name': 'Security-Societal', 'concept_type': client.url('Narrowly Defined Value')},
            {'name': 'Security-Personal', 'concept_type': client.url('Narrowly Defined Value')},
            {'name': 'Face', 'concept_type': client.url('Narrowly Defined Value')},
    {'name': 'Self-enhancement', 'concept_type': client.url('Higher Order Value')},
        {'name': 'Power', 'concept_type': client.url('Original Value')},
            {'name': 'Power-Resources', 'concept_type': client.url('Narrowly Defined Value')},
            {'name': 'Power-Dominance', 'concept_type': client.url('Narrowly Defined Value')},
        {'name': 'Achievement (O)', 'concept_type': client.url('Original Value')},
            {'name': 'Achievement', 'concept_type': client.url('Narrowly Defined Value')},
        {'name': 'Hedonism (O)', 'concept_type': client.url('Original Value')},
            {'name': 'Hedonism', 'concept_type': client.url('Narrowly Defined Value')},
    {'name': 'Openness to change', 'concept_type': client.url('Higher Order Value')},
        {'name': 'Stimulation (O)', 'concept_type': client.url('Original Value')},
            {'name': 'Stimulation', 'concept_type': client.url('Narrowly Defined Value')},
        {'name': 'Self-Direction', 'concept_type': client.url('Original Value')},
            {'name': 'Self-Direction-Action', 'concept_type': client.url('Narrowly Defined Value')},
            {'name': 'Self-Direction-Thought', 'concept_type': client.url('Narrowly Defined Value')},
    ):
    response = client.post("/rest/concepts/", data=value)
