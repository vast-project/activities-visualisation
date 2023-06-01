from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from inspect import signature
import sys, os

class ErrorLoggingAPIViewList:
    http_method_names = ["get", "post"]

class ErrorLoggingAPIViewDetail:
    http_method_names = ["get", "put", "patch", "delete"]

class ErrorLoggingAPIView(APIView):
    """
    Base class to implement an error logging APIView.
    """
    status_exception_default  = status.HTTP_400_BAD_REQUEST
    status_exception          = status.HTTP_400_BAD_REQUEST
    data_exception            = {}

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        ## Get the number of arguments of the list & retrieve methods...
        sig_list     = signature(self.list)
        sig_retrieve = signature(self.retrieve)
        self.arguments_list     = list(sig_list.parameters.keys())[1:] # drop 'request'
        self.arguments_retrieve = list(sig_retrieve.parameters.keys())[1:] # drop 'request'
        # print("##############", self.arguments_list, self.arguments_retrieve)

    def logException(self, request, ex, method):
        print(self.__class__.__name__, "-", method+"() - Catch Exception:", ex)
        print(" User:", request.user, request.user.pk, request.user.email)
        tb = ex.__traceback__
        # Skip the outer layer...
        if tb is not None:
            tb = tb.tb_next
        if tb is not None:
            print("filename:", tb.tb_frame.f_code.co_filename,
                  "name:", tb.tb_frame.f_code.co_name,
                  "lineno:", tb.tb_lineno)
        else:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)
        response = Response(data={
            "success": False,
            "message": str(ex),
            "data": self.data_exception
            }, status=self.status_exception)
        self.status_exception = self.status_exception_default
        self.data_exception   = {}
        return response

    def returnResponse(self, data, method):
        if type(data) is tuple:
            # Expects two elements, data & status
            return Response(data=data[0], status=data[1])
        return Response(data={"success": True, "data": data},
                            status=status.HTTP_200_OK)

    def get(self, request, *args, **kwargs):
        try:
            ## Are the arguments of retrieve satisfiled?
            if all(param in kwargs for param in self.arguments_retrieve):
                data = self.retrieve(request, *args, **kwargs)
                method = 'retrieve'
            elif all(param in kwargs for param in self.arguments_list):
                data = self.list(request, *args, **kwargs)
                method = 'list'
            else:
                raise "Cannot decide over list() or retrieve()!"
            return self.returnResponse(data, method)
        except Exception as ex:
            return self.logException(request, ex, "list/retrieve")

    def post(self, request, *args, **kwargs):
        try:
            data = self.create(request, *args, **kwargs)
            return self.returnResponse(data, "create")
        except Exception as ex:
            return self.logException(request, ex, "create")

    def put(self, request, *args, **kwargs):
        try:
            data = self.update(request, *args, **kwargs)
            return self.returnResponse(data, "update")
        except Exception as ex:
            return self.logException(request, ex, "update")

    def patch(self, request, *args, **kwargs):
        try:
            data = self.partial_update(request, *args, **kwargs)
            return self.returnResponse(data, "partial_update")
        except Exception as ex:
            return self.logException(request, ex, "partial_update")

    def delete(self, request, *args, **kwargs):
        try:
            data = self.destroy(request, *args, **kwargs)
            return self.returnResponse(data, "destroy")
        except Exception as ex:
            return self.logException(request, ex, "destroy")

    # From: https://github.com/encode/django-rest-framework/blob/master/rest_framework/mixins.py

    # List all instances. (GET)
    def list(self, request):
        raise NotImplementedError
    # Retrieve a single instance. (GET)
    def retrieve(self, request, detail):
        raise NotImplementedError
    # Create a new instance. (POST)
    def create(self, request):
        raise NotImplementedError
    # Update an existing instance. (PUT)
    def update(self, request, detail):
        raise NotImplementedError
    # Partially update an existing instance. (PATCH)
    def partial_update(self, request, detail):
        raise NotImplementedError
    # Destroy an existing instance. (DELETE)
    def destroy(self, request, detail):
        raise NotImplementedError

class VASTRepositoryAPIView(ErrorLoggingAPIView):
    @staticmethod
    def request_data(request, key, default=None):
        return request.data.get(key, default)


class VASTRepositoryAPIViewList(ErrorLoggingAPIViewList):
    pass

class VASTRepositoryAPIViewDetail(ErrorLoggingAPIViewDetail):
    pass

