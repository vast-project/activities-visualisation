from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt, csrf_protect, ensure_csrf_cookie
from rest_framework.views import APIView
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, AllowAny
from .vast_repository import RDFStoreVAST
from .models import *
from .serializers import *

@method_decorator(csrf_exempt, name='dispatch')
class RDFSparqlView(GenericAPIView):
    permission_classes = (AllowAny,)

    serializer_class = SparqlQuerySerializer

    param_query = 'q'

    def sparql(self, query):
        rdf = RDFStoreVAST()
        results = rdf.querySPARQL(query)
        del rdf
        return results

    def get_query(self, request):
        if self.param_query in request.query_params:
            return request.query_params.get(self.param_query)
        else:
            return request.data.get(self.param_query)

    def do_sparql(self, request):
        query = self.get_query(request)
        if isinstance(query, str):
            return Response(
                data={"success": True, "data": self.sparql(query)},
                status=status.HTTP_200_OK
            )
        else:
            return Response(
                data={"success": False, "message": "Parameter 'q' is missing", "data": {}},
                status=status.HTTP_200_OK
            )

    def get(self, request):
        # print("GET:", request.query_params, request.data)
        return self.do_sparql(request)

    def post(self, request):
        # print("POST:", request.data)
        return self.do_sparql(request)
