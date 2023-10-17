from django.contrib.auth.models import User
from django.db.utils import IntegrityError
from rest_framework import status, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response

from datetime import datetime

from backend.serializers import VisitorSerializer
from .models import Age, Context, ProductAnnotation, ProductStatement, ConceptType, Event, Organisation, Stimulus, Activity, ProductType, Visitor, ActivityStep, Product, Concept, Statement, Predicate
from .models import Education
from .models import Gender
from .models import Language
from .models import Nationality
from .models import VisitorGroup


@api_view(['POST'])
@permission_classes((permissions.AllowAny,))
def save_values_workshop(request):
    data = request.data
    saved_items: int = 0
    error_response = Response({"error": "Error saving data"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    # Find user to use as created_by
    creator_user = User.objects.get(username="values_workshop")
    if not creator_user:
        return error_response
    
    # Find activity, to use when creating the visitor
    values_activity = Activity.objects.get(name="Values Workshop", created_by=creator_user)
    if not values_activity:
        return error_response
    
    # Find visitor group, to use when creating the visitor
    visitor_group = VisitorGroup.objects.get(name="Values Workshop Users", created_by=creator_user)
    if not visitor_group:
        return error_response
    
    # Create the visitor
    visitor_name = data["userId"]
    current_timestamp = datetime.now().strftime("%Y.%m.%d-%H.%M.%S")
    visitor = Visitor.objects.create(name=f"ValuesWorkshop_{current_timestamp}_{visitor_name}",
                                     created_by=creator_user,
                                     date_of_visit=datetime.now(),
                                     activity=values_activity,
                                     visitor_group=visitor_group,
                                     userid=visitor_name)
    
    # Find activity step and the "annotation" product type, to use in creating the product
    activity_step = ActivityStep.objects.get(name="Values Workshop Annotation", created_by=creator_user)
    annotation_prod_type = ProductType.objects.get(name="Annotation")
    if not annotation_prod_type or not activity_step:
        return error_response
    
    # Create the product
    product = Product.objects.create(name=f"ValuesWorkshop_{current_timestamp}_{visitor_name}",
                                     created_by=creator_user,
                                     product_type=annotation_prod_type,
                                     visitor=visitor,
                                     activity_step=activity_step)
    
    # Save product annotations
    annotations = data["annotations"]
    for annotation in annotations:
        # Get the value as a concept
        value_name = annotation["comment"]
        value_concept = get_concept(name=value_name, concept_type_name="Non-expert Keyword", created_by=creator_user)

        # Create the product annotation
        annotation_name = f"VW_{current_timestamp}_{visitor_name}_{saved_items + 1}"
        ProductAnnotation.objects.create(name=annotation_name,
                                         span_type="text",
                                         product=product,
                                         value=value_concept,
                                         text=annotation["text"],
                                         created_by=creator_user)
        saved_items += 1        
    
    
    return Response({"saved_items": saved_items}, status=status.HTTP_201_CREATED)


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
def save_ftm_statements(request):
    error = Response(status=status.HTTP_400_BAD_REQUEST)

    # Get user to create the objects as
    creator_user = User.objects.get(username='digitisation_ftm')
    if creator_user is None:
        return error

    # Get request data
    data = request.data
    
    # Find or create the activity
    activity, _ = Activity.objects.get_or_create(name="FTM Annotation", created_by=creator_user)
    
    # Get language from request, and find the stimulus text from the DB (it should be created already)
    language = data["language"]
    frog_price_stimulus = Stimulus.objects.filter(name=f"The Frog Price ({language})").first()
    no_stimulus = Stimulus.objects.filter(name="No stimulus").first()
    if frog_price_stimulus is None or no_stimulus is None:
        return error
    
    # Find or create the activity steps
    annotation_activity_step, _ = ActivityStep.objects.get_or_create(name="FTM Pre-questionnaire Annotation",
                                                                     activity=activity, 
                                                                     stimulus=frog_price_stimulus,
                                                                     created_by=creator_user)
    story_writing_step, _ = ActivityStep.objects.get_or_create(name="FTM Story Writing",
                                                                     activity=activity, 
                                                                     stimulus=no_stimulus,
                                                                     created_by=creator_user)
    
    # Get NCSR-D host organisation
    host_organisation = Organisation.objects.filter(name="NCSR-D").first()
    
    # Get Generic Context
    generic_context = Context.objects.filter(name="Generic Context").first()
    
    # Find or create the Event
    event, _ = Event.objects.get_or_create(name="FTM App",
                                           activity=activity,
                                           context=generic_context,
                                           host_organisation=host_organisation,
                                           created_by=creator_user)
    
    # Find or create the Visitor Group
    visitor_group, _ = VisitorGroup.objects.get_or_create(name="FTM App User Group",
                                                          event=event,
                                                          created_by=creator_user)
    
    # Find or create the Visitor
    visitor, _ = Visitor.objects.get_or_create(name="FTM App Visitor",
                                               activity=activity,
                                               visitor_group=visitor_group,
                                               created_by=creator_user)
    
    # Find product types
    document_product_type = ProductType.objects.filter(name="Document").first()
    if document_product_type is None:
        return error
    
    # Create product for story statements (it includes the story)
    current_timestamp = datetime.now().strftime("%Y.%m.%d-%H.%M.%S")
    writing_product_name = f"FTM App Story {current_timestamp}"
    story_text = data["story"]
    if not story_text:
        return error
    writing_product = Product.objects.create(name=writing_product_name,
                                             product_type=document_product_type,
                                             activity_step=story_writing_step,
                                             visitor=visitor,
                                             text=story_text,
                                             created_by=creator_user)
    
    # Save story statements
    statements_count = 0
    for statement in data["storyStatements"]:
        # Create concept
        object_name = statement["object"]
        concept = get_concept(object_name, "Non-expert Keyword", creator_user)
        
        # Get predicate
        predicate_name = statement["predicate"]
        predicate = get_predicate(predicate_name, creator_user)
        
        # Save statement with story_subject, predicate & concept as object.
        ps = ProductStatement.objects.create(name=f"Story_{current_timestamp}.{predicate_name}.{object_name}",
                                             subject=writing_product,
                                             predicate=predicate,
                                             object=concept,
                                             created_by=creator_user)
        if ps:
            statements_count += 1
        
    # Find the frog price story product
    product_name = f"The Frog Prince Story ({language})"
    annotation_product = Product.objects.filter(name=product_name).first()
    if not annotation_product:
        return error
    
    annotations_count = 0
    for annotation in data["annotations"]:
        annotation_segment = annotation["segment"]
        annotation_start = annotation["start"]
        annotation_end = annotation["end"]
        annotation_value = annotation["value"]
        concept = get_concept(annotation_value, "Non-expert Keyword", creator_user)
        annotation_name = f"Frog Prince_{current_timestamp}_{annotation_start}-{annotation_end}_{annotation_value}"
        pa = ProductAnnotation.objects.create(name=annotation_name,
                                              product=annotation_product,
                                              value=concept,
                                              text=annotation_segment,
                                              start=annotation_start,
                                              end=annotation_end,
                                              span_type="text",
                                              created_by=creator_user)
        if pa:
            annotations_count += 1

    return Response({
            "new_annotations": annotations_count,
            "new_story_statements": statements_count,
        },
        status=status.HTTP_201_CREATED)


def get_predicate(name: str, created_by: User) -> Predicate:
    """
    Find or create a predicate. If a predicate with the given name exists, even if created by a
    different user, it will not be created again.

    Args:
        name (str): The predicate name
        created_by (User): The user to create the predicate as, if needed

    Returns:
        Predicate: The predicate
    """
    # Try to find predicate with this name
    predicate = Predicate.objects.filter(name=name).first()
    
    if not predicate:
        # Create the predicate
        predicate = Predicate.objects.create(name=name,
                                             created_by=created_by)
    return predicate


def get_concept(name: str, concept_type_name: str, created_by: User) -> Concept | None:
    """
    Find or create a concept with the given name and type.

    Args:
        name (str): The concept name/value
        concept_type_name (str): The type of the concept. Should be available in the DB (won't be created).
        created_by (User): The user to create the concept as.

    Returns:
        Concept: The created concept
    """
    # Find concept type
    concept_type = ConceptType.objects.filter(name=concept_type_name).first()
    if not concept_type:
        return None
        
    # Try to find the concept, otherwise create it
    concept = Concept.objects.filter(name=name, concept_type=concept_type).first()
    if not concept:
        concept = Concept.objects.create(name=name,
                                         concept_type=concept_type,
                                         created_by=created_by)
    return concept

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
