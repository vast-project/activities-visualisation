from django.core.management.base import BaseCommand
from activity_data.models import CulturalHeritageArtifact
from django.contrib.auth.models import User

## RDF Graph...
from vast_rdf.vast_repository import RDFStoreVAST, GRAPH_ID_ELLOGON_ANNOTATION_TOOL

class Command(BaseCommand):
    help = 'Update Cultural Heritage Artifacts'

    def handle(self, *args, **options):
        try:
            uid = User.objects.get(username='admin')
        except:
            print("No admin user?")
            return None
        rdf = RDFStoreVAST(identifier=GRAPH_ID_ELLOGON_ANNOTATION_TOOL)
        # Get all Collections...
        sparql = f'SELECT ?c ?n WHERE {{ ?c a vast:vastCollection . ?c foaf:name ?n }}'
        results = rdf.querySPARQL(sparql)
        del rdf
        for row in results:
            obj, created = CulturalHeritageArtifact.objects.update_or_create(
                name = row.n,
                created_by = uid
            )
            print(created, row.n, obj)
