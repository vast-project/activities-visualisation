import requests
import urllib.parse

local = False
local = True

if local:
    API          = "http://127.0.0.1:8000"
    PASSWORD     = "praxis"
else:
    API          = "https://activities-backend.vast-project.eu"
    PASSWORD     = "99_JgxL,7FRq$%9"

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
    "name": "Host Organisation",
    "description": "Adding a Host Organisation to Test Graph",
})
response = client.post("/rest/organisation_types/", data={
    "name": "School",
    "description": "Adding a School to Test Graph",
})

## Declare some organisations...
response = client.post("/rest/organisations/", data={
    "name": "Museo Galileo",
    "description": "Museo Galileo - Instituto e Museo di Storia della Scienza",
    "name_local": "Museo Galileo",
    "description_local": "Museo Galileo - Instituto e Museo di Storia della Scienza",
    "language_local": client.url("Italian"),  # Italian
    "type": client.url("Host Organisation"),  # Host Organisation
    "location": "Florence",
    "is_visitor": "No"
})
response = client.post("/rest/organisations/", data={
    "name": "New School in Florence",
    "description": "A school from Florence",
    "type": client.url("School"),   # School
    "location": "Florence",
    "is_visitor": "Yes"
})

## Declare an activity...
response = client.post("/rest/activities/", data={
    "name": "Museo Galileo Default Activity",
    "description": "A default activity in Museo Galileo",
    "name_local": "Museo Galileo Default Activity",
    "description_local": "A default activity in Museo Galileo in Italian",
    "language_local": client.url("Italian"),                    # Italian
})

## Declare a stimulus...
response = client.post("/rest/stimuli/", data={
    "name": "Museo Galileo Stimulus Video",
    "description": "A performance in Museo Galileo",
    "uriref": "https://www.youtube.com/channel/UC2oyweCFfvyP66hmsaU1aUA",
    "stimulus_type": "Video"
})

## Declare an activity step...
response = client.post("/rest/activity_steps/", data={
    "name": "Default Activity Step",
    "description": "The only activity step in activity",
    "activity": client.url("Museo Galileo Default Activity"),   # Museo Galileo Default Activity
    "stimulus": client.url("Museo Galileo Stimulus Video")      # Museo Galileo Stimulus Video
})

## Declare a context
response = client.post("/rest/contexts/", data={
    "name": "Museo Galileo VAST Participation",
    "description": "A context for running activities in Museo Galileo",
    "name_local": "Museo Galileo VAST Participation",
    "description_local": "A context for running activities in Museo Galileo in Italian",
    "language_local": client.url("Italian") # Italian
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
    "name": "Secondary School",
    "name_local": "Scuola secondaria di secondo grado",
    "language_local": client.url("Italian") # Italian
})

## Declare an event...
response = client.post("/rest/events/", data={
    "name": "Museo Galileo Event",
    "description": "An event by Museo Galileo",
    "name_local": "Museo Galileo Event",
    "description_local": "An event by Museo Galileo in Italian",
    "language_local": client.url("Italian"),                    # Italian
    "host_organisation": client.url("Museo Galileo"),           # Museo Galileo
    "activity": client.url("Museo Galileo Default Activity"),   # Museo Galileo Event
    "context": client.url("Museo Galileo VAST Participation"),  # Museo Galileo VAST Participation
    "language": client.url("Italian"),                          # Italian
    "nature": client.url("On-site"),                            # On-site
    "education": client.url("Secondary School"),                # Secondary School
    "date_from": "2020-12-01T00:00:00",
    "date_to":   "2024-02-24T23:59:59"
})

## Declare some ages...
response = client.post("/rest/ages/", data={
    "name": "18-99",
})
response = client.post("/rest/ages/", data={
    "name": "5-17",
})

## Declare some genders...
response = client.post("/rest/genders/", data={
    "name": "Male",
})
response = client.post("/rest/genders/", data={
    "name": "Female",
})

## Declare some nationalities...
response = client.post("/rest/nationalities/", data={
    "name": "Greek Nationality",
})
response = client.post("/rest/nationalities/", data={
    "name": "Italian Nationality",
})

## Declare a visitor group...
response = client.post("/rest/visitor_groups/", data={
    "name": "Group for Activity",
    "composition": 30,
    "event": client.url("Museo Galileo Event"),                  # Museo Galileo Event
    "age":  client.url("18-99"),                                 # 18-99
    "education": client.url("Secondary School"),                 # Secondary School
    "nationality": client.url("Italian Nationality"),            # Italian Nationality
    "mother_language": client.url("Italian"),                    # Italian
    "visitor_organisation": client.url("New School in Florence") # New School in Florence
})

## Declare a visitor...
response = client.post("/rest/visitors/", data={
    "name": "Georgios Petasis",
    "age":  client.url("18-99"),                              # 18-99
    "gender": client.url("Male"),                             # Male
    "date_of_visit": "2023-01-01T09:45",
    "nationality": client.url("Italian Nationality"),         # Italian Nationality
    "mother_language": client.url("Italian"),                 # Italian
    "activity": client.url("Museo Galileo Default Activity"), # Museo Galileo Default Activity
    "visitor_group": client.url("Group for Activity"),        # Group for Activity
    "school": "1st School in Florence",
})

## Declare a product type...
response = client.post("/rest/product_types/", data={
    "name": "MindMap",
})

## Declare a product...
response = client.post("/rest/products/", data={
    "product_type": client.url("MindMap"),                # MindMap
    "visitor": client.url("Georgios Petasis"),            # Georgios Petasis
    "activity_step": client.url("Default Activity Step"), # Default Activity Step
})
product = response.json().get("url")

## Declare some concepts...
response = client.post("/rest/concepts/", data={
    "name": "value 1",
    "name_local": "Italian value 1",
    "language_local": client.url("Italian"),             # Italian
})
response = client.post("/rest/concepts/", data={
    "name": "value 2",
    "name_local": "Italian value 2",
    "language_local": client.url("Italian"),             # Italian
})

## Declare some predicates...
response = client.post("/rest/predicates/", data={
    "name": "equivalent",
})
response = client.post("/rest/predicates/", data={
    "name": "consequence",
})

## Declare a statement...
response = client.post("/rest/statements/", data={
    "product": product,
    "subject": client.url("value 1"),
    "predicate": client.url("consequence"),
     "object": client.url("value 2"),
})

## Delete the added statement (to test deletion)...
# location = response.headers.get("Location", None)
# if (location):
#     print("DELETING Statement:", location)
#     response = client.delete(location)

## Declare an application...
response = client.post("/rest/applications/", data={
    "name": "IMSS MindMap",
    "uriref": "https://imss-activity.vast-project.eu/",
})

## Declare a QR code...
response = client.post("/rest/qr_codes/", data={
    "name": "IMSS QR1",
    "event": client.url("Museo Galileo Event"),               # Museo Galileo Event
    "activity": client.url("Museo Galileo Default Activity"), # Museo Galileo Default Activity
    "activity_step": client.url("Default Activity Step"),     # Default Activity Step
    "visitor_group": client.url("Group for Activity"),        # Group for Activity
    "application": client.url("IMSS MindMap"),                # IMSS MindMap
})
