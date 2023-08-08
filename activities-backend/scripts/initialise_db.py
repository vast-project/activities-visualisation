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
response = client.post("/rest/educations/", data={
    "name": "Preschool",
})
response = client.post("/rest/educations/", data={
    "name": "Elementary school",
})
response = client.post("/rest/educations/", data={
    "name": "Middle school",
})
response = client.post("/rest/educations/", data={
    "name": "High school",
})
response = client.post("/rest/educations/", data={
    "name": "Primary school",
})
response = client.post("/rest/educations/", data={
    "name": "Secondary school",
})

## Declare some genders...
response = client.post("/rest/genders/", data={
    "name": "Male",
})
response = client.post("/rest/genders/", data={
    "name": "Female",
})

## Declare some groups...
response = client.post("/rest/groups/", data={
    "name": "Aylon Lyceum",
})
response = client.post("/rest/groups/", data={
    "name": "Fairy Tales Museum",
})
response = client.post("/rest/groups/", data={
    "name": " Museo Galileo - Istituto e Museo di Storia della Scienza",
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
