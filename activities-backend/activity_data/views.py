from django.contrib.auth.models import User
from django.db.utils import IntegrityError
from rest_framework import status, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response

from backend.serializers import VisitorSerializer
from .models import Age, ProductType, Visitor, ActivityStep, Product, Concept, Statement, Predicate
from .models import Education
from .models import Gender
from .models import Language
from .models import Nationality
from .models import VisitorGroup


@api_view(['POST'])
@permission_classes((permissions.AllowAny,))
def save_statements(request):
    saved_statements: int = 0
    data = request.data

    # Find user to use as created_by (based on the given username)
    creator_user = User.objects.get(username=data["creator_username"])
    if not creator_user:
        return Response({"error": "Error saving statement"}, status=status.HTTP_400_BAD_REQUEST)

    # Find visitor
    visitor_name = data["visitor_name"]
    visitor = Visitor.objects.get(name=visitor_name, created_by=creator_user)

    # Find product type, or create it
    product_type_name = data["product"]
    product_type, _ = ProductType.objects.get_or_create(name=product_type_name, created_by=creator_user)

    # Find activity step
    activity_step = ActivityStep.objects.get(id=data["activity_step"])

    # Get or create the product in the DB
    product_name = "-".join([visitor_name, product_type_name, activity_step.name])
    product, _ = Product.objects.get_or_create(name=product_name, created_by=creator_user,
                                               product_type_id=product_type.id,
                                               activity_step_id=activity_step.id, visitor_id=visitor.id)

    # Get or create a subject in the DB
    subject_name = data["subject"]
    subject, _ = Concept.objects.get_or_create(name=subject_name, created_by=creator_user)

    # Get predicates
    predicates: dict = data["predicates"]
    for predicate, objects in predicates.items():
        # Get or create predicate in the DB
        predicate, _ = Predicate.objects.get_or_create(name=predicate, created_by=creator_user)

        # Create statements
        for obj in objects:
            # Get or create object in the DB
            obj, _ = Concept.objects.get_or_create(name=obj, created_by=creator_user)

            # Create statement with subject, predicate and object
            try:
                Statement.objects.create(subject=subject, predicate=predicate, object=obj, product=product,
                                         created_by=creator_user)
                saved_statements += 1
            except IntegrityError:
                # Ignore IntegrityError (statement already exists)
                pass

    return Response({"saved_statements": saved_statements}, status=status.HTTP_201_CREATED)


@api_view(['POST'])
@permission_classes((permissions.AllowAny,))
def save_visitor(request):
    # Find user by the username in the POST body, and set it as the user of the request
    creator_user = User.objects.get(username=request.data['creator_username'])
    if creator_user is not None:
        # Create a visitor object
        new_visitor = Visitor()

        new_visitor.created_by = creator_user
        new_visitor.name = request.data['name']
        new_visitor.school = request.data['school']
        new_visitor.date_of_visit = request.data['date_of_visit']

        new_visitor.activity_id = int(request.data['activity'])
        new_visitor.activity_step_id = int(request.data['activity_step'])
        new_visitor.visitor_group = VisitorGroup.objects.filter(id=int(request.data['visitor_group'])).first()

        new_visitor.age = Age.objects.filter(name=request.data['age']).first()
        new_visitor.gender = Gender.objects.filter(name=request.data['gender']).first()
        new_visitor.nationality = Nationality.objects.filter(name=request.data['nationality']).first()
        new_visitor.education = Education.objects.filter(name=request.data['education_level']).first()
        new_visitor.mother_language = Language.objects.filter(name=request.data['mother_language']).first()

        new_visitor.save()
        return Response(VisitorSerializer(new_visitor, context={"request": request}).data,
                        status=status.HTTP_201_CREATED)
    else:
        return Response(status=status.HTTP_400_BAD_REQUEST)
