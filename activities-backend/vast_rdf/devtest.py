from rdflib import Graph, URIRef, Literal

from vast_repository import RDFStoreVAST
rdf = RDFStoreVAST()

for triple in rdf.g.triples( (URIRef("vast:vastOrganisationType/084867ac-70b4-4e8c-8ea1-6e6f556a7581"), None, None),  ):
    print(triple)

for triple in rdf.g.triples( (None, None, None),  ):
    print(triple)
